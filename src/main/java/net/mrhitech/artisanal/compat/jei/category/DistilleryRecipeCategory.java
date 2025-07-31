package net.mrhitech.artisanal.compat.jei.category;

import mezz.jei.api.gui.builder.IRecipeLayoutBuilder;
import mezz.jei.api.gui.builder.IRecipeSlotBuilder;
import mezz.jei.api.gui.drawable.IDrawable;
import mezz.jei.api.gui.ingredient.IRecipeSlotsView;
import mezz.jei.api.helpers.IGuiHelper;
import mezz.jei.api.recipe.IFocusGroup;
import mezz.jei.api.recipe.RecipeIngredientRole;
import mezz.jei.api.recipe.RecipeType;
import net.dries007.tfc.common.recipes.PotRecipe;
import net.dries007.tfc.common.recipes.ingredients.FluidStackIngredient;
import net.dries007.tfc.common.recipes.ingredients.ItemStackIngredient;
import net.dries007.tfc.compat.jei.JEIIntegration;
import net.dries007.tfc.compat.jei.category.BaseRecipeCategory;
import net.dries007.tfc.util.Metal;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraftforge.fluids.FluidStack;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.common.recipes.DistilleryRecipe;

import java.util.List;
import java.util.Optional;

public class DistilleryRecipeCategory extends BaseRecipeCategory<DistilleryRecipe> {
    public DistilleryRecipeCategory(RecipeType<DistilleryRecipe> recipeType, IGuiHelper guiHelper) {
        super(recipeType, guiHelper, guiHelper.createBlankDrawable(121, 41), new ItemStack(ArtisanalItems.DISTILLERIES.get(Metal.Default.WROUGHT_IRON).get()));
    }
    
    protected void setInitialIngredients(IRecipeLayoutBuilder builder, DistilleryRecipe recipe) {
        int i = 0;
        
        ItemStackIngredient itemIngredient = recipe.getIngredientItem();
        FluidStackIngredient fluidStackIngredient = recipe.getIngredientFluid();
        
        IRecipeSlotBuilder inputItemSlot = builder.addSlot(RecipeIngredientRole.INPUT, 6, 26);
        inputItemSlot.addIngredients(itemIngredient.ingredient());
        inputItemSlot.setBackground(slot, -1, -1);
        
        IRecipeSlotBuilder inputFluidSlot = builder.addSlot(RecipeIngredientRole.INPUT, 26, 26);
        inputFluidSlot.addIngredients(JEIIntegration.FLUID_STACK, collapse(fluidStackIngredient));
        inputFluidSlot.setFluidRenderer(1, false, 16, 16);
        inputFluidSlot.setBackground(slot, -1, -1);
        
    }
    
    @Override
    public void setRecipe(IRecipeLayoutBuilder builder, DistilleryRecipe recipe, IFocusGroup focusGroup) {
        
        ItemStackIngredient itemStackIngredient = recipe.getIngredientItem();
        FluidStackIngredient fluidStackIngredient = recipe.getIngredientFluid();
        Optional<ItemStack> resultItem = recipe.getResultItem();
        Optional<FluidStack> resultFluid = recipe.getResultFluid();
        Optional<ItemStack> leftoverItem = recipe.getLeftoverItem();
        Optional<FluidStack> leftoverFluid = recipe.getLeftoverFluid();
        
        if (itemStackIngredient.count() != 0) {
            IRecipeSlotBuilder inputItem = builder.addSlot(RecipeIngredientRole.INPUT, 1, 21);
            inputItem.addIngredients(itemStackIngredient.ingredient());
            inputItem.setBackground(slot, -1, -1);
        }
        
        if (fluidStackIngredient.amount() != 0) {
            IRecipeSlotBuilder inputFluidSlot = builder.addSlot(RecipeIngredientRole.INPUT, 21, 21);
            inputFluidSlot.addIngredients(JEIIntegration.FLUID_STACK, collapse(fluidStackIngredient));
            inputFluidSlot.setFluidRenderer(1, false, 16, 16);
            inputFluidSlot.setBackground(slot, -1, -1);
        }
        
        resultItem.ifPresent(stack -> {
            if (stack.isEmpty()) return;
            IRecipeSlotBuilder resultSlot = builder.addSlot(RecipeIngredientRole.OUTPUT, 81, 1);
            resultSlot.addItemStacks(List.of(stack));
            resultSlot.setBackground(slot, -1, -1);
        });
        
        resultFluid.ifPresent(stack -> {
            if (stack.isEmpty()) return;
            IRecipeSlotBuilder resultSlot = builder.addSlot(RecipeIngredientRole.OUTPUT, 101, 1);
            resultSlot.addIngredient(JEIIntegration.FLUID_STACK, stack);
            resultSlot.setFluidRenderer(1, false, 16, 16);
            resultSlot.setBackground(slot, -1, -1);
        });
        
        leftoverItem.ifPresent(stack -> {
            if (stack.isEmpty()) return;
            IRecipeSlotBuilder leftoverSlot = builder.addSlot(RecipeIngredientRole.OUTPUT, 81, 21);
            leftoverSlot.addItemStacks(List.of(stack));
            leftoverSlot.setBackground(slot, -1, -1);
        });
        
        leftoverFluid.ifPresent(stack -> {
            if (stack.isEmpty()) return;
            IRecipeSlotBuilder resultSlot = builder.addSlot(RecipeIngredientRole.OUTPUT, 101, 21);
            resultSlot.addIngredient(JEIIntegration.FLUID_STACK, stack);
            resultSlot.setFluidRenderer(1, false, 16, 16);
            resultSlot.setBackground(slot, -1, -1);
        });
    }
    
    @Override
    public void draw(DistilleryRecipe recipe, IRecipeSlotsView recipeSlotsView, GuiGraphics guiGraphics, double mouseX, double mouseY) {
        arrow.draw(guiGraphics,  51, 10);
        arrowAnimated.draw(guiGraphics, 51, 10);
    }
}
