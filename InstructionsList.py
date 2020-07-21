from Constants import DoublyLinkedNode


class InstructionsList(object):

    MISSING_NODE_ERROR = "List does not contain target node!"  # global error messages

    ERROR_SUFFIX = "Terminating..."

    def __init__(self, initial_node=None, final_node=None):
        self.__initial_node = initial_node
        self.__final_node = final_node

        self.__length = int(initial_node is not None) + int(final_node is not None)

    def __str__(self):
        return str(list(self.as_python_list()))

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return list(self.as_python_list()).__eq__(list(other.as_python_list()))

    def __len__(self):
        return self.length

    @staticmethod
    def of(*values):
        for value in values:
            dll.append(DoublyLinkedNode(value))
        return dll

    def as_python_list(self):
        self.forward_traversal(lambda node: py_list.append(node.data))
        return py_list

    def contains(self, node):
        self.forward_traversal(lambda current_node: contains.append(current_node.__eq__(node)))
        return sum(contains) > 0

    def forward_traversal(self, func):
        node_index = 0
        current_node = self.initial_node
        while current_node:
            func(current_node, node_index)
            current_node = current_node.next_node
            node_index += 1

    def backward_traversal(self, func):
        node_index = self.length - 1
        current_node = self.final_node
        while current_node:
            func(current_node, node_index)
            current_node = current_node.prev_node
            node_index -= 1

    def insert_after(self, target_node, new_node):
        new_node.prev_node = target_node
        if not target_node.next_node:
            new_node.next_node = None
            self.final_node = new_node
        else:
            new_node.next_node = target_node.next_node
            target_node.next_node.prev_node = new_node
        target_node.next_node = new_node

        self.length += 1

    def insert_before(self, target_node, new_node):
        new_node.next_node = target_node
        if not target_node.prev_node:
            new_node.prev_node = None
            self.initial_node = new_node
        else:
            new_node.prev_node = target_node.prev_node
            target_node.prev_node.next_node = new_node
        target_node.prev_node = new_node

        self.length += 1

    def prepend(self, node):
        if not self.initial_node:
            self.initial_node, self.final_node = node, node
            node.prev_node, node.next_node = None, None
            self.length += 1
        else:
            self.insert_before(self.initial_node, node)

    def append(self, node):
        if not self.final_node:
            self.prepend(node)
        else:
            self.insert_after(self.final_node, node)

    def remove(self, target_node):
        if not self.contains(target_node):
            raise \
                Exception(
                    " ".join(list([
                        InstructionsList.MISSING_NODE_ERROR,
                        InstructionsList.ERROR_SUFFIX
                    ]))
                )

        if not target_node.prev_node:  # if the first target_node is being removed
            self.initial_node = target_node.next_node
        else:
            target_node.prev_node.next_node = target_node.next_node
        if not target_node.next_node:
            self.final_node = target_node.prev_node
        else:
            target_node.next_node.prev_node = target_node.prev_node

        self.length -= 1
        
    @property
    def initial_node(self):
        return self.__initial_node

    @initial_node.setter
    def initial_node(self, initial_node):
        self.__initial_node = initial_node

    @property
    def final_node(self):
        return self.__final_node

    @final_node.setter
    def final_node(self, final_node):
        self.__final_node = final_node

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, length):
        self.__length = length
