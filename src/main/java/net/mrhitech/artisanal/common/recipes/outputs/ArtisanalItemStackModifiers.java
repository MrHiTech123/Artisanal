package net.mrhitech.artisanal.common.recipes.outputs;

import com.google.common.collect.BiMap;
import com.google.common.collect.HashBiMap;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifiers;
import net.minecraft.resources.ResourceLocation;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalItemStackModifiers {
    private static final BiMap<ResourceLocation, ItemStackModifier.Serializer<?>> REGISTRY = HashBiMap.create();
    
    public static void registerItemStackModifiers() {
        register("copy_dynamic_food", CopyDynamicFoodModifier.INSTANCE);
        register("copy_dynamic_food_never_expires", CopyDynamicFoodNeverExpiresModifier.INSTANCE);
        register("extract_canned_food", ExtractCannedFoodModifier.INSTANCE);
        register("homogenous_ingredients", HomogenousIngredientsModifier.INSTANCE);
    }
    
    
    private static void register(String name, ItemStackModifier.Serializer<?> serializer)
    {
        ItemStackModifiers.register(new ResourceLocation(Artisanal.MOD_ID, name), serializer);
    }
}