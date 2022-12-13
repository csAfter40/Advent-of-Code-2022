from typing import Any, List

class Packet():
    def __init__(self, text:str) -> None:
        if isinstance(text, list):
            text = str(text)
        self.text = text
        self.set_value()

    def __repr__(self) -> str:
        return self.text

    def __getitem__(self, item:Any) -> Any:
        return self.value[item]

    def __len__(self) -> int:
        return len(self.value)

    def __lt__(self, other) -> bool:
        for i, item in enumerate(self.value):
            if len(other)>i:
                if str(item) == str(other[i]):
                    continue
                if isinstance(item, int) and isinstance(other[i], Packet):
                    if str([item]) == str(other[i]):
                        continue
                    return Packet(str([item])) < other[i]
                elif isinstance(item, Packet) and isinstance(other[i], int):
                    if str(item) == str([other[i]]):
                        continue
                    return item < Packet(str([other[i]]))
                else:
                    if str(item) == str(other[i]):
                        print(item, other[i])
                        continue
                    return item < other[i]
            else:
                return False
        return True

    def set_value(self) -> None:
        """
        Sets value of the object using object's text.
        """
        self.value = []
        evaluated_value = eval(self.text)
        if evaluated_value:
            for item in evaluated_value:
                if isinstance(item, list):
                    self.value.append(Packet(str(item)))
                else:
                    self.value.append(item)


class App():
    def __init__(self, file_path:str) -> None:
        self.file_path:str = file_path
        self.pair_list:list(list) = []
        self.order_list:list(int) = [] # 1 if right order, 0 otherwise
        self.packets:list(Packet) = []

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()
            
    def create_pair_list(self) -> None:
        """
        Reads input from file and creates a list of package pairs.
        """
        pair = []
        for line in self.get_lines():
            if not line:
                self.pair_list.append(pair)
                pair = []
                continue
            packet = Packet(line)
            self.packets.append(packet)
            pair.append(packet)
        self.pair_list.append(pair)

    def compare_pairs(self) -> None:
        """
        Compares pairs in 
        """
        for pair in self.pair_list:
            self.order_list.append(1) if pair[0] < pair[1] else self.order_list.append(0)    

    def get_indices_sum(self) -> int:
        """
        Returns sum of indices of order list where value is 1.
        """
        return sum([i+1 for i, value in enumerate(self.order_list) if value == 1])

    def add_to_packets(self, *args:Any) -> None:
        """
        Appends the given packet to packets list.
        """
        for arg in args:
            if isinstance(arg, list):
                arg = Packet(str(arg))
            self.packets.append(arg)

    def get_sorted_packets(self, reverse=False) -> List[Packet]:
        """
        Returns sorted packets list.
        """
        return sorted(self.packets, reverse=reverse)

if __name__ == "__main__":
    # app = App("13/test_input.txt")
    app = App("13/distress_signal.txt")
    app.create_pair_list()
    app.compare_pairs()
    print(f"Sum of indices: {app.get_indices_sum()}")
    
    divider1 = Packet([[2]])
    divider2 = Packet([[6]])
    app.add_to_packets(divider1, divider2)
    sorted_packets = app.get_sorted_packets()
    decoder_key = (sorted_packets.index(divider1)+1) * (sorted_packets.index(divider2)+1)
    print(f"Decoder key: {decoder_key}")