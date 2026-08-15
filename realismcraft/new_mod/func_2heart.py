ejercisio = 1 #mide cuanto el jugador se mueve
ejercisio_data = ejercisio << PosZ
salud = 1 #mide la relación entre ejercisio y sedentarismo
salud_data = salud << posY
corazonxp = 0
sedentarismo = 1 #mide como el jugador descansa y se queda quieto
sedentarismo_data = sedentarismo << posX
corazon = Numeraso_maker(ejercisio, 1, salud, 1, sedentarismo, 1)
#ejercicio → salud → sedentarismo → ejercisio
corazon, corazonxp = Numeraso_rules("Numerasos",corazon, corazonxp, 
                                    "Afecta negativamente: ",
                                    "Ejercisio: " sedentarismo, 
                                    "Salud: ", ejercisio, 
                                    "Sendentarismo: ",salud, 
                                    "Afecta positivamente: ",
                                    "Ejercisio: ", salud, 
                                    "Salud: ",sedentarismo, 
                                    "Sedentarismo: ",ejercisio)
ejercisio, salud, sedentarismo = Numeraso_extract(corazon)
