package net.mrhitech.artisanal.common.blockentities;

import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity;
import net.dries007.tfc.common.blockentities.InventoryBlockEntity;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.devices.FirepitBlock;
import net.dries007.tfc.common.capabilities.*;
import net.dries007.tfc.common.capabilities.heat.HeatCapability;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.common.items.TFCItems;
import net.dries007.tfc.common.recipes.PotRecipe;
import net.dries007.tfc.common.recipes.RecipeHelpers;
import net.dries007.tfc.common.recipes.ingredients.ItemStackIngredient;
import net.dries007.tfc.common.recipes.inventory.EmptyInventory;
import net.dries007.tfc.config.TFCConfig;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.common.capabilities.Capability;
import net.minecraftforge.common.util.INBTSerializable;
import net.minecraftforge.common.util.LazyOptional;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.fluids.capability.IFluidHandler;
import net.minecraftforge.fluids.capability.templates.FluidTank;
import net.minecraftforge.items.IItemHandlerModifiable;
import net.minecraftforge.items.ItemStackHandler;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.recipes.DistilleryRecipe;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.Objects;
import java.util.Optional;

public class DistilleryBlockEntity extends AbstractFirepitBlockEntity<DistilleryBlockEntity.DistilleryInventory> {
    
    private static final Component NAME = Component.translatable(Artisanal.MOD_ID + ".block_entity.distillery");
    
    public static final int SLOT_INPUT_ITEM = 4;
    public static final int SLOT_OUTPUT_ITEM = 5;
    public static final int TANK_INPUT_FLUID = 0;
    public static final int TANK_OUTPUT_FLUID = 1;
    public static final int PRE_BOIL_TIME = 100;
    
    private final SidedHandler.Builder<IFluidHandler> sidedFluidInventory;
    @Nullable private DistilleryRecipe cachedRecipe;
    private int boilingTicks, preBoilingTicks;
    
    public DistilleryBlockEntity(BlockPos pPos, BlockState pBlockState) {
        super(ArtisanalBlockEntities.DISTILLERY.get(), pPos, pBlockState, DistilleryInventory::new, NAME);
        
        cachedRecipe = null;
        boilingTicks = 0;
        preBoilingTicks = 0;
        sidedFluidInventory = new SidedHandler.Builder<>(inventory);
        syncableData.add(() -> boilingTicks, value -> boilingTicks = value);
        
        if (TFCConfig.SERVER.firePitEnableAutomation.get()) {
            sidedInventory
                .on(new PartialItemHandler(inventory).insert(SLOT_FUEL_INPUT).extract(4, 5), Direction.Plane.HORIZONTAL)
                .on(new PartialItemHandler(inventory).insert(4, 5), Direction.UP);

            sidedFluidInventory
                .on(new PartialFluidHandler(inventory).insert(), Direction.UP)
                .on(new PartialFluidHandler(inventory).extract(), Direction.Plane.HORIZONTAL);
        }
        
    }
    
    @Override
    public void loadAdditional(CompoundTag nbt) {
        boilingTicks = nbt.getInt("boilingTicks");
        preBoilingTicks = nbt.getInt("preBoilingTicks");
        
        super.loadAdditional(nbt);
    }
    
    @Override
    public void saveAdditional(CompoundTag nbt) {
        nbt.putInt("boilingTicks", boilingTicks);
        nbt.putInt("preBoilingTicks", preBoilingTicks);
        
        super.saveAdditional(nbt);
    }
    
    @Override
    public boolean isItemValid(int slot, ItemStack stack) {
        if (slot < SLOT_INPUT_ITEM) {
            return super.isItemValid(slot, stack);
        }
        else {
            return true;
        }
    }
    
    @Override
    public int getSlotStackLimit(int slot) {
        return super.getSlotStackLimit(slot);
    }
    
