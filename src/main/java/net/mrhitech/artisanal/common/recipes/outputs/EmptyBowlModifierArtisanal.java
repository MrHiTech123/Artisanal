package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.capabilities.food.DynamicBowlHandler;
import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.capabilities.food.IFood;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

public enum EmptyBowlModifierArtisanal implements ItemStackModifier.SingleInstance<EmptyBowlModifierArtisanal> {
    INSTANCE;
    
    private ItemStack oneStep(ItemStack input) {
        return net.dries007.tfc.common.recipes.outputs.EmptyBowlModifier.INSTANCE.apply(ItemStack.EMPTY, input);
    }
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        if (input.getItem() == Items.AIR) {
            return new ItemStack(Items.BOWL);
        }
        
        boolean currentlyDynamicBowl = true;
        
        while (currentlyDynamicBowl) {
            input = oneStep(input);
            
            if (!(FoodCapability.get(input) instanceof DynamicBowlHandler)) {
                currentlyDynamicBowl = false;
            }
            
        }
        
        return input;
    }
    
    public EmptyBowlModifierArtisanal instance() {
        return INSTANCE;
    }
}
