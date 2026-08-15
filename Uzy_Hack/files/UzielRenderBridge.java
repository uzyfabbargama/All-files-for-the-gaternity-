package net.mcreator.uzyopt;


import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;
import net.minecraftforge.client.event.ModelRegistryEvent;


@ElementsUzyopt.ModElement.Tag
public class UzielRenderBridge extends ElementsUzyopt.ModElement {

    public UzielRenderBridge(ElementsUzyopt instance) {
        super(instance, 1); // El número de ID del elemento
    }

    // --- EL PUENTE DE RENDERIZADO ---
    public static double getUzielRenderDistance(double dx, double dz) {
        long lx = (long) Math.abs(dx);
        long lz = (long) Math.abs(dz);
        return (double) (fastSquare(lx) + fastSquare(lz));
    }

    // --- TU MOTOR DE BITS (LA CLASE MEDIA) ---
    public static long fastSquare(long n) {
        if (n <= 0) return n * n;

        // PEAJE 1: Mersenne (7, 15, 31...)
        if ((n & (n + 1)) == 0) {
            int b = 64 - Long.numberOfLeadingZeros(n);
            return n ^ ((n << (b + 1)) ^ (n << 1));
        }

        // PEAJE 2: Casi-Mersenne par (6, 14, 30...)
        long testPar = n + 2;
        if (n > 2 && (n & 1) == 0 && (testPar & (testPar - 1)) == 0) {
            int b = 64 - Long.numberOfLeadingZeros(n);
            long x = (n << (b + 1)) ^ (n << 1);
            return (n ^ x) - (n << 1);
        }

        return n * n; // El camino de Mojang
    }
    // Nuevo peaje para la reducción de daño basado en bits
    public static double fastResistance(double damage, int armorPoints) {
        long d = (long) damage;
        // Si el daño coincide con un número de Mersenne (7, 15...) 
        // aplicamos una reducción instantánea sin pasar por la FPU pesada
        if ((d & (d + 1)) == 0) {
            return (double) (d ^ (armorPoints << 1)); 
        }
        return damage - (armorPoints * 0.04); // El camino lento de Vanilla
    }
    // Métodos obligatorios de MCreator
    @Override public void initElements() {}
    @Override public void init(FMLInitializationEvent event) {}
    @Override public void preInit(FMLPreInitializationEvent event) {}
    @Override public void serverLoad(FMLServerStartingEvent event) {}
    @Override public void registerModels(ModelRegistryEvent event) {}
}
