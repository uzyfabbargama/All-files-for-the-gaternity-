Falta_agua
Agua_sucia
Salud
Agua_limpia
kidney= Numeraso_maker(Falta_agua,1, Salud, 1, Agua_Limpia, 1)
kidney, kidneyxp Numeraso_rules("Numerasos: ", kidney, kidneyxp,
                                "Afecta negativamente: ",
                                "Falta_agua: ", Salud,
                                "Salud: ", Falta_agua,
                                "Agua_limpia: ", Salud,
                                "Afecta positivamente: ",
                                "Falta_agua", Falta_agua,
                                "Salud: ", Salud,
                                "Agua_limpia", Salud)
#Tomar agua sucia, de un río sin tratar en Minecraft, te suma simultáneamente, en Agua_limpia y Falta_agua
