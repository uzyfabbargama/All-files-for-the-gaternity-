def Numeraso_maker(int(a), bool(a_cotrol), int(b), bool(b_control), int(c), bool(c_control)):
    global posZ, posC1, posY, posC2, posX, posC3
    Numeraso = (a<<posZ)+ (a_cotrol<<posC1)+ (b<<posY)+ (b_control<<posC1)+ (c<<posX)+ (c_control<<posC2)
    return Numeraso
def Numeraso_extract(int(Numeraso)):
    global posZ, posC1, posY, posC2, posX, posC3
    a = (Numeraso >> posZ) & (1 << 10 - 1) #10 bits (aprovechamos que primero el << y luego la resta)
    b = (Numeraso >> posY) & (1 << 10 - 1)
    c = (Numeraso >> posX) & (1 << 10 - 1)
    aC1 = (Numeraso >> posC1) & 1
    bC2 = (Numeraso >> posC2) & 1
    cC3 = (Numeraso >> posC3) & 1
    return a, b, c, aC1, bC2, cC3
def Numeraso_rules(str(text1),int(Numeraso),int(Numerasoxp), str(text2), str(text4), int(a_minus), str(text5), int(b_minus), str(text6), int(c_minus), str(text3), str(text7), int(a_add), str(text8), int(b_add), str(text9), int(c_add)):
    global posZ, posC1, posY, posC2, posX, posC3
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
