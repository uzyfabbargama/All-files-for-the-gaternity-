// Este codigo ha sido generado por el modulo psexport 20230904-l64 de PSeInt.
// Es posible que el codigo generado no sea completamente correcto. Si encuentra
// errores por favor reportelos en el foro (http://pseint.sourceforge.net).

#include<iostream>
#include<cmath>
#include<sstream>
using namespace std;

// No hay en el C++ estandar una funcion equivalente a "convertiratexto", pero puede programarse una equivalente.
string convertiratexto(float f);

// Para las variables que no se pudo determinar el tipo se utiliza la constante
// int. El usuario debe reemplazar sus ocurrencias por el tipo adecuado
// (usualmente int,float,string o bool).
using int = string;

// Para leer variables de texto se utiliza el operador << del objeto cin, que
// lee solo una palabra. Para leer una linea completa (es decir, incluyendo los
// espacios en blanco) se debe utilzar getline (ej, reemplazar cin>>x por
// getline(cin,x)), pero obliga a agregar un cin.ignore() si antes del getline
// se leyó otra variable con >>.

// Declaraciones adelantadas de las funciones
void verificar_todo(float &registro, float registro2, float &flag);
void opcode(int registro, float reg1, float reg2, int &regv, bool &frac, bool &frac1, bool &estado);
void v_ans(int regv, int &rega, int &regb, int &regc, int &rega1, int &regb1, int &regc1, int &rega2, int &regb2, int &regc2, int &rega3, int &regb3, int &regc3, int vans);
void dibujar_pantalla(int r_ram[]);

void verificar_todo(float &registro, float registro2, float &flag) {
	flag = 0;
	if (registro==0) {
		// Z
		registro = 0;
		flag = flag+1;
	}
	if (registro==registro2) {
		// I
		flag = flag+2;
	}
	if (registro<0) {
		// N
		flag = flag+4;
		if (registro<-127) {
			flag = 0;
			registro = 0;
		}
	}
	if (registro>=256) {
		// C
		flag = flag+8;
		registro = 0;
	}
}

void opcode(int registro, float reg1, float reg2, int &regv, bool &frac, bool &frac1, bool &estado) {
	float den;
	float den1;
	float den2;
	int num;
	float num2;
	switch (registro) {
	case 1:
		estado = true;
		regv = reg1+reg2;
		break;
	case 2:
		estado = true;
		regv = reg1-reg2;
		break;
	case 3:
		estado = true;
		if (frac==false && frac1==false) {
			regv = reg1*reg2;
		} else {
			if (frac==true && frac1==false) {
				regv = reg1+((reg1-1)*reg2*16+1);
			} else {
				if (frac==false && frac1==true) {
					regv = ((reg2-1)*reg1*16+1)+reg2;
				} else {
					if (frac==true && frac1==true) {
						regv = ((reg1-1)*reg2*16+1)+((reg2-1)*reg1*16+1);
					}
				}
			}
		}
		break;
	case 4:
		estado = true;
		if (frac==false && frac1==false) {
			regv = (reg1*16)+reg2;
			frac = true;
		} else {
			if (frac==true && frac1==false) {
				regv = reg1+(((reg1*(reg2-1))%16)+reg2+16);
			} else {
				if (frac==false && frac1==true) {
					regv = (((reg2*(reg1-1))%16)+reg1+16)+reg2;
				} else {
					if (frac==true && frac1==true) {
						den = reg1%16;
						// tomamos denomidador
						den2 = reg2%16;
						// tomamos el otro
						num = int(reg1/16);
						// tomamos numerados
						num = int(reg2/16);
						reg1 = den*16+num;
						// los intercambiamos
						reg2 = den1*16+num2;
						regv = (((int(reg1)*(int(reg2)-1))%16)+int(reg2)+16)+(((int(reg2)*(int(reg1)-1))%16)+int(reg1)+16);
					}
				}
			}
		}
		break;
	case 5:
		estado = true;
		regv = reg1*pow(2, (int(reg2)%8));
		break;
	case 6:
		estado = true;
		regv = int(reg1/pow(2, reg2));
		break;
	case 7:
		// incondicional falso
		estado = true;
		regv = 0;
		break;
	case 15:
		// sero
		estado = true;
		if (reg1==0 && reg2==0) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 23:
		// igual
		estado = true;
		if (reg1==reg2) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 39:
		// negativ0
		estado = true;
		if (reg1-reg2<0) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 71:
		// carry
		estado = true;
		if (reg1+reg2>=256) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 31:
		// igual, zero
		estado = true;
		if (reg1==reg2 && reg1==0 && reg2==0) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 89:
		// zero carry
		estado = true;
		if (reg1==0 && reg2==0 && reg1+reg2>=256) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 55:
		// igual negativo
		estado = true;
		if (reg1-reg2<0 && reg1==reg2) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 87:
		// igual carry
		estado = true;
		if (reg1==reg2 && reg1+reg2>=256) {
			regv = 0;
		} else {
			regv = 1;
		}
		break;
	case 7+128:
		// incondicional falso
		estado = true;
		regv = 0;
		break;
	case 15+128:
		// sero
		estado = true;
		if (reg1==0 && reg2==0) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	case 23+128:
		// igual
		estado = true;
		if (reg1==reg2) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	case 39+128:
		// negativ0
		estado = true;
		if (reg1-reg2<0) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	case 71+128:
		// carry
		estado = true;
		if (reg1+reg2>=256) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	case 31+128:
		// igual, zero
		estado = true;
		if (reg1==reg2 && reg1==0 && reg2==0) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	case 89+128:
		// zero carry
		estado = true;
		if (reg1==0 && reg2==0 && reg1+reg2>=256) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	case 55+128:
		// igual negativo
		estado = true;
		if (reg1-reg2<0 && reg1==reg2) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	case 87+128:
		// igual carry
		estado = true;
		if (reg1==reg2 && reg1+reg2>=256) {
			regv = 1;
		} else {
			regv = 0;
		}
		break;
	default:
		estado = false;
	}
}

