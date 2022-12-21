from typing import List, Dict, Tuple

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
        self.results["humn"] = None

    def make_operation(self, operation:List) -> int:
        """
        Given two numbers and a sign, returns the result of the operation.
        """
        monkey1 = self.calculate(operation[0])
        monkey2 = self.calculate(operation[2])
        if not monkey1 or not monkey2:
            return None
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

    def reverse_operation(self, value:int, sign:str, yell:int) -> int:
        """
        Given result, sign and a number, finds and returns other number of the operation.
        """
        if sign == "+":
            return value - yell
        elif sign == "-":
            return value + yell
        elif sign == "*":
            return int(value / yell)
        elif sign == "/":
            return value * yell

    def set_unknown_value(self, monkey:str, value:int):
        """
        Finds and sets the value of 'humn' monkey.
        """
        if monkey == "humn":
            self.results["humn"] = value
            return
        monkey1, sign, monkey2 = self.operations[monkey]
        yell1 = self.calculate(monkey1)
        yell2 = self.calculate(monkey2)
        if yell1:
            if sign == "-":
                yell2 = self.reverse_operation(yell1, "+", value)
            elif sign == "/":
                yell2 = self.reverse_operation(yell1, "*", value)
            else:
                yell2 = self.reverse_operation(value, sign, yell1)
            self.set_unknown_value(monkey2, yell2)
            self.results[monkey2] = yell2
        elif yell2:
            yell1 = self.reverse_operation(value, sign, yell2)
            self.set_unknown_value(monkey1, yell1)
            self.results[monkey1] = yell1


    def solve_equation(self) -> None:
        """
        Starter function for the recursive set_unknown_value function.
        """
        monkey1, monkey2 = self.operations["root"][0], self.operations["root"][2]
        yell1 = self.calculate(monkey1)
        yell2 = self.calculate(monkey2)
        if yell1:
            self.set_unknown_value(monkey2, yell1)
        self.set_unknown_value(monkey1, yell2)


if  __name__ == "__main__":
    file_path = "21/monkey_math.txt"
    # file_path = "21/test_input.txt"
    app = App(file_path)
    app.setup()
    app.solve_equation()
    print(app.results["humn"])
    print(len(app.results))