
exec("print('hola')")
seed = 112
#ascii_code = [112, 114, 105, 110, 116, 40, 39, 104, 111, 108, 97, 126, 39, 41]
d = 2
dees = 0
#for i in dees:
    #dees = 112
#ascii_code = [seed, seed+d, seed-d*3-1, seed-d, seed+d*2, seed-(72), seed-73, seed-d**3, seed-1, seed-d*2, seed-(d**4-1), seed-73, seed-71]
#string = "".join([chr(c) for c in ascii_code])

#exec(string)
pr = "print"
ascii_text = [ 188,44,156,12,124,236,92,204,60,172,28,140,252,108,220,76,188,44,156,]
string = "".join([chr(c) for c in ascii_text])
exec(f"{pr}('{string}')")