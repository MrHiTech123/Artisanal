package net.mrhitech.artisanal.common.recipes.outputs;

import com.google.common.collect.BiMap;
import com.google.common.collect.HashBiMap;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifiers;
import net.minecraft.resources.ResourceLocation;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalItemStackModifiers {
    public static void registerItemStackModifiers() {
        register("cap_heat", CapHeatModifier.Serializer.INSTANCE);
        register("copy_dynamic_food", CopyDynamicFoodModifier.INSTANCE);
        register("copy_dynamic_food_never_expires", CopyDynamicFoodNeverExpiresModifier.INSTANCE);
        register("empty_bowl", EmptyBowlModifierArtisanal.INSTANCE);
        register("extract_canned_food", ExtractCannedFoodModifier.INSTANCE);
        register("homogenous_ingredients", HomogenousIngredientsModifier.INSTANCE);
        register("inherit_decay", InheritDecayModifier.Serializer.INSTANCE);
        register("modify_fluid", OutputFluidItemIngredientModifier.Serializer.CHANGE_FLUID_NBT);
        register("only_if_generic_animal_fat", OnlyIfGenericAnimalFatModifier.INSTANCE);
        register("remove_butter", RemoveButterModifier.INSTANCE);
    }
    
    
    private static void register(String name, ItemStackModifier.Serializer<?> serializer)
    {
        ItemStackModifiers.register(new ResourceLocation(Artisanal.MOD_ID, name), serializer);
    }
}
