Frio = 0
Salud = 0
Calor = 0
Calor_data = Calor << posX
Frio_data = Frio << posZ
temperatura = Numeraso_maker(Frio, 1, Salud, 1, Calor, 1)
temperatura, temperaturaxp = Numeraso_rules("Numerasos: ",,temperatura, temperaturaxp, 
                                            "Afecta negativamente: ", 
                                            "Frio: "(Salud + Calor_data), 
                                            "Salud: ",Frio, 
                                            "Calor: ", ((Salud + Frio_data)), 
                                            "Afecta positivamente: ",
                                            "Frio: ", Frio,
                                            "Salud: ", Calor,
                                            "Calor: ", Salud)
