package net.mcreator.gnulmod.procedure;

import net.minecraft.item.ItemStack;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.EnumHand;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.util.text.TextComponentString;
import net.mcreator.gnulmod.ElementsGnulmod;

public class ProcedureFilterRightClickedInAir {

	public static void executeProcedure(java.util.HashMap<String, Object> dependencies) {
		EntityPlayer entity = (EntityPlayer) dependencies.get("entity");
		
		// Mano principal: El Clay Pot
		ItemStack mainHand = entity.getHeldItem(EnumHand.MAIN_HAND);
		// Mano secundaria: El Filtro
		ItemStack offHand = entity.getHeldItem(EnumHand.OFF_HAND);

		// Verificamos que tengamos el Pote y el Filtro donde corresponden
		if (mainHand.getItem().getRegistryName().toString().equals("gnulmod:claypot") && 
		    offHand.getItem().getRegistryName().toString().equals("gnulmod:filter")) {
			
			if (!mainHand.hasTagCompound()) mainHand.setTagCompound(new NBTTagCompound());
			NBTTagCompound nbt = mainHand.getTagCompound();
			
			int data = nbt.getInteger("pot_logic");
			int tipoAgua = data & 0x3;      // Extraemos bits 0-1
			int desgaste = (data >> 2) & 0x3; // Extraemos bits 2-3

			// CONDICIÓN: Si el agua está CALIENTE (tipo 2)
			if (tipoAgua == 2) {
				// TRANSFORMACIÓN DE BITS:
				// Pasamos el tipo de 2 (10) a 3 (11) -> Agua Pura
				int newData = (desgaste << 2) | 3; 
				
				nbt.setInteger("pot_logic", newData);
				
				// Consumir el filtro (desaparece)
				if (!entity.capabilities.isCreativeMode) {
					offHand.shrink(1);
				}

				entity.sendStatusMessage(new TextComponentString("§b[Gnul] §fFiltrando agua caliente... ¡Ahora es pura!"), true);
				
				// Efecto visual rápido
				entity.world.spawnParticle(net.minecraft.util.EnumParticleTypes.WATER_SPLASH, 
					entity.posX, entity.posY + 1.5, entity.posZ, 0, 0.1, 0);
			} else {
				entity.sendStatusMessage(new TextComponentString("§cEl agua debe estar hervida para filtrarla correctamente."), true);
			}
		}
	}
}