    private void removeIngredients() {
        RecipeHelpers.setCraftingInput(inventory, SLOT_INPUT_ITEM, SLOT_OUTPUT_ITEM);
        
        RecipeHelpers.clearCraftingInput();
        
        inventory.inputBowlFluidTank.setFluid(FluidStack.EMPTY);
        inventory.outputBowlFluidTank.setFluid(FluidStack.EMPTY);
        
        inventory.setStackInSlot(SLOT_INPUT_ITEM, inventory.getStackInSlot(SLOT_INPUT_ITEM).getCraftingRemainingItem());
        
    }
    
    private void putOutputInInventory(ItemStack itemStackProviderInput) {
        DistilleryRecipe recipe = cachedRecipe;
        if (recipe == null) return;
        
        recipe.getLeftoverItem(itemStackProviderInput).ifPresent(leftoverItem -> {
            inventory.setStackInSlot(SLOT_INPUT_ITEM, leftoverItem);
        });
        
        recipe.getResultItem(itemStackProviderInput).ifPresent(resultItem -> {
            inventory.setStackInSlot(SLOT_OUTPUT_ITEM, resultItem);
        });
        
        recipe.getLeftoverFluid().ifPresent(leftoverFluid -> {
            inventory.setFluidInTank(TANK_INPUT_FLUID, leftoverFluid);
        });
        
        recipe.getResultFluid().ifPresent(resultFluid -> {
            inventory.setFluidInTank(TANK_OUTPUT_FLUID, resultFluid);
        });
    }
    
    private void resetRecipeProgress() {
        cachedRecipe = null;
        boilingTicks = 0;
        preBoilingTicks = 0;
        updateCachedRecipe();
        markForSync();
    }
    
    private void finishCooking() {
        ItemStack input = inventory.getStackInSlot(SLOT_INPUT_ITEM);
        removeIngredients();
        putOutputInInventory(input);
        resetRecipeProgress();
    }
    
    @Override
    protected void handleCooking() {
        if (isBoiling()) {
            if (preBoilingTicks < PRE_BOIL_TIME) {
                ++preBoilingTicks;
                return;
            }
            assert cachedRecipe != null;
            if (boilingTicks < cachedRecipe.getDuration()) {
                ++boilingTicks;
                if (boilingTicks == 1) {
                    updateCachedRecipe();
                    markForSync();
                }
            }
            else {
                finishCooking();
            }
        }
        else if (boilingTicks > 0) {
            coolInstantly();
        }
    }
    
    @Override
    public void onCalendarUpdate(long ticks) {
        assert level != null;
        
        if (level.getBlockState(worldPosition).getValue(FirepitBlock.LIT)) {
            final HeatCapability.Remainder remainder = HeatCapability.consumeFuelForTicks(ticks, inventory, burnTicks, burnTemperature, SLOT_FUEL_CONSUME, SLOT_FUEL_INPUT);
            
            burnTicks = remainder.burnTicks();
            burnTemperature = remainder.burnTemperature();
            needsSlotUpdate = true;
            
            if (remainder.ticks() > 0) // Consumed all fuel, so extinguish and cool instantly
            {
                if (isBoiling())
                {
                    assert cachedRecipe != null;
                    final long ticksUsedWhileBurning = ticks - remainder.ticks();
                    if (ticksUsedWhileBurning > cachedRecipe.getDuration() - boilingTicks)
                    {
                        boilingTicks = cachedRecipe.getDuration();
                        handleCooking();
                    }
                }
                extinguish(level.getBlockState(worldPosition));
                coolInstantly();
            }
            else
            {
                if (isBoiling())
                {
                    boilingTicks += ticks;
                }
            }
        }
    }
    
    @Override
    protected void coolInstantly() {
        boilingTicks = 0;
        preBoilingTicks = 0;
        markForSync();
    }
    
    public FluidTank getOutputTank() {
        return inventory.outputBowlFluidTank;
    }
    
    @Override
    protected void updateCachedRecipe() {
        assert level != null;
        cachedRecipe = DistilleryRecipe.fromInventory(level, inventory).orElse(null);
    }
    
    public boolean isBoiling() {
        return cachedRecipe != null && cachedRecipe.isHotEnough(temperature);
    }
    
