package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;

public enum ExtractCannedFoodModifier implements ItemStackModifier.SingleInstance<ExtractCannedFoodModifier> {
    INSTANCE;
    
    
    
    
    
    
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        AtomicReference<List<ItemStack>> ingredients = new AtomicReference<>(new ArrayList<>());
        AtomicBoolean isRotten = new AtomicBoolean(false);
        
        input.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
            if (cap instanceof FoodHandler.Dynamic outHandler) {
                ingredients.set(outHandler.getIngredients());
                isRotten.set(outHandler.isRotten());
            }
        });
        
        if (ingredients.get().isEmpty()) {
            return new ItemStack(ArtisanalItems.DEBUG_WHATEVER_FOOD_WAS_INSIDE_THE_CAN.get());
        }
        
        ItemStack output = ingredients.get().get(0);
        output = new ItemStack(output.getItem(), output.getCount());
        
        // If the opened can is rotten (only possible in the case of sealed-but-not-sterilized cans), so is the output food.
        if (isRotten.get()) {
            output.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
                cap.setCreationDate(1);
            });
        }
        
        return output;
        
    
    
    }
    
    
    @Override
    public ExtractCannedFoodModifier instance()
    {
        return INSTANCE;
    }
}
