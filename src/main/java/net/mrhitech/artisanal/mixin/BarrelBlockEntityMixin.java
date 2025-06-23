package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blockentities.BarrelInventoryCallback;
import net.dries007.tfc.common.blockentities.TickableInventoryBlockEntity;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.calendar.ICalendarTickable;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluid;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.common.block.DrumBlock;
import net.mrhitech.artisanal.util.IBarrelBlockEntityMixin;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.util.concurrent.atomic.AtomicBoolean;


@Mixin(BarrelBlockEntity.class)
public abstract class BarrelBlockEntityMixin extends TickableInventoryBlockEntity<BarrelBlockEntity.BarrelInventory> implements ICalendarTickable, BarrelInventoryCallback, IBarrelBlockEntityMixin {
    protected BarrelBlockEntityMixin(BlockEntityType<?> type, BlockPos pos, BlockState state, InventoryFactory<BarrelBlockEntity.BarrelInventory> inventory, Component defaultName) {
        super(type, pos, state, inventory, defaultName);
    }
    
    public BarrelBlockEntity.BarrelInventory getInventory() {
        return inventory;
    }
    
    private boolean isDrum = false;

    public void makeDrum() {
        isDrum = true;
        enableDrumFluids();
    }
    
    public void enableDrumFluids() {
        final TagKey<Fluid> usableFluids;
        if (getBlockState().getBlock() instanceof DrumBlock drumBlock) {
            usableFluids = drumBlock.getUsableFluids();
        }
        else {
            usableFluids = TFCTags.Fluids.USABLE_IN_BARREL;
        }
        
        ((BarrelInventoryAccessor)inventory).getTank().setValidator(
                fluid -> Helpers.isFluid(fluid.getFluid(), usableFluids));
    }
    
    @Inject(method = "<init>", remap = false, at = @At("RETURN"))
    public void constructor$Inject(BlockPos pos, BlockState state, CallbackInfo info) {
        if (getBlockState().getBlock() instanceof DrumBlock) {
            enableDrumFluids();
        }
    }
    
    @Inject(method = "loadAdditional", remap = false, at = @At("RETURN"))
    public void loadAdditional$Inject(CompoundTag nbt, CallbackInfo info) {
        if (getBlockState().getBlock() instanceof DrumBlock) {
            enableDrumFluids();
        }
    }
    
    
}
