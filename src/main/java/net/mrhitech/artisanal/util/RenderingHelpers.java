package net.mrhitech.artisanal.util;

import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.PoseStack;
import net.dries007.tfc.common.fluids.TFCFluids;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.ScreenEffectRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.material.Fluids;
import net.minecraftforge.client.gui.overlay.ForgeGui;
import net.minecraftforge.fluids.FluidType;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;
import net.mrhitech.artisanal.common.fluids.Waterlikes;
import net.mrhitech.artisanal.common.item.LabGogglesItem;

import java.util.HashMap;
import java.util.Map;

public class RenderingHelpers {
    
    // If you want your own overlays, put them in here
    
    public static final Map<FluidType, ResourceLocation> overlays = new HashMap<>();
    static {
        overlays.put(Fluids.WATER.getFluidType(), TFCFluids.UNDERWATER_LOCATION);
        overlays.put(
                ArtisanalFluids.WATERLIKES.get(Waterlikes.SWEET_CRUDE_OIL).getSource().getFluidType(), 
                Waterlikes.SWEET_CRUDE_OIL.getUnderneathTexture()
        );
        
        overlays.put(
                ArtisanalFluids.WATERLIKES.get(Waterlikes.SOUR_CRUDE_OIL).getSource().getFluidType(),
                Waterlikes.SOUR_CRUDE_OIL.getUnderneathTexture()
        );
        
    }
    
    public static void renderWaterlike(Minecraft minecraft, PoseStack poseStack) {
        if (minecraft.player == null) return;
        
        FluidType fluidType = minecraft.player.getEyeInFluidType();
        ResourceLocation textureToRender = overlays.getOrDefault(fluidType, TFCFluids.UNDERWATER_LOCATION);
        
        ScreenEffectRenderer.renderFluid(minecraft, poseStack, textureToRender);
        
    }
    
    public static void renderTextureOverlay(GuiGraphics graphics, ResourceLocation location, float alpha)
    {
        final Minecraft mc = Minecraft.getInstance();
        final int screenWidth = mc.getWindow().getGuiScaledWidth();
        final int screenHeight = mc.getWindow().getGuiScaledHeight();

        RenderSystem.disableDepthTest();
        RenderSystem.depthMask(false);
        graphics.setColor(1.0F, 1.0F, 1.0F, alpha);
        graphics.blit(location, 0, 0, -90, 0.0F, 0.0F, screenWidth, screenHeight, screenWidth, screenHeight);
        RenderSystem.depthMask(true);
        RenderSystem.enableDepthTest();
        graphics.setColor(1.0F, 1.0F, 1.0F, 1.0F);
    }
    
    public static void renderLabGogglesOverWorldIfWorn(ForgeGui gui, GuiGraphics graphics, float partialTicks, int width, int height) {
        
        if (!Minecraft.getInstance().options.getCameraType().isFirstPerson()) return;
        
        LocalPlayer player = Minecraft.getInstance().player;
        
        if (player == null) return;
        
        if (LabGogglesItem.wearingLabGoggles(player)) {
            renderTextureOverlay(graphics, LabGogglesItem.OVERLAY_TEXTURE, 1f);
        }
    }
}
