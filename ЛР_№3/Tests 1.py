import pytest
import math
from LR_1 import calculate, convert_precision


def test_convert_precision():
    assert convert_precision(1e-6) == 6
    assert convert_precision(1e-4) == 4
    assert convert_precision(1e-8) == 8
    with pytest.raises(ValueError):
        convert_precision(-1e-6)


def test_calculate_with_tolerance():
    # Проверка округления с разной точностью
    assert calculate(1, 3, '/', tolerance=1e-4) == 0.3333
    assert calculate(1, 3, '/', tolerance=1e-6) == 0.333333
    assert calculate(2.34567, 1.11111, '+', tolerance=1e-3) == 3.457
    assert calculate(5.6789, 2.3456, '*', tolerance=1e-2) == 13.32


def test_calculate_basic_operations():
    assert calculate(2, 3, '+') == 5.0
    assert calculate(5, 2, '-') == 3.0
    assert calculate(4, 3, '*') == 12.0
    assert calculate(10, 2, '/') == 5.0
    assert calculate(10, 0, '/') == "Error"


def test_calculate_invalid_operand():
    assert calculate(2, 3, '%') == "Error: Invalid operand."