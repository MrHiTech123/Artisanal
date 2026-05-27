package net.mrhitech.artisanal.common.block.devices;

import net.dries007.tfc.util.Metal;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.material.Fluid;
import net.mrhitech.artisanal.common.ArtisanalTags;

public enum DrumMetal {
    BISMUTH_BRONZE(Metal.BISMUTH_BRONZE, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    BLACK_BRONZE(Metal.BLACK_BRONZE, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    BRONZE(Metal.BRONZE, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    STEEL(Metal.STEEL, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    RED_STEEL(Metal.RED_STEEL, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    BLUE_STEEL(Metal.BLUE_STEEL, ArtisanalTags.FLUIDS.USABLE_IN_LAVA_DRUM);
    
    private final Metal metal;
    private final TagKey<Fluid> usableFluids;
    
    public Metal getMetal() {
        return metal;
    }
    
    public TagKey<Fluid> getUsableFluids() {
        return usableFluids;
    }
    
    DrumMetal(Metal metal, TagKey<Fluid> usableFluids) {
        this.metal = metal;
        this.usableFluids = usableFluids;
    };
}
