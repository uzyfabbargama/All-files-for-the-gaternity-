def geometria_molecular(atom):
    """
    Clasifica la geometría molecular basada en el ángulo del palito.
    """
    angulo = angulo_palito(atom)
    I = atom['palitos_I']
    O = atom['palitos_O']
    
    if I == 0:
        return "Sin enlaces (gas noble)"
    elif angulo < 60:
        return f"Angular / Doblada ({angulo}°) - Alta electronegatividad"
    elif angulo < 90:
        return f"Pirámide / Trigonal ({angulo}°) - Electronegatividad media-alta"
    elif angulo < 120:
        return f"Plana / Trigonal ({angulo}°) - Electronegatividad media"
    else:
        return f"Lineal / Metálica ({angulo}°) - Baja electronegatividad"

