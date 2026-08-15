movimiento = 0
salud = 0
nutrientes = 0
leg_left= Numeraso_maker(movimiento, 1, salud, 1, nutrientes, 1)
leg_left, leg_leftxp = Numeraso_rules("Numerasos: ", leg_left, leg_leftxp,
                                      "Afecta negativamente: ", 
                                      "movimiento: ", nutrientes,
                                      "salud: ", nutrientes,
                                      "nutrientes: ", salud,
                                      "Afecta Positivamente: "
                                      "movimiento: ", salud,
                                      "salud: ", movimiento,
                                      "nutientes", nutrientes)
