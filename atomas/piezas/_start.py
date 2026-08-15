# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    print("🔬 Generando tabla periódica de palitos...")
    atomos = generar_todos_los_atomos()
    print(f"✅ Generados {len(atomos)} átomos")
    
    # Cabecera CSV (actualizada con radiactividad)
    print("\n" + "="*130)
    print("N°,Nombre,Capas,I,O,Longitud,P.Fusion,Desap,Mag,Fuerza,Conduct,React,Radiact")
    print("-"*130)
    
    for atom in atomos:
        print(mostrar_propiedades(atom))
    
    print("="*130)
    print(f"✅ Total: {len(atomos)} átomos generados")
