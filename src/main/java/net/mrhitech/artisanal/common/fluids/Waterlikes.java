package net.mrhitech.artisanal.common.fluids;

import net.dries007.tfc.common.fluids.TFCFluids;
import net.dries007.tfc.util.Helpers;
import net.minecraft.resources.ResourceLocation;
import net.mrhitech.artisanal.Artisanal;

import java.util.Locale;

public enum Waterlikes {
    
    LARD(-8514),
    SCHMALTZ(-2831206),
    SOAP(-2831206), // TODO: Change color
    SOAPY_WATER(-2303550),
    SUGARCANE_JUICE(-6730172),
    FILTERED_SUGARCANE_JUICE(-31886),
    ALKALIZED_SUGARCANE_JUICE(-4684915),
    CLARIFIED_SUGARCANE_JUICE(-18491),
    MOLASSES(-13562873),
    CONDENSED_MILK(-1251140),
    CONDENSED_GOAT_MILK(-921644),
    CONDENSED_YAK_MILK(-1381679),
    APPLE_JUICE(-11263),
    CARROT_JUICE(-1670359),
    LEMON_JUICE(-6525),
    DILUTED_LEMON_JUICE(-3390),
    ORANGE_JUICE(-28671),
    PEACH_JUICE(-2978449),
    PINEAPPLE_JUICE(-4213136),
    TOMATO_JUICE(-1035741),
    SCREWDRIVER(-1198481),
    SOUR_CRUDE_OIL(-14671871, new ResourceLocation(Artisanal.MOD_ID, "textures/misc/under/sour_crude_oil.png")),
    SWEET_CRUDE_OIL(-2237024, new ResourceLocation(Artisanal.MOD_ID, "textures/misc/under/sweet_crude_oil.png")),
    KEROSENE(-71),
    SULFURIC_ACID(-2240864),
    MERCURY(-8421504);
    
    private final int color;
    private final String id;
    private final ResourceLocation underneathTexture;
    
    Waterlikes(int color) {
        this(color, null);
    }
    
    Waterlikes(int color, ResourceLocation underneathTexture) {
        this.id = this.name().toLowerCase(Locale.ROOT);
        this.color = color;
        this.underneathTexture = underneathTexture;
    }
    
    public String getId() {
        return id;
    }
    
    public int getColor() {
        return color;
    }
    
    public ResourceLocation getUnderneathTexture() {
        return underneathTexture;
    }
    
}
