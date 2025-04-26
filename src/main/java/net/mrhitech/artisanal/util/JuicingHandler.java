package net.mrhitech.artisanal.util;

import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.recipes.inventory.ItemStackInventory;
import net.dries007.tfc.config.TFCConfig;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.fluids.capability.IFluidHandler;
import net.minecraftforge.items.ItemStackHandler;
import net.mrhitech.artisanal.common.recipes.JuicingRecipe;
import net.mrhitech.artisanal.util.advancements.ArtisanalAdvancements;

import java.util.List;


public class JuicingHandler {
    public static void handle(ItemStackHandler inventory, Level level, BlockPos pos) {
        ItemStack inputStack = ((ItemStackHandler)inventory).getStackInSlot(1);
        
        ItemStackInventory wrapper = new ItemStackInventory(inputStack);
        JuicingRecipe recipe = JuicingRecipe.getRecipe(level, wrapper);
        
        if (recipe != null && recipe.matches(wrapper, level)) {
            FluidStack outputStack = recipe.getResultFluid();
            level.getBlockEntity(pos.below(), TFCBlockEntities.BARREL.get()).ifPresent(barrel -> {
                Direction fluidOriginDirection;
                if (TFCConfig.SERVER.barrelEnableAutomation.get()) {
                    fluidOriginDirection = Direction.UP;
                }
                else {
                    fluidOriginDirection = null;
                }
                barrel.getCapability(Capabilities.FLUID, fluidOriginDirection).ifPresent(cap -> {
                    cap.fill(outputStack, IFluidHandler.FluidAction.EXECUTE);
                    if (barrel.canModify()) {
                        Helpers.playSound(level, barrel.getBlockPos(), SoundEvents.BREWING_STAND_BREW);
                    }
                    
                    List<Player> playersGettingAdvancement = ArtisanalHelpers.playersNear(level, pos, 10);
                    
                    for (Player player : playersGettingAdvancement) {
                        if (player instanceof ServerPlayer serverPlayer) {
                            ArtisanalAdvancements.JUICING.trigger(serverPlayer);
                        }
                    }
                });
            });
        }
        
        
    }
}
