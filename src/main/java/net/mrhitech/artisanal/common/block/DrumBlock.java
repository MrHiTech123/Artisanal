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
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraftforge.common.ForgeConfig;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.mixin.BarrelInventoryAccessor;
import net.mrhitech.artisanal.util.IBarrelBlockEntityAccessor;
import org.jetbrains.annotations.Nullable;

import java.util.concurrent.atomic.AtomicBoolean;


public class DrumBlock extends BarrelBlock {
    public DrumBlock(ExtendedProperties properties) {
        super(properties);
        System.out.println("Here");
        
    }
    
    @Override
    public @Nullable BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        BlockEntity entity = super.newBlockEntity(pos, state);
        if (entity instanceof BarrelBlockEntity barrel) {
            modifyBlockEntity(barrel);
        }
        return entity;
    }
    
    private static void modifyBlockEntity(BarrelBlockEntity barrel) {
        ((BarrelInventoryAccessor)((IBarrelBlockEntityAccessor)barrel).getInventory()).getTank().setValidator(
                    fluid -> Helpers.isFluid(fluid.getFluid(), ArtisanalTags.FLUIDS.USABLE_IN_DRUM));
    }
}
