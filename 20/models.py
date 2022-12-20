class Node():
    def __init__(self, value:int=None) -> None:
        self.value = value
        self.next = None
        self.previous = None

    def __repr__(self) -> str:
        return f"{self.value} <-> "

class Sequence():
    def __init__(self, head:Node=Node()) -> None:
        self.head = head

    def __repr__(self) -> str:
        string = self.head.__repr__()
        current = self.head.next
        while current and not current == self.head:
            string += current.__repr__()
            current = current.next
        return string

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def __len__(self) -> int:
        current = self.head
        count = 0
        while True:
            count += 1
            if current.next == self.head:
                break
            current = current.next
        return count

    def remove(self, node:Node) -> None:
        """
        Removes the given node from Sequence.
        """
        if node == self.head:
            self.head = node.next
        node.previous.next = node.next
        node.next.previous = node.previous

    def insert_after(self, target:Node, node:Node) -> None:
        """
        Inserts given node after the target node.
        """
        node.next = target.next
        node.previous = target
        target.next.previous = node
        target.next = node
        
    def insert_before(self, target:Node, node:Node) -> None:
        """
        Inserts given node before the target node.
        """
        node.next = target
        node.previous = target.previous
        target.previous.next = node
        target.previous = node

    def move_forward(self, node:Node, distance:int) -> None:
        """
        Moves the given node forward with the given distance.
        """
        if distance == 0:
            return
        target = node
        for _ in range(distance):
            target = target.next
        self.remove(node)
        self.insert_after(target, node)
    
    def move_backward(self, node:Node, distance:int) -> None:
        """
        Moves the given node backward with the given distance.
        """
        if distance == 0:
            return
        target = node
        for _ in range(distance):
            target = target.previous
        self.remove(node)
        self.insert_before(target, node)

    def get_forward_node(self, node:Node, distance:int) -> Node:
        """
        Traverses the sequence and gets the node in the given distance forward.
        """
        current = node
        for _ in range(distance):
            current = current.next
        return current
    
    def get_backward_node(self, node:Node, distance:int) -> Node:
        """
        Traverses the sequence and gets the node in the given distance backward.
        """
        current = node
        for _ in range(distance):
            current = current.previous
        return current