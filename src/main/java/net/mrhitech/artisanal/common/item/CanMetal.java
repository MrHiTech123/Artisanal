package net.mrhitech.artisanal.common.item;

import java.util.Locale;

public enum CanMetal {
    TIN,
    STAINLESS_STEEL;
    
    String getSerializedName() {
        return name().toLowerCase(Locale.ROOT);
    }
}
