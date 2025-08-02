package net.mrhitech.artisanal.util;

import com.mojang.blaze3d.vertex.PoseStack;
import net.dries007.tfc.common.fluids.TFCFluids;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.ScreenEffectRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.FluidTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.material.Fluid;
import net.minecraft.world.level.material.Fluids;
import net.minecraftforge.fluids.FluidType;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;
import net.mrhitech.artisanal.common.fluids.Waterlikes;

import java.util.HashMap;
import java.util.Map;

public class RenderingHelper {
    
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
}
