from typing import List
from models import Node, Sequence

class App():
    def __init__(self, file_path:str, *args, **kwargs) -> None:
        self.file_path = file_path
        self.nodes:List[Node] = []
        self.sequence:Sequence = None

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def extract_data(self) -> None:
        """
        Reads file and parses data.
        """
        previous = Node()
        for line in self.get_lines():
            value = int(line)
            node = Node(value)
            if value == 0:
                self.sequence = Sequence(node)
            node.previous = previous
            previous.next = node
            self.nodes.append(node)
            previous = node
        self.nodes[0].previous = self.nodes[-1]
        self.nodes[-1].next = self.nodes[0]
        

    def setup(self) -> None:
        """
        Setup data structure.
        """
        self.extract_data()

    def run(self) -> None:
        """
        Run mixing process.
        """
        for node in self.nodes:
            value = node.value
            if value > 0:
                if value%(len(self.nodes)-1) == 0:
                    continue
                self.sequence.move_forward(node, value%(len(self.nodes)-1))
            if value < 0:
                if abs(value)%(len(self.nodes)-1) == 0:
                    continue
                self.sequence.move_backward(node, abs(value)%(len(self.nodes)-1))

    def get_decrypted_product(self) -> int:
        """
        Returns decrypted product from the list.        
        """
        indexes = [1000, 2000, 3000]
        total = 0
        for index in indexes:
            target_node = self.sequence.get_forward_node(self.sequence.head, index%len(self.nodes))
            total += target_node.value
        return total

if  __name__ == "__main__":
    file_path = "20/encryption.txt"
    # file_path = "20/test_input.txt"
    app = App(file_path)
    app.setup()
    app.run()
    product = app.get_decrypted_product()
    print(product)