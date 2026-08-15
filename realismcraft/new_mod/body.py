posZ = 0
posC1 = 10
posY = 11
posC2 = 21
posX = 22
posC3 = 32
def Numeraso_maker(int(a), bool(a_cotrol), int(b), bool(b_control), int(c), bool(c_control)):
    global posZ, posC1, posY, posC1, posX, posC2
    Numeraso = (a<<posZ)+ (a_cotrol<<posC1)+ (b<<posY)+ (b_control<<posC1)+ (c<<posX)+ (c_control<<posC2)
    return Numeraso
def Numeraso_extract(int(Numeraso)):
    global posZ, posC1, posY, posC1, posX, posC2
    a = (Numeraso >> posZ) & (1 << 10 - 1) #10 bits (aprovechamos que primero el << y luego la resta)
    b = (Numeraso >> posY) & (1 << 10 - 1)
    c = (Numeraso >> posX) & (1 << 10 - 1)
    aC1 = (Numeraso >> posC1) & 1
    bC2 = (Numeraso >> posC2) & 1
    cC3 = (Numeraso >> posC3) & 1
    return a, b, c, aC1, bC2, cC3
def Numeraso_rules(int(Numeraso),int(Numerasoxp), int(a_minus), int(b_minus), int(c_minus), int(a_add), int(b_add), int(c_add)):
    global posZ, posC1, posY, posC1, posX, posC2
    a, b, c, C1, C2, C3 = Numeraso_extract(Numeraso)
    caso = C1 + C2 + C3
    ax, bx, cx = Numeraso_extract(Numerasoxp)
    while caso != 3:
        D1 = 1 - C1
        D2 = 1 - C2
        D3 = 1 - C3
        a_res = (a << posZ) // (1 + ax) * D1
        b_res = (b << posY) // (1 + bx) * D2
        c_res = (c << posX) // (1 + cx) * D3
        a_minus = (a_minus << posZ)*D1
        b_minus = (b_minus << posY)*D2
        c_minus = (c_minus << posX)*D3
        a_add = (a_add << posZ)*D1
        b_add = (b_add << posY)*D2
        c_add = (c_add << posX)*D3
        Numeraso += a_add + b_add + c_add + (a_res + b_res + c_res)
        Numeraso -= a_minus + b_minus + c_minus
    Numerasoxp = Numeraso_maker(ax, 1, bx, 1, cx, 1)
    return Numeraso, Numerasoxp
ejercisio = 1 #mide cuanto el jugador se mueve
ejercisio_data = ejercisio << PosZ
salud = 1 #mide la relación entre ejercisio y sedentarismo
salud_data = salud << posY
corazonxp = 0
sedentarismo = 1 #mide como el jugador descansa y se queda quieto
sedentarismo_data = sedentarismo << posX
corazon = Numeraso_maker(ejercisio, 1, salud, 1, sedentarismo, 1)
#ejercicio → salud → sedentarismo → ejercisio
corazon, corazonxp = Numeraso_rules(corazon, corazonxp, sedentarismo, ejercisio, salud, salud, sedentarismo, ejercisio)
ejercisio, salud, sedentarismo = Numeraso_extract(corazon)
iluminación_aire = 1 #usaremos esta teoría: si está muy oscuro, el aire es frío, si está muy brillante, es cálido, y el aire es muy cálido (usaremos los 4 bits de Minecraft (del 0 al 15, para sumarle a este valor, con la siguiente tabla) 15 = -7 → 7 (tomando el valor absoluto) una iluminación promedio = un aire puro (¿qué tiene que ver? no sé xd), 0 = 7, PD: Minecraft nos engaña (cuando es de noche, la iluminación dice que es 15, pero igual afecta, así que está bien (por eso usamos valor absoluto)
salud = 1 #indicador de salud
movimiento = iluminación_aire #si corremos bajo mucha o poca iluminación, también afecta a salud
pulmon = Numeraso_maker(iluminación_aire, 1, salud, 1, movimiento, 1)
pulmon, pulmonxp = Numeraso_rules(pulmon, pulmonxp, salud, salud, iluminación_aire, iluminación_aire, movimiento, salud)
