package net.mcreator.gnulmod.procedure;

import net.minecraft.world.World;
import net.minecraft.entity.player.EntityPlayer;
import net.mcreator.gnulmod.Gnulmod;
import net.mcreator.gnulmod.gui.GuiGnulStatus;
import net.mcreator.gnulmod.ElementsGnulmod;

import java.util.Map;

@ElementsGnulmod.ModElement.Tag
public class ProcedureGuidetailsOnKeyPressed extends ElementsGnulmod.ModElement {
	public ProcedureGuidetailsOnKeyPressed(ElementsGnulmod instance) {
		super(instance, 10);
	}

	public static void executeProcedure(Map<String, Object> dependencies) {
		if (dependencies.get("entity") == null) return;
		if (dependencies.get("world") == null) return;
		if (dependencies.get("x") == null) return;
		if (dependencies.get("y") == null) return;
		if (dependencies.get("z") == null) return;

		EntityPlayer entity = (EntityPlayer) dependencies.get("entity");
		World world = (World) dependencies.get("world");
		entity.getEntityData().setInteger("gnul_msg_timer", 200)
		int x = (int) dependencies.get("x");
		int y = (int) dependencies.get("y");
		int z = (int) dependencies.get("z");

		// Ahora sí, Java sabe qué es Gnulmod y GuiGnulStatus
		entity.openGui(Gnulmod.instance, GuiGnulStatus.GUIID, world, x, y, z);
	}
}
