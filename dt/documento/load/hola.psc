SubProceso verificar_Todo(registro Por Referencia, registro2, flag Por Referencia)
	flag <- 0
	si registro = 0 //Z
		registro <- 0
		flag <- flag + 1
	FinSi
	si registro = registro2 //I
		flag <- flag + 2
	FinSi
	si registro < 0 //N
		flag <- flag + 4
		si registro < -127
			flag <- 0
			registro <- 0
		FinSi
	FinSi
	si registro >= 256 //C
		flag <- flag + 8
		registro <- 0
	FinSi
FinSubProceso
SubProceso opcode(registro, reg1, reg2, regv Por Referencia, frac Por Referencia, frac1 Por Referencia, estado Por Referencia)
	Segun registro
		caso 1:
			estado <- Verdadero
			regv <- reg1 + reg2
		caso 2:
			estado <- Verdadero
			regv <- reg1 - reg2
		caso 3:
			estado <- Verdadero
			si frac = falso & frac1 = falso
				regv <- reg1 *  reg2
			SiNo
				si frac = Verdadero & frac1 = falso
					regv <- reg1 + ((reg1-1)*reg2 * 16 + 1)
				SiNo
					si frac = falso & frac1 = Verdadero
						regv <- ((reg2-1)*reg1 * 16 + 1) + reg2
					sino 
						si frac = Verdadero & frac1 = Verdadero
							regv <- ((reg1-1)*reg2 * 16 + 1) + ((reg2-1)*reg1 * 16 + 1)
						FinSi
					FinSi
				FinSi
			FinSi
		caso 4:
			estado <- Verdadero
			si frac = falso & frac1 = falso
				regv <- (reg1 * 16) + reg2
				frac <- Verdadero
			SiNo
				si frac = Verdadero & frac1 = falso
					regv <- reg1 + (((reg1 * (reg2-1)) % 16)+reg2 + 16)
				SiNo
					si frac = falso & frac1 = Verdadero
						regv <- (((reg2 * (reg1-1)) % 16)+reg1 + 16) + reg2
					sino 
						si frac = Verdadero & frac1 = Verdadero
							den <- reg1 % 16 //tomamos denomidador
							den2 <- reg2 % 16 //tomamos el otro
							num <- trunc(reg1 / 16) //tomamos numerados
							num <- trunc(reg2/16)
							reg1 <- den * 16 + num // los intercambiamos
							reg2 <- den1 * 16 + num2
							regv <- (((reg1 * (reg2-1)) % 16)+reg2 + 16) + (((reg2 * (reg1-1)) % 16)+reg1 + 16)
						FinSi
					FinSi
				FinSi
			FinSi
		caso 5:
			estado <- Verdadero
			regv <- reg1 * 2^(reg2 % 8)
		caso 6:
			estado <- Verdadero
			regv <- trunc(reg1 / 2^reg2)
		caso 7: //incondicional falso
			estado <- Verdadero
			regv <- 0
		caso 15: //sero
			estado <- Verdadero
			si reg1 = 0 & reg2 = 0
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 23: //igual
			estado <- Verdadero
			si reg1 = reg2
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 39: //negativ0
			estado <- Verdadero
			si reg1 - reg2 < 0
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 71: //carry
			estado <- Verdadero
			si reg1 + reg2 >= 256
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 31: //igual, zero
			estado <- Verdadero
			si reg1 = reg2 & reg1 = 0 & reg2 = 0
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 89: // zero carry
			estado <- Verdadero
			si reg1 = 0 & reg2 = 0 & reg1 + reg2 >= 256
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 55: //igual negativo
			estado <- Verdadero
			si reg1 - reg2 <0 & reg1 = reg2
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 87: //igual carry
			estado <- Verdadero
			si reg1 = reg2 & reg1 + reg2 >= 256
				regv <- 0
			SiNo
				regv <- 1
			FinSi
		caso 7+128: //incondicional falso
			estado <- Verdadero
			regv <- 0
		caso 15+128: //sero
			estado <- Verdadero
			si reg1 = 0 & reg2 = 0
				regv <- 1
			SiNo
				regv <- 0
			FinSi
		caso 23+128: //igual
			estado <- Verdadero
			si reg1 = reg2
				regv <- 1
			SiNo
				regv <- 0
			FinSi
		caso 39+128: //negativ0
			estado <- Verdadero
			si reg1 - reg2 < 0
				regv <- 1
			SiNo
				regv <- 0
			FinSi
		caso 71+128: //carry
			estado <- Verdadero
			si reg1 + reg2 >= 256
				regv <- 1
			SiNo
				regv <- 0
			FinSi
		caso 31+128: //igual, zero
			estado <- Verdadero
			si reg1 = reg2 & reg1 = 0 & reg2 = 0
				regv <- 1
			SiNo
				regv <- 0
			FinSi
		caso 89+128: // zero carry
			estado <- Verdadero
			si reg1 = 0 & reg2 = 0 & reg1 + reg2 >= 256
				regv <- 1
			SiNo
				regv <- 0
			FinSi
		caso 55+128: //igual negativo
			estado <- Verdadero
			si reg1 - reg2 <0 & reg1 = reg2
				regv <- 1
			SiNo
				regv <- 0
			FinSi
		caso 87+128: //igual carry
			estado <- Verdadero
			si reg1 = reg2 & reg1 + reg2 >= 256
				regv = 1
			SiNo
				regv <- 0
			FinSi
		De Otro Modo:
			estado <- falso
	FinSegun
			
