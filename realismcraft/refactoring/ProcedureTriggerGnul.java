package net.mcreator.gnulmod.procedure;

import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.common.MinecraftForge;
import net.mcreator.gnulmod.ElementsGnulmod;

// En ProcedureTriggerGnul.java - CORREGIDO
@ElementsGnulmod.ModElement.Tag
public class ProcedureTriggerGnul extends ElementsGnulmod.ModElement {

    public ProcedureTriggerGnul(ElementsGnulmod instance) {
        super(instance, 2);
    }

    @SubscribeEvent
    public void onPlayerTick(TickEvent.PlayerTickEvent event) {
        if (event.phase == TickEvent.Phase.END && !event.player.world.isRemote) {
            ProcedureLifetick.onTickStatic(event);
        }
    }

    @Override
    public void preInit(FMLPreInitializationEvent event) {
        MinecraftForge.EVENT_BUS.register(this);
    }
}
