package net.mrhitech.artisanal.client.screen;

import net.dries007.tfc.TerraFirmaCraft;
import net.dries007.tfc.client.RenderHelpers;
import net.dries007.tfc.client.screen.BlockEntityScreen;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.capabilities.heat.Heat;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.config.TFCConfig;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Tooltips;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.Inventory;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.fml.ModList;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;
import net.mrhitech.artisanal.common.container.DistilleryContainer;

public class DistilleryScreen extends BlockEntityScreen<DistilleryBlockEntity, DistilleryContainer> {
    private static final ResourceLocation BACKGROUND = new ResourceLocation(Artisanal.MOD_ID, "textures/gui/fire_pit_distillery.png");
    private static final int TICKS_PER_DRIP_ANIMATION_CYCLE = DistilleryBlockEntity.TICKS_PER_DRIP_SOUND * 4;
    
    
    public DistilleryScreen(DistilleryContainer container, Inventory playerInventory, Component name) {
        super(container, playerInventory, name, BACKGROUND);
        inventoryLabelY += 20;
        imageHeight += 20;
    }
    
    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        super.renderLabels(graphics, mouseX, mouseY);
        
        if (blockEntity.shouldRenderAsBoiling()) {
            drawDisabled(graphics, DistilleryBlockEntity.SLOT_INPUT_ITEM, DistilleryBlockEntity.SLOT_INPUT_ITEM);
        }
        
        final MutableComponent text = Component.empty();
        if (blockEntity.shouldRenderAsBoiling()) {
            text.append(Component.translatable("tfc.tooltip.pot_boiling"));
        }
        
        final int x = 118 - font.width(text) / 2;
        graphics.drawString(font, text, x, 80, 0x404040, false);
        
    }
    
    @Override
    protected void renderTooltip(GuiGraphics graphics, int mouseX, int mouseY) {
        super.renderTooltip(graphics, mouseX, mouseY);
        
        if (RenderHelpers.isInside(mouseX, mouseY, getGuiLeft() + 76, getGuiTop() + 47, 86 - 76, 54 - 47)) {
            final FluidStack fluid = blockEntity.getFluidInTank(DistilleryBlockEntity.TANK_OUTPUT_FLUID);
            if (!fluid.isEmpty()) {
                graphics.renderTooltip(font, Tooltips.fluidUnitsAndCapacityOf(fluid, FluidHelpers.BUCKET_VOLUME), mouseX, mouseY);
            }
        }
        else if (RenderHelpers.isInside(mouseX, mouseY, getGuiLeft() + 61, getGuiTop() + 51, 92 - 61, 77 - 51)) {
            final FluidStack fluid = blockEntity.getCapability(Capabilities.FLUID)
                    .map(c -> c.getFluidInTank(0))
                    .orElse(FluidStack.EMPTY);
            if (!fluid.isEmpty()) {
                graphics.renderTooltip(font, Tooltips.fluidUnitsAndCapacityOf(fluid, FluidHelpers.BUCKET_VOLUME), mouseX, mouseY);
            }
        }
        
        if (RenderHelpers.isInside(mouseX, mouseY, leftPos + 30, topPos + 76 - 51, 15, 51))
        {
            final var text = TFCConfig.CLIENT.heatTooltipStyle.get().formatColored(blockEntity.getTemperature());
            if (text != null)
            {
                graphics.renderTooltip(font, text, mouseX, mouseY);
            }
        }
    }
    
    @Override
    protected void renderBg(GuiGraphics graphics, float partialTicks, int mouseX, int mouseY) {
        super.renderBg(graphics, partialTicks, mouseX, mouseY);
        
        if (ModList.get().isLoaded("jei"))
        {
            graphics.blit(texture, getGuiLeft() + 77, getGuiTop() + 6, 247, 0, 9, 14);
        }
        
        int temp = Heat.scaleTemperatureForGui(blockEntity.getTemperature());
        if (temp > 0) {
            graphics.blit(texture, leftPos + 30, topPos + 76 - Math.min(51, temp), 176, 0, 15, 5);
        }
        
        if (blockEntity.getTemperature() > 0)
        {
            graphics.blit(BACKGROUND, leftPos + 54, topPos + 78, 192, 0, 13, 13);
            graphics.blit(BACKGROUND, leftPos + 69, topPos + 78, 192, 0, 13, 13);
            graphics.blit(BACKGROUND, leftPos + 84, topPos + 78, 192, 0, 13, 13);
        }
        
        if (blockEntity.shouldRenderAsBoiling())
        {
            final int ticks = (blockEntity.getBoilingTicks() % TICKS_PER_DRIP_ANIMATION_CYCLE);
            final int vHeight = Mth.ceil((float)ticks / TICKS_PER_DRIP_ANIMATION_CYCLE * 8);
            
            graphics.blit(BACKGROUND, leftPos + 79, topPos + 38, 178, 7, 2, vHeight);
            
            // graphics.blit(BACKGROUND, leftPos + 131, topPos + 10 + 20 - vHeight, 193, 16 + 21 - vHeight, 11, vHeight);
            // graphics.blit(BACKGROUND, leftPos + 144, topPos + 10 + 20 - vHeight, 193, 16 + 21 - vHeight, 11, vHeight);
        }
        
        
        int fluidColor = -1;
        FluidStack outputFluid = blockEntity.getFluidInTank(1);
        if (!outputFluid.isEmpty()) {
            fluidColor = RenderHelpers.getFluidColor(outputFluid);
        }
        
        if (fluidColor != -1) {
            RenderHelpers.setShaderColor(fluidColor);
            graphics.blit(BACKGROUND, leftPos + 76, topPos + 47, 208, 0, 10, 3);
            resetToBackgroundSprite();
        }
    }
}
