package net.mrhitech.artisanal.common.recipes.outputs;

import com.google.common.collect.BiMap;
import com.google.common.collect.HashBiMap;
import com.mojang.serialization.MapCodec;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifierType;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifiers;
import net.dries007.tfc.util.registry.RegistryHolder;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.resources.ResourceLocation;
import net.mrhitech.artisanal.Artisanal;
import net.neoforged.neoforge.registries.DeferredHolder;

public class ArtisanalItemStackModifiers {
    public static void registerItemStackModifiers() {
        register("blind_crafting_player", BlindCraftingPlayerModifier.INSTANCE);
        register("cap_heat", CapHeatModifier.Serializer.INSTANCE);
        register("copy_dynamic_food", CopyDynamicFoodModifier.INSTANCE);
        register("copy_dynamic_food_never_expires", CopyDynamicFoodNeverExpiresModifier.INSTANCE);
        register("empty_bowl", EmptyBowlModifierArtisanal.INSTANCE);
        register("extract_canned_food", ExtractCannedFoodModifier.INSTANCE);
        register("homogenous_ingredients", HomogenousIngredientsModifier.INSTANCE);
        register("inherit_decay", InheritDecayModifier.Serializer.INSTANCE);
        register("modify_fluid", OutputFluidItemIngredientModifier.Serializer.CHANGE_FLUID_NBT);
        register("only_if_generic_animal_fat", OnlyIfGenericAnimalFatModifier.INSTANCE);
        register("remove_butter", RemoveButterModifier.INSTANCE.instance());
    }
    
    
    
    private static <T extends ItemStackModifier> Id<T> register(String name, T singleInstance)
    {
        return new Id<>(ItemStackModifiers.TYPES.register(name, () -> new ItemStackModifierType<>(MapCodec.unit(singleInstance), StreamCodec.unit(singleInstance))));
    }

    private static <T extends ItemStackModifier> Id<T> register(String name, MapCodec<T> codec, StreamCodec<? super RegistryFriendlyByteBuf, T> streamCodec)
    {
        return new Id<>(ItemStackModifiers.TYPES.register(name, () -> new ItemStackModifierType<>(codec, streamCodec.cast())));
    }

    record Id<T extends ItemStackModifier>(DeferredHolder<ItemStackModifierType<?>, ItemStackModifierType<T>> holder)
        implements RegistryHolder<ItemStackModifierType<?>, ItemStackModifierType<T>> {}
}
