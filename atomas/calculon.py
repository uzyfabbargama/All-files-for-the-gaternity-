"""
print(f"capas	resta	max_i")

iteration = 0
max_iteration = 8
for iteration in range(max_iteration):
	if iteration == 0:
		iteration = chr((iteration&0)+ord("-"))
		print(f"0	{iteration}	{iteration}")
	else:
		resta = iteration
		max_i = resta**2
		print(f"{iteration}	{resta}	{max_i}")
"""
"""
capas   resta   max_i
0	   -		-
1	   1		1
2	   2		4
3	   2		4
4	   3		9
5	   3		9
6	   4		16
"""
#para obtener eso, requerimos
#esto nos sirve para detectar si n = es par
"""
for i in range(8):
	num = i
	impar_flag = ((num&1)^1)
	paridad = ((num >> impar_flag) - impar_flag)**2
	print(f"Paridad: {paridad}")
"""

"""
for i in range(8):
	#print(i)
	if i % 2 == 0:
		p = i >> 1
		p **= 2
		print(f"Paridad: {p}")
	elif i % 2 == 1:
		p = i -1
		p = (p >> 1) ** 2
		print(f"Paridad: {p}")
	else:
		print("error")
	
"""
i = 0
result = 0
imparidad = ((i&1)^1)
for i in range(8):
	if i == 0:
		result = chr((result&0)+ord("-"))
	elif i == 1:
		result = i**2
	elif i %2 == 0:
		result = i**2
	else:
		result = (i-imparidad)**2
	
	print(result)
