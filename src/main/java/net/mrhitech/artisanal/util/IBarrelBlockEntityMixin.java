package net.mrhitech.artisanal.util;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;

import java.util.concurrent.atomic.AtomicBoolean;

public interface IBarrelBlockEntityMixin {
    void enableDrumFluids();
    void requireDrumFluids();
    BarrelBlockEntity.BarrelInventory getInventory();
}
