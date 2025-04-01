# mypackage/calculator.py


# 변수 (global)
__version__ = 0.1


# 함수
def plus(num1, num2):
    return num1 + num2

def minus(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

if __name__ == "__main__":
    print(">>>>>name<<<<<<", __name__)
    print(plus(3,5))
    print(minus(76,32))
    print(multiply(84, 39))
    print(divide(172, 83))