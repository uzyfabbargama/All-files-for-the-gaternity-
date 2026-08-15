package net.mcreator.gnulmod;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.reflect.TypeToken;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ResourceLocation;
import java.io.*;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Map;

public class GnulFoodReader {
    private static Map<String, FoodData> registry = new HashMap<>();
    private static final File CONFIG_FILE = new File("config/gnul_foods.json");

    public static class FoodData {
        public int carne, vegetal, cereal, toxinas;
        public FoodData(int c, int v, int ce, int t) {
            this.carne = c; this.vegetal = v; this.cereal = ce; this.toxinas = t;
        }
    }

    public static void load() {
        if (!CONFIG_FILE.exists()) {
            generateDefaultConfig();
        }
        try (Reader reader = new FileReader(CONFIG_FILE)) {
            registry = new Gson().fromJson(reader, new TypeToken<Map<String, FoodData>>(){}.getType());
            System.out.println("[Gnul] JSON de comidas cargado: " + registry.size() + " entradas.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void generateDefaultConfig() {
        Map<String, FoodData> defaults = new HashMap<>();
        defaults.put("minecraft:apple", new FoodData(0, 10, 0, 0));
        defaults.put("minecraft:cooked_beef", new FoodData(30, 0, 0, 5));
        defaults.put("minecraft:bread", new FoodData(0, 0, 20, 0));
        defaults.put("minecraft:rotten_flesh", new FoodData(10, 0, 0, 50));
        
        try (Writer writer = new FileWriter(CONFIG_FILE)) {
            new Gson().toJson(defaults, writer);
        } catch (IOException e) { e.printStackTrace(); }
    }

    public static FoodData getNutrients(ItemStack stack) {
        if (stack.isEmpty()) return new FoodData(0,0,0,0);
        String name = stack.getItem().getRegistryName().toString();
        return registry.getOrDefault(name, new FoodData(0, 0, 0, 0));
    }
}
