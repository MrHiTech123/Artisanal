package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.config.ArtisanalServerConfig;

public enum OnlyIfGenericAnimalFatModifier implements ItemStackModifier.SingleInstance<OnlyIfGenericAnimalFatModifier> {
    INSTANCE;
    
    public OnlyIfGenericAnimalFatModifier instance() {
        return INSTANCE;
    }
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        if (!ArtisanalServerConfig.SPEC.isLoaded()) {
            return stack;
        }
        
        if (!ArtisanalServerConfig.GENERIC_ANIMAL_FAT.get()) {
            return new ItemStack(Items.AIR);
        }
        return stack;
    }
    
    
    
}
