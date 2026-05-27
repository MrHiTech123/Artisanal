package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.util.Metal;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.Tier;

import java.util.Locale;

public enum SteelMetal {
    STEEL(Metal.STEEL),
    BLACK_STEEL(Metal.BLACK_STEEL),
    BLUE_STEEL(Metal.RED_STEEL),
    RED_STEEL(Metal.BLUE_STEEL);
    
    private Metal metal;
    SteelMetal(Metal f_metal) {
        metal = f_metal;
    }
    
    public String getSerializedName() {
        return this.name().toLowerCase(Locale.ROOT);
    }
    public Tier getTier() {
        return this.metal.toolTier();
    }
    
    public Rarity getRarity() {
        return this.metal.rarity();
    }
}

