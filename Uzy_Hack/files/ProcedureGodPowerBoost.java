package net.mcreator.uzyopt.procedure;

import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.common.MinecraftForge;

import net.minecraft.world.World;

import net.mcreator.uzyopt.ElementsUzyopt;

@ElementsUzyopt.ModElement.Tag
public class ProcedureGodPowerBoost extends ElementsUzyopt.ModElement {
	public ProcedureGodPowerBoost(ElementsUzyopt instance) {
		super(instance, 1);
	}

	public static void executeProcedure(java.util.HashMap<String, Object> dependencies) {
		if (dependencies.get("world") != null) {
			net.minecraft.world.World world = (net.minecraft.world.World) dependencies.get("world");
//			for (net.minecraft.entity.Entity entity : world.loadedEntityList) {
//				double renderDist = net.mcreator.uzyopt.UzielRenderBridge.getUzielRenderDistance(entity.posX, entity.posZ);
//				entity.renderDistanceWeight = net.mcreator.uzyopt.UzielRenderBridge.fastResistance(renderDist, 0) / 100.0;
//			}
		}
	}

	@SubscribeEvent
	public void onWorldTick(TickEvent.WorldTickEvent event) {
		if (event.phase == TickEvent.Phase.END) {
			Object worldObj = event.world; net.minecraft.world.World world = (net.minecraft.world.World) worldObj;
			java.util.HashMap<String, Object> dependencies = new java.util.HashMap<>();
			dependencies.put("world", world);
			dependencies.put("event", event);
			this.executeProcedure(dependencies);
		}
	}

	@Override
	public void preInit(FMLPreInitializationEvent event) {
		MinecraftForge.EVENT_BUS.register(this);
	}
}
