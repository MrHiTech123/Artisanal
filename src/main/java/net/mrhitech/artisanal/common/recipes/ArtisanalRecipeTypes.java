package net.mrhitech.artisanal.common.recipes;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalRecipeTypes {
    public static final DeferredRegister<RecipeType<?>> RECIPE_TYPES = DeferredRegister.create(Registries.RECIPE_TYPE, Artisanal.MOD_ID);
    
    public static final RegistryObject<RecipeType<DistilleryRecipe>> DISTILLERY = register("distillery");
    public static final RegistryObject<RecipeType<JuicingRecipe>> JUICING = register("juicing");
    
    public static void register(IEventBus bus) {
        RECIPE_TYPES.register(bus);
    }
    
    private static <R extends Recipe<?>> RegistryObject<RecipeType<R>> register(String name)
    {
        return RECIPE_TYPES.register(name, () -> new RecipeType<>() {
            @Override
            public String toString()
            {
                return name;
            }
        });
    }
    
}
