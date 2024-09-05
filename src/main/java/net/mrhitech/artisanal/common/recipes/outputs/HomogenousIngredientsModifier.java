package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraftforge.registries.ForgeRegistries;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public enum HomogenousIngredientsModifier implements ItemStackModifier.SingleInstance<HomogenousIngredientsModifier> {
    INSTANCE;
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        AtomicInteger numOfDiffIngredients = new AtomicInteger(-1);
        
        stack.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
            if (cap instanceof FoodHandler.Dynamic dynamicHandler) {
                numOfDiffIngredients.set(dynamicHandler.getIngredients().size());
            }
        
        });
        
        if (numOfDiffIngredients.get() > 1){
            return new ItemStack(Items.AIR);
        }
        else {
            return stack;
        }
        
        
        
        
        
    }
    
    public HomogenousIngredientsModifier instance() {
        return INSTANCE;
    }
}
