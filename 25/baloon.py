from typing import List
from models import Snafu


class App():
    def __init__(self, file_path:str, *args, **kwargs) -> None:
        self.file_path = file_path
        self.snafus:List[Snafu] = []
        self.conversion_map = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def extract_data(self) -> None:
        """
        Reads file and adds coordinates of walls, blizzards, start and finish 
        points to the related attributes.
        """
        for line in self.get_lines():
            self.snafus.append(Snafu(line))

       
    def setup(self) -> None:
        """
        Setup data structure.
        """
        self.extract_data()

    def convert_decimal_to_snafu(self, num:int) -> Snafu:
        """
        Given a decimal number, returns Snafu equivalent.
        """
        result = ""
        while num>0:
            remainder = num%5
            num = num//5
            if remainder > 2:
                remainder = remainder - 5
                num += 1
            result = self.conversion_map[remainder] + result
        return Snafu(result)

if  __name__ == "__main__":
    file_path = "25/baloon.txt"
    # file_path = "25/test_input.txt"
    app = App(file_path)
    app.setup()
    decimal_total = sum([snafu.get_decimal() for snafu in app.snafus])
    print(app.convert_decimal_to_snafu(decimal_total))
    