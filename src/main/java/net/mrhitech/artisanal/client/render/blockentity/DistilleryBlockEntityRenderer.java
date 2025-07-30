package net.mrhitech.artisanal.client.render.blockentity;

import com.mojang.blaze3d.vertex.PoseStack;
import net.dries007.tfc.client.render.blockentity.FirepitBlockEntityRenderer;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraftforge.fluids.FluidStack;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;

public class DistilleryBlockEntityRenderer extends FirepitBlockEntityRenderer<DistilleryBlockEntity> {
    @Override
    public void render(DistilleryBlockEntity distillery, float partialTick, PoseStack poseStack, MultiBufferSource bufferSource, int combinedLight, int combinedOverlay) {
        super.render(distillery, partialTick, poseStack, bufferSource, combinedLight, combinedOverlay);
        
        if (!distillery.hasLevel()) return;
        
        final FluidStack outputStack = distillery.getFluidInTank(DistilleryBlockEntity.TANK_OUTPUT_FLUID);
        
        if (!outputStack.isEmpty()) {
            // Show the output fluid?
        }
        
        
        
    }
}
