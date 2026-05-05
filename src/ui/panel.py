# ─────────────────────────────────────────────────────────────────────────────
#  src/ui/panel.py  –  build_panel helper
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import Callable

from PyQt6.QtCore    import Qt
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget,
)

from ui       import theme
from ui.card  import ItemCard


def build_panel(
    items:         list,
    title:         str,
    on_left_click: Callable[[ItemCard], None],
    on_right_click: Callable,
) -> tuple[QWidget, list[ItemCard], QScrollArea]:
    """
    Build a single scroll panel for one list of items.

    Returns
    -------
    panel      – top-level QWidget (put in a layout)
    cards      – list of ItemCard instances in display order
    scroll     – the QScrollArea (used by the window for scroll-to)
    """
    cards: list[ItemCard] = []

    # ── Outer container ───────────────────────────────────────────────────────
    panel = QWidget()
    panel.setObjectName("Panel")
    panel.setStyleSheet(f"QWidget#Panel {{ background: {theme.BG_DARK}; }}")

    v = QVBoxLayout(panel)
    v.setContentsMargins(0, 0, 0, 0)
    v.setSpacing(0)

    # ── Sub-header ────────────────────────────────────────────────────────────
    bar = QWidget()
    bar.setObjectName("SubBar")
    bar.setFixedHeight(46)
    bar.setStyleSheet(f"""
        QWidget#SubBar {{
            background    : {theme.BG_TOOLBAR};
            border-bottom : 1px solid {theme.BORDER_DEFAULT};
        }}
    """)
    bl = QHBoxLayout(bar)
    bl.setContentsMargins(18, 0, 18, 0)

    title_lbl = QLabel(title)
    title_lbl.setStyleSheet(
        f"color:{theme.TEXT_PRIMARY}; font-size:13px; font-weight:700;"
        f" background:transparent;"
    )
    count_lbl = QLabel(f"{len(items)} items")
    count_lbl.setStyleSheet(
        f"color:{theme.TEXT_MUTED}; font-size:11px; background:transparent;"
    )

    bl.addWidget(title_lbl)
    bl.addStretch()
    bl.addWidget(count_lbl)
    v.addWidget(bar)

    # ── Scroll area ───────────────────────────────────────────────────────────
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setStyleSheet(f"""
        QScrollArea {{
            background : {theme.BG_DARK};
            border     : none;
        }}
        QScrollBar:vertical {{
            background    : {theme.BG_DARK};
            width         : 8px;
            margin        : 0;
            border-radius : 4px;
        }}
        QScrollBar::handle:vertical {{
            background    : {theme.BORDER_DEFAULT};
            min-height    : 32px;
            border-radius : 4px;
        }}
        QScrollBar::handle:vertical:hover {{
            background : {theme.ACCENT_BLUE};
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{ height: 0; }}
    """)

    # ── Cards container ───────────────────────────────────────────────────────
    container = QWidget()
    container.setObjectName("CardsContainer")
    container.setStyleSheet(
        f"QWidget#CardsContainer {{ background: {theme.BG_DARK}; }}"
    )

    cl = QVBoxLayout(container)
    cl.setContentsMargins(14, 12, 14, 16)
    cl.setSpacing(8)

    if items:
        for i, item in enumerate(items):
            card = ItemCard(item, i)
            card.left_clicked.connect(on_left_click)
            card.right_clicked.connect(on_right_click)
            cl.addWidget(card)
            cards.append(card)
    else:
        empty = QLabel("No items to display")
        empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty.setStyleSheet(
            f"color:{theme.TEXT_MUTED}; font-size:14px; padding:60px;"
        )
        cl.addWidget(empty)

    cl.addStretch()
    scroll.setWidget(container)
    v.addWidget(scroll)

    return panel, cards, scroll
