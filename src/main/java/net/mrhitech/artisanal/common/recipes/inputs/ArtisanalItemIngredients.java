package net.mrhitech.artisanal.common.recipes.inputs;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraftforge.common.crafting.CraftingHelper;
import net.minecraftforge.common.crafting.IIngredientSerializer;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalItemIngredients {
    
    public static void registerIngredientTypes() {
        register("universal_ingredient", UniversalIngredient.Serializer.INSTANCE);
    }
    
    private static <T extends Ingredient> void register(String name, IIngredientSerializer<T> serializer)
    {
        CraftingHelper.register(new ResourceLocation(Artisanal.MOD_ID, name), serializer);
    }
}
