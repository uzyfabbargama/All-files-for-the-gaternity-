Valor = int(input("Escriba un número")) %8000000

C = (Valor) % 100 #dato
C1 = (Valor // 100) % 2 #control
C2 = (Valor // 200) % 100 #dato
C3 = (Valor // 20000) % 2 #control
C4 = (Valor // 40000) % 100 #dato
C5 = (Valor // 4000000) % 2 #control

#C6 = (Valor // 8000000) % 100 #dato
#C7 = (Valor // 800000000) % 2 #control 

print (C5,C4,C3,C2,C1,C)
Exit = input("Por aquí salga")

#200 = 100*2
#20000 = 100*2*100 = (100**2)*2
#40000 = 100*2*100*2 = (100**2)*(2**2)
#4000000= 100*2*100*2*100 = (100**3)*(2**2)
#8000000 = 100*2*100*2*100*2 = (100**3)*(2**3)
#800000000 = 100*2*100*2*100*2*100 = (100**4)*(2**3)
##1600000000 = 100*2*100*2*100*2*100*2 = (100**4)*(2**4) (no hace falta, pero demuestra que se puede expandir) se usará para el mod 
