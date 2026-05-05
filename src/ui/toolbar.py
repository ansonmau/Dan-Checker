# ─────────────────────────────────────────────────────────────────────────────
#  src/ui/toolbar.py  –  ToolBar
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

from PyQt6.QtCore    import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QWidget,
)

from ui import theme


# ─────────────────────────────────────────────────────────────────────────────
class ToolBar(QWidget):
    """
    Top toolbar.  Emits:
      name_changed(str)     – user typed in the name field
      connect_toggled(bool) – connect mode on / off
      sync_clicked()        – sync button pressed
    """

    name_changed    = pyqtSignal(str)
    connect_toggled = pyqtSignal(bool)
    sync_clicked    = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ToolBar")
        self.setFixedHeight(54)
        self.setStyleSheet(f"""
            QWidget#ToolBar {{
                background    : {theme.BG_TOOLBAR};
                border-bottom : 1px solid {theme.BORDER_DEFAULT};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 0, 22, 0)
        layout.setSpacing(0)

        # ── 1. Name ───────────────────────────────────────────────────────────
        layout.addWidget(_muted_label("Name"))
        layout.addSpacing(8)

        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("Your name…")
        self._name_input.setFixedWidth(160)
        self._name_input.setStyleSheet(f"""
            QLineEdit {{
                background    : {theme.BG_DARK};
                color         : {theme.TEXT_PRIMARY};
                border        : 1px solid {theme.BORDER_DEFAULT};
                border-radius : 6px;
                padding       : 4px 10px;
                font-size     : 12px;
            }}
            QLineEdit:focus {{
                border : 1px solid {theme.ACCENT_BLUE}99;
            }}
            QLineEdit::placeholder {{
                color : {theme.TEXT_MUTED};
            }}
        """)
        self._name_input.textChanged.connect(self.name_changed)
        layout.addWidget(self._name_input)

        layout.addWidget(_vsep())

        # ── 2. Connect ────────────────────────────────────────────────────────
        self._connect_btn = _tool_button("Connect", theme.ACCENT_BLUE, checkable=True)
        self._connect_btn.clicked.connect(
            lambda checked: self.connect_toggled.emit(checked)
        )
        layout.addWidget(self._connect_btn)

        layout.addWidget(_vsep())

        # ── 3. Sync ───────────────────────────────────────────────────────────
        self._sync_btn = _tool_button("⟳  Sync", theme.ACCENT_TEAL)
        self._sync_btn.clicked.connect(self.sync_clicked)
        layout.addWidget(self._sync_btn)

        layout.addStretch()

    # ── Public ────────────────────────────────────────────────────────────────
    def get_name(self) -> str:
        return self._name_input.text()


# ── Private helpers ───────────────────────────────────────────────────────────

def _muted_label(text: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setStyleSheet(
        f"color:{theme.TEXT_MUTED}; font-size:9px; font-weight:800;"
        f" letter-spacing:1.5px; background:transparent;"
    )
    return lbl


def _vsep() -> QWidget:
    """Thin vertical separator with horizontal breathing room."""
    wrapper = QWidget()
    wrapper.setFixedSize(30, 54)
    wrapper.setStyleSheet("background:transparent;")
    line = QFrame(wrapper)
    line.setFrameShape(QFrame.Shape.VLine)
    line.setFixedSize(1, 24)
    line.move(14, 15)
    line.setStyleSheet(f"background:{theme.BORDER_DEFAULT};")
    return wrapper


def _tool_button(text: str, accent: str, checkable: bool = False) -> QPushButton:
    btn = QPushButton(text)
    btn.setCheckable(checkable)
    btn.setStyleSheet(f"""
        QPushButton {{
            background    : transparent;
            color         : {accent};
            border        : 1px solid {accent}55;
            border-radius : 6px;
            padding       : 5px 16px;
            font-size     : 11px;
            font-weight   : 700;
            letter-spacing: 0.4px;
        }}
        QPushButton:hover {{
            background : {accent}1A;
            border     : 1px solid {accent}AA;
        }}
        QPushButton:checked {{
            background : {accent}2E;
            border     : 1px solid {accent};
        }}
    """)
    return btn
