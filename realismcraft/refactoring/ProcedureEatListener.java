package net.mcreator.gnulmod;

// Imports de Minecraft
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NBTTagCompound;

// Imports de Forge (Eventos)
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.event.entity.living.LivingEntityUseItemEvent;

// Imports de tu Mod
import net.mcreator.gnulmod.GnulBody;
import net.mcreator.gnulmod.GnulFoodReader;
import net.mcreator.gnulmod.GnulFoodReader.FoodData; // Importante para reconocer los datos del JSON

public class ProcedureEatListener {

    @SubscribeEvent
    public void onPlayerEat(LivingEntityUseItemEvent.Finish event) {
        if (event.getEntityLiving() instanceof EntityPlayer) {
            EntityPlayer player = (EntityPlayer) event.getEntityLiving();
            ItemStack itemStack = event.getItem();
            
            // Usamos el lector de JSON que creamos
            FoodData data = GnulFoodReader.getNutrients(itemStack);
            
            // Verificamos si el ítem tiene valores nutricionales definidos (al menos uno > 0)
            if (data.carne > 0 || data.vegetal > 0 || data.cereal > 0 || data.toxinas > 0) {
                NBTTagCompound nbt = player.getEntityData();
                
                // 1. Enviamos a la transurgencia digestiva
                GnulBody.processDigestive(player, nbt, data.carne, data.vegetal, data.cereal);
                
                // 2. Si tiene toxinas, se guardan para el próximo tick del hígado
                if (data.toxinas > 0) {
                    // Usamos una suma para no sobrescribir si come varias cosas rápido
                    int toxinasActuales = nbt.getInteger("gnul_input_toxinas");
                    nbt.setInteger("gnul_input_toxinas", toxinasActuales + data.toxinas);
                }
            }
        }
    }
}
