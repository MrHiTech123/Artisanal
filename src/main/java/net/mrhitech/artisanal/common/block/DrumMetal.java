package net.mrhitech.artisanal.common.block;

import net.dries007.tfc.util.Metal;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.material.Fluid;
import net.mrhitech.artisanal.common.ArtisanalTags;

public enum DrumMetal {
    BISMUTH_BRONZE(Metal.Default.BISMUTH_BRONZE, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    BLACK_BRONZE(Metal.Default.BLACK_BRONZE, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    BRONZE(Metal.Default.BRONZE, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    STEEL(Metal.Default.STEEL, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    RED_STEEL(Metal.Default.RED_STEEL, ArtisanalTags.FLUIDS.USABLE_IN_DRUM),
    BLUE_STEEL(Metal.Default.BLUE_STEEL, ArtisanalTags.FLUIDS.USABLE_IN_LAVA_DRUM);
    
    private final Metal.Default metal;
    private final TagKey<Fluid> usableFluids;
    
    public Metal.Default getMetal() {
        return metal;
    }
    
    public TagKey<Fluid> getUsableFluids() {
        return usableFluids;
    }
    
    DrumMetal(Metal.Default metal, TagKey<Fluid> usableFluids) {
        this.metal = metal;
        this.usableFluids = usableFluids;
    };
}
