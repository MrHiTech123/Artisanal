package net.mrhitech.artisanal.util;

import net.dries007.tfc.client.TFCSounds;
import net.dries007.tfc.common.TFCArmorMaterials;
import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blockentities.InventoryBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.common.recipes.inventory.ItemStackInventory;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraftforge.common.util.INBTSerializable;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.fluids.capability.IFluidHandler;
import net.minecraftforge.items.IItemHandlerModifiable;
import net.mrhitech.artisanal.common.recipes.JuicingRecipe;
 


public class JuicingHandler {
    public static void handle(ItemStack inputStack, Level level, BlockPos pos) {
        ItemStackInventory wrapper = new ItemStackInventory(inputStack);
        JuicingRecipe recipe = JuicingRecipe.getRecipe(level, wrapper);
        if (recipe != null && recipe.matches(wrapper, level)) {
            FluidStack outputStack = recipe.getResultFluid();
            level.getBlockEntity(pos.below(), TFCBlockEntities.BARREL.get()).ifPresent(barrel -> {
                barrel.getCapability(Capabilities.FLUID, Direction.UP).ifPresent(cap -> {
                    cap.fill(outputStack, IFluidHandler.FluidAction.EXECUTE);
                    Helpers.playSound(level, barrel.getBlockPos(), SoundEvents.BREWING_STAND_BREW);
                });
            });
        }
        
        
    }
}
