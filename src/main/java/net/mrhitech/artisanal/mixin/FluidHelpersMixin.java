package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.util.Helpers;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.material.Fluid;
import net.mrhitech.artisanal.common.ArtisanalTags;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(value = FluidHelpers.class)
public class FluidHelpersMixin {
    
    @Inject(method = "isInWaterLikeFluid", at = @At("HEAD"), remap = false, cancellable = true)
    private static void artisanal$isInWaterLikeFluid(Entity entity, CallbackInfoReturnable<Boolean> callbackInfoReturnable) {
        for (Fluid fluid : Helpers.allFluids(ArtisanalTags.FLUIDS.WATER_VISION).toList()) {
            if (entity.isInFluidType(((fluidType, aDouble) -> fluidType == fluid.getFluidType()))) {
                callbackInfoReturnable.setReturnValue(true);
                return;
            }
        }
    }
    
    @Inject(method = "isEyeInWaterLikeFluid", at = @At("HEAD"), remap = false, cancellable = true)
    private static void artisanal$isEyeInWaterLikeFluid(Entity entity, CallbackInfoReturnable<Boolean> callbackInfoReturnable) {
        for (Fluid fluid : Helpers.allFluids(ArtisanalTags.FLUIDS.WATER_VISION).toList()) {
            if (entity.isEyeInFluidType(fluid.getFluidType())) {
                callbackInfoReturnable.setReturnValue(true);
                return;
            }
        }
    }
    
}
