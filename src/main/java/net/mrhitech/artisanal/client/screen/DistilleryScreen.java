package net.mrhitech.artisanal.client.screen;

import net.dries007.tfc.client.RenderHelpers;
import net.dries007.tfc.client.screen.BlockEntityScreen;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.config.TFCConfig;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Tooltips;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;
import net.minecraftforge.fluids.FluidStack;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;
import net.mrhitech.artisanal.common.container.DistilleryContainer;

public class DistilleryScreen extends BlockEntityScreen<DistilleryBlockEntity, DistilleryContainer> {
    private static final ResourceLocation BACKGROUND = new ResourceLocation("textures/gui/fire_pit_distillery.png");
    
    public DistilleryScreen(DistilleryContainer container, Inventory playerInventory, Component name) {
        super(container, playerInventory, name, BACKGROUND);
        inventoryLabelY += 20;
        imageHeight += 20;
    }
    
    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        super.renderLabels(graphics, mouseX, mouseY);
        
        if (blockEntity.shouldRenderAsBoiling()) {
            drawDisabled(graphics, DistilleryBlockEntity.SLOT_INPUT_ITEM, DistilleryBlockEntity.SLOT_OUTPUT_ITEM + 1);
        }
        
        final MutableComponent text = Component.empty();
        if (blockEntity.shouldRenderAsBoiling()) {
            text.append(Component.translatable("artisanal.tooltip.distillery_boiling"));
        }
        
        final int x = 118 - font.width(text) / 2;
        graphics.drawString(font, text, x, 80, 0x404040, false);
        
    }
    
    @Override
    protected void renderTooltip(GuiGraphics graphics, int mouseX, int mouseY) {
        super.renderTooltip(graphics, mouseX, mouseY);
        
        if (RenderHelpers.isInside(mouseX, mouseY, getGuiLeft() + 121, getGuiTop() + 30, 162 - 121, 58 - 30)) {
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
        
        
        
    }
}
