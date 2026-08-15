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
movimiento = 0
salud = 0
nutrientes = 0
right_left= Numeraso_maker(movimiento, 1, salud, 1, nutrientes, 1)
right_left, right_leftxp = Numeraso_rules("Numerasos: ", right_left, 
                                          right_leftxp,
                                          "Afecta negativamente: ", 
                                          "movimiento: ", nutrientes,
                                          "salud: ", nutrientes,
                                          "nutrientes: ", salud,
                                          "Afecta Positivamente: "
                                          "movimiento: ", salud,
                                          "salud: ", movimiento,
                                          "nutientes", nutrientes)
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
movimiento = 0
salud = 0
sedentarismo = 0
leg_rightmuscle= Numeraso_maker(movimiento, 1, salud, 1, sedentarismo, 1)
leg_rightmuscle, leg_rightmusclexp = Numeraso_rules("Numerasos: ", 
                                                  "Afecta negativamente: ", 
                                                  "movimiento: ", sedentarismo,
                                                  "salud: ", sedentarismo,
                                                  "sedentarismo: ", salud,
                                                  "Afecta Positivamente: "
                                                  "movimiento: ", salud,
                                                  "salud: ", movimiento,
                                                  "sedentarismo", sedentarismo)
daño = 0
salud = 0
nutrientes = leg_right #tomamos los nutrientes de la pierna correspondiente
leg_rightmuscle= Numeraso_maker(daño, 1, salud, 1, nutrientes, 1)
leg_rightmuscle, leg_rightmusclexp = Numeraso_rules("Numerasos: ", 
                                                  "Afecta negativamente: ", 
                                                  "daño: ", salud,
                                                  "salud: ", daño,
                                                  "nutrientes: ", daño,
                                                  "Afecta Positivamente: "
                                                  "daño: ", daño,
                                                  "salud: ", salud,
                                                  "nutrientes", nutrientes)
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
movimiento = 0
salud = 0
nutrientes = 0
right_left= Numeraso_maker(movimiento, 1, salud, 1, nutrientes, 1)
right_left, right_leftxp = Numeraso_rules("Numerasos: ", right_left, 
                                          right_leftxp,
                                          "Afecta negativamente: ", 
                                          "movimiento: ", nutrientes,
                                          "salud: ", nutrientes,
                                          "nutrientes: ", salud,
                                          "Afecta Positivamente: "
                                          "movimiento: ", salud,
                                          "salud: ", movimiento,
                                          "nutientes", nutrientes)
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
movimiento = 0
salud = 0
sedentarismo = 0
leg_rightmuscle= Numeraso_maker(movimiento, 1, salud, 1, sedentarismo, 1)
leg_rightmuscle, leg_rightmusclexp = Numeraso_rules("Numerasos: ", 
                                                  "Afecta negativamente: ", 
                                                  "movimiento: ", sedentarismo,
                                                  "salud: ", sedentarismo,
                                                  "sedentarismo: ", salud,
                                                  "Afecta Positivamente: "
                                                  "movimiento: ", salud,
                                                  "salud: ", movimiento,
                                                  "sedentarismo", sedentarismo)
daño = 0
salud = 0
nutrientes = leg_right #tomamos los nutrientes de la pierna correspondiente
leg_rightmuscle= Numeraso_maker(daño, 1, salud, 1, nutrientes, 1)
leg_rightmuscle, leg_rightmusclexp = Numeraso_rules("Numerasos: ", 
                                                  "Afecta negativamente: ", 
                                                  "daño: ", salud,
                                                  "salud: ", daño,
                                                  "nutrientes: ", daño,
                                                  "Afecta Positivamente: "
                                                  "daño: ", daño,
                                                  "salud: ", salud,
                                                  "nutrientes", nutrientes)
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
