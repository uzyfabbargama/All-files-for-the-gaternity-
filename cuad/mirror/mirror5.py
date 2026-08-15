from math import log2
a_value = 0
a_values = []
b_value = 0
b_values = []
for i in range(128):
	a_value += 1 
	b_value = (int(log2(a_value)))+1
	a_values.append(a_value)
	b_values.append(b_value)
i = True
iteration = 0
print("Numero	Despl.  square.		mir result.	diff.	diff_bits")
while i:
    a = a_values[iteration]
    b = b_values[iteration]
    resultado = a << b
    resultado = resultado | a
    muesca = 1 << b | 1
    resultado -= muesca
    resultado ^= a
    cuadrado = a**2
    offset = resultado - cuadrado
    diff_bits = bin(offset)
    #resultado -= offset
    if iteration+2 > len(a_values):
    	i = False
    print(f"{a}	{b}	{cuadrado}		{resultado}		{offset}	{diff_bits}")
    iteration += 1
