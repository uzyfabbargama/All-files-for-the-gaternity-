print(hex(16 - 1))

#6, (11), 9C, F, (01), F, (01), 9C

valor =(((((((((((((6*4)+3)*256)+156)*16)+15)*4)+1)*16)+15)*4)+1)*256)+156
bvalor = bin(valor)[2:]
print(valor)

#110 11 10011100 1111 01 1111 01 10011100
#110 0011 10011100 1111 0001 1111 0001 10011100
count=len(str(bvalor))
posS, posT, posU, posV, posW, posX, posY, posZ = 2**2, 2**4, 2**12, 2**16, 2**18, 2**22, 2**24, 2**32
cseis = len(str(bin(posT)[2:]))
resultado = str((valor // 2 **(count - cseis))%4)
print(f"\033[32m{resultado}\033[0m")
#10000 =

