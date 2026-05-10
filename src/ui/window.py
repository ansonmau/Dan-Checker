# ─────────────────────────────────────────────────────────────────────────────
#  src/ui/window.py  –  DualItemListWindow 
# ───────────────────────────────────────────────────────────────────────────── 
from __future__ import annotations

from PyQt6.QtCore    import QPoint, QTimer
from PyQt6.QtGui     import QColor, QPalette, QWindow
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QMainWindow,
    QScrollArea, QVBoxLayout, QWidget,
)

from ui             import theme
from ui.card        import ItemCard
from ui.note_popup  import NotePopup
from ui.panel       import build_panel
from ui.toolbar     import ToolBar


class DualItemListWindow(QMainWindow):
    """
    Top-level window displaying two item lists side by side.

    Parameters
    ----------
    items_left / items_right
        Lists of objects that implement get_date(), get_location(), get_amount().
    title / title_left / title_right
        Window and sub-panel labels.
    """

    def __init__(
        self,
        items_left:  list,
        items_right: list,
        title:       str = "Transaction Comparison",
        title_left:  str = "List A",
        title_right: str = "List B",
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(1250, 700)
        self.setMinimumSize(900, 500)
        self._apply_palette()

        # ── State ─────────────────────────────────────────────────────────────
        self._cards_left:   list[ItemCard]   = []
        self._cards_right:  list[ItemCard]   = []
        self._scroll_left:  QScrollArea | None = None
        self._scroll_right: QScrollArea | None = None

        self._connect_mode = False
        self._connect_pending:  dict[str, list[ItemCard]] = {"left": [], "right": []}
        self._connections:      list[tuple[ItemCard, ItemCard]] = []
        self._click_timer:      QTimer | None = None

        # ── Root ──────────────────────────────────────────────────────────────
        root = QWidget()
        root.setObjectName("Root")
        root.setStyleSheet(f"QWidget#Root {{ background:{theme.BG_DARK}; }}")
        self.setCentralWidget(root)

        ml = QVBoxLayout(root)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        # ── Toolbar ───────────────────────────────────────────────────────────
        toolbar = ToolBar()
        toolbar.connect_toggled.connect(self._on_connect_toggle)
        toolbar.sync_clicked.connect(self._on_sync)
        ml.addWidget(toolbar)

        # ── Title bar ─────────────────────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar.setFixedHeight(56)
        title_bar.setStyleSheet(f"""
            QWidget#TitleBar {{
                background    : {theme.BG_TOOLBAR};
                border-bottom : 1px solid {theme.BORDER_DEFAULT};
            }}
        """)
        tl = QHBoxLayout(title_bar)
        tl.setContentsMargins(28, 0, 28, 0)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            f"color:{theme.TEXT_PRIMARY}; font-size:18px; font-weight:700;"
            f" letter-spacing:0.3px; background:transparent;"
        )

        tl.addWidget(title_lbl)
        tl.addStretch()
        ml.addWidget(title_bar)

        # ── Two panels ────────────────────────────────────────────────────────
        panels_row = QHBoxLayout()
        panels_row.setContentsMargins(0, 0, 0, 0)
        panels_row.setSpacing(0)

        lp, self._cards_left, self._scroll_left = build_panel(
            items_left, title_left,
            on_left_click  = lambda c: self._on_left_click(c, "left"),
            on_right_click = self._on_right_click,
        )

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setFixedWidth(1)
        divider.setStyleSheet(f"background:{theme.BORDER_DEFAULT};")

        rp, self._cards_right, self._scroll_right = build_panel(
            items_right, title_right,
            on_left_click  = lambda c: self._on_left_click(c, "right"),
            on_right_click = self._on_right_click,
        )

        panels_row.addWidget(lp,      stretch=1)
        panels_row.addWidget(divider)
        panels_row.addWidget(rp,      stretch=1)

        panels_widget = QWidget()
        panels_widget.setObjectName("PanelsWidget")
        panels_widget.setStyleSheet(
            f"QWidget#PanelsWidget {{ background:{theme.BG_DARK}; }}"
        )
        panels_widget.setLayout(panels_row)
        ml.addWidget(panels_widget, stretch=1)

    # ── Left click ────────────────────────────────────────────────────────────

    def _on_left_click(self, card: ItemCard, side: str):
        if self._connect_mode:
            self._handle_connect(card, side)
            return

        # Cancel any in-progress click highlight
        if self._click_timer is not None:
            self._click_timer.stop()
            self._click_timer = None
            self._reset_click_states()

        # timer
        self._click_timer = QTimer(self)
        self._click_timer.setSingleShot(True)
        self._click_timer.timeout.connect(self._reset_click_states)

        source_scroll = self._scroll_left  if side == "left" else self._scroll_right
        target_cards  = self._cards_right  if side == "left" else self._cards_left
        target_scroll = self._scroll_right if side == "left" else self._scroll_left

        focused_cards = [c for c in target_cards if c.get_date_str() == card.get_date_str()]
        special_cards = {c for c in focused_cards if c.get_location_str() == card.get_location_str()}
        focused_set   = set(focused_cards)

        if not focused_cards:
            for c in self._cards_left:
                c.set_state(ItemCard.STATE_GREYED)
        else:
            # Apply visual states to all cards
            for c in self._cards_left + self._cards_right:
                if c is card:
                    c.set_state(ItemCard.STATE_SOURCE)
                elif c in special_cards:
                    c.set_state(ItemCard.STATE_SPECIAL)
                elif c in focused_set:
                    c.set_state(ItemCard.STATE_FOCUSED)
                else:
                    c.set_state(ItemCard.STATE_GREYED)

            # Scroll source and first focused card to center in their panels
            # self._scroll_to_center(source_scroll, card)
            self._scroll_to_center(target_scroll, focused_cards[0])

        self._click_timer.start(2000)

    def _reset_click_states(self):
        for c in self._cards_left + self._cards_right:
            c.set_state(ItemCard.STATE_NORMAL)
        self._click_timer = None

    def _scroll_to_center(self, scroll: QScrollArea | None, card: ItemCard):
        if scroll is None:
            return
        card_y          = card.mapTo(scroll.widget(), QPoint(0, 0)).y()
        viewport_height = scroll.viewport().height()
        target          = card_y - (viewport_height - card.height()) // 2
        scroll.verticalScrollBar().setValue(max(0, target))

    # ── Right click ───────────────────────────────────────────────────────────

    def _on_right_click(self, card: ItemCard, global_pos: QPoint):
        popup = NotePopup(card, self)
        popup.show_near(self._get_point_for_center(popup))
        popup.exec()

    # ── Connect mode ──────────────────────────────────────────────────────────
    def _on_connect_toggle(self, active: bool):
        self._connect_mode = active
        if not active:
            note_contents = ["==CONNECTED=="]
            format_str = "[{}]   ->   {}   {}   ${}"
            for card in self._connect_pending["left"]:
                # QB side
                note_contents.append(format_str[:].format(
                    "Quickbooks",
                    card.get_date_str(),
                    card.get_location_str(),
                    card.get_amount_str()
                    ))
                card.set_connect_selected(False)
                        
            for card in self._connect_pending["right"]:
                #bank side
                note_contents.append(format_str[:].format(
                    "Bank",
                    card.get_date_str(),
                    card.get_location_str(),
                    card.get_amount_str()
                    ))
                card.set_connect_selected(False)

            for card in self._connect_pending["right"] + self._connect_pending["left"]:
                card.set_note("\n".join(note_contents))

            self._clear_connect_pending()

    def _clear_connect_pending(self):
        self._connect_pending["left"].clear()
        self._connect_pending["right"].clear()

    def _handle_connect(self, card: ItemCard, side: str):
        # Toggle off if already pending on this side
        if card in self._connect_pending[side]:
            card.set_connect_selected(False)
            self._connect_pending[side].remove(card)
            return

        card.set_connect_selected(True)
        self._connect_pending[side].append(card)

    # ── Center window ──────────────────────────────────────────────────────────────────
    def _get_point_for_center(self, window:QWidget):
        geo = self.frameGeometry()

        # move function moves TOP LEFT corner
        target_x = geo.x() + (geo.width() - window.width()) // 2
        target_y = geo.y() + (geo.height() - window.height()) // 2

        return QPoint(target_x, target_y)
    # ── Sync ──────────────────────────────────────────────────────────────────

    def _on_sync(self):
        # TODO: fetch from GitHub URL and refresh lists
        pass

    # ── Palette ───────────────────────────────────────────────────────────────

    def _apply_palette(self):
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window,     QColor(theme.BG_DARK))
        p.setColor(QPalette.ColorRole.WindowText, QColor(theme.TEXT_PRIMARY))
        p.setColor(QPalette.ColorRole.Base,       QColor(theme.BG_CARD_BASE))
        p.setColor(QPalette.ColorRole.Text,       QColor(theme.TEXT_PRIMARY))
        self.setPalette(p)
