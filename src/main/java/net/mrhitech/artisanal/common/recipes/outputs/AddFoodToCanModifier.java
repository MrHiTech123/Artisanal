package net.mrhitech.artisanal.common.recipes.outputs;

import com.google.common.collect.Lists;
import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.recipes.RecipeHelpers;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.nbt.Tag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.ArrayList;

public enum AddFoodToCanModifier implements ItemStackModifier.SingleInstance<AddFoodToCanModifier> {
    
    INSTANCE;
    
    @Override
    public ItemStack apply(ItemStack stack, ItemStack input) {
        ArrayList<ItemStack> allIngredients = Lists.newArrayList(RecipeHelpers.getCraftingInput());
        
        for (ItemStack ingredient : allIngredients) {
            System.out.println(ingredient.getItem());
            
        }
        
        
        return stack;
        
    }
    
    public AddFoodToCanModifier instance() {
        return this;
    }
    
    
}
