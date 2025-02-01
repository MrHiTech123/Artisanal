package net.mrhitech.artisanal.config;

import net.minecraftforge.common.ForgeConfigSpec;

public class ArtisanalServerConfig {
    public static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();
    public static final ForgeConfigSpec SPEC;
    
    public static final ForgeConfigSpec.ConfigValue<Boolean> GENERIC_ANIMAL_FAT;
    
    static {
        BUILDER.push("Artisanal Configs");
        
        GENERIC_ANIMAL_FAT = BUILDER.comment("If true, animals drop generic animal fat items, and non-generic animal fats can be crafted into their generic ones. If false, animals drop their species-specific animal fats.").define("genericAnimalFat", false);
        
        SPEC = BUILDER.build();
        
    }
    
}
