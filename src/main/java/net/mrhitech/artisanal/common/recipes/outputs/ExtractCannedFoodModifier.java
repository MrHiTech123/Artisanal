package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.util.Helpers;
import net.minecraft.nbt.Tag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.ArrayList;
import java.util.List;

public enum ExtractCannedFoodModifier implements ItemStackModifier.SingleInstance<ExtractCannedFoodModifier> {
    INSTANCE;
    
    
    
    
    
    
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        if (input.getTag() == null) {
            return new ItemStack(Items.AIR);
        }
        
        
        List<ItemStack> ingredients = new ArrayList<>();
        
        
        Helpers.readItemStacksFromNbt(ingredients, input.getTag().getList("ingredients", Tag.TAG_COMPOUND));
        
        ItemStack to_return = (ingredients.get(0));
        
        
        return to_return;
        
    
    
    }
    
    
    @Override
    public ExtractCannedFoodModifier instance()
    {
        return INSTANCE;
    }
}
