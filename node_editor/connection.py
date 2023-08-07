from node_editor.gui.connection_graphics import Connection_Graphics


class Connection(Connection_Graphics):
    def __init__(self, parent):
        super().__init__(parent)

        self.start_pin = None
        self.end_pin = None

    def pins(self):
        """
        Returns a tuple of the two connected pins.

        Returns:
        tuple: A tuple of the two Pin objects connected by this Connection.
        """
        def impl(self):
            for pin in (self.start_pin, self.end_pin):
                if pin is not None:
                    yield pin
        return tuple(impl(self))
        

    def other_pin(self, otherPin):
        """
        Given a pin in this connection returns the other pin

        Returns:
        pin: The other pin
        """
        for pin in self.pins():
            if pin != otherPin:
                return pin
        return None

    def disconnect_start_pin(self):
        if self.start_pin is not None:
            self.start_pin.on_disconnected(self)
            self.start_pin.connections.remove(self)
        self.start_pin = None

    def disconnect_end_pin(self, eventAlreadyCalled = False):
        if self.end_pin is not None:
            if not eventAlreadyCalled:
                self.end_pin.on_disconnected(self)
            self.end_pin.connections.remove(self)
        self.end_pin = None

    def delete(self):
        """
        Deletes the connection and removes it from the scene and any connected pins.
        """
        if self.end_pin is not None: 
            self.end_pin.on_disconnected(self)
        self.disconnect_start_pin()
        self.disconnect_end_pin(True) # When we disconnect specify that we don't want to fire the disconnect event a second time!

        self.scene().removeItem(self)

    def set_start_pin(self, pin):
        self.disconnect_start_pin()
        self.start_pin = pin
        self.start_pin.connections.append(self)
        self.start_pin.on_connected(self)

    def set_end_pin(self, pin):
        self.disconnect_end_pin()
        self.end_pin = pin
        self.end_pin.connections.append(self)
        self.end_pin.on_connected(self)

    
    def nodes(self):
        """
        Returns a tuple of the two connected nodes.

        Returns:
        tuple: A tuple of the two Node objects connected by this Connection.
        """
        def impl(self):
            for pin in self.pins():
                if pin:
                    yield pin.node
        # return (self.start_pin.node, self.end_pin.node)

        return tuple(impl(self))

    def update_start_and_end_pos(self):
        """
        Update the start and end positions of the Connection.

        Get the start and end pins and use them to set the start and end positions.
        """

        if self.start_pin and not self.start_pin.is_output:
            temp = self.end_pin
            self.end_pin = self.start_pin
            self.start_pin = temp

        if self.start_pin:
            self.start_pos = self.start_pin.scenePos()

        if self.end_pin:
            self.end_pos = self.end_pin.scenePos()

        self.update_path()
