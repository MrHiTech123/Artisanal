package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifiers;
import net.minecraft.resources.ResourceLocation;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalItemStackModifiers {
    
    
    
    public static void registerItemStackModifierTypes() {
        register("add_food_to_can", AddFoodToCanModifier.INSTANCE);
    }
    
    private static void register(String name, ItemStackModifier.Serializer<?> serializer) {
        ItemStackModifiers.register(new ResourceLocation(Artisanal.MOD_ID, name), serializer);
    }
    
    
}