FinSubProceso
SubProceso V_Ans (regv, regA Por Referencia, regB Por Referencia, regC Por Referencia,regA1 Por Referencia, regB1 Por Referencia, regC1 Por Referencia,regA2 Por Referencia, regB2 Por Referencia, regC2 Por Referencia,regA3 Por Referencia, regB3 Por Referencia, regC3 Por Referencia, vans)
	Segun regv
		caso 1: //0001
			regA <- regv
		caso 2: //0010
			regB <- regv
		caso 3: //0011
			regC <- regv
		caso 5: //0101
			regA1 <- regv
		caso 6: //0110
			regB1 <- regv
		caso 7: //0111
			regC1 <- regv
		caso 9: //1001
			regA2 <- regv
		caso 10: //1010
			regB2 <- regv
		caso 11: //1011
			regC2 <- regv
		caso 13: //1101
			regA3 <- regv
		caso 14: //1110
			regB3 <- regv
		caso 15: //1111
			regC3 <- regv
	FinSegun
FinSubProceso
SubProceso Dibujar_Pantalla(R_RAM Por Referencia)
	Definir textura Como Caracter
	textura <- "abcdefghijklmnopqrstuvwxyzáéíóúABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ¿?¡!|&^°.-,0123456789#$%/()=/[]()<>*´`~@??¶?<-??øþæßð?????«»¢??· ?§¢®?¥^?ØÞÆ?Ðª?©???º¯"
    Limpiar Pantalla
    Para fila <- 0 Hasta 15 Con Paso 1 Hacer
        linea <- ""
        Para columna <- 0 Hasta 15 Hacer
		dato <- R_RAM[(fila * 16 + columna) + 1]
            
            Si dato >= 1 y dato <= 156 Entonces
                // Extraemos el símbolo correspondiente
			linea <- linea + "[" + Subcadena(textura, dato, dato) + "]"
            SiNo
                Si dato > 147 y dato <= 170 Entonces
				linea <- linea + "[" + ConvertirATexto(dato) + "]" 
                SiNo
                    // El símbolo por defecto o "apagado"
				linea <- linea + "(/)"
                FinSi
            FinSi
        FinPara
        Escribir linea
    FinPara
FinSubProceso

Algoritmo sin_titulo
	Dimensionar A_RAM[256]
	Dimensionar B_RAM[256]
	Dimensionar R_RAM[256]
	Dimensionar V_RAM[256]
	Definir A, A1, A2, A3, B, B1, B2, B3, R, R1, R2, R3, V, V1, V2, V3 Como Entero
	Definir flags_A Como entero
	Definir flags_B Como entero
	Definir flags_R Como entero
	Definir flags_V Como entero
	Definir frac, frac1, frac2, frac3, frac4, frac5, frac6, frac7 Como logico
	Definir encendido Como Logico
	Definir int, PC Como Entero
	Definir dat Como Entero
	Definir dir Como Entero
	Definir vans Como Entero
	encendido <- Verdadero
//	//instrucciones
	A_RAM[1] <- 1 //suma
	B_RAM[1] <- 10 //val1
	R_RAM[1] <- 6 //val2
	
	A_RAM[2] <- 16 //save
	B_RAM[2] <- 10 //val1
	A_RAM[3] <- V //val2
	
	
	Repetir
	//1
