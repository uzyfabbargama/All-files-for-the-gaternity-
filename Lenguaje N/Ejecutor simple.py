id = -1
while True:
    id += 1
    msg = input("")
    print(msg[id])
    igual = ord("=") #61
    igual = str(igual)
    espacio = ord(" ") #32
    coma = ord(",") #44
    parentesis = [ord("("), ord(")")] #40 41
    comillas = [34, 39] #34 = " y 39 = '
    puntocoma = ord(";") #59
    llaves = [ord("{"), ord("}")] #123 125
    corchetes = [ord("["), ord("]")]
    print(igual, espacio, coma, parentesis[0], parentesis[1], comillas[0], comillas[1], puntocoma, llaves[0], llaves[1], corchetes[0], corchetes[1])
    
    if msg == "exit":
        break