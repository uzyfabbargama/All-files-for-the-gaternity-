daño = 0
salud = 0
nutrientes = leg_left #tomamos los nutrientes de la pierna correspondiente
leg_leftmuscle= Numeraso_maker(daño, 1, salud, 1, nutrientes, 1)
leg_leftmuscle, leg_leftmusclexp = Numeraso_rules("Numerasos: ", 
                                                  "Afecta negativamente: ", 
                                                  "daño: ", salud,
                                                  "salud: ", daño,
                                                  "nutrientes: ", daño,
                                                  "Afecta Positivamente: "
                                                  "daño: ", daño,
                                                  "salud: ", salud,
                                                  "nutrientes", nutrientes)
