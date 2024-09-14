/*
 * Licensed under the EUPL, Version 1.2.
 * You may obtain a copy of the Licence at:
 * https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
 */

package net.mrhitech.artisanal.compat.patchouli.component;
import net.dries007.tfc.compat.patchouli.component.RecipeComponent;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.Recipe;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraftforge.fluids.FluidStack;
import net.mrhitech.artisanal.common.recipes.SimpleFluidRecipe;
import vazkii.patchouli.api.IComponentRenderContext;

import net.dries007.tfc.compat.patchouli.PatchouliIntegration;

public abstract class InputFluidOutputComponent<T extends SimpleFluidRecipe> extends RecipeComponent<T>
{
    @Override
    public void render(GuiGraphics graphics, IComponentRenderContext context, float partialTicks, int mouseX, int mouseY)
    {
        if (recipe == null) return;

        renderSetup(graphics);

        graphics.blit(PatchouliIntegration.TEXTURE, 9, 0, 0, 90, 98, 26, 256, 256);

        context.renderIngredient(graphics, 14, 5, mouseX, mouseY, recipe.getIngredient());
        renderFluidStack(context, graphics, 86, 5, mouseX, mouseY, recipe.getResultFluid());
        graphics.pose().popPose();



    }

    // these methods take a recipe parameter to avoid the nullability of recipe
}