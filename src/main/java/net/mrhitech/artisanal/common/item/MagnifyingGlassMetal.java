package net.mrhitech.artisanal.common.item;

import java.util.Locale;

public enum MagnifyingGlassMetal {
    BRASS();
    
    MagnifyingGlassMetal() {
        
    }
    
    public String getSerializedName() {
        return this.name().toLowerCase(Locale.ROOT);
    }
}
