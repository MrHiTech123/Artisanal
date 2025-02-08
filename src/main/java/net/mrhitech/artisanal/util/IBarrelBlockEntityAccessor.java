package net.mrhitech.artisanal.util;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;

public interface IBarrelBlockEntityAccessor {
    BarrelBlockEntity.BarrelInventory getInventory();
}