//	verificar_Todo(A,B,flags_A)
//	verificar_Todo(B,R,flags_B)
//	verificar_Todo(R,V,flags_R)
//	verificar_Todo(V,A,flags_V)
////	//2
//	verificar_Todo(A1,B1,flags_A)
//	verificar_Todo(B1,R1,flags_B)
//	verificar_Todo(R1,V1,flags_R)
//	verificar_Todo(V1,A1,flags_V)
////	//3
//	verificar_Todo(A2,B2,flags_A)
//	verificar_Todo(B2,R2,flags_B)
//	verificar_Todo(R2,V2,flags_R)
//	verificar_Todo(V2,A2,flags_V)
////	//4
//	verificar_Todo(A3,B3,flags_A)
//	verificar_Todo(B3,R3,flags_B)
//	verificar_Todo(R3,V3,flags_R)
//	verificar_Todo(V3,A3,flags_V)

	PC <- PC + 1
	// 3. TRANSURGENCIA DE VELOCIDAD
	// V-Ans tipo 2 (VB): Movemos el resultado a B.
	// Esto hace que si el resultado fue grande, el siguiente "salto" sea más largo.
	//	//instrucciones
	A_RAM[PC] <- 1 //suma
	B_RAM[PC] <- 10 //val1
	R_RAM[PC] <- 6 //val2
	
	A_RAM[PC] <- 16 //save
	B_RAM[PC] <- 10 //val1
	A_RAM[PC] <- V //val2
	
	V_RAM[PC+2] <- 20
	//instrucciones
		
		A <- A_RAM[PC] //intrucción
		R <- R_RAM[PC] //dato
		B <- B_RAM[PC] //dirección
		
		opcode(A, B, R, V, frac, frac1, encendido)
		si A = 16
			encendido = Verdadero
			R_RAM[B+1] <- R
		FinSi
		si A = 32
			encendido = Verdadero
			R <- R_RAM[B]
		FinSi
	
		
		PC <- PC + 1
		A1 <- A_RAM[PC]
		R1 <- R_RAM[PC]
		B1 <- B_RAM[PC]
		opcode(A1, B1, R1, V1, frac2, frac3, encendido)
		si A1 = 16
			R_RAM[B1] <- R1
		FinSi
		si A1 = 32
			R <- R_RAM[B]
		FinSi
		
		// 2. ESCRIBIR EN PANTALLA
		// Guardamos el "píxel" en la dirección V
		A_RAM[PC+1] <- 16 
		
	
		A2 <- A_RAM[PC]
		R2 <- R_RAM[PC]
		B2 <- B_RAM[PC]
		opcode(A2, B2, R2, V2, frac4, frac5, encendido)
		si A2 = 16
			R_RAM[B2] <- R2
		FinSi
		si A2 = 32
			R <- R_RAM[B]
		FinSi
		PC <- PC + 1
		si PC >= 256 entonces 
			PC <- 1
		FinSi
		
		B_RAM[PC+1] <- V // Usamos V-Ans para que el destino sea el resultado previo
		PC <- PC + 1
		int <- A_RAM[PC]
		dat <- R_RAM[PC]
		R3 <- dat
		dir <- B_RAM[PC]
		B3 <- dir
		opcode(A3, B3, R3, V3, frac6, frac7, encendido)
		si int = 16
			R_RAM[B3] <- R3
		FinSi
		si int = 32
			R <- R_RAM[B]
		FinSi
		
		
		
		PC <- PC + 1
		vans <- V_RAM[PC]
		V_Ans(V, A, B, R, A1, B1, R1,A2, B2, R2,A3, B3, R3,vans)
		si vans = 4+16
			A_RAM[B] <- V
		FinSi
		si vans = 4+32
			V <- A_RAM[B]
		FinSi
		si vans = 5+16
			B_RAM[B] <- V
		FinSi
		si vans = 5+32
			V <- B_RAM[B]
		FinSi
		si vans = 6+16
			V_RAM[B] <- V
		FinSi
		si vans = 6+32
			V <- V_RAM[B]
		FinSi
		
		
		PC <- PC + 1
		vans <- V_RAM[PC]
		V_Ans(V1, A, B, R, A1, B1, R1,A2, B2, R2,A3, B3, R3,vans)
		si vans = 4+16
			A_RAM[B1] <- V1
		FinSi
		si vans = 4+32
			V1 <- A_RAM[B1]
		FinSi
		si vans = 5+16
			B_RAM[B1] <- V1
		FinSi
		si vans = 5+32
			V <- B_RAM[B1]
		FinSi
		si vans = 6+16
			V_RAM[B] <- V1
		FinSi
		si vans = 6+32
			V1 <- V_RAM[B1]
		FinSi
		
		
		PC <- PC + 1
		vans <- V_RAM[PC]
		V_Ans(V2, A, B, R, A1, B1, R1,A2, B2, R2,A3, B3, R3,vans)
		si vans = 4+16
			A_RAM[B2] <- V2
		FinSi
		si vans = 4+32
			V2 <- A_RAM[B2]
		FinSi
		si vans = 5+16
			B_RAM[B2] <- V2
		FinSi
		si vans = 5+32
			V2 <- B_RAM[B2]
		FinSi
		si vans = 6+16
			V_RAM[B] <- V2
		FinSi
		si vans = 6+32
			V2 <- V_RAM[B2]
		FinSi
		
		
		PC <- PC + 1
		vans <- V_RAM[PC]
		V_Ans(V3, A, B, R, A1, B1, R1,A2, B2, R2,A3, B3, R3, vans)
		si vans = 4+16
			A_RAM[B3] <- V3
		FinSi
		si vans = 4+32
			V3 <- A_RAM[B3]
		FinSi
		si vans = 5+16
			B_RAM[B3] <- V3
		FinSi
		si vans = 5+32
			V3 <- B_RAM[B3]
		FinSi
		si vans = 6+16
			V_RAM[B3] <- V3
		FinSi
		si vans = 6+32
			V3 <- V_RAM[B3]
		FinSi
		
		
		si PC >= 256
			PC <- 0
		FinSi
		Dibujar_Pantalla(R_RAM)
	Hasta Que encendido = Verdadero
FinAlgoritmo
