#import Keyword /* in pogress */
print("==== Bienvenidos ====")
DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
_1754_7020_176 = int(DATA[0]) 		#Mapa.Object.X
_1754_7020_178 = int(DATA[1]) 		#Mapa.Object.Y
_1754_7020_180 = int(DATA[2])		#Mapa.Object.Z
_1754_7020_52470 = int(DATA[3])		#Mapa.Object.BlockArea
_1754_7020_3365862 = int(DATA[4])	#Mapa.Object.BlockResistance
_1754_7020_214037034 = int(DATA[5])	#Mapa.Object.BlockElectronAfinity
_1754_7020_209070 = int(DATA[6])	#Mapa.Object.BlockEnergy

_1754_7020 = [_1754_7020_176, _1754_7020_178, _1754_7020_180, _1754_7020_52470, _1754_7020_3365862, _1754_7020_214037034, _1754_7020_209070]

_1754 = [_1754_7020]

_59818_1914 = int(20) 		#Personaje.Vida
_59818_6818 = str(DATA[7])	#Personaje.Nombre
_59818_1662 = int(DATA[8])	#Personaje.Item
_59818_3524 = 0				#Personaje.MoveX
_59818_3520 = 0				#Personaje.MoveZ
_59818_3526 = 0				#Personaje.MoveY
_59818_176 = 0				#Personaje.X
_59818_178 = 0				#Personaje.Y
_59818_180 = 0				#Personaje.Z
_59818_1852 = 1				#Personaje.SeeX
_59818_1854 = 1				#Personaje.SeeY
_59818_1848 = 1				#Personaje.SeeZ
_59818_3740 = -1			#Personaje.SeeMX
_59818_3742 = -1			#Personaje.SeeMY
_59818_3736 = -1			#Personaje.SeeMZ

while True:
	_59818_176 += _59818_3524
	_59818_178 += _59818_3526
	_59818_180 += _59818_3520
	_59818_1852 += _59818_176
	_59818_1854 += _59818_178
	_59818_1848 += _59818_180
	_59818_3740 -= _59818_176
	_59818_3742 -= _59818_178
	_59818_3736 -= _59818_180
	while True:
		if _1754_7020_176 == _59818_1852 or _1754_7020_176 == _59818_3740:
			_59818_3524 = 0
		if _1754_7020_178 == _59818_1854 or _1754_7020_178 == _59818_3742:
			_59818_3526 = 0
		if _1754_7020_180 == _59818_1848 or _1754_7020_180 == _59818_3736:
			_59818_3520 = 0
			#/* Pronto se añadirán teclado */
