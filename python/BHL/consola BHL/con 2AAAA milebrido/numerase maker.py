Base = 1000
Pos = []
PosCX = []
i = 0
d = 0
while i <= 6:
    # comment: 
    Pos.append(Base ** i * (2 ** d))
    PosCX.append(Base ** (1+i) * (2 ** d))
    print(Pos[i])
    print(PosCX[i])
    i += 1
    d += 1
# end while


#output:
#1 (PosZ), 1000 (1er ctrl), 2000 (PosY) ,2000000 (2do ctrl) ,4000000 (PosX) ,4000000000 ,8000000000 ,8000000000000 ,16000000000000 ,16000000000000000 ,32000000000000000 ,32000000000000000000 

#
base = 1000
PosC2 = (base**3)*2**2 #2**33
PosX = (base**2) * 2**2#2**22
PosC1 =(base**2)*2 #2**21
PosY = base*2 #2**11
PosC = base #2**10
PosZ = 1
print(base, PosC2, PosX, PosC1, PosY, PosC, PosZ)
#output 1 (PosZ), 1000 (1er ctrl), 2000 (PosY) ,2000000 (2do ctrl) ,4000000 (PosX)

#In summary: he creado una función que crea controladores y un numeraso dado un número de entrada

i = 0
d = 0
Numeraso = 0
while i <= 6:
    # comment: 
    
    Numeraso += Pos[i] + PosCX[d]
    i += 1
    d += 1
# end while
print(Numeraso)

#todo el numeraso de 6 variables y controladores, construido