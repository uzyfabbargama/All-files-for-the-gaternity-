import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class BellaService {
  // --- LÓGICA DE BAJO NIVEL ---
  private bits = 15;
  private mask = (1 << this.bits) - 1;
  private PosZ = 0;
  private PosC = this.bits;
  private PosY = this.bits + 1;
  private PosC1 = (this.bits * 2) + 1;
  private PosX = (this.bits * 2) + 2;
  private PosC2 = (this.bits * 3) + 2;
  private num_n = 1048576;

  private traductor: { [key: number]: string } = {};
  private memoria = new BigInt64Array(this.num_n).fill(BigInt((1 << this.PosC) + (1 << this.PosC1) + (1 << this.PosC2)));
  private exps: number[][] = Array.from({ length: this.num_n }, () => [0, 0, 0]);

  constructor() {}

  private numerasoExp(ExpX: number, ExpY: number, ExpZ: number): number[] {
    let NumerasoXP = (BigInt(ExpX) << BigInt(this.PosX)) + (BigInt(ExpY) << BigInt(this.PosY)) + 
                     (BigInt(ExpZ) << BigInt(this.PosZ)) + (1n << BigInt(this.PosC)) + 
                     (1n << BigInt(this.PosC1)) + (1n << BigInt(this.PosC2));
    
    let getC = (val: bigint, pos: number) => Number((val >> BigInt(pos)) & 1n);
    let C1 = getC(NumerasoXP, this.PosC), C2 = getC(NumerasoXP, this.PosC1), C3 = getC(NumerasoXP, this.PosC2);

    while ((C1 + C2 + C3) !== 3) {
      let D1 = 1 - C1, D2 = 1 - C2, D3 = 1 - C3;
      NumerasoXP += (BigInt(D1) << BigInt(this.PosC)) + (BigInt(D2) << BigInt(this.PosC1)) + (BigInt(D3) << BigInt(this.PosC2));
      NumerasoXP += BigInt(D1) - (BigInt(D1) << BigInt(this.PosY)) - (BigInt(D2) << BigInt(this.PosZ)) - (BigInt(D3) << BigInt(this.PosX));
      C1 = getC(NumerasoXP, this.PosC); C2 = getC(NumerasoXP, this.PosC1); C3 = getC(NumerasoXP, this.PosC2);
      NumerasoXP %= (1n << BigInt(this.PosC2 + 1));
    }
    return [
      Number((NumerasoXP >> BigInt(this.PosX)) & BigInt(this.mask)), 
      Number((NumerasoXP >> BigInt(this.PosY)) & BigInt(this.mask)), 
      Number((NumerasoXP >> BigInt(this.PosZ)) & BigInt(this.mask))
    ];
  }

 // En bella.service.ts - MODIFICAR función entrenar()

entrenar(texto: string): number {
  // 1. Limpiar texto
  const textoLimpio = texto.replace(/[.,!?;:()"']/g, ' ').trim();
  
  // 2. Separar por espacios (como en Python)
  const palabras = textoLimpio.split(/\s+/);
  
  // 3. Procesar cada palabra completa
  for (const palabra of palabras) {
    // Saltar palabras muy cortas
    if (palabra.length < 3) continue;
    
    // Procesar palabra completa (NO fragmentos de 8)
    let energia = this.xorid(palabra);
    let idx = (Math.floor(energia / 20)) % this.num_n;
    
    this.traductor[idx] = palabra;
    this.memoria[idx] += BigInt(energia);
    
    let [n_gen, ex0, ex1, ex2] = this.numeraso2Update(
      this.exps[idx][0], 
      this.exps[idx][1], 
      this.exps[idx][2], 
      this.memoria[idx]
    );
    this.memoria[idx] = n_gen;
    this.exps[idx] = [ex0, ex1, ex2];
  }
  
  return this.exps.reduce((acc, e) => acc + e[2], 0);
}

  proyectar(): string {
    let candidatas = [...Array(this.num_n).keys()]
      .filter(i => this.exps[i][2] > 0 && this.traductor[i])
      .sort((a, b) => this.exps[b][2] - this.exps[a][2])
      .slice(0, 5);

    let frase = candidatas.map(i => {
      let f = this.traductor[i];
      this.exps[i][2] = Math.max(0, this.exps[i][2] - 2);
      return f;
    }).join(" ");

    return frase || "...";
  }

  private xorid(frag: string): number {
    let id_acc = 0;
    for (let i = 0; i < frag.length; i++) id_acc = (id_acc ^ frag.charCodeAt(i)) << 1;
    return id_acc * 20;
  }

  private numeraso2Update(expx: number, expy: number, expz: number, Numero_generado: bigint): [bigint, number, number, number] {
    let n_gen = Numero_generado;
    let getC = (val: bigint, pos: number) => Number((val >> BigInt(pos)) & 1n);
    let C4 = getC(n_gen, this.PosC), C5 = getC(n_gen, this.PosC1), C6 = getC(n_gen, this.PosC2);
    
    [expx, expy, expz] = this.numerasoExp(expx, expy, expz);
    
    while ((C4 + C5 + C6) !== 3) {
      let D4 = 1 - C4, D5 = 1 - C5, D6 = 1 - C6;
      expx += D6; expy += D5; expz += D4;
      n_gen += (BigInt(D4) << BigInt(this.PosZ)) + (BigInt(D4) << BigInt(this.PosC)) + (BigInt(D5) << BigInt(this.PosC1)) + (BigInt(D6) << BigInt(this.PosC2));
      n_gen += (BigInt(D4) * BigInt(expx)) << BigInt(this.PosZ);
      n_gen -= (BigInt(D4) * BigInt(expx)) << BigInt(this.PosY);
      C4 = getC(n_gen, this.PosC); C5 = getC(n_gen, this.PosC1); C6 = getC(n_gen, this.PosC2);
      n_gen %= (1n << BigInt(this.PosC2 + 1));
    }
    return [n_gen, expx, expy, expz];
  }
}
