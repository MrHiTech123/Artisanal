package net.mrhitech.artisanal.common.recipes;

import net.dries007.tfc.util.registry.RegistryHolder;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.item.crafting.RecipeType;
import net.mrhitech.artisanal.Artisanal;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ArtisanalRecipeTypes {
    public static final DeferredRegister<RecipeType<?>> RECIPE_TYPES = DeferredRegister.create(Registries.RECIPE_TYPE, Artisanal.MOD_ID);
    
    public static final Id<DistilleryRecipe> DISTILLERY = register("distillery");
    public static final Id<JuicingRecipe> JUICING = register("juicing");
    
    
    
    private static <R extends Recipe<?>> Id<R> register(String name)
    {
        return new Id<>(RECIPE_TYPES.register(name, () -> new RecipeType<>() {
            @Override
            public String toString()
            {
                return name;
            }
        }));
    }

    public record Id<T extends Recipe<?>>(DeferredHolder<RecipeType<?>, RecipeType<T>> holder)
        implements RegistryHolder<RecipeType<?>, RecipeType<T>> {}
    
}
