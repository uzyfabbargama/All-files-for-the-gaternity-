package net.mcreator.uzyopt.procedure;

import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.event.entity.living.LivingAttackEvent;
import net.minecraftforge.common.MinecraftForge;

import net.minecraft.world.World;
import net.minecraft.entity.Entity;

import net.mcreator.uzyopt.ElementsUzyopt;

@ElementsUzyopt.ModElement.Tag
public class ProcedureGPattackboost extends ElementsUzyopt.ModElement {
	public ProcedureGPattackboost(ElementsUzyopt instance) {
		super(instance, 2);
	}

	public static void executeProcedure(java.util.HashMap<String, Object> dependencies) {
		if (dependencies.get("amount") != null && dependencies.get("entity") != null) {
			float originalDamage = (float) dependencies.get("amount");
			net.minecraft.entity.Entity entityLiving = (net.minecraft.entity.Entity) dependencies.get("entity");
			if (entityLiving instanceof Object) {
				int armor = 0;
				double finalDamage = net.mcreator.uzyopt.UzielRenderBridge.fastResistance((double) originalDamage, armor);
				if (dependencies.get("event") instanceof net.minecraftforge.event.entity.living.LivingAttackEvent) {
					((net.minecraftforge.event.entity.living.LivingAttackEvent) dependencies.get("event")).setCanceled(true);
				}
			}
		}
	}

	@SubscribeEvent
	public void onEntityAttacked(LivingAttackEvent event) {
		if (event != null && event.getEntity() != null) {
			Object entityObj = event.getEntity(); net.minecraft.entity.Entity entity = (net.minecraft.entity.Entity) entityObj;
			int i = (int) event.getEntity().p;
			int j = (int) event.getEntity().q;
			int k = (int) event.getEntity().r;
			Object worldObj = event.getEntity().l; net.minecraft.world.World world = (net.minecraft.world.World) worldObj;
			java.util.HashMap<String, Object> dependencies = new java.util.HashMap<>();
			dependencies.put("x", i);
			dependencies.put("y", j);
			dependencies.put("z", k);
			dependencies.put("world", world);
			dependencies.put("entity", entity);
			dependencies.put("event", event);
			this.executeProcedure(dependencies);
		}
	}

	@Override
	public void preInit(FMLPreInitializationEvent event) {
		MinecraftForge.EVENT_BUS.register(this);
	}
}
