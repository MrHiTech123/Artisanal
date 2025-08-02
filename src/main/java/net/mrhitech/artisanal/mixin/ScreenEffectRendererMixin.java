package net.mrhitech.artisanal.mixin;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.ScreenEffectRenderer;
import net.mrhitech.artisanal.util.RenderingHelper;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Overwrite;
import org.spongepowered.asm.mixin.injection.Inject;

@Mixin(ScreenEffectRenderer.class)
public class ScreenEffectRendererMixin {
    @Overwrite
    public static void renderWater(Minecraft minecraft, PoseStack poseStack) {
        RenderingHelper.renderWaterlike(minecraft, poseStack);
    }
}
