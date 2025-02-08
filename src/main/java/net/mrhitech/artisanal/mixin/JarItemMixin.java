package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.items.JarItem;
import net.minecraft.world.item.ItemStack;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Overwrite;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(value = JarItem.class, remap = false)
public class JarItemMixin {
    /**
     * @author MrHiTech
     * @reason Jars can get dirty
     */
    @Overwrite
    public ItemStack getCraftingRemainingItem(ItemStack stack) {
        return new ItemStack(ArtisanalItems.DIRTY_JAR.get());
    }
}
