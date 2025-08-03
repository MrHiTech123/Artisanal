package net.mrhitech.artisanal.common.fluids;

import net.minecraft.resources.ResourceLocation;
import net.mrhitech.artisanal.Artisanal;
import org.joml.Vector3f;

import java.util.Locale;
import java.awt.Color;

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
    SOUR_CRUDE_OIL(-14671871, new ResourceLocation(Artisanal.MOD_ID, "textures/misc/under/sour_crude_oil.png"), 1, 3, false),
    SWEET_CRUDE_OIL(-5395071, new ResourceLocation(Artisanal.MOD_ID, "textures/misc/under/sweet_crude_oil.png"), 1, 12, true),
    KEROSENE(-71),
    SULFURIC_ACID(-2240864),
    MERCURY(-8421504);
    
    private final int colorNum;
    private final String id;
    private final ResourceLocation underneathTexture;
    private final float shaderFogStart;
    private final float shaderFogEnd;
    private final boolean transparent;
    
    Waterlikes(int colorNum) {
        this(colorNum, null, 1, 6, true);
    }
    
    Waterlikes(int colorNum, ResourceLocation underneathTexture, float shaderFogStart, float shaderFogEnd, boolean transparent) {
        this.id = this.name().toLowerCase(Locale.ROOT);
        this.colorNum = colorNum;
        this.underneathTexture = underneathTexture;
        this.shaderFogStart = shaderFogStart;
        this.shaderFogEnd = shaderFogEnd;
        this.transparent = transparent;
    }
    
    public String getId() {
        return id;
    }
    
    public int getColorNum() {
        return colorNum;
    }
    
    public Vector3f getColor() {
        int positiveColor = 0xFFFFFF + colorNum;
        
        float red = (float)((positiveColor & 0xFF0000) >> 16);
        float green = (float)((positiveColor & 0x00FF00) >> 8);
        float blue = (float)(positiveColor & 0x0000FF);
        
        return new Vector3f(red / 255, green / 255, blue / 255);
    }
    
    public ResourceLocation getUnderneathTexture() {
        return underneathTexture;
    }
    
    public float getShaderFogStart() {
        return shaderFogStart;
    }
    
    public float getShaderFogEnd() {
        return shaderFogEnd;
    }
    
    public boolean isTransparent() {
        return transparent;
    }
    
}
