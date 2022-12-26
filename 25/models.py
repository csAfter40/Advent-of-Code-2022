
from  __future__ import annotations

class Snafu:
    coefficient_map = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}

    def __init__(self, text:str, *args, **kwargs) -> None:
        self.text = text
        self.set_coefficients()
    
    def __repr__(self) -> str:
        return self.text

    def set_coefficients(self) -> None:
        """
        Reads self.text and creates a list of coefficients for each digit.
        """
        self.coefficients = []
        for char in self.text:
            self.coefficients.append(self.coefficient_map[char])

    def get_decimal(self) -> int:
        """
        Returns decimal equivalent of the Snafu.
        """
        decimal = 0
        for i, value in enumerate(self.coefficients[-1::-1]):
            decimal += value*(5**i)
        return decimal