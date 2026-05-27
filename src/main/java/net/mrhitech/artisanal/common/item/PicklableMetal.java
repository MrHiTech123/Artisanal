package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.util.Metal;

public enum PicklableMetal {
    WROUGHT_IRON(Metal.WROUGHT_IRON),
    STEEL(Metal.STEEL);
    
    private Metal metal;
    
    public Metal getMetal() {
        return metal;
    }
    
    PicklableMetal(Metal f_metal) {
        metal = f_metal;
    }
    
}
