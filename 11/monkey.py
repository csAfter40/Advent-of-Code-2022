from __future__ import annotations
from typing import List, Tuple, ClassVar, Iterator
from dataclasses import dataclass

@dataclass
class Monkey:
    instances: ClassVar[List] = []
    obj_count: ClassVar[int] = 0
    id: int
    items: List[int]
    operation: Tuple
    divisible:int
    true_target: int
    false_target: int
    inspect_count: int = 0

    def __post_init__(self) -> None:
        Monkey.instances.append(self)
        Monkey.obj_count += 1

    @classmethod
    def filter(cls, **kwargs) -> List:
        """
        Given kwargs, creates and returns alist of Monkey instances that fits 
        the properties given by kwargs.
        """
        return [obj for obj in cls.instances 
            if all(getattr(obj, key) == value for key, value in kwargs.items())]

    @classmethod
    def get(cls, **kwargs) -> List:
        """
        Given kwargs, creates and returns the first Monkey instance that fits 
        the properties given by kwargs. Returns None if no instance found.
        """
        instances = [obj for obj in cls.instances 
            if all(getattr(obj, key) == value for key, value in kwargs.items())]
        return instances[0] if instances else None

    def add_to_items(self, level:int) -> None:
        """
        Given worry level is appended to items list.
        """
        self.items.append(level)

    def remove_from_items(self, level:int) -> None:
        """
        Given a worry level, First matching level is removed from items list.
        """
        self.items.remove(level)

    def throw_to_target(self, level:int, target_id:int) -> None:
        """
        Given worry level and target id, worry level is appended to target 
        monkey's items list.
        """
        target = Monkey.get(id=target_id)
        target.add_to_items(level)

    def run_round(self) -> None:
        """
        Runs an inspection round due to problem intructions.
        """
        for item in self.items:
            old = item
            operation_level = eval(self.operation) #old variable used in eval function
            bored_level = operation_level//3
            if bored_level % self.divisible == 0:
                self.throw_to_target(bored_level, self.true_target)
            else:
                self.throw_to_target(bored_level, self.false_target)
            self.inspect_count += 1
        self.items = []

class App:
    def __init__(self, path:str, rounds:int) -> None:
        self.path = path
        self.rounds = rounds

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.path) as f:
            for line in f:
                yield line.strip()

    def get_monkey_data(self) -> List[dict]:
        """
        Reads data from file, creates and returns a list of dictonary of monkey 
        data extracted from the file.
        """
        monkeys = []
        monkey = {}
        for line in self.get_lines():
            if line.startswith("Monkey"):
                monkey = {}
                monkey["id"] = int(line.split()[1][:-1])
            if line == "":
                monkeys.append(monkey)
            if line.startswith("Starting"):
                monkey["items"] = [int(num) for num in line.split(":")[1].split(",")]
            if line.startswith("Operation"):
                monkey["operation"] = line.split(":")[1].split("=")[1]
            if line.startswith("Test"):
                monkey["divisible"] = int(line.split()[-1])
            if "true" in line:
                monkey["true_target"] = int(line.split()[-1])
            if "false" in line:
                monkey["false_target"] = int(line.split()[-1])
        return monkeys

    def create_monkeys(self) -> None:
        """
        Read data from file at self.path and creates monkey instances.
        """ 
        data = self.get_monkey_data()
        try:
            for item in data:
                Monkey(**item)
        except Exception:
            raise Exception("No proper data available to create monkeys")

    def run_monkeys(self) -> None:
        """
        Start monkey activities due to problem logic.
        """
        for round in range(self.rounds):
            for monkey in Monkey.instances:
                monkey.run_round()
            

    def get_monkey_business(self) -> None:
        """
        Finds two most active monkeys and returns monkey business value.
        """
        inspect_counts = sorted([monkey.inspect_count for monkey in Monkey.instances], reverse=True)
        return inspect_counts[0] * inspect_counts[1]

    def main(self):
        self.create_monkeys()
        self.run_monkeys()
        monkey_business = self.get_monkey_business()
        print(monkey_business)

if __name__ == "__main__":
    app = App("11/monkey.txt", 20)
    app.main()
