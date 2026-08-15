if (transformedName.equals("net.minecraft.entity.Entity")) {
    ClassReader cr = new ClassReader(basicClass);
    ClassNode cn = new ClassNode();
    cr.accept(cn, 0);

    for (MethodNode mn : cn.methods) {
        // func_70091_d es el nombre ofuscado de 'move' en 1.12.2
        if (mn.name.equals("move") || mn.name.equals("func_70091_d")) {
            for (AbstractInsnNode insn : mn.instructions.toArray()) {
                // Buscamos el opcode DADD (Double Add)
                if (insn.getOpcode() == Opcodes.DADD) {
                    // Lo cambiamos por una llamada a nuestro puente
                    mn.instructions.set(insn, new MethodInsnNode(
                        Opcodes.INVOKESTATIC, 
                        "net/mcreator/uzyopt/UzyGridBridge", 
                        "preciseAdd", "(DD)D", false));
                }
            }
        }
    }
    ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
    cn.accept(cw);
    return cw.toByteArray();
}
// --- INYECCIÓN DE TRANSURGENCIA EN EL ADN DE MINECRAFT ---

if (transformedName.equals("net.minecraft.client.renderer.EntityRenderer") || transformedName.equals("buq")) { 
    ClassReader cr = new ClassReader(basicClass);
    ClassNode cn = new ClassNode();
    cr.accept(cn, 0);

    for (MethodNode mn : cn.methods) {
        // Buscamos cualquier método que use matemáticas pesadas de renderizado
        for (AbstractInsnNode insn : mn.instructions.toArray()) {
            
            // REEMPLAZO DE RAÍZ CUADRADA (La joya de la corona)
            if (insn.getOpcode() == Opcodes.INVOKESTATIC) {
                MethodInsnNode min = (MethodInsnNode) insn;
                if (min.owner.equals("java/lang/Math") && min.name.equals("sqrt")) {
                    // Redirigimos al puente de Uziel que usa el motor de bits
                    mn.instructions.set(insn, new MethodInsnNode(
                        Opcodes.INVOKESTATIC,
                        "net/mcreator/uzyopt/UzielRenderBridge",
                        "fastSqrtBridge", "(D)D", false));
                }
            }
        }
    }
    ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
    cn.accept(cw);
    return cw.toByteArray();
}

// Mantenemos tu optimización de movimiento en Entity
if (transformedName.equals("net.minecraft.entity.Entity") || transformedName.equals("vg")) {
    // ... (Tu código de DADD a preciseAdd se mantiene aquí) ...
}
