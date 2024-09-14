package net.mrhitech.artisanal.compat.jei.category;

import mezz.jei.api.gui.builder.IRecipeLayoutBuilder;
import mezz.jei.api.gui.builder.IRecipeSlotBuilder;
import mezz.jei.api.gui.ingredient.IRecipeSlotsView;
import mezz.jei.api.helpers.IGuiHelper;
import mezz.jei.api.recipe.IFocusGroup;
import mezz.jei.api.recipe.RecipeIngredientRole;
import mezz.jei.api.recipe.RecipeType;
import net.dries007.tfc.compat.jei.JEIIntegration;
import net.dries007.tfc.compat.jei.category.BaseRecipeCategory;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.core.RegistryAccess;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.mrhitech.artisanal.common.recipes.SimpleFluidRecipe;

import javax.annotation.Nullable;
import java.util.List;
import java.util.logging.Level;

public abstract class SimpleFluidRecipeCategory<T extends SimpleFluidRecipe> extends BaseRecipeCategory<T>
{
    public SimpleFluidRecipeCategory(RecipeType<T> type, IGuiHelper helper, ItemStack icon)
    {
        super(type, helper, helper.createBlankDrawable(98, 26), icon);
    }
    
    @Override
    public void setRecipe(IRecipeLayoutBuilder builder, T recipe, IFocusGroup focuses)
    {
        final IRecipeSlotBuilder inputSlot = builder.addSlot(RecipeIngredientRole.INPUT, 6, 5);
        inputSlot.setBackground(slot, -1, -1);
        IRecipeSlotBuilder toolSlot = null;
        if (getToolTag() != null)
        {
            toolSlot = builder.addSlot(RecipeIngredientRole.CATALYST, 26, 5);
        }
        IRecipeSlotBuilder outputSlot = builder.addSlot(RecipeIngredientRole.OUTPUT, 76, 5);
        
        final Ingredient ingredient = recipe.getIngredient();
        final List<ItemStack> inputList = List.of(ingredient.getItems());
        inputSlot.addIngredients(JEIIntegration.ITEM_STACK, inputList);
        
        if (toolSlot != null)
        {
            toolSlot.addIngredients(Ingredient.of(getToolTag()));
            toolSlot.setBackground(slot, -1, -1);
        }
        
        outputSlot.addFluidStack(recipe.getResultFluid().getFluid(), recipe.getResultFluid().getAmount());
        outputSlot.setBackground(slot, -1, -1);
        
        if (!addItemsToOutputSlot(recipe, outputSlot, inputList))
        {
            builder.createFocusLink(inputSlot, outputSlot);
        }
    }
    
    @Override
    public void draw(T recipe, IRecipeSlotsView recipeSlots, GuiGraphics stack, double mouseX, double mouseY)
    {
        arrow.draw(stack, getToolTag() == null ? 36 : 48, 5);
        arrowAnimated.draw(stack, getToolTag() == null ? 36 : 48, 5);
    }
    
    protected boolean addItemsToOutputSlot(T recipe, IRecipeSlotBuilder output, List<ItemStack> inputs)
    {
        return false;
    }
    
    @Nullable
    protected abstract TagKey<Item> getToolTag();
}
