package net.mrhitech.artisanal.compat.patchouli.component;

import net.dries007.tfc.compat.patchouli.component.RecipeComponent;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraftforge.fluids.FluidStack;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeTypes;
import net.mrhitech.artisanal.common.recipes.DistilleryRecipe;
import org.jetbrains.annotations.NotNull;
import vazkii.patchouli.api.IComponentRenderContext;

public class DistilleryRecipeComponent extends RecipeComponent<DistilleryRecipe> {
    
    public static final ResourceLocation TEXTURE = new ResourceLocation(Artisanal.MOD_ID, "textures/gui/book/icons.png");
    public static final int SIZE_OF_STACK_SLOT = 28;
    
    private static final int START_INPUT_SLOT_X_COORD = 3;
    private static final int START_OUTPUT_SLOT_X_COORD = 71;
    private static final int START_SLOT_Y_COORD = 5;
    
    
    @Override
    public void render(GuiGraphics graphics, IComponentRenderContext context, float partialTicks, int mouseX, int mouseY) {
        if (recipe == null) return;
        
        renderSetup(graphics);
        
        graphics.blit(TEXTURE, 0, 0, 2, 168, 122, 218 - 166, 256, 256);
        
        context.renderIngredient(graphics, START_INPUT_SLOT_X_COORD, START_SLOT_Y_COORD + SIZE_OF_STACK_SLOT, mouseX, mouseY, recipe.getIngredientItem().ingredient());
        renderFluidStacks(context, graphics, START_INPUT_SLOT_X_COORD + SIZE_OF_STACK_SLOT, START_SLOT_Y_COORD + SIZE_OF_STACK_SLOT, mouseX, mouseY, unpackFluidStackIngredient(recipe.getIngredientFluid()));
        
        ItemStack resultItem = recipe.getResultItem().orElse(ItemStack.EMPTY);
        FluidStack resultFluid = recipe.getResultFluid().orElse(FluidStack.EMPTY);
        ItemStack leftoverItem = recipe.getLeftoverItem().orElse(ItemStack.EMPTY);
        FluidStack leftoverFluid = recipe.getLeftoverFluid().orElse(FluidStack.EMPTY);
        
        
        if (!resultItem.isEmpty()) {
            context.renderItemStack(graphics, START_OUTPUT_SLOT_X_COORD, START_SLOT_Y_COORD, mouseX, mouseY, resultItem);
        }
        
        if (!resultFluid.isEmpty()) {
            renderFluidStack(context, graphics, START_OUTPUT_SLOT_X_COORD + SIZE_OF_STACK_SLOT, START_SLOT_Y_COORD, mouseX, mouseY, resultFluid);
        }
        
        if (!leftoverItem.isEmpty()) {
            context.renderItemStack(graphics, START_OUTPUT_SLOT_X_COORD, START_SLOT_Y_COORD + SIZE_OF_STACK_SLOT, mouseX, mouseY, leftoverItem);
        }
        
        if (!leftoverFluid.isEmpty()) {
            renderFluidStack(context, graphics, START_OUTPUT_SLOT_X_COORD + SIZE_OF_STACK_SLOT, START_SLOT_Y_COORD + SIZE_OF_STACK_SLOT, mouseX, mouseY, leftoverFluid);
        }
        
        graphics.pose().popPose();
        
    }
    
    @Override
    protected @NotNull RecipeType<DistilleryRecipe> getRecipeType() {
        return ArtisanalRecipeTypes.DISTILLERY.get();
    }
}
