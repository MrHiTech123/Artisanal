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
    
    @Overwrite
    public ItemStack getBowl() {
        if (this.stack.getItem().equals(ArtisanalItems.DIRTY_BOWL.get())) {
            return this.bowl;
        }
        else {
            ItemStack toReturn = new ItemStack(ArtisanalItems.DIRTY_BOWL.get());
            System.out.println("Inside the function");
            toReturn.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
                System.out.println("Inside the capability");
                if (cap instanceof DynamicBowlHandler bowlHandler) {
                    System.out.println(this.bowl.getItem());
                    bowlHandler.setBowl(this.bowl);
                    System.out.println(this.bowl.getItem());
                    System.out.println("Bowl handler's bowl is:");
                    System.out.println(bowlHandler.getBowl());
                }
            });
            
            return toReturn;
            
        }
    }
}
