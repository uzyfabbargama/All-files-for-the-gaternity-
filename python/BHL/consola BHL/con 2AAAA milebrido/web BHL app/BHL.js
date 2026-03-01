import { GoogleGenAI} from "@google/genai";
const ai = new GoogleGenAI({apiKey:'AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM'});
const ai1 =new GoogleGenAI([])
async function generar_contenido() {
    try {
        const response = await ai.generateContent({
            model: "gemini-2.5-flash",
            contents: "Explica en pocas palabras como funciona la inteligencia artificial",

        })

    } catch (error) {
        console.error("Error al generar contenido:", error);
    }
}
generar_contenido();
let base = 1000
let PosC2 = (base ** 3) * (2 ** 3)
let PosX = (base ** 2) * (2 ** 2)
let PosC1 = (base ** 2) * 2
let PosY = base*2
let PosC = base
let PosZ = 1

Numeraso_Exp =(ExpB, ExpH, ExpL, PosX, PosC, PosY, PosC1, PosZ, PosC2) => {
NumerasoXP = (ExpB*PosX) + (ExpH*PosY) + (ExpL*PosZ) + PosC + PosC1 + PosC2 //armar el numeraso
C1 = Math.floor(NumerasoXP / PosC) % 2 //Primer controlador Bondad
C2 = Math.floor(NumerasoXP / PosC1) % 2 //segundo controlador Hostilidad
C3 = Math.floor(NumerasoXP / PosC2) % 2 //tercer controlador
caso = C1 + C2 + C3 //verifica si los controladores están activos
while (caso != 3) { // bucle
    D1 = 1 - C1 //detector not
    D2 = 1 - C2 //detector not
    D3 = 1 - C3 //detector not
    NumerasoXP += D1 * PosC + D2 * PosC1 + D3 * PosC2 //
    NumerasoXP += D1
    NumerasoXP -= (D1)*PosY
    NumerasoXP -= D2*PosZ
    NumerasoXP -= (D3)*PosX
    C1 = Math.floor(NumerasoXP / PosC) % 2
    C2 = Math.floor(NumerasoXP / PosC1) % 2
    C3 = Math.floor(NumerasoXP / PosC2) % 2
    caso = C1 + C2 + C3
}

return NumerasoXP    
}

Numeraso =(a, b, c, PosX, PosC, PosY, PosC1, PosZ, PosC2) => {
    Bondad = a //input de bondad
    Hostilidad = b //input de hostilidad
    Lógica = c //input de lógica
    Numero_generado = (Bondad*PosX) + (Hostilidad*PosY) + (Lógica*PosZ) + PosC + PosC1 + PosC2
    return expB,expH,expL,Numero_generado
}

Numeraso_update = () => {
expB,expH,expL,Numero_generado = Numeraso(a,b,c,PosX, PosC, PosY, PosC1, PosZ, PosC2)
    
C1 = Math.floor(Numero_generado / PosC) % 2 
C2 = Math.floor(Numero_generado / PosC1) % 2 
C3 = Math.floor(Numero_generado / PosC2) % 2 
caso = C1 + C2 + C3
expL = 0
expB = 0
expH = 0
tiempo = 0
while (caso != 3){
    D1 = 1 - C1
    D2 = 1 - C2
    D3 = 1 - C3
    expB += D1
    expH += D2
    expL += D3
    tiempo += D1*0.000238923 + D2*2.2781388 + D3*1.7238498
    Numero_generado += D1 * PosC + D2 * PosC1 + D3 * PosC2
    Numero_generado += D1*expB
    Numero_generado -= (D1*expB)*PosY
    Numero_generado -= D2*expH*PosZ - D2*expH*PosX
    Numero_generado -= (D3*expL)*PosX - D3*expL*PosY
    Numero_generado += D1 * Math.floor(base/(expL+1))%base + D2 * Math.floor(base/(expH+1))%base + D3 * Math.floor(base/(expB+1))%base
    C1 = Math.floor(Numero_generado / PosC) % 2 
    C2 = Math.floor(Numero_generado / PosC1) % 2 
    C3 = Math.floor(Numero_generado / PosC2) % 2 
    caso = C1 + C2 + C3
}
return Numero_generado % ((base**3) * 2**3), expB, expH, expL, tiempo
}

Numeraso2 = (a, b, c,PosX, PosC, PosY, PosC1, PosZ, PosC2) => {
C = a //input de cagar
H = b //input de hambre
S = c //insput 
Numero_de_necesidad = (C*PosX) + (H*PosY) + (S*PosZ)
Numero_de_necesidad += PosC + PosC1 + PosC2
return Numero_de_necesidad
}

Numeraso2_update = () => {
Numero_de_necesidad = Numeraso2(baño, hambre, sueño, PosX, PosC, PosY, PosC1, PosZ, PosC2)
C4 = Math.floor(Numero_de_necesidad / PosC) % 2
C5 = Math.floor(Numero_de_necesidad / PosC1) % 2
C6 = Math.floor(Numero_de_necesidad / PosC2) % 2
caso = C4 + C5 + C6
expS = 0
expHu = 0
expC = 0
while (caso != 3) {
D4 =  1 - C4
D5 =  1 - C5
D6 =  1 - C6
expS += D4
expHu += D5
expC += D6
Numero_de_necesidad += (D4)*PosZ
Numero_generado += D4 * PosC + D5 * PosC1 + D6 * PosC2
Numero_generado += D4*expC*PosZ
Numero_generado -= (D4*expC)*PosY
Numero_generado -= D5*expHu*PosZ - D5*expHu*PosX
Numero_generado -= (D6*expS)*PosX - D6*expS*PosY
C4 = Math.floor(Numero_de_necesidad / PosC) % 2
C5 = Math.floor(Numero_de_necesidad / PosC1) % 2
C6 = Math.floor(Numero_de_necesidad / PosC2) % 2
caso = C4 + C5 + C6
Numero_de_necesidad += D4 * Math.floor(base/(expS+1)) % base + D5 * Math.floor(base/(expHu+1))%base + D6 * Math.floor(base/(expC+1))%base
Math.floor(Numero_de_necesidad)
}
return Numero_de_necesidad % ((base**3) * 2**3), expS, expHu, expC
}
a = 20
b = 20
c = 20
baño = 50
hambre = 50
sueño = 50
Numeraso(a,b,c,PosX, PosC, PosY, PosC1, PosZ, PosC2)
Numeraso2(baño, hambre, sueño,PosX, PosC, PosY, PosC1, PosZ, PosC2)
Numero, expB, expH, expL, tiempo = Numeraso_update()
Numero1, expS, expHu, expC = Numeraso2_update()

//el equivalente del bucle while True
Numero1 += 1*PosX + 1*PosY + 1*PosZ //esto le suma 1 a todas las necesidades
Necesidad_C = Math.floor(Numero1 / PosX) %base
Necesidad_H = Math.floor(Numero1 / PosY) %base
Necesidad_S = Math.floor(Numero1 / PosZ ) %base
Numero -= Math.floor(Necesidad_C / PosX) %base + Math.floor(Necesidad_H / PosX) %base + Math.floor(Necesidad_S / PosX)%base //reduce bondad por las necesidades
NumerasoXP = Numeraso_Exp()
ExpB = Math.floor(NumerasoXP / PosX) % base
ExpH = Math.floor(NumerasoXP / PosY) % base
ExpL = Math.floor(NumerasoXP / PosZ) % base
