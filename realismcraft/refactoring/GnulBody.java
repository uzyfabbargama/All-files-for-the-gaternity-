package net.mcreator.gnulmod;

import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.world.WorldServer;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.potion.PotionEffect;
import net.minecraft.init.MobEffects;
import net.mcreator.gnulmod.NumerasoEngine;

public class GnulBody {

    public static void processVitals(EntityPlayer player, NBTTagCompound nbt, int aireFactor, int inputLimpia, int inputFalta, int factorFrio, int factorCalor) {
        if (!nbt.hasKey("gnul_pulmon")) {
            nbt.setLong("gnul_pulmon", NumerasoEngine.makeNumeraso(500, true, 1023, true, 500, true));
            nbt.setLong("gnul_pulmon_xp", 0L);
            nbt.setLong("gnul_corazon", NumerasoEngine.makeNumeraso(500, true, 1023, true, 500, true));
            nbt.setLong("gnul_corazon_xp", 0L);
            nbt.setLong("gnul_temp", NumerasoEngine.makeNumeraso(0, true, 500, true, 0, true));
            nbt.setLong("gnul_temp_xp", 0L);
            nbt.setLong("gnul_kidney", NumerasoEngine.makeNumeraso(0, true, 1023, true, 500, true));
            nbt.setLong("gnul_kidney_xp", 0L);
        }

        long pulmon = nbt.getLong("gnul_pulmon");
        long corazon = nbt.getLong("gnul_corazon");
        long temp = nbt.getLong("gnul_temp");
        long kidney = nbt.getLong("gnul_kidney");

        int sTemp = (int)((temp >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
        int f = (int)((temp >> NumerasoEngine.posZ) & NumerasoEngine.MASK10);
        int salud = (int)((corazon >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
        int sedentarismo = (int)((corazon >> NumerasoEngine.posX) & NumerasoEngine.MASK10);
        int saludK = (int)((kidney >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
        int faltaAgua = (int)((kidney >> NumerasoEngine.posZ) & NumerasoEngine.MASK10);

        // --- BONUS: HUMEDAD ---
        boolean estaMojado = player.isInWater() || player.isWet();
        int factorHumedadFrio = estaMojado ? 150 : 100;
        int factorHumedadCalor = estaMojado ? 70 : 100;
        int factorFrioFinal = (factorFrio * factorHumedadFrio) / 100;
        int factorCalorFinal = (factorCalor * factorHumedadCalor) / 100;

        long[] resTemp = NumerasoEngine.applyRules(temp, nbt.getLong("gnul_temp_xp"), (sTemp + (f << 10)), f, (sTemp + (f << 10)), f + factorFrioFinal, sTemp, sTemp + factorCalorFinal);
        long[] resPulmon = NumerasoEngine.applyRules(pulmon, nbt.getLong("gnul_pulmon_xp"), 0, aireFactor, 0, aireFactor, 0, (player.isSprinting() ? 5 : 2));
        int castigoCorazon = ((resPulmon[0] >> NumerasoEngine.posC2) & 1) == 1 ? 20 : 0;
        long[] resCorazon = NumerasoEngine.applyRules(corazon, nbt.getLong("gnul_corazon_xp"), sedentarismo + castigoCorazon, 0, salud, salud, sedentarismo, 0);
        long[] resKidney = NumerasoEngine.applyRules(kidney, nbt.getLong("gnul_kidney_xp"), saludK, faltaAgua, saludK, faltaAgua + inputFalta, saludK, saludK + inputLimpia);

        nbt.setLong("gnul_temp", resTemp[0]);
        nbt.setLong("gnul_temp_xp", resTemp[1]);
        nbt.setLong("gnul_pulmon", resPulmon[0]);
        nbt.setLong("gnul_pulmon_xp", resPulmon[1]);
        nbt.setLong("gnul_corazon", resCorazon[0]);
        nbt.setLong("gnul_corazon_xp", resCorazon[1]);
        nbt.setLong("gnul_kidney", resKidney[0]);
        nbt.setLong("gnul_kidney_xp", resKidney[1]);

        if (player.world.getTotalWorldTime() % 40 == 0) {
            player.sendStatusMessage(new net.minecraft.util.text.TextComponentString("§b[Gnul] §fSist. Vital Operativo"), true);
        }
    }

    public static void processLegs(EntityPlayer player, NBTTagCompound nbt, int movFactor, int dañoFisico) {
        if (!nbt.hasKey("gnul_leg_l_bn")) {
            nbt.setLong("gnul_leg_l_bn", NumerasoEngine.makeNumeraso(0, true, 1023, true, 500, true));
            nbt.setLong("gnul_leg_l_bnxp", 0L); // Corregido: añadida la XP faltante
            nbt.setLong("gnul_leg_l_ml", NumerasoEngine.makeNumeraso(0, true, 1023, true, 500, true));
            nbt.setLong("gnul_leg_l_mlxp", 0L); // Corregido: añadida la XP faltante
        }

        long boneL = nbt.getLong("gnul_leg_l_bn");
        long muscleL = nbt.getLong("gnul_leg_l_ml");
        int saludOsea = (int)((boneL >> NumerasoEngine.posY) & NumerasoEngine.MASK10);

        long[] resBone = NumerasoEngine.applyRules(boneL, nbt.getLong("gnul_leg_l_bnxp"), saludOsea, dañoFisico, dañoFisico, dañoFisico, saludOsea, 500);
        long[] resMuscle = NumerasoEngine.applyRules(muscleL, nbt.getLong("gnul_leg_l_mlxp"), 0, movFactor, 500, 500, 0, movFactor);

        nbt.setLong("gnul_leg_l_bn", resBone[0]);
        nbt.setLong("gnul_leg_l_bnxp", resBone[1]);
        nbt.setLong("gnul_leg_l_ml", resMuscle[0]);
        nbt.setLong("gnul_leg_l_mlxp", resMuscle[1]);

        if (saludOsea < 200) {
            player.addPotionEffect(new PotionEffect(MobEffects.SLOWNESS, 40, 2));
        }
    }

    public static void processArms(EntityPlayer player, NBTTagCompound nbt, int workLoad) {
        if (!nbt.hasKey("gnul_arm_l_ml")) {
            nbt.setLong("gnul_arm_l_ml", NumerasoEngine.makeNumeraso(0, true, 1023, true, 500, true));
            nbt.setLong("gnul_arm_l_mlxp", 0L);
        }

        long armML = nbt.getLong("gnul_arm_l_ml");
        long armXP = nbt.getLong("gnul_arm_l_mlxp");
        
        long[] resArm = NumerasoEngine.applyRules(armML, armXP, 0, workLoad, 500, 500, 0, workLoad);

        nbt.setLong("gnul_arm_l_ml", resArm[0]);
        nbt.setLong("gnul_arm_l_mlxp", resArm[1]);

        int fuerza = (int) (resArm[1] / 1000);
        if (fuerza > 0) {
            player.addPotionEffect(new PotionEffect(MobEffects.HASTE, 40, fuerza - 1));
        }
    }
    	public static void processDigestive(EntityPlayer player, NBTTagCompound nbt, int carne, int vegetales, int cereales) {
    	// 1. INICIALIZACIÓN
    	if (!nbt.hasKey("gnul_estomago")) {
        	nbt.setLong("gnul_estomago", NumerasoEngine.makeNumeraso(500, true, 1023, true, 0, true));
        	nbt.setLong("gnul_higado", NumerasoEngine.makeNumeraso(500, true, 1023, true, 0, true));
        	nbt.setLong("gnul_pancreas", NumerasoEngine.makeNumeraso(500, true, 1023, true, 0, true));
    	}
	
    	long estomago = nbt.getLong("gnul_estomago");
    	long higado = nbt.getLong("gnul_higado");
    	long pancreas = nbt.getLong("gnul_pancreas");
	
    	// 2. EXTRACCIÓN DE SALUD (Bit central de cada órgano)
    	int sEst = (int)((estomago >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
    	int sHig = (int)((higado >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
    	int sPan = (int)((pancreas >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
	
    	// 3. APLICACIÓN DE REGLAS (Basado en tus archivos func_*.py)
	
    	// Estómago: Vegetales lo hacen trabajar de más (negativo), Salud lo estabiliza.
    	long[] resEst = NumerasoEngine.applyRules(estomago, nbt.getLong("gnul_estomago_xp"), 
        	sEst, vegetales, sEst, vegetales, sEst, sEst + carne);
	
    	// Hígado: Toxinas o exceso de carne lo cansan, vegetales lo limpian.
    	long[] resHig = NumerasoEngine.applyRules(higado, nbt.getLong("gnul_higado_xp"), 
        	sHig, carne, sHig, carne, sHig, sHig + vegetales);
	
    	// Páncreas: Azúcares/Cereales lo agotan, vegetales le dan salud.
    	long[] resPan = NumerasoEngine.applyRules(pancreas, nbt.getLong("gnul_pancreas_xp"), 
        	sPan, cereales, sPan, cereales, sPan, sPan + vegetales);
	
    	// 4. GUARDADO
    	nbt.setLong("gnul_estomago", resEst[0]);
    	nbt.setLong("gnul_higado", resHig[0]);
    	nbt.setLong("gnul_pancreas", resPan[0]);
	
    	// 5. DISTRIBUCIÓN DE NUTRIENTES (La Transurgencia)
    	// Estos valores irán a parar a los inputs de processVitals, processArms y processLegs
    	nbt.setInteger("gnul_buff_musculo", (carne * 2) + vegetales); // Mejora músculos
    	nbt.setInteger("gnul_buff_hueso", vegetales * 2); // Vegetales mejoran huesos
    	nbt.setInteger("gnul_buff_vitals", vegetales + cereales); // Mejora general
	}
}
