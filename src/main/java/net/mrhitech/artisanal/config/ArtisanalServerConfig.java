package net.mrhitech.artisanal.config;


import net.neoforged.neoforge.common.ModConfigSpec;

public class ArtisanalServerConfig {
    public static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();
    public static final ModConfigSpec SPEC;
    
    public static final ModConfigSpec.ConfigValue<Boolean> GENERIC_ANIMAL_FAT;
    public static final ModConfigSpec.ConfigValue<Boolean> FLUX_MAKES_LIMEWATER;
    
    static {
        BUILDER.push("Artisanal Configs");
        
        GENERIC_ANIMAL_FAT = BUILDER.comment(" If true, animals drop generic animal fat items,\n and non-generic animal fats can be crafted into their generic ones.\n If false, animals drop their species-specific animal fats.").define("genericAnimalFat", false);
        FLUX_MAKES_LIMEWATER = BUILDER.comment(" If true, enables the barrel recipe in which Flux can be\n mixed with water to make Slaked Lime").define("fluxMakesLimewater", false);
        
        SPEC = BUILDER.build();
        
    }
    
}
