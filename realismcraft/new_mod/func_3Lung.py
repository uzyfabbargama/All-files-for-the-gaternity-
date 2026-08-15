iluminación_aire = 1 #usaremos esta teoría: si está muy oscuro, el aire es frío, si está muy brillante, es cálido, y el aire es muy cálido (usaremos los 4 bits de Minecraft (del 0 al 15, para sumarle a este valor, con la siguiente tabla) 15 = -7 → 7 (tomando el valor absoluto) una iluminación promedio = un aire puro (¿qué tiene que ver? no sé xd), 0 = 7, PD: Minecraft nos engaña (cuando es de noche, la iluminación dice que es 15, pero igual afecta, así que está bien (por eso usamos valor absoluto)
salud = 1 #indicador de salud
movimiento = iluminación_aire #si corremos bajo mucha o poca iluminación, también afecta a salud
pulmon = Numeraso_maker(iluminación_aire, 1, salud, 1, movimiento, 1)
#pulmon, pulmonxp = Numeraso_rules(pulmon, pulmonxp, salud, salud, iluminación_aire, iluminación_aire, movimiento, salud)
pulmon, pulmonxp = Numeraso_rules("Numerasos: "pulmon, pulmonxp,
                                  "Afecta negativamente: ", 
                                  "iluminación_aire: ",salud, 
                                  "salud: ", iluminación_aire, 
                                  "movimiento: ",salud, 
                                  "Afecta postivamente: ", 
                                  "iluminación_aire", iluminación_aire, 
                                  "salud",movimiento, 
                                  "movimiento: ",salud)
