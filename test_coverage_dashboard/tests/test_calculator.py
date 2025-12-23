from src.calculator import *

def test_add(): assert add(3, 2) == 5
def test_sub(): assert sub(5, 3) == 2
def test_mul(): assert mul(4, 2) == 8

# We intentionally skip div test to show uncovered code!
