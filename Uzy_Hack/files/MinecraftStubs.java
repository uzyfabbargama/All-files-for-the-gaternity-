package net.minecraft.world; public class World { public java.util.List<net.minecraft.entity.Entity> loadedEntityList; }
package net.minecraft.entity; public class Entity { public double posX, posY, posZ; public float renderDistanceWeight; public World world; }
package net.minecraft.entity; public class EntityLivingBase extends Entity { public int getTotalArmorValue(){return 0;} }
package net.minecraftforge.fml.common.gameevent; public class TickEvent { public enum Phase { START, END } public static class WorldTickEvent { public Phase phase; public net.minecraft.world.World world; } }
package net.minecraftforge.fml.common.eventhandler; public @interface SubscribeEvent {}
package net.minecraftforge.event.entity.living; public class LivingAttackEvent { public net.minecraft.entity.Entity getEntity(){return null;} public void setCanceled(boolean c){} }
// Agrega estas líneas extra para ElementsUzyopt
package net.minecraft.util; public class ResourceLocation {}
package net.minecraft.item; public class ItemStack {}
package net.minecraft.block; public class Block {}
