from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import math

'''Resource https://www.learnpyqt.com/courses/custom-widgets/creating-your-own-custom-widgets/'''

class _Bar(QtWidgets.QWidget):

    clickedValue = QtCore.pyqtSignal(int)

    def __init__(self, steps, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.NUM_BAR = steps
        self.PADDING = 5

    def _calculate_clicked_value(self, e):
        parent = self.parent()
        vmin, vmax = parent._dial.minimum(), parent._dial.maximum()
        d_height = self.size().height() + (self.PADDING * 2)
        step_size = d_height / self.NUM_BAR
        click_y = e.y() - self.PADDING - step_size / 2

        pc = (d_height - click_y) / d_height
        value = vmin + pc * (vmax - vmin)
        self.clickedValue.emit(value)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        self._calculate_clicked_value(e)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self._calculate_clicked_value(e)

    def sizeHint(self):
        return QtCore.QSize(40, 200)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        outer_brush = QtGui.QBrush()
        outer_brush.setColor(QtGui.QColor(10,10,10,10))
        outer_brush.setStyle(QtCore.Qt.SolidPattern)
        outer_rect = QtCore.QRect(0,0,painter.device().width(), painter.device().height())
        painter.fillRect(outer_rect, outer_brush)

        dial = self.parent()._dial
        vmin = dial.minimum()
        vmax = dial.maximum()
        value = dial.value()
        converted_value = (value - vmin) / (vmax - vmin)
        value_step = int(converted_value * self.NUM_BAR)


        # pen = painter.pen()
        # pen.setColor(QtGui.QColor('pink'))
        # painter.setPen(pen)


        # painter.drawText(10,20,f'{vmin} -- {value} -- {vmax} -- {converted_value} -- {n_steps_to_draw}')

        bar_brush = QtGui.QBrush()
        bar_brush.setColor(QtGui.QColor('pink'))
        bar_brush.setStyle(QtCore.Qt.SolidPattern)
        canvas_height = painter.device().height() - (self.PADDING * 2)
        canvas_width = painter.device().width() - (self.PADDING * 2)
        step_size = canvas_height / self.NUM_BAR
        bar_height = step_size * 0.6
        bar_space = step_size * 0.4 / 2

        for i in range(value_step):
            bar_brush.setColor(QtGui.QColor(converted_value* 200,110,0, 255))
            bar_rect = QtCore.QRect(
                self.PADDING, # left x
                self.PADDING + canvas_height -((i+1) * step_size) + bar_space, # top y
                canvas_width, # width
                bar_height # height
            )
            painter.fillRect(bar_rect, bar_brush)

        painter.end()



    def _trigger_refresh(self):
        self.update()


# class _Dial(QtWidgets.QDial):
#     pass

class PowerBar(QtWidgets.QWidget):
    def __init__(self, steps=5, *args, **kwargs):
        super(PowerBar, self).__init__(*args, **kwargs)


        layout = QtWidgets.QVBoxLayout()

        self._bar = _Bar(steps=10)
        layout.addWidget(self._bar)

        self._dial = QtWidgets.QDial()
        layout.addWidget(self._dial)
        self._dial.setNotchesVisible(True)
        self._dial.valueChanged.connect(self._bar._trigger_refresh)
        self._bar.clickedValue.connect(self._dial.setValue)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    pbar = PowerBar(steps=10)
    pbar.show()
    app.exec_()