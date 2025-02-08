package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.capabilities.InventoryFluidTank;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

@Mixin(BarrelBlockEntity.BarrelInventory.class)
public interface BarrelInventoryAccessor {
    @Accessor(remap = false) InventoryFluidTank getTank();
}
