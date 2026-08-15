// Nuevo archivo: EventHandlerRegistry.java
package net.mcreator.gnulmod;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.mcreator.gnulmod.procedure.*;

public class EventHandlerRegistry {
    
    public static void registerHandlers(FMLPreInitializationEvent event) {
        // Registrar todos los event handlers
        MinecraftForge.EVENT_BUS.register(new ProcedureLifetick.TriggerHandler());
        MinecraftForge.EVENT_BUS.register(new ProcedureDrinkwater());
        MinecraftForge.EVENT_BUS.register(new ProcedureManualMining(null));
        MinecraftForge.EVENT_BUS.register(new ProcedureEatListener()); // <-- ESTE FALTABA
        MinecraftForge.EVENT_BUS.register(new ProcedureClaypotHandler()); // Si existe
    }
}