void v_ans(int regv, int &rega, int &regb, int &regc, int &rega1, int &regb1, int &regc1, int &rega2, int &regb2, int &regc2, int &rega3, int &regb3, int &regc3, int vans) {
	switch (regv) {
	case 1:
		// 0001
		rega = regv;
		break;
	case 2:
		// 0010
		regb = regv;
		break;
	case 3:
		// 0011
		regc = regv;
		break;
	case 5:
		// 0101
		rega1 = regv;
		break;
	case 6:
		// 0110
		regb1 = regv;
		break;
	case 7:
		// 0111
		regc1 = regv;
		break;
	case 9:
		// 1001
		rega2 = regv;
		break;
	case 10:
		// 1010
		regb2 = regv;
		break;
	case 11:
		// 1011
		regc2 = regv;
		break;
	case 13:
		// 1101
		rega3 = regv;
		break;
	case 14:
		// 1110
		regb3 = regv;
		break;
	case 15:
		// 1111
		regc3 = regv;
		break;
	}
}

void dibujar_pantalla(int r_ram[]) {
	float columna;
	int dato;
	float fila;
	string linea;
	string textura;
	textura = "abcdefghijklmnopqrstuvwxyzáéíóúABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ¿?¡!|&^°.-,0123456789#$%/()=/[]()<>*´`~@??¶?<-??øþæßð?????«»¢??· ?§¢®?¥^?ØÞÆ?Ðª?©???º¯";
	cout << endl; // no hay forma directa de borrar la pantalla con C++ estandar
	for (fila=0; fila<=15; ++fila) {
		linea = "";
		for (columna=0; columna<=15; ++columna) {
			dato = r_ram[(fila*16+columna)];
			if (dato>=1 && dato<=156) {
				// Extraemos el símbolo correspondiente
				linea = linea+"["+textura.substr(dato-1, dato-dato+1)+"]";
			} else {
				if (dato>147 && dato<=170) {
					linea = linea+"["+convertiratexto(dato)+"]";
				} else {
					// El símbolo por defecto o "apagado"
					linea = linea+"(/)";
				}
			}
		}
		cout << linea << endl;
	}
}

