package net.mrhitech.artisanal.common;

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
    LEMON_JUICE(-6525),
    ORANGE_JUICE(-28671),
    SCREWDRIVER(-1198481),
    PETROLEUM(-16777216);
    
    private final int color;
    private final String id;
    
    
    Waterlikes(int color) {
        this.id = this.name().toLowerCase(Locale.ROOT);
        this.color = color;
    }
    
    public String getId() {
        return id;
    }
    
    public int getColor() {
        return color;
    }
    
}
