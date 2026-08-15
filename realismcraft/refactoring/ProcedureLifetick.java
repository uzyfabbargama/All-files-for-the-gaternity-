package net.mcreator.gnulmod.procedure;

import net.minecraftforge.fml.common.gameevent.TickEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraft.world.WorldServer;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.util.DamageSource;
import net.minecraft.potion.PotionEffect;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.init.MobEffects;
import net.minecraft.entity.player.EntityPlayer;

import net.mcreator.gnulmod.NumerasoEngine;
import net.mcreator.gnulmod.ElementsGnulmod;

@ElementsGnulmod.ModElement.Tag
public class ProcedureLifetick extends ElementsGnulmod.ModElement {

	public ProcedureLifetick(ElementsGnulmod instance) {
		super(instance, 1);
	}

	public static void onTickStatic(TickEvent.PlayerTickEvent event) {
		if (event.phase == TickEvent.Phase.END && !event.player.world.isRemote) {
			EntityPlayer player = event.player;
			NBTTagCompound nbt = player.getEntityData();

			// 1. INICIALIZACIÓN (Aseguramos que todos los registros existan)
			if (!nbt.hasKey("gnul_pulmon")) {
				nbt.setLong("gnul_pulmon", NumerasoEngine.makeNumeraso(500, true, 1023, true, 500, true));
				nbt.setLong("gnul_pulmon_xp", 0L);
				nbt.setLong("gnul_corazon", NumerasoEngine.makeNumeraso(500, true, 1023, true, 500, true));
				nbt.setLong("gnul_corazon_xp", 0L);
				nbt.setLong("gnul_temp", NumerasoEngine.makeNumeraso(0, true, 500, true, 0, true));
				nbt.setLong("gnul_temp_xp", 0L);
				nbt.setLong("gnul_kidney", NumerasoEngine.makeNumeraso(0, true, 1023, true, 500, true));
				nbt.setLong("gnul_kidney_xp", 0L);
				nbt.setLong("gnul_leg_l", NumerasoEngine.makeNumeraso(0, true, 500, true, 200, true));
				nbt.setLong("gnul_leg_lxp", 0L);
				nbt.setLong("gnul_leg_r", NumerasoEngine.makeNumeraso(0, true, 500, true, 200, true));
				nbt.setLong("gnul_leg_rxp", 0L);
				nbt.setLong("gnul_leg_l_bn", NumerasoEngine.makeNumeraso(0, true, 500, true, 200, true));
				nbt.setLong("gnul_leg_l_bnxp", 0L);
				nbt.setLong("gnul_leg_r_bn", NumerasoEngine.makeNumeraso(0, true, 500, true, 200, true));
				nbt.setLong("gnul_leg_r_bnxp", 0L);
				nbt.setLong("gnul_leg_l_ml", NumerasoEngine.makeNumeraso(0, true, 500, true, 200, true));
				nbt.setLong("gnul_leg_l_mlxp", 0L);
				nbt.setLong("gnul_leg_r_ml", NumerasoEngine.makeNumeraso(0, true, 500, true, 200, true));
				nbt.setLong("gnul_leg_r_mlxp", 0L);
			}

			// 2. LECTURA DE REGISTROS
			long pulmon = nbt.getLong("gnul_pulmon");
			long pulmonXP = nbt.getLong("gnul_pulmon_xp");
			long corazon = nbt.getLong("gnul_corazon");
			long corazonXP = nbt.getLong("gnul_corazon_xp");
			long temp = nbt.getLong("gnul_temp");
			long tempXP = nbt.getLong("gnul_temp_xp");
			long kidney = nbt.getLong("gnul_kidney");
			long kidneyXP = nbt.getLong("gnul_kidney_xp");
            long leg_l = nbt.getLong("gnul_leg_l");
            long leg_lxp = nbt.getLong("gnul_leg_lxp");
            long leg_r = nbt.getLong("gnul_leg_r");
            long leg_rxp = nbt.getLong("gnul_leg_rxp");
            long leg_r_bn = nbt.getLong("gnul_leg_r_bn");
            long leg_r_bnxp = nbt.getLong("gnul_leg_r_bnxp");
            long leg_l_bn = nbt.getLong("gnul_leg_l_bn");
            long leg_l_bnxp = nbt.getLong("gnul_leg_l_bnxp");
            long leg_l_ml = nbt.getLong("gnul_leg_l_ml");
            long leg_l_mlxp = nbt.getLong("gnul_leg_l_mlxp");
            long leg_r_ml = nbt.getLong("gnul_leg_r_ml");
            long leg_r_mlxp = nbt.getLong("gnul_leg_r_mlxp");
			// 3. EXTRACCIÓN DE DATOS (Desempaquetamos los 10 bits)
			// En ProcedureLifetick.onTickStatic(), después de leer los NBTs existentes:

// Leer los buffs del sistema digestivo
int buffMusculo = nbt.getInteger("gnul_buff_musculo");
int buffHueso = nbt.getInteger("gnul_buff_hueso");
int buffVitals = nbt.getInteger("gnul_buff_vitals");

// APLICAR BUFFS A LOS ÓRGANOS (esto es lo que faltaba)
// Modificar los valores de applyRules para usar estos buffs
long[] resCorazon = NumerasoEngine.applyRules(corazon, corazonXP, 
    sedentarismo + castigoCorazon, ejercisio + buffVitals, 
    salud, salud + buffVitals, 
    sedentarismo, ejercisio + buffMusculo);

long[] resKidney = NumerasoEngine.applyRules(kidney, kidneyXP, 
    saludK + buffVitals, faltaAgua, 
    saludK + buffVitals, faltaAgua + inputFalta + (buffVitals/10), 
    saludK, saludK + inputLimpia + (buffVitals/10));

// Limpiar los buffs después de usarlos (para que no se acumulen)
nbt.setInteger("gnul_buff_musculo", 0);
nbt.setInteger("gnul_buff_hueso", 0);
nbt.setInteger("gnul_buff_vitals", 0);
			int f = (int)((temp >> NumerasoEngine.posZ) & NumerasoEngine.MASK10);
			int sTemp = (int)((temp >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
			int cTemp = (int)((temp >> NumerasoEngine.posX) & NumerasoEngine.MASK10);

			int ejercisio = (int)((corazon >> NumerasoEngine.posZ) & NumerasoEngine.MASK10);
			int salud = (int)((corazon >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
			int sedentarismo = (int)((corazon >> NumerasoEngine.posX) & NumerasoEngine.MASK10);

			int faltaAgua = (int)((kidney >> NumerasoEngine.posZ) & NumerasoEngine.MASK10);
			int saludK = (int)((kidney >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
			int aguaLimpia = (int)((kidney >> NumerasoEngine.posX) & NumerasoEngine.MASK10);

			// 4. SENSORES AMBIENTALES E INPUTS
			BlockPos pos = new BlockPos(player.posX, player.posY + 1, player.posZ);
			int luz = player.world.getLight(pos);
			int aireFactor = Math.abs(luz - 7);
			int movFactor = player.isSprinting() ? 5 : (player.distanceWalkedModified > 0 ? 3 : 0);
			
			float tempBioma = player.world.getBiome(player.getPosition()).getTemperature(player.getPosition());
			int factorFrio = tempBioma < 0.2 ? (int)((0.2 - tempBioma) * 100) : 0;
			int factorCalor = tempBioma > 0.8 ? (int)((tempBioma - 0.8) * 100) : 0;

			int inputLimpia = nbt.getInteger("gnul_input_agua_limpia");
			int inputFalta = nbt.getInteger("gnul_input_falta_agua");
			nbt.setInteger("gnul_input_agua_limpia", 0);
			nbt.setInteger("gnul_input_falta_agua", 0);

			// 5. APLICACIÓN DE REGLAS (Mecánica de Transurgencia)

			// REGLA 1: Temperatura
			long[] resTemp = NumerasoEngine.applyRules(temp, tempXP, (sTemp + (cTemp << 10)), f, (sTemp + (f << 10)), f + factorFrio, sTemp, sTemp + factorCalor);
			
			// REGLA 2: Pulmón
			long[] resPulmon = NumerasoEngine.applyRules(pulmon, pulmonXP, 0, aireFactor, 0, aireFactor, 0, movFactor);
			long falloPulmon = (resPulmon[0] >> NumerasoEngine.posC2) & 1;
			int castigoCorazon = (int) (falloPulmon * 20);

			// REGLA 3: Corazón
			long[] resCorazon = NumerasoEngine.applyRules(corazon, corazonXP, sedentarismo + castigoCorazon, ejercisio, salud, salud, sedentarismo, ejercisio);

			// REGLA 4: Riñones
			long[] resKidney = NumerasoEngine.applyRules(kidney, kidneyXP, saludK, faltaAgua, saludK, faltaAgua + inputFalta, saludK, saludK + inputLimpia);

			// 6. GUARDADO
			nbt.setLong("gnul_temp", resTemp[0]);
			nbt.setLong("gnul_temp_xp", resTemp[1]);
			nbt.setLong("gnul_pulmon", resPulmon[0]);
			nbt.setLong("gnul_pulmon_xp", resPulmon[1]);
			nbt.setLong("gnul_corazon", resCorazon[0]);
			nbt.setLong("gnul_corazon_xp", resCorazon[1]);
			nbt.setLong("gnul_kidney", resKidney[0]);
			nbt.setLong("gnul_kidney_xp", resKidney[1]);

			// 7. EFECTOS Y FEEDBACK
			long saludPulmon = (resPulmon[0] >> NumerasoEngine.posY) & NumerasoEngine.MASK10;
			int msgTimer = nbt.getInteger("gnul_msg_timer");
			if (msgTimer > 0) {
				nbt.setInteger("gnul_msg_timer", msgTimer - 1);
				if (player.world.getTotalWorldTime() % 40 == 0) {
					player.sendStatusMessage(new net.minecraft.util.text.TextComponentString("§b[Gnul] §fPulmón: " + saludPulmon + " | Corazón: " + salud), true);
				}
	
				if (player.world.getTotalWorldTime() % 60 == 0) {
					player.sendStatusMessage(new net.minecraft.util.text.TextComponentString("§9[Riñones] §fHidratación: " + aguaLimpia), true);
				}
			}

			if (saludPulmon < 300) {
				player.addPotionEffect(new PotionEffect(MobEffects.MINING_FATIGUE, 40, 0));
				if (falloPulmon == 1) {
					((WorldServer) player.world).spawnParticle(EnumParticleTypes.SMOKE_LARGE, player.posX, player.posY + 1.6, player.posZ, 2, 0.05, 0, 0.05, 0.02);
				}
			}
		}
	}

	@Override
	public void preInit(FMLPreInitializationEvent event) {}
}
