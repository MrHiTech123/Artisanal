package net.mrhitech.artisanal.common.block;

import net.dries007.tfc.util.Metal;

public enum DrumMetal {
    BISMUTH_BRONZE(Metal.Default.BISMUTH_BRONZE),
    BLACK_BRONZE(Metal.Default.BLACK_BRONZE),
    BRONZE(Metal.Default.BRONZE),
    STEEL(Metal.Default.STEEL);
    
    private Metal.Default metal;
    
    public Metal.Default getMetal() {
        return metal;
    }
    
    DrumMetal(Metal.Default f_metal) {
        metal = f_metal;
    };
}
