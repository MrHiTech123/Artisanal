package net.mrhitech.artisanal.common.block;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.devices.BarrelBlock;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.mixin.BarrelInventoryAccessor;
import net.mrhitech.artisanal.util.IBarrelBlockEntityAccessor;

import java.util.concurrent.atomic.AtomicBoolean;


public class DrumBlock extends BarrelBlock {
    private final AtomicBoolean blockEntityAlreadyModified;
    public DrumBlock(ExtendedProperties properties) {
        super(properties);
        blockEntityAlreadyModified = new AtomicBoolean(false);
        System.out.println("Here");
    }
    
    // @Override
    // public void onPlace(BlockState pState, Level pLevel, BlockPos pPos, BlockState pOldState, boolean pIsMoving) {
    //     super.onPlace(pState, pLevel, pPos, pOldState, pIsMoving);
    //     if (!blockEntityAlreadyModified.get()) {
    //         pLevel.getBlockEntity(pPos, TFCBlockEntities.BARREL.get()).ifPresent(barrel -> {
    //             ((BarrelInventoryAccessor)((IBarrelBlockEntityAccessor)barrel).getInventory()).getTank().setValidator(
    //                     fluid -> Helpers.isFluid(fluid.getFluid(), ArtisanalTags.FLUIDS.USABLE_IN_DRUM)
    //             );
    //             blockEntityAlreadyModified.set(true);
    //         });
    //     }
    // }
}
