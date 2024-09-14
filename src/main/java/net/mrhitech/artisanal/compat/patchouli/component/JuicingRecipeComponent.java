package net.mrhitech.artisanal.compat.patchouli.component;

import net.minecraft.world.item.crafting.RecipeType;
import net.mrhitech.artisanal.compat.patchouli.component.InputFluidOutputComponent;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeTypes;
import net.mrhitech.artisanal.common.recipes.JuicingRecipe;

public class JuicingRecipeComponent extends InputFluidOutputComponent<JuicingRecipe> {
    protected RecipeType<JuicingRecipe> getRecipeType() {
        return ArtisanalRecipeTypes.JUICING.get();
    }
}
