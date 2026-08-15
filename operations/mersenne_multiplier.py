a = 0
# 1 = 1
# 2 = 2
# 3 = 2
b = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4]
c = 0
d = 0
e = 0
f = 0
g = 0
print("X(4b)	MMB(X)	Decimal	¿Qué parece?	Rel Sqr")
while a != 15:
    a += 1 # a = 1
    c = ((a << b[a]) | a) - ((1<<b[a])|1) # c = 1
    d = c ^ a
    e = d - a
    f = d - a*a
    #g = a
    #e -= f
    if e != 0:
        print(f"{a}	{c}	{d}	{e}		{a}²+{f}")
    else:
        print(f"{a}	{c}	{d}	Constante	{a}²+{f}")

#a = 11
#a <<= b[a]
#a |= a