    public boolean hasRecipeStarted() {
        return isBoiling() && preBoilingTicks >= PRE_BOIL_TIME;
    }
    
    public boolean shouldRenderAsBoiling() {
        return boilingTicks > 0;
    }
    
    public int getBoilingTicks() {
        return boilingTicks;
    }
    
    @Override
    public @NotNull <T> LazyOptional<T> getCapability(@NotNull Capability<T> cap, @Nullable Direction side) {
        if (cap == Capabilities.FLUID) {
            return sidedFluidInventory.getSidedHandler(side).cast();
        }
        
        return super.getCapability(cap, side);
    }
    
    public static class DistilleryInventory implements EmptyInventory, DelegateItemHandler, DelegateFluidHandler, INBTSerializable<CompoundTag> {
        private final DistilleryBlockEntity distillery;
        private final ItemStackHandler inventory;
        private final FluidTank inputBowlFluidTank;
        private final FluidTank outputBowlFluidTank;
        
        private static final int amountOfInventorySlots = 6;
        
        public DistilleryInventory(InventoryBlockEntity<DistilleryInventory> distillery) {
            this.distillery = (DistilleryBlockEntity) distillery;
            this.inventory = new InventoryItemHandler(distillery, amountOfInventorySlots);
            this.inputBowlFluidTank = new FluidTank(FluidHelpers.BUCKET_VOLUME, fluid -> Helpers.isFluid(fluid.getFluid(), TFCTags.Fluids.USABLE_IN_POT));
            this.outputBowlFluidTank = new FluidTank(FluidHelpers.BUCKET_VOLUME, fluid -> Helpers.isFluid(fluid.getFluid(), TFCTags.Fluids.USABLE_IN_POT));
        }
        
        @NotNull
        @Override
        public ItemStack extractItem(int slot, int amount, boolean simulate) {
            return inventory.extractItem(slot, amount, simulate);
        }
        
        public boolean matchItemIngredient(ItemStackIngredient required, int slot) {
            return required.test(inventory.getStackInSlot(slot));
        }
        
        
        
        @Override
        public @NotNull FluidStack getFluidInTank(int tank) {
            return switch (tank) {
                case TANK_INPUT_FLUID -> inputBowlFluidTank.getFluid();
                case TANK_OUTPUT_FLUID -> outputBowlFluidTank.getFluid();
                default -> throw new IllegalArgumentException(
                        "Error: expected tank to be 0 (TANK_INPUT_FLUID) or 1 (TANK_OUTPUT_FLUID), was " + tank
                );
            };
        }
        
        public void setFluidInTank(int tank, FluidStack stack) {
            FluidTank tankToSet = switch (tank) {
                case TANK_INPUT_FLUID -> inputBowlFluidTank;
                case TANK_OUTPUT_FLUID -> outputBowlFluidTank;
                default -> throw new IllegalArgumentException("Error: expected tank to be 0 (TANK_INPUT_FLUID) or 1 (TANK_OUTPUT_FLUID), was " + tank);
            };
            
            tankToSet.setFluid(stack);
        }
        
        @Override
        public @NotNull IFluidHandler getFluidHandler() {
            return inputBowlFluidTank;
        }
        
        @Override
        public IItemHandlerModifiable getItemHandler() {
            return inventory;
        }
        
        @Override
        public CompoundTag serializeNBT() {
            CompoundTag toReturn = new CompoundTag();
            
            toReturn.put("inventory", inventory.serializeNBT());
            toReturn.put("inputTank", inputBowlFluidTank.writeToNBT(new CompoundTag()));
            toReturn.put("outputTank", outputBowlFluidTank.writeToNBT(new CompoundTag()));
            
            return toReturn;
            
        }
        
        @Override
        public void deserializeNBT(CompoundTag nbt) {
            inventory.deserializeNBT(nbt.getCompound("inventory"));
            inputBowlFluidTank.readFromNBT(nbt.getCompound("inputTank"));
            outputBowlFluidTank.readFromNBT(nbt.getCompound("outputTank"));
        }
    }
    
}
