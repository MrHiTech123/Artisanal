package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

public enum ExtractCannedFoodModifier implements ItemStackModifier.SingleInstance<ExtractCannedFoodModifier> {
    INSTANCE;
    
    
    
    
    
    
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        AtomicReference<List<ItemStack>> ingredients = new AtomicReference<>(new ArrayList<>());
        
        input.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
            if (cap instanceof FoodHandler.Dynamic outHandler) {
                ingredients.set(outHandler.getIngredients());
            }
        });
        
        if (ingredients.get().isEmpty()) {
            return new ItemStack(Items.COOKED_BEEF);
        }
        
        ItemStack output = ingredients.get().get(0);
        output = new ItemStack(output.getItem(), output.getCount());
        
        
        return output;
        
    
    
    }
    
    
    @Override
    public ExtractCannedFoodModifier instance()
    {
        return INSTANCE;
    }
}
