Nutrientes_vegetales_cereales_carne = 0 #toma 1 de cada 1 para estabilizarse, es decir: un pack de los 3 nutrientes, le suma 1 punto de salud
Nutrientes_vegetales_cereales_carne_data = Nutrientes_vegetales_cereales_carne << PosZ
Salud = 0
Toxinas_o_carne = 0 #veneno, efectos de pociones, la carne podrida es un golpe de hígado 2ble, ya que es carne y es veneno
Higado, HigadoXp = Numeraso_rules("Numerasos: ", Higado, HigadoXp,
                        "Afecta negativamente: ",
                        "Nutrientes_3: ", Toxinas_o_carne,
                        "Salud: ", Nutrientes_3, #consume nutrientes
                        "Toxinas: ",Salud,
                        "Afecta postivamente:",
                        "Nutriente_3: ", Salud
                        "Salud: ", Salud,
                        "Toxinas: ", Toxinas+(carne * Nutrientes_vegetales_cereales_carne_data)) #si es carne, agrega a nutrientes
