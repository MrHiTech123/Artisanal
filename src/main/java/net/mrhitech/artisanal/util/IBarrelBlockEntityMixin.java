package net.mrhitech.artisanal.util;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;

public interface IBarrelBlockEntityMixin {
    void enableDrumFluids();
    
    boolean getCheckedIfDrum();
    void setCheckedIfDrum(boolean f_checkedIfDrum);
    BarrelBlockEntity.BarrelInventory getInventory();
}
