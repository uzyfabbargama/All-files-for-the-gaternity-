def adder(a, b):
    carry = 1
    while carry != 0:
        i = 1
        a = ((a + b) % 2) * 10^i
        carry = ((a * b) % 2) * 10 ^i
        i += 1
    return a
num1 = int(input())
num2 = int(input())
resultado = adder(num1, num2)
print(resultado)