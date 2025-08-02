package net.mrhitech.artisanal.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.ScreenEffectRenderer;
import net.mrhitech.artisanal.util.RenderingHelper;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Overwrite;

@Mixin(ScreenEffectRenderer.class)
public class ScreenEffectRendererMixin {
    /**
     * @author MrHiTech
     * @reason Make the water texture be based on current block type to render more than water
     */
    @Overwrite
    public static void renderWater(Minecraft minecraft, PoseStack poseStack) {
        RenderingHelper.renderWaterlike(minecraft, poseStack);
    }
}
