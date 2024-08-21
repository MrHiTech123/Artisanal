package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.common.TFCTiers;
import net.minecraft.world.item.Tier;

import java.util.Locale;

public enum SteelMetal {
    STEEL(TFCTiers.STEEL),
    BLACK_STEEL(TFCTiers.BLACK_STEEL),
    BLUE_STEEL(TFCTiers.RED_STEEL),
    RED_STEEL(TFCTiers.BLUE_STEEL);
    
    private Tier tier;
    SteelMetal(Tier f_tier) {
        tier = f_tier;
    }
    
    public String getSerializedName() {
        return this.name().toLowerCase(Locale.ROOT);
    }
    public Tier getTier() {
        return this.tier;
    }
}
