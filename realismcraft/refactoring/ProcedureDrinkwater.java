package net.mcreator.gnulmod.procedure;

import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.common.MinecraftForge;

import net.minecraft.world.World;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.nbt.NBTTagCompound; // <--- ESTE ES EL QUE FALTABA
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.text.TextComponentString;

import net.mcreator.gnulmod.ElementsGnulmod;

@ElementsGnulmod.ModElement.Tag
public class ProcedureDrinkwater extends ElementsGnulmod.ModElement {
	public ProcedureDrinkwater(ElementsGnulmod instance) {
		super(instance, 3);
	}

	public static void executeProcedure(java.util.HashMap<String, Object> dependencies) {
		if (dependencies.get("entity") == null || dependencies.get("world") == null) return;
		
		EntityPlayer entity = (EntityPlayer) dependencies.get("entity");
		World world = (World) dependencies.get("world");
		int x = (int) dependencies.get("x");
		int y = (int) dependencies.get("y");
		int z = (int) dependencies.get("z");

		if (world.getBlockState(new BlockPos(x, y, z)).getMaterial() == net.minecraft.block.material.Material.WATER) {
			NBTTagCompound nbt = entity.getEntityData();
			
			// Inyectamos los valores para que el Riñón los procese en el siguiente tick
			nbt.setInteger("gnul_input_agua_limpia", 15);
			nbt.setInteger("gnul_input_falta_agua", 10); 
			
			entity.sendStatusMessage(new TextComponentString("§b[Gnul] §fBebiendo agua de río..."), true);
		}
	}

	@SubscribeEvent
	public void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
		EntityPlayer entity = event.getEntityPlayer();
		int i = event.getPos().getX();
		int j = event.getPos().getY();
		int k = event.getPos().getZ();
		World world = event.getWorld();
		java.util.HashMap<String, Object> dependencies = new java.util.HashMap<>();
		dependencies.put("x", i);
		dependencies.put("y", j);
		dependencies.put("z", k);
		dependencies.put("world", world);
		dependencies.put("entity", entity);
		dependencies.put("event", event);
		this.executeProcedure(dependencies);
	}

	@Override
	public void preInit(FMLPreInitializationEvent event) {
		MinecraftForge.EVENT_BUS.register(this);
	}
}