num = 256
i = 0
all = []
reset = 0
add = 1
def rules(cut):
	colors_found = []
	alu = 0
	for bit in cut:
		bita = int(bit)
		
		if bita == 0:
			alu = reset
		elif bita == 1:
			alu += add
			
		if alu == 0:
			colors_found.append("negro")
		elif alu == 1:
			colors_found.append("blanco")
		elif alu == 2:
			colors_found.append("rojo")
		elif alu == 3:
			colors_found.append("verde")
		elif alu == 4:
			colors_found.append("azul")
		elif alu == 5:
			colors_found.append("verde rojo")
		elif alu == 6:
			colors_found.append("azul rojo")
		elif alu == 7:
			colors_found.append("azul verde")
		elif alu == 8:
			colors_found.append("blanco rojo verde rojo")
	return" ".join(colors_found)
for _ in range(0, 255):
	bina = bin(num)
	cut = bina[3:]
	all.append(rules(cut))
	print(f"{cut} = {all}")
	num += 1
