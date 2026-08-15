package net.mcreator.gnulmod.procedure;

import net.minecraft.world.World;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.EnumHand;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.item.ItemStack;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.block.material.Material;
import net.minecraft.init.Blocks;
import net.minecraft.util.text.TextComponentString;

public class ProcedureClaypotRightClickedOnBlock {

	public static void executeProcedure(java.util.HashMap<String, Object> dependencies) {
		EntityPlayer entity = (EntityPlayer) dependencies.get("entity");
		World world = (World) dependencies.get("world");
		int x = (int) dependencies.get("x");
		int y = (int) dependencies.get("y");
		int z = (int) dependencies.get("z");
		ItemStack itemstack = entity.getHeldItem(EnumHand.MAIN_HAND);

		// 1. RECOGER AGUA
		if (world.getBlockState(new BlockPos(x, y, z)).getMaterial() == Material.WATER) {
			if (!itemstack.hasTagCompound()) itemstack.setTagCompound(new NBTTagCompound());
			
			// Guardamos que el pote ahora tiene AGUA SUCIA (tipo 1)
			itemstack.getTagCompound().setInteger("water_type", 1);
			entity.sendStatusMessage(new net.minecraft.util.text.TextComponentString("§8[ClayPot] §fLlenado con agua de río."), true);
		} 
		
		// 2. PURIFICAR (Si haces click en un horno o fogata con el pote lleno)
		// Esto es abstracto: hervimos el agua al tocar un bloque caliente
		else if (world.getBlockState(new BlockPos(x, y, z)).getBlock() == net.minecraft.init.Blocks.LIT_FURNACE) {
			if (itemstack.hasTagCompound() && itemstack.getTagCompound().getInteger("water_type") == 1) {
				itemstack.getTagCompound().setInteger("water_type", 2);
				entity.sendStatusMessage(new net.minecraft.util.text.TextComponentString("§b[ClayPot] §fAgua purificada (hervida)."), true);
			}
		}
		
		// 3. BEBER
		else if (entity.isSneaking()) {
			if (itemstack.hasTagCompound()) {
				int type = itemstack.getTagCompound().getInteger("water_type");
				NBTTagCompound playerNbt = entity.getEntityData();
				
				if (type == 1) { // Sucia
					playerNbt.setInteger("gnul_input_agua_limpia", 10);
					playerNbt.setInteger("gnul_input_falta_agua", 20); // Mucha suciedad
					itemstack.getTagCompound().setInteger("water_type", 0);
				} else if (type == 2) { // Limpia
					playerNbt.setInteger("gnul_input_agua_limpia", 40); // Hidratación máxima
					int faltaActual = playerNbt.getInteger("gnul_input_falta_agua");
					if (faltaActual > 0) {
						int nuevaFalta = Math.max(0, faltaActual - 20);
						playerNbt.setInteger("gnul_input_falta_agua", nuevaFalta); // Limpia el riñón, pero lo protege, del numeraso
					}
					itemstack.getTagCompound().setInteger("water_type", 0);
					entity.sendStatusMessage(new net.minecraft.util.text.TextComponentString("§b[ClayPot] §fAgua pura. ¡Qué refrescante!"), true);
				}
			}
		}
	}
}
