package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.capabilities.food.DynamicBowlHandler;
import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodData;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.util.Helpers;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.Tag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import java.util.ArrayList;
import java.util.List;

public enum CopyDynamicFoodNeverExpiresModifier implements ItemStackModifier.SingleInstance<CopyDynamicFoodNeverExpiresModifier> {
    INSTANCE;
    
    @Override
    public ItemStack apply(ItemStack stack, ItemStack input)
    {

        stack.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
            if (cap instanceof FoodHandler.Dynamic outHandler)
            {
                input.getCapability(FoodCapability.CAPABILITY).ifPresent(inputCap -> {
                    if (inputCap instanceof FoodHandler.Dynamic inHandler)
                    {
                        FoodData data = inHandler.getData();
                        data = new FoodData(data.hunger(), data.water(), data.saturation(), data.grain(), data.fruit(), data.vegetables(), data.protein(), data.dairy(), 0);
                        outHandler.setFood(data);
                        outHandler.setNonDecaying();
                        outHandler.setIngredients(inHandler.getIngredients());
                    }
                    if (cap instanceof DynamicBowlHandler outBowl && inputCap instanceof DynamicBowlHandler inBowl)
                    {
                        ItemStack newBowl = inBowl.getBowl();
                        if (newBowl.isEmpty())
                        {
                            newBowl = new ItemStack(Items.BOWL);
                        }
                        outBowl.setBowl(newBowl);
                    }
                });
            }
        });
        
        
        return stack;
    }
    
    @Override
    public CopyDynamicFoodNeverExpiresModifier instance()
    {
        return INSTANCE;
    }
}
