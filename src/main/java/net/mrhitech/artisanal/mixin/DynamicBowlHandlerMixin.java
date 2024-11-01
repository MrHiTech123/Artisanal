package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.capabilities.food.DynamicBowlHandler;
import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Overwrite;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;

@Mixin(value = DynamicBowlHandler.class, remap = false)
public class DynamicBowlHandlerMixin{
    @Shadow
    private final ItemStack stack;
    @Shadow
    private ItemStack bowl;
    
    public DynamicBowlHandlerMixin() {
        stack = new ItemStack(ArtisanalItems.DIRTY_JAR.get(), 1);
    }
    
    /**
     * @author hi
     * @reason dumb stupid
     */
    @Overwrite
    public ItemStack getBowl() {
        
        
        
        if (this.stack.getItem().equals(ArtisanalItems.DIRTY_BOWL.get())) {
            return this.bowl;
        }
        else if (this.bowl.isEmpty()) {
            return ItemStack.EMPTY;
        }
        else {
            ItemStack toReturn = new ItemStack(ArtisanalItems.DIRTY_BOWL.get());
            toReturn.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
                if (cap instanceof DynamicBowlHandler bowlHandler) {
                    bowlHandler.setBowl(this.bowl);
                }
            });
            
            return toReturn;
            
        }
    }
}
