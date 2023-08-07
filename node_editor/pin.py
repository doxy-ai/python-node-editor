from node_editor.gui.pin_graphics import Pin_Graphics


class Pin(Pin_Graphics):
    def __init__(self, parent, scene):
        super().__init__(parent, scene)

        self.name = None
        self.node = None
        # self.connection = None
        self.connections = []
        self.max_connections = 1

    def set_execution(self, execution):
        self.execution = execution
        super().set_execution(execution)

    def set_name(self, name):
        self.name = name
        super().set_name(name)

    # def clear_connection(self):
    def clear_connections(self):
        if len(self.connections) > 0:
            for connection in self.connections:
                connection.delete()
        connections = []

    # Called when a new pin is connected
    def on_connected(self, connection):
        pass

    # Called when a new pin is disconnected
    def on_disconnected(self, connection):
        pass

    def all_connected_pins(self):
        for connection in self.connections:
            for pin in connection.pins():
                if pin != self:
                    yield pin

    def can_connect_to(self, pin):
        if not pin:
            return False
        if pin.node == self.node:
            return False

        # If either pin can't accept any more connections... false
        if len(self.connections) > self.max_connections - 1\
          or len(pin.connections) > pin.max_connections - 1:
            return False
        # If we are already connected to this pin... false
        if pin in self.all_connected_pins():
            return False

        return self.is_output != pin.is_output

    def is_connected(self):
        return bool(len(self.connections) > 0)

    def get_data(self):
        # Get a list of nodes in the order to be computed. Forward evaluation by default.
        def get_node_compute_order(node, forward=False):
            # Create a set to keep track of visited nodes
            visited = set()
            # Create a stack to keep track of nodes to visit
            stack = [node]
            # Create a list to store the evaluation order
            order = []

        # Get the next nodes that this node is dependent on
        def get_next_input_node(node):
            pass

        # Get the next nodes that is affected by the input node.
        def get_next_output_node(node):
            pass

        # if pin isn't connected, return it current data

        # get the evalutation order of the owning node of the pin

        # loop over each node and process it

        # return the pin's data
