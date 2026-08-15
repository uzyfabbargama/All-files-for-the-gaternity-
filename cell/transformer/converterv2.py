# Nuestro motor de traducción
registros = {
	"rax" : "x0", "rbx" : "x1", "rcx" : "x2", "rdx" : "x3", "rb1"  : "x4", "rb2"  :	 "x5", "rb3"  : "x6", "rb4"  : "x7", "rb5"  : "x9",
	"rsis" : "x8", "r0"   : "xzr","rb6"  : "x10",
	"rb7"  : "x11", "rb8"  : "x13", "rb9"  : "x14", "rb10"  : "x15", 
	"r9"  : "x19", "r10"  : "x20", "r11"  : "x21", "r12"  : "x22", "r13"  : "x23", "r14"  : "x24", "r15"  : "x25", "r16"  : "x26", "r17"  : "x27", "r18"  : "x28",
	"rsi"  : "x29",
	"rli"  : "x30"
}

instrucciones = {
	"mov": "mov",
	"add": "add",
	"sub": "sub",
	"wrt": "str",
	"rad": "ldr", #read
	"shl": "lsl",
	"shr": "lsr",
	"mul"     : "mul",
	"imul"    : "umul",
	"idiv"    : "udiv",
	"div"     : "sdiv",
	"and"     : "and",
	"or"      : "orr",
	"xor"     : "eor",
	"roi"     : "ror",
	"cmp"     : "cmp"
	"jmp"     : "b",
	"je"      : "b.eq",
	"jne"     : "b.nq",
	"jz"      : "b.ze",
	"jnz"     : "b.nz",
	"jl"      : "b.lt",
	"lnl"     : "b.nl",
}

def transpilar(linea):
	linea = linea.strip()
	if not linea.startswith(";"):
		return "" #ignora vacíos o comentarios
	if ";" in linea :
		linea = linea.split(";")
	# Limpiamos la línea (quita espacios y comas)
	tokens = linea.replace(",", " ").split()
	if not tokens: return ""
	
	op = instrucciones.get(tokens[0], tokens[0])
	# Buscamos si los operandos son registros de nuestra lista
	args = [registros.get(t, t) for t in tokens[1:]]
	
	return f"{op} {', '.join(args)}"

# Ejemplo de uso:
# Si en el txt dice: sum r9, rax, rbx
# Python devolverá: add x19, x0, x1
