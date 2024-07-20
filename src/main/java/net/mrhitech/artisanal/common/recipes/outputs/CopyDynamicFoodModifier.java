// Code copied with gratitude from EERussianGuy's FirmaLife mod, licensed under MIT license.
// https://github.com/eerussianguy/firmalife/tree/1.20.x
package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.util.Tooltips;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

import net.dries007.tfc.common.capabilities.food.DynamicBowlHandler;
import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;


public enum CopyDynamicFoodModifier implements ItemStackModifier.SingleInstance<CopyDynamicFoodModifier>
{
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
                        outHandler.setFood(inHandler.getData());
                        outHandler.setCreationDate(FoodCapability.getRoundedCreationDate());
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
    public CopyDynamicFoodModifier instance()
    {
        return INSTANCE;
    }
}