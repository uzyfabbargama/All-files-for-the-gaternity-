movimiento = 0
salud = 0
sedentarismo = 0
leg_leftmuscle= Numeraso_maker(movimiento, 1, salud, 1, sedentarismo, 1)
leg_leftmuscle, leg_leftmusclexp = Numeraso_rules("Numerasos: ", 
                                                  "Afecta negativamente: ", 
                                                  "movimiento: ", sedentarismo,
                                                  "salud: ", sedentarismo,
                                                  "sedentarismo: ", salud,
                                                  "Afecta Positivamente: "
                                                  "movimiento: ", salud,
                                                  "salud: ", movimiento,
                                                  "sedentarismo", sedentarismo)
