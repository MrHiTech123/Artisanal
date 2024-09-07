package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.capabilities.food.DynamicBowlHandler;
import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.IFood;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.world.item.ItemStack;

public enum EmptyBowlModifierArtisanal implements ItemStackModifier.SingleInstance<EmptyBowlModifierArtisanal> {
    INSTANCE;
    
    private ItemStack oneStep(ItemStack input) {
        return net.dries007.tfc.common.recipes.outputs.EmptyBowlModifier.INSTANCE.apply(ItemStack.EMPTY, input);
    }
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        
        boolean currentlyDynamicBowl = true;
        
        while (currentlyDynamicBowl) {
            IFood cap = FoodCapability.get(input);
            if (cap instanceof DynamicBowlHandler bowlHandler) {
                input = bowlHandler.getBowl();
            }
            else {
                currentlyDynamicBowl = false;
            }
            
        }
        
        return input;
    }
    
    public EmptyBowlModifierArtisanal instance() {
        return INSTANCE;
    }
}
