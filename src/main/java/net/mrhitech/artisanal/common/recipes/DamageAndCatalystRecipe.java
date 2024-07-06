package net.mrhitech.artisanal.common.recipes;

import net.dries007.tfc.common.recipes.DamageInputsCraftingRecipe;
import net.dries007.tfc.common.recipes.IRecipeDelegate;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.Container;
import net.minecraft.world.inventory.CraftingContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraftforge.common.crafting.IShapedRecipe;
import net.mrhitech.artisanal.common.ArtisanalTags;
import org.jetbrains.annotations.NotNull;

public abstract class DamageAndCatalystRecipe<R extends Recipe<CraftingContainer>> extends DamageInputsCraftingRecipe {
    
    protected DamageAndCatalystRecipe (ResourceLocation id, R recipe)
    {
        super(id, recipe);
    }
    
    
    protected static boolean isUnbreakable(@NotNull ItemStack stack) {
        if (Helpers.isItem(stack.getItem(), ArtisanalTags.ITEMS.CRAFTING_CATALYSTS)) {
            return true;
        }
        else {
            return DamageInputsCraftingRecipe.isUnbreakable(stack);
        }
    }
    
    @Override
    public NonNullList<ItemStack> getRemainingItems(CraftingContainer inv)
    {
        NonNullList<ItemStack> items = NonNullList.withSize(inv.getContainerSize(), ItemStack.EMPTY);
        for (int i = 0; i < items.size(); ++i)
        {
            ItemStack stack = inv.getItem(i);
            if (stack.isDamageableItem())
            {
                items.set(i, Helpers.damageCraftingItem(stack, 1).copy());
            }
            else if (isUnbreakable(stack)) // unbreakable items are not damageable, but should still be able to be used in crafting
            {
                items.set(i, stack.copy());
            }
            else if (stack.hasCraftingRemainingItem())
            {
                items.set(i, stack.getCraftingRemainingItem());
            }
        }
        return items;
    }
    
    public static class Shapeless extends DamageAndCatalystRecipe<Recipe<CraftingContainer>>
    {
        public Shapeless(ResourceLocation id, Recipe<CraftingContainer> recipe)
        {
            super(id, recipe);
        }
        
        @Override
        public RecipeSerializer<?> getSerializer()
        {
            return ArtisanalRecipeSerializers.DAMAGE_AND_CATALYST_SHAPELESS.get();
        }
    }
    

}
