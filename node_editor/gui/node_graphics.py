from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from node_editor.common import Node_Status

from itertools import zip_longest


class Node_Graphics(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.title_text = "Title"
        self.title_color = QtGui.QColor(123, 33, 177)
        self.size = QtCore.QRectF()  # Size of
        self.status = Node_Status.DIRTY

        self.widget = QtWidgets.QWidget()
        self.widget.resize(0, 0)

        self.type_text = "base"

        self._width = 20  # The Width of the node
        self._height = 20  # the height of the node
        self._pins = []  # A list of pins
        self.uuid = None  # An identifier to used when saving and loading the scene

        self.node_color = QtGui.QColor(20, 20, 20, 200)

        self.title_path = QtGui.QPainterPath()  # The path for the title
        self.type_path = QtGui.QPainterPath()  # The path for the type
        self.misc_path = QtGui.QPainterPath()  # a bunch of other stuff
        self.status_path = QtGui.QPainterPath()  # A path showing the status of the node

        self.horizontal_margin = 15  # horizontal margin
        self.vertical_margin = 15  # vertical margin

    def get_status_color(self):
        if self.status == Node_Status.CLEAN:
            return QtGui.QColor(0, 255, 0)
        elif self.status == Node_Status.DIRTY:
            return QtGui.QColor(255, 165, 0)
        elif self.status == Node_Status.ERROR:
            return QtGui.QColor(255, 0, 0)

    def boundingRect(self):
        return self.size

    def set_color(self, title_color=(123, 33, 177), background_color=(20, 20, 20, 200)):
        self.title_color = QtGui.QColor(title_color[0], title_color[1], title_color[2])
        self.node_color = QtGui.QColor(background_color[0], background_color[1], background_color[2])

    def paint(self, painter, option=None, widget=None):
        """
        Paints the node on the given painter.

        Args:
            painter (QtGui.QPainter): The painter to use for drawing the node.
            option (QStyleOptionGraphicsItem): The style options to use for drawing the node (optional).
            widget (QWidget): The widget to use for drawing the node (optional).
        """

        painter.setPen(self.node_color.lighter())
        painter.setBrush(self.node_color)
        painter.drawPath(self.path)

        gradient = QtGui.QLinearGradient()
        gradient.setStart(0, -90)
        gradient.setFinalStop(0, 0)
        gradient.setColorAt(0, self.title_color)  # Start color (white)
        gradient.setColorAt(1, self.title_color.darker())  # End color (blue)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(self.title_color)
        painter.drawPath(self.title_bg_path.simplified())

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.white)

        painter.drawPath(self.title_path)
        painter.drawPath(self.type_path)
        painter.drawPath(self.misc_path)

        # Status path
        painter.setBrush(self.get_status_color())
        painter.setPen(self.get_status_color().darker())
        painter.drawPath(self.status_path.simplified())

        # Draw the highlight
        if self.isSelected():
            painter.setPen(QtGui.QPen(self.title_color.lighter(), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(self.path)

    def build(self):
        """
        Builds the node by constructing its graphical representation.

        This method calculates the dimensions of the node, sets the fonts for various elements, and adds the necessary
        graphical components to the node, such as the title, type, and pins. Once the graphical representation of the node
        is constructed, the `setPath` method is called to set the path for the node.

        Returns:
            None.
        """

        self.init_widget()  # configure the widget side of things. We need to get the size of the widget before building the rest of the node
        self.widget.setStyleSheet("background-color: " + self.node_color.name() + ";")
        self.title_path = QtGui.QPainterPath()  # reset
        self.type_path = QtGui.QPainterPath()  # The path for the type
        self.misc_path = QtGui.QPainterPath()  # a bunch of other stuff

        bg_height = 35  # background title height

        total_width = self.widget.size().width()
        self.path = QtGui.QPainterPath()  # The main path
        # The fonts what will be used
        title_font = QtGui.QFont("Lucida Sans Unicode", pointSize=12)
        title_type_font = QtGui.QFont("Lucida Sans Unicode", pointSize=8)
        pin_font = QtGui.QFont("Lucida Sans Unicode")

        # Get the dimentions of the title and type
        title_dim = {
            "w": QtGui.QFontMetrics(title_font).horizontalAdvance(self.title_text),
            "h": QtGui.QFontMetrics(title_font).height(),
        }

        title_type_dim = {
            "w": QtGui.QFontMetrics(title_type_font).horizontalAdvance(f"{self.type_text}"),
            "h": QtGui.QFontMetrics(title_type_font).height(),
        }

        # Get the max width
        for dim in [title_dim["w"], title_type_dim["w"]]:
            if dim > total_width:
                total_width = dim

        # Add both the title and type height together for the total height
        # total_height = sum([title_dim["h"], title_type_dim["h"]]) + self.widget.size().height()
        total_height = bg_height + self.widget.size().height()

        pin_dim = None
        # Add the heigth for each of the pins
        pin_height = QtGui.QFontMetrics(pin_font).height()

        def pins(self, input, execution):
            for pin in self.input_pins() if input else self.output_pins():
                if pin.execution if execution else not pin.execution:
                    yield pin
        for (inPin, outPin) in zip_longest(pins(self, True, True), pins(self, False, True), fillvalue=None):
            in_pin_dim_width = 0 if inPin is None else QtGui.QFontMetrics(pin_font).horizontalAdvance(inPin.name)
            if inPin and not inPin.execution_show_text: in_pin_dim_width = 0
            out_pin_dim_width = 0 if outPin is None else QtGui.QFontMetrics(pin_font).horizontalAdvance(outPin.name)
            if outPin and not outPin.execution_show_text: out_pin_dim_width = 0

            total_width = max(total_width, in_pin_dim_width + out_pin_dim_width)

            # if pin.execution and not exec_height_added or not pin.execution:
            total_height += pin_height
                # exec_height_added = True
        for (inPin, outPin) in zip_longest(pins(self, True, False), pins(self, False, False), fillvalue=None):
            in_pin_dim_width = 0 if inPin is None else QtGui.QFontMetrics(pin_font).horizontalAdvance(inPin.name)
            out_pin_dim_width = 0 if outPin is None else QtGui.QFontMetrics(pin_font).horizontalAdvance(outPin.name)

            total_width = max(total_width, in_pin_dim_width, out_pin_dim_width)

            # 
            total_height += ((0 if inPin is None else 1) + (0 if outPin is None else 1)) * pin_height
                # exec_height_added = True

        # Add the margin to the total_width
        total_width += self.horizontal_margin
        # total_height += self.vertical_margin

        # Draw the background rectangle
        self.size = QtCore.QRectF(-total_width / 2, -total_height / 2, total_width, total_height)
        self.path.addRoundedRect(-total_width / 2, -total_height / 2, total_width, total_height + 10, 5, 5)

        # Draw the status rectangle
        self.status_path.setFillRule(Qt.WindingFill)
        self.status_path.addRoundedRect(total_width / 2 - 12, -total_height / 2 + 2, 10, 10, 2, 2)
        # self.status_path.addRect(total_width / 2 - 10, -total_height / 2, 5, 5)
        # self.status_path.addRect(total_width / 2 - 10, -total_height / 2 + 15, 5, 5)
        # self.status_path.addRect(total_width / 2 - 5, -total_height / 2 + 15, 5, 5)

        # The color on the title
        self.title_bg_path = QtGui.QPainterPath()  # The title background path
        self.title_bg_path.setFillRule(Qt.WindingFill)
        self.title_bg_path.addRoundedRect(-total_width / 2, -total_height / 2, total_width, bg_height, 5, 5)
        self.title_bg_path.addRect(-total_width / 2, -total_height / 2 + bg_height - 10, 10, 10)  # bottom left corner
        self.title_bg_path.addRect(total_width / 2 - 10, -total_height / 2 + bg_height - 10, 10, 10)  # bottom right corner

        # Draw the title
        self.title_path.addText(
            -total_width / 2 + 5,
            (-total_height / 2) + title_dim["h"] / 2 + 5,
            title_font,
            self.title_text,
        )

        # Draw the type
        self.type_path.addText(
            -total_width / 2 + 5,
            (-total_height / 2) + title_dim["h"] + 5,
            title_type_font,
            f"{self.type_text}",
        )

        # Position the pins. Execution pins stay on the same row
        if len(self._pins) > 0:
            # y = (-total_height / 2) + title_dim["h"] + title_type_dim["h"] + 5
            y = bg_height - total_height / 2 - 10
            inY = y
            outY = y

            # Do the execution pins
            exe_shifted = 0
            for pin in self._pins:
                if not pin.execution:
                    continue
                if pin.is_output:
                    outY += pin_height
                    pin.setPos(total_width / 2 - 10, outY)
                else:
                    inY += pin_height
                    pin.setPos(-total_width / 2 + 10, inY)
            
            y = max(inY, outY)

            # Do the rest of the pins
            for pin in self._pins:
                if pin.execution:
                    continue

                if pin.is_output:
                    y += pin_height
                    pin.setPos(total_width / 2 - 10, y)
                else:
                    y += pin_height
                    pin.setPos(-total_width / 2 + 10, y)

        self._width = total_width
        self._height = total_height

        # move the widget to the bottom
        self.widget.move(-self.widget.size().width() / 2, total_height / 2 - self.widget.size().height() + 5)
