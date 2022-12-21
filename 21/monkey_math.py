from typing import List, Dict

class App():
    def __init__(self, file_path:str, *args, **kwargs) -> None:
        self.file_path = file_path
        self.results:Dict = {}
        self.operations:Dict = {} 

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
        for line in self.get_lines():
            monkey, yell = line.split(": ")
            if yell.strip().isnumeric():
                self.results[monkey] = int(yell.strip())
                continue
            self.operations[monkey] = yell.split()
        

    def setup(self) -> None:
        """
        Setup data structure.
        """
        self.extract_data()

    def make_operation(self, operation:List) -> int:
        """
        Given two numbers and a sign, returns the result of the operation.
        """
        monkey1 = self.calculate(operation[0])
        monkey2 = self.calculate(operation[2])
        sign = operation[1]
        if sign == "+":
            return monkey1 + monkey2
        elif sign == "-":
            return monkey1 - monkey2
        elif sign == "*":
            return monkey1 * monkey2
        elif sign == "/":
            return int(monkey1 / monkey2)

    def calculate(self, monkey:str) -> int:
        """
        Returns value of the monkey or makes the operation if value is not yet found.
        """
        if monkey in self.results:
            return self.results[monkey]
        result = self.make_operation(self.operations[monkey])
        self.results[monkey] = result
        return result

if  __name__ == "__main__":
    file_path = "21/monkey_math.txt"
    # file_path = "21/test_input.txt"
    app = App(file_path)
    app.setup()
    result = app.calculate("root")
    print(result)