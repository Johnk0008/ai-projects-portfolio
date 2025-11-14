import pytest
from calculator import Calculator

def test_addition():
    calc = Calculator()
    assert calc.add(5, 3) == 8
    assert calc.add(-1, 1) == 0

def test_subtraction():
    calc = Calculator()
    assert calc.subtract(10, 4) == 6

def test_multiplication():
    calc = Calculator()
    assert calc.multiply(3, 7) == 21

def test_division():
    calc = Calculator()
    assert calc.divide(15, 3) == 5

def test_division_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(10, 0)

def test_power():
    calc = Calculator()
    assert calc.power(2, 3) == 8

if __name__ == "__main__":
    pytest.main()