package net.mrhitech.artisanal.common.recipes;

import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.core.registries.Registries;
import net.mrhitech.artisanal.Artisanal;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Supplier;

public class ArtisanalRecipeSerializers {
    public static final DeferredRegister<RecipeSerializer<?>> RECIPE_SERIALIZERS = DeferredRegister.create(Registries.RECIPE_SERIALIZER, Artisanal.MOD_ID);
    
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> SCALABLE_POT = register("scalable_pot", ScalablePotRecipe.Serializer::new);
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> DAMAGE_AND_CATALYST_SHAPELESS = register("damage_and_catalyst_shapeless_crafting", () -> DelegateRecipe.Serializer.shapeless(DamageAndCatalystRecipe.Shapeless::new));
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> DISTILLERY = register("distillery", DistilleryRecipe.Serializer::new);
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> JUICING_RECIPE = register("juicing", () -> new SimpleFluidRecipe.Serializer<>(JuicingRecipe::new));
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> ONLY_IF_FLUX_MAKES_LIMEWATER_BARREL = register("only_if_flux_makes_limewater_instant_barrel", OnlyIfFluxMakesLimewaterBarrelRecipe.Serializer::new);
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> SPECIFIC_NO_REMAINDER_DAMAGE_SHAPED = register("specific_no_remainder_damage_shaped", SpecificNoRemainderDamageShapedRecipe.Serializer::new);
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> SPECIFIC_NO_REMAINDER_SHAPED = register("specific_no_remainder_shaped", SpecificNoRemainderShapedRecipe.Serializer::new);
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> SPECIFIC_NO_REMAINDER_SHAPELESS = register("specific_no_remainder_shapeless", SpecificNoRemainderShapelessRecipe.Serializer::new);
    public static final DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> SPRAYS_ACID_IN_EYES_INSTANT_BARREL_RECIPE = register("sprays_acid_in_eyes_instant_barrel", SpraysAcidInEyesInstantBarrelRecipe.Serializer::new);
    
    public static <I extends RecipeSerializer<?>> DeferredHolder<RecipeSerializer<?>, RecipeSerializer<?>> register(String name, Supplier<? extends I> sup) {
        return RECIPE_SERIALIZERS.register(name, sup);
    }
    
    public static void register(IEventBus bus) {
        RECIPE_SERIALIZERS.register(bus);
    }
    
    
}
