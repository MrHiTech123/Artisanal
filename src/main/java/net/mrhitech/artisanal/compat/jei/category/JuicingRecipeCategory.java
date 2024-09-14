package net.mrhitech.artisanal.compat.jei.category;

import mezz.jei.api.helpers.IGuiHelper;
import mezz.jei.api.recipe.RecipeType;
import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.common.recipes.JuicingRecipe;

public class JuicingRecipeCategory extends SimpleFluidRecipeCategory<JuicingRecipe>
{
    public JuicingRecipeCategory(RecipeType<JuicingRecipe> type, IGuiHelper helper)
    {
        super(type, helper, new ItemStack(TFCBlocks.QUERN.get()));
    }
    
    @Override
    protected TagKey<Item> getToolTag()
    {
        return TFCTags.Items.HANDSTONE;
    }
}