int main() {
	int a;
	int a1;
	int a2;
	int a3;
	int a_ram[256];
	int b;
	int b1;
	int b2;
	int b3;
	int b_ram[256];
	int dat;
	int dir;
	bool encendido;
	bool falso);;
	int flags_a;
	int flags_b;
	int flags_r;
	int flags_v;
	bool frac;
	bool frac1;
	bool frac2;
	bool frac3;
	bool frac4;
	bool frac5;
	bool frac6;
	bool frac7;
	int intruction;
	int pc;
	int r;
	int r1;
	int r2;
	int r3;
	int r_ram[256];
	int v;
	int v1;
	int v2;
	int v3;
	int vans;
	int v_ram[256];
	encendido = true;
	// //instrucciones
	a_ram[0] = 1;
	b_ram[0] = 10;
	r_ram[0] = 5;
	a_ram[1] = 16;
	b_ram[1] = 10;
	r_ram[1] = v;
	do {
		// 1
		verificar_todo(a, b, flags_a);
		verificar_todo(b, r, flags_b);
		verificar_todo(r, v, flags_r);
		verificar_todo(v, a, flags_v);
		// //2
		verificar_todo(a1, b1, flags_a);
		verificar_todo(b1, r1, flags_b);
		verificar_todo(r1, v1, flags_r);
		verificar_todo(v1, a1, flags_v);
		// //3
		verificar_todo(a2, b2, flags_a);
		verificar_todo(b2, r2, flags_b);
		verificar_todo(r2, v2, flags_r);
		verificar_todo(v2, a2, flags_v);
		// //4
		verificar_todo(a3, b3, flags_a);
		verificar_todo(b3, r3, flags_b);
		verificar_todo(r3, v3, flags_r);
		verificar_todo(v3, a3, flags_v);
		pc = pc+1;
		// 3. TRANSURGENCIA DE VELOCIDAD
		// V-Ans tipo 2 (VB): Movemos el resultado a B.
		// Esto hace que si el resultado fue grande, el siguiente "salto" sea más largo.
		v_ram[pc+1] = 2;
		// instrucciones
		pc = pc+1;
		a = a_ram[pc-1];
		// intrucción
		r = r_ram[pc-1];
		// dato
		b = b_ram[pc-1];
		// dirección
		opcode(a, b, r, v, frac, frac1, encendido);
		if (a==16) {
			encendido = true;
			r_ram[b] = r;
		}
		if (a==32) {
			encendido = true;
			r = r_ram[b-1];
		}
		pc = pc+1;
		a1 = a_ram[pc-1];
		r1 = r_ram[pc-1];
		b1 = b_ram[pc-1];
		opcode(a1, b1, r1, v1, frac2, frac3, encendido);
		if (a1==16) {
			r_ram[b1-1] = r1;
		}
		if (a1==32) {
			r = r_ram[b-1];
		}
		// 2. ESCRIBIR EN PANTALLA
		// Guardamos el "píxel" en la dirección V
		a_ram[pc] = 16;
		a2 = a_ram[pc-1];
		r2 = r_ram[pc-1];
		b2 = b_ram[pc-1];
		opcode(a2, b2, r2, v2, frac4, frac5, encendido);
		if (a2==16) {
			r_ram[b2-1] = r2;
		}
		if (a2==32) {
			r = r_ram[b-1];
		}
		pc = pc+1;
		if (pc>=256) {
			pc = 1;
		}
		b_ram[pc] = v;
		// Usamos V-Ans para que el destino sea el resultado previo
		pc = pc+1;
		intruction = a_ram[pc-1];
		dat = r_ram[pc-1];
		r3 = dat;
		dir = b_ram[pc-1];
		b3 = dir;
		opcode(a3, b3, r3, v3, frac6, frac7, encendido);
		if (intruction==16) {
			r_ram[b3-1] = r3;
		}
		if (intruction==32) {
			r = r_ram[b-1];
		}
		pc = pc+1;
		vans = v_ram[pc-1];
		v_ans(v, a, b, r, a1, b1, r1, a2, b2, r2, a3, b3, r3, vans);
		if (vans==4+16) {
			a_ram[b-1] = v;
		}
		if (vans==4+32) {
			v = a_ram[b-1];
		}
		if (vans==5+16) {
			b_ram[b-1] = v;
		}
		if (vans==5+32) {
			v = b_ram[b-1];
		}
		if (vans==6+16) {
			v_ram[b-1] = v;
		}
		if (vans==6+32) {
			v = v_ram[b-1];
		}
		pc = pc+1;
		vans = v_ram[pc-1];
		v_ans(v1, a, b, r, a1, b1, r1, a2, b2, r2, a3, b3, r3, vans);
		if (vans==4+16) {
			a_ram[b1-1] = v1;
		}
		if (vans==4+32) {
			v1 = a_ram[b1-1];
		}
		if (vans==5+16) {
			b_ram[b1-1] = v1;
		}
		if (vans==5+32) {
			v = b_ram[b1-1];
		}
		if (vans==6+16) {
			v_ram[b-1] = v1;
		}
		if (vans==6+32) {
			v1 = v_ram[b1-1];
		}
		pc = pc+1;
		vans = v_ram[pc-1];
		v_ans(v2, a, b, r, a1, b1, r1, a2, b2, r2, a3, b3, r3, vans);
		if (vans==4+16) {
			a_ram[b2-1] = v2;
		}
		if (vans==4+32) {
			v2 = a_ram[b2-1];
		}
		if (vans==5+16) {
			b_ram[b2-1] = v2;
		}
		if (vans==5+32) {
			v2 = b_ram[b2-1];
		}
		if (vans==6+16) {
			v_ram[b-1] = v2;
		}
		if (vans==6+32) {
			v2 = v_ram[b2-1];
		}
		pc = pc+1;
		vans = v_ram[pc-1];
		v_ans(v3, a, b, r, a1, b1, r1, a2, b2, r2, a3, b3, r3, vans);
		if (vans==4+16) {
			a_ram[b3-1] = v3;
		}
		if (vans==4+32) {
			v3 = a_ram[b3-1];
		}
		if (vans==5+16) {
			b_ram[b3-1] = v3;
		}
		if (vans==5+32) {
			v3 = b_ram[b3-1];
		}
		if (vans==6+16) {
			v_ram[b3-1] = v3;
		}
		if (vans==6+32) {
			v3 = v_ram[b3-1];
		}
		dibujar_pantalla(r_ram);
	} while (encendido!=false);
	return 0;
}


string convertiratexto(float f) {
	stringstream ss;
	ss << f;
	return ss.str();
}
