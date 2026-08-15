package net.mcreator.gnulmod.procedure;

import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.event.world.BlockEvent;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.block.state.IBlockState;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraft.init.MobEffects;
import net.minecraft.potion.PotionEffect;

import net.mcreator.gnulmod.ElementsGnulmod;

@ElementsGnulmod.ModElement.Tag
public class ProcedureManualMining extends ElementsGnulmod.ModElement {

	public ProcedureManualMining(ElementsGnulmod instance) {
		super(instance, 10); // ID único para el elemento
	}

	@SubscribeEvent
	public void onBlockBreak(BlockEvent.BreakEvent event) {
		EntityPlayer entity = event.getPlayer();
		if (entity == null) return;

		World world = event.getWorld();
		BlockPos pos = event.getPos();
		IBlockState state = world.getBlockState(pos);
		NBTTagCompound nbt = entity.getEntityData();

		// 1. Obtener la dureza del bloque (Ej: Piedra = 1.5, Obsidiana = 50.0)
		float hardness = state.getBlockHardness(world, pos);
		
		// 2. Obtener la XP del brazo izquierdo (o el promedio de ambos)
		long fuerzaXP = nbt.getLong("gnul_arm_l_mlxp");

		// 3. Tu Lógica Maestra: Dureza desplazada 4 bits (Dureza * 16)
		// Si el material es Piedra (1.5), el umbral es 24.
		int umbralMaterial = ((int) hardness) << 4;

		// 4. Verificación de "Manos de Saitama"
		// Si la XP acumulada por el ejercicio supera la resistencia estructural del bloque...
		if (fuerzaXP > umbralMaterial) {
			// Forzamos el drop del ítem aunque no se use la herramienta correcta
			if (!entity.capabilities.isCreativeMode) {
				state.getBlock().dropBlockAsItem(world, pos, state, 0);
			}
			// El bloque se rompe con éxito
		} else if (entity.getHeldItemMainhand().isEmpty()) {
			// Si no tiene fuerza suficiente y está usando la mano vacía, cancelamos la rotura
			// Esto evita que rompas cosas "imposibles" sin haber entrenado
			event.setCanceled(true);
		}
	}
}
