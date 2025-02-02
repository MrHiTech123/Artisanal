package net.mrhitech.artisanal.common.recipes;

import net.dries007.tfc.common.recipes.BarrelRecipe;
import net.dries007.tfc.common.recipes.DelegateRecipe;
import net.dries007.tfc.common.recipes.InstantBarrelRecipe;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;

import java.util.function.Supplier;

public class ArtisanalRecipeSerializers {
    public static final DeferredRegister<RecipeSerializer<?>> RECIPE_SERIALIZERS = DeferredRegister.create(Registries.RECIPE_SERIALIZER, Artisanal.MOD_ID);
    
    public static final RegistryObject<RecipeSerializer<?>> SCALABLE_POT = RECIPE_SERIALIZERS.register("scalable_pot", ScalablePotRecipe.Serializer::new);
    public static final RegistryObject<RecipeSerializer<?>> DAMAGE_AND_CATALYST_SHAPELESS = RECIPE_SERIALIZERS.register("damage_and_catalyst_shapeless_crafting", () -> DelegateRecipe.Serializer.shapeless(DamageAndCatalystRecipe.Shapeless::new));
    public static final RegistryObject<RecipeSerializer<?>> JUICING_RECIPE = RECIPE_SERIALIZERS.register("juicing", () -> new SimpleFluidRecipe.Serializer<>(JuicingRecipe::new));
    public static final RegistryObject<RecipeSerializer<?>> ONLY_IF_FLUX_MAKES_LIMEWATER_BARREL = RECIPE_SERIALIZERS.register("only_if_flux_makes_limewater_instant_barrel", OnlyIfFluxMakesLimewaterBarrelRecipe.Serializer::new);
    
    
    public static void register(IEventBus bus) {
        RECIPE_SERIALIZERS.register(bus);
    }
    
    
}
