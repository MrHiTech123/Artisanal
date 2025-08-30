package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blockentities.InventoryBlockEntity;
import net.mrhitech.artisanal.util.IBarrelInventoryMixin;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(BarrelBlockEntity.BarrelInventory.class)
public class BarrelInventoryMixin implements IBarrelInventoryMixin {
    @Unique private BarrelBlockEntity artisanal$blockEntity;
    
    @Inject(method = "<init>", remap = false, at = @At("RETURN"))
    public void constructor$Inject(InventoryBlockEntity<?> blockEntity, CallbackInfo info) {
        if (blockEntity instanceof BarrelBlockEntity barrelBlockEntity) {
            this.artisanal$blockEntity = barrelBlockEntity;
        }
        else {
            this.artisanal$blockEntity = null;
        }
    }
    
    @Unique
    public BarrelBlockEntity artisanal$getBlockEntity() {
        return artisanal$blockEntity;
    }
}
