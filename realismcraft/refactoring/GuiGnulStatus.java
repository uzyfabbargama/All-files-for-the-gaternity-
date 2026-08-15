package net.mcreator.gnulmod.gui;

import net.minecraft.client.gui.inventory.GuiContainer;
import net.minecraft.client.renderer.GlStateManager;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.util.ResourceLocation;
import net.mcreator.gnulmod.NumerasoEngine;
import java.io.IOException;

public class GuiGnulStatus extends GuiContainer {
    public static final int GUIID = 1;
    // Usaremos una textura básica para el fondo o colores planos para mayor claridad
    private static final ResourceLocation texture = new ResourceLocation("gnulmod:textures/gui/status_bg.png");
    // Añade esta variable al inicio de la clase
	private int timer = 0;
	private final int MAX_TIME = 100; // Aproximadamente 5 segundos (20 ticks por segundo)
    private final EntityPlayer entity;
    @Override
	public void updateScreen() {
    	super.updateScreen();
    	timer++;
    	// Si pasa el tiempo, cerramos la GUI automáticamente para liberar recursos
    	if (timer > MAX_TIME) {
        	this.mc.player.closeScreen();
    	}
	}
	
    public GuiGnulStatus(EntityPlayer entity) {
        super(new net.minecraft.inventory.Container() {
            @Override
            public boolean canInteractWith(EntityPlayer playerIn) { return true; }
        });
        this.entity = entity;
        this.xSize = 176;
        this.ySize = 166;
    }

    @Override
    public void drawScreen(int mouseX, int mouseY, float partialTicks) {
        this.drawDefaultBackground();
        super.drawScreen(mouseX, mouseY, partialTicks);
        this.renderHoveredToolTip(mouseX, mouseY);
    }

    @Override
	protected void drawGuiContainerBackgroundLayer(float partialTicks, int mouseX, int mouseY) {
    	// Solo dibujamos si el timer es bajo, para dar ese efecto de "desvanecimiento" mental
    	if (timer < MAX_TIME) {
        	GlStateManager.color(1, 1, 1, 1);
        	
        	// El fondo oscuro
        	this.drawGradientRect(this.guiLeft, this.guiTop, this.guiLeft + this.xSize, this.guiTop + this.ySize, 0xFF000000, 0xFF111111);
	
        	NBTTagCompound nbt = entity.getEntityData();
        	
        	// Dibujamos las barras (esto es lo que consume ciclos de renderizado)
        	drawOrganBar("Corazón", nbt.getLong("gnul_corazon"), this.guiLeft + 10, this.guiTop + 20, 0xFFFF0000);
        	drawOrganBar("Hígado", nbt.getLong("gnul_higado"), this.guiLeft + 10, this.guiTop + 45, 0xFF8B4513);
        	drawOrganBar("Páncreas", nbt.getLong("gnul_pancreas"), this.guiLeft + 10, this.guiTop + 70, 0xFFFFD700);
    	}
	}

    private void drawOrganBar(String name, long numeraso, int x, int y, int color) {
        // Extraemos la salud del Bit Y (Posición 11 a 20)
        int salud = (int)((numeraso >> NumerasoEngine.posY) & NumerasoEngine.MASK10);
        float porcentaje = salud / 1023.0f;
        int barWidth = (int)(porcentaje * 150);

        // Texto del órgano
        this.fontRenderer.drawString(name + ": " + salud, x, y, 0xFFFFFF);
        
        // Fondo de la barra (Gris oscuro)
        drawRect(x, y + 10, x + 150, y + 18, 0xFF333333);
        
        // Barra de salud (Color del órgano)
        drawRect(x, y + 10, x + barWidth, y + 18, color);
    }
}
