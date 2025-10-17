package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.common.ForgeHooks;
import net.mrhitech.artisanal.util.SulfuricAcidEffects;

public enum BlindCraftingPlayerModifier implements ItemStackModifier.SingleInstance<BlindCraftingPlayerModifier> {
    INSTANCE;
    
    @Override
    public BlindCraftingPlayerModifier instance() {
        return INSTANCE;
    }
    
    @Override
    public ItemStack apply(ItemStack stack, ItemStack input) {
        Player player = ForgeHooks.getCraftingPlayer();
        if (player != null) {
            SulfuricAcidEffects.sprayAcidAtPlayerEyes(player);
        }
        return stack;
    }
}
