# ─────────────────────────────────────────────────────────────────────────────
#  src/ui/card.py  –  ItemCard widget
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

from PyQt6.QtCore    import Qt, pyqtSignal
from PyQt6.QtGui     import QCursor
from PyQt6.QtWidgets import (
    QFrame, QGraphicsOpacityEffect, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget,
)

from ui import theme


class ItemCard(QFrame):
    """A single row card.  Visual state is driven by note content, connect mode, and click state."""

    NOTE_PREVIEW_MAX = 50

    # ── Click-state constants ─────────────────────────────────────────────────
    STATE_NORMAL  = "normal"
    STATE_SOURCE  = "source"    # the card that was clicked
    STATE_FOCUSED = "focused"   # date match in the other panel
    STATE_SPECIAL = "special"   # date + location match in the other panel
    STATE_GREYED  = "greyed"    # not involved – dimmed

    # ── Signals ───────────────────────────────────────────────────────────────
    left_clicked  = pyqtSignal(object)          # emits self
    right_clicked = pyqtSignal(object, object)  # emits (self, QPoint)
    # ─────────────────────────────────────────────────────────────────────────
    def __init__(self, item, index: int, parent=None):
        super().__init__(parent)
        self._item           =   item
        self._index          =   index
        self._date_str       =   str(item.get_date())
        self._location_str   =   str(item.get_location())
        self._amount_str     =   str(item.get_amount())

        self._note             = ""
        self._state            = self.STATE_NORMAL
        self._connect_selected = False
        self._connected        = []

        self.setObjectName("ItemCard")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMinimumHeight(84)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self._build_ui()
        self._refresh_style()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        badge = QLabel(str(self._index + 1).zfill(2))
        badge.setFixedWidth(36)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"color:{theme.TEXT_MUTED}; font-size:11px; font-weight:700;"
            f" letter-spacing:1px; background:transparent;"
        )

        def vline():
            ln = QFrame()
            ln.setFrameShape(QFrame.Shape.VLine)
            ln.setFixedWidth(1)
            ln.setStyleSheet(f"background:{theme.BORDER_DEFAULT};")
            return ln

        def field(label_txt: str, value_txt: str, accent: str, min_w: int = 90):
            col = QVBoxLayout()
            col.setSpacing(3)
            col.setContentsMargins(0, 0, 0, 0)

            lbl = QLabel(label_txt.upper())
            lbl.setStyleSheet(
                f"color:{accent}; font-size:9px; font-weight:700;"
                f" letter-spacing:1.5px; background:transparent;"
            )

            val = QLabel(value_txt)
            val.setStyleSheet(
                f"color:{theme.TEXT_PRIMARY}; font-size:20;"
                f" font-weight:500; background:transparent;"
            )
            val.setWordWrap(True)

            col.addWidget(lbl)
            col.addWidget(val)

            wrapper = QWidget()
            wrapper.setMinimumWidth(min_w)
            wrapper.setLayout(col)
            wrapper.setStyleSheet("background:transparent;")
            return wrapper

        # ── Note preview column ───────────────────────────────────────────────
        note_col = QVBoxLayout()
        note_col.setSpacing(3)
        note_col.setContentsMargins(0, 0, 0, 0)

        note_header = QLabel("NOTE")
        note_header.setStyleSheet(
            f"color:{theme.TEXT_MUTED}; font-size:9px; font-weight:700;"
            f" letter-spacing:1.5px; background:transparent;"
        )

        self._note_preview_lbl = QLabel("")
        self._note_preview_lbl.setStyleSheet(
            f"color:{theme.TEXT_LABEL}; font-size:18px;"
            f" font-style:italic; background:transparent;"
        )

        note_col.addWidget(note_header)
        note_col.addWidget(self._note_preview_lbl)

        note_wrapper = QWidget()
        note_wrapper.setMinimumWidth(100)
        note_wrapper.setLayout(note_col)
        note_wrapper.setStyleSheet("background:transparent;")

        # ── Row assembly ──────────────────────────────────────────────────────
        row = QHBoxLayout(self)
        row.setContentsMargins(14, 14, 16, 14)
        row.setSpacing(12)

        row.addWidget(field("Date", self._date_str, theme.ACCENT_TEAL,  90))
        row.addWidget(vline())
        row.addWidget(field("Location", self._location_str, theme.ACCENT_BLUE, 90), stretch=1)
        row.addWidget(vline())
        row.addWidget(note_wrapper, stretch=1)
        row.addWidget(vline())
        row.addWidget(field("Amount",   f"${self._item.get_amount()}", theme.ACCENT_AMBER, 70))

    # ── Public API ────────────────────────────────────────────────────────────

    def get_date_str(self)         ->     str:  return self._date_str
    def get_location_str(self)     ->     str:  return self._location_str
    def get_amount_str(self)       ->     str:  return self._amount_str
    def get_note(self)             ->     str:  return self._note
    def has_note(self)             ->     bool: return bool(self._note.strip())


    def set_note(self, text: str):
        self._note    =  text
        display_text  =  ""
        preview_line  =  text.split('\n')[0]
        print(f"preview line: {preview_line}")
        if len(preview_line) > self.NOTE_PREVIEW_MAX:
            # only show the first x chars
            display_text = preview_line[-self.NOTE_PREVIEW_MAX:] + "..."
        else:
            display_text = preview_line
        self._note_preview_lbl.setText(display_text)
        self._refresh_style()

    def set_state(self, state: str):
        if self._state == state:
            return
        self._state = state
        if state == self.STATE_GREYED:
            eff = QGraphicsOpacityEffect(self)
            eff.setOpacity(0.25)
            self.setGraphicsEffect(eff)
        else:
            self.setGraphicsEffect(None)
        self._refresh_style()

    def set_connect_selected(self, on: bool):
        self._connect_selected = on
        self._refresh_style()

    def set_connected(self, connected_cards: dict[str, ItemCard]):
        if (not connected_cards):
            return
        
        self._refresh_style()

    # ── Stylesheet ────────────────────────────────────────────────────────────

    def _refresh_style(self):
        bg = theme.NOTE_HAS_BG if self.has_note() else theme.NOTE_NONE_BG

        if self._connect_selected:
            border = f"2px solid {theme.CONNECT_SELECT}"
        elif self._connected:
            border = f"1px solid {theme.CONNECT_PAIRED}"
        elif self._state == self.STATE_SPECIAL:
            border = f"2px solid {theme.SPECIAL_BORDER}"
        elif self._state == self.STATE_SOURCE:
            border = f"2px solid {theme.ACCENT_TEAL}"
        else:
            border = f"1px solid {theme.BORDER_DEFAULT}"

        self.setStyleSheet(f"""
            QFrame#ItemCard {{
                background : {bg};
                border      : {border};
            }}
        """)

    # ── Mouse events ──────────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_clicked.emit(self)
        elif event.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit(self, event.globalPosition().toPoint())
        super().mousePressEvent(event)

