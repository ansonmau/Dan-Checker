# ─────────────────────────────────────────────────────────────────────────────
#  src/ui/note_popup.py  –  floating note editor
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore    import Qt, QPoint
from PyQt6.QtGui     import QColor, QPainter, QPen, QPainterPath
from PyQt6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QVBoxLayout, QWidget,
)

from ui import theme

if TYPE_CHECKING:
    from ui.card import ItemCard


class NotePopup(QDialog):
    """
    Minimal, borderless note editor.  Appears near the right-clicked card.
    Saves its content back to the card on "Save".
    """

    _RADIUS  = 1
    _PADDING = 10   # transparent margin so the shadow can breathe

    def __init__(self, card: "ItemCard", parent=None):
        super().__init__(parent)
        self._card = card

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(990, 702)

        # ── Outer transparent margin ──────────────────────────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(
            self._PADDING, self._PADDING,
            self._PADDING, self._PADDING,
        )

        # ── Visible card (handles its own background via paintEvent) ──
        self._panel = _PopupPanel()
        outer.addWidget(self._panel)

        # ── Inner layout ──────────────────────────────────────────────
        layout = QVBoxLayout(self._panel)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        header_container = QHBoxLayout()
        header_txt_1 = QLabel( card.get_date_str() )
        header_txt_2 = QLabel( card.get_location_str() )
        header_txt_3 = QLabel( "".join(["$", card.get_amount_str()]) )
        for header_txt in [header_txt_1, header_txt_2, header_txt_3]:
            header_txt.setStyleSheet(
                f"color:{theme.TEXT_LABEL}; font-size:18; font-weight:400;"
                f" letter-spacing:0.8px; background:transparent;"
            )
            header_container.addWidget(header_txt)
        layout.addLayout(header_container)

        self._editor = QTextEdit()
        self._editor.setPlaceholderText("Write a note…")
        self._editor.setPlainText(card.get_note())
        self._editor.setStyleSheet(f"""
            QTextEdit {{
                background : {theme.BG_DARK};
                color      : {theme.TEXT_PRIMARY};
                border     : 1px solid {theme.BORDER_DEFAULT};
                border-radius : 1px;
                padding    : 16px;
                font-size  : 18px;
            }}
            QTextEdit:focus {{
                border: 1px solid {theme.ACCENT_BLUE}99;
            }}
            QScrollBar:vertical {{
                background : {theme.BG_DARK};
                width      : 10px;
                border-radius : 5px;
            }}
            QScrollBar::handle:vertical {{
                background    : {theme.BORDER_DEFAULT};
                border-radius : 5px;
            }}
        """)
        layout.addWidget(self._editor, stretch=1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addStretch()
        btn_row.addWidget(_btn("Cancel", theme.TEXT_MUTED, theme.BORDER_DEFAULT, self.reject))
        btn_row.addWidget(_btn("Save",   "#0a0a0a",        theme.ACCENT_TEAL,    self._save, filled=True))
        layout.addLayout(btn_row)

    # ── Positioning helper ────────────────────────────────────────────────────

    def show_near(self, global_pos: QPoint):
        """Position the popup near a global screen point, clamped to screen."""
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = min(global_pos.x() + 6, screen.right()  - self.width())
        y = min(global_pos.y() + 6, screen.bottom() - self.height())
        self.move(max(x, screen.left()), max(y, screen.top()))

    # ─────────────────────────────────────────────────────────────────────────

    def _save(self):
        self._card.set_note(self._editor.toPlainText())
        self.accept()


# ── Internal helpers ──────────────────────────────────────────────────────────

class _PopupPanel(QWidget):
    """Rounded rectangle panel — paints its own background."""

    _R = NotePopup._RADIUS

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Soft shadow layer
        for i in range(6, 0, -1):
            p.setBrush(QColor(0, 0, 0, 18))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(
                self.rect().adjusted(i, i, -i, -i),
                self._R, self._R,
            )

        # Background fill
        p.setBrush(QColor(theme.BG_POPUP))
        p.setPen(QPen(QColor(theme.BORDER_DEFAULT), 1))
        p.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), self._R, self._R)
        p.end()


def _btn(text: str, fg: str, color: str, slot, filled: bool = False) -> QPushButton:
    bg = color if filled else "transparent"
    b = QPushButton(text)
    b.setStyleSheet(f"""
        QPushButton {{
            background    : {bg};
            color         : {fg};
            border        : 1px solid {color};
            border-radius : 8px;
            padding       : 10px 28px;
            font-size     : 18px;
            font-weight   : 700;
        }}
        QPushButton:hover {{
            background : {color}{"" if filled else "22"};
        }}
    """)
    b.clicked.connect(slot)
    return b
