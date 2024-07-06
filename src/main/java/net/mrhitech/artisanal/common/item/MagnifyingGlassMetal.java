package net.mrhitech.artisanal.common.item;

import java.util.Locale;

public enum MagnifyingGlassMetal {
    BISMUTH(),
    BRASS(),
    GOLD(),
    ROSE_GOLD(),
    SILVER(),
    STERLING_SILVER(),
    TIN();
    
    
    MagnifyingGlassMetal() {
        
    }
    
    public String getSerializedName() {
        return this.name().toLowerCase(Locale.ROOT);
    }
}
