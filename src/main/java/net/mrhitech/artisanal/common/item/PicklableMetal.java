package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.util.Metal;

public enum PicklableMetal {
    WROUGHT_IRON(Metal.Default.WROUGHT_IRON),
    STEEL(Metal.Default.STEEL);
    
    private Metal.Default metal;
    
    public Metal.Default getMetal() {
        return metal;
    }
    
    PicklableMetal(Metal.Default f_metal) {
        metal = f_metal;
    }
    
}
