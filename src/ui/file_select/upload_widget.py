from PyQt6.QtWidgets import QWidget, QFileDialog, QSizePolicy
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect, pyqtSignal
import os


class FileUploadWidget(QWidget):
    fileSelected = pyqtSignal(str)  # emits the full file path on selection

    def __init__(self, placeholder: str = "Click to attach a file...", parent=None):
        super().__init__(parent)
        self._placeholder = placeholder
        self._file_path: str | None = None

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(48)
        self.setMinimumWidth(200)

        # Colors
        self._color_border_empty = QColor("#555555")
        self._color_border_filled = QColor("#2ecc71")
        self._color_text_placeholder = QColor("#666666")
        self._color_text_filename = QColor("#eeeeee")
        self._color_bg = QColor("#1a1a1a")
        self._color_hover_bg = QColor("#222222")

        self._hovered = False

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def setPlaceholder(self, text: str):
        """Set the greyed-out hint text shown before a file is chosen."""
        self._placeholder = text
        self.update()

    def filePath(self) -> str | None:
        """Returns the selected file path, or None if nothing chosen yet."""
        return self._file_path

    def fileName(self) -> str | None:
        """Returns just the file name, or None if nothing chosen yet."""
        return os.path.basename(self._file_path) if self._file_path else None

    def clear(self):
        """Reset back to the empty/placeholder state."""
        self._file_path = None
        self.update()

    # ------------------------------------------------------------------ #
    #  Events                                                              #
    # ------------------------------------------------------------------ #

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._open_dialog()

    def enterEvent(self, event):
        self._hovered = True
        self.update()

    def leaveEvent(self, event):
        self._hovered = False
        self.update()

    def _open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self._file_path = path
            self.update()
            self.fileSelected.emit(path)

    # ------------------------------------------------------------------ #
    #  Painting                                                            #
    # ------------------------------------------------------------------ #

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(2, 2, -2, -2)  # inset so border isn't clipped
        radius = 8

        # Background
        bg = self._color_hover_bg if self._hovered else self._color_bg
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # Border
        pen = QPen()
        pen.setWidth(2)

        if self._file_path:
            # Solid green border when a file is attached
            pen.setStyle(Qt.PenStyle.SolidLine)
            pen.setColor(self._color_border_filled)
        else:
            # Dashed grey border when empty
            pen.setStyle(Qt.PenStyle.DashLine)
            pen.setColor(self._color_border_empty)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

        # Text
        font = QFont("Segoe UI", 10)
        painter.setFont(font)

        if self._file_path:
            painter.setPen(self._color_text_filename)
            # Elide the filename if it's too wide
            fm = QFontMetrics(font)
            padding = 32  # icon placeholder space on left
            available_width = rect.width() - padding - 12
            elided = fm.elidedText(
                self.fileName(), Qt.TextElideMode.ElideMiddle, available_width
            )
            text_rect = QRect(rect.x() + padding, rect.y(), available_width, rect.height())
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

            # Draw a small file icon on the left
            self._draw_file_icon(painter, rect, filled=True)
        else:
            painter.setPen(self._color_text_placeholder)
            text_rect = QRect(rect.x() + 12, rect.y(), rect.width() - 24, rect.height())
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._placeholder)

        painter.end()

    def _draw_file_icon(self, painter: QPainter, container: QRect, filled: bool):
        """Draws a tiny file icon on the left side of the widget."""
        color = self._color_border_filled if filled else self._color_border_empty
        pen = QPen(color, 1.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        x = container.x() + 10
        cy = container.center().y()
        w, h = 11, 14
        fold = 4

        # Body (with folded top-right corner)
        from PyQt6.QtGui import QPolygon
        from PyQt6.QtCore import QPoint
        body = QPolygon([
            QPoint(x,          cy - h // 2),
            QPoint(x + w - fold, cy - h // 2),
            QPoint(x + w,      cy - h // 2 + fold),
            QPoint(x + w,      cy + h // 2),
            QPoint(x,          cy + h // 2),
        ])
        painter.drawPolygon(body)

        # Fold corner line
        painter.drawLine(x + w - fold, cy - h // 2, x + w - fold, cy - h // 2 + fold)
        painter.drawLine(x + w - fold, cy - h // 2 + fold, x + w, cy - h // 2 + fold)

