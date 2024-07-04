package net.mrhitech.artisanal.common.recipes;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalRecipeSerializers {
    public static final DeferredRegister<RecipeSerializer<?>> RECIPE_SERIALIZERS = DeferredRegister.create(Registries.RECIPE_SERIALIZER, Artisanal.MOD_ID);
    
    public static final RegistryObject<RecipeSerializer<?>> SCALABLE_POT = RECIPE_SERIALIZERS.register("scalable_pot", ScalablePotRecipe.Serializer::new);
    
    public static void register(IEventBus bus) {
        RECIPE_SERIALIZERS.register(bus);
    }
    
    
}
