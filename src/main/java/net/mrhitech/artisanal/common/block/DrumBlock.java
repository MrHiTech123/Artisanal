package net.mrhitech.artisanal.common.block;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.devices.BarrelBlock;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraftforge.items.ItemHandlerHelper;
import net.mrhitech.artisanal.common.blockentity.ArtisanalBlockEntities;
import org.jetbrains.annotations.NotNull;

public class DrumBlock extends BarrelBlock {
    
    public DrumBlock(ExtendedProperties properties) {
        super(properties);
    }
    
    public static void toggleSeal(Level level, BlockPos pos, BlockState state)
    {
        level.getBlockEntity(pos, ArtisanalBlockEntities.DRUM.get()).ifPresent(barrel -> {
            final boolean previousSealed = state.getValue(SEALED);
            level.setBlockAndUpdate(pos, state.setValue(SEALED, !previousSealed));
            
            if (previousSealed)
            {
                barrel.onUnseal();
            }
            else
            {
                barrel.onSeal();
            }
        });
    }
    
    @Override
    @SuppressWarnings("deprecation")
    public @NotNull InteractionResult use(BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hit)
    {
        final BarrelBlockEntity barrel = level.getBlockEntity(pos, ArtisanalBlockEntities.DRUM.get()).orElse(null);
        if (barrel != null)
        {
            final ItemStack stack = player.getItemInHand(hand);
            if (stack.isEmpty() && player.isShiftKeyDown())
            {
                if (state.getValue(RACK) && level.getBlockState(pos.above()).isAir() && hit.getLocation().y - pos.getY() > 0.875f)
                {
                    ItemHandlerHelper.giveItemToPlayer(player, new ItemStack(TFCBlocks.BARREL_RACK.get().asItem()));
                    level.setBlockAndUpdate(pos, state.setValue(RACK, false));
                }
                else
                {
                    toggleSeal(level, pos, state);
                }
                level.playSound(null, pos, SoundEvents.WOOD_PLACE, SoundSource.BLOCKS, 1.0f, 0.85f);
                return InteractionResult.SUCCESS;
            }
            else if (Helpers.isItem(stack, TFCBlocks.BARREL_RACK.get().asItem()) && state.getValue(FACING) != Direction.UP && !state.getValue(RACK))
            {
                if (!player.isCreative())
                {
                    stack.shrink(1);
                }
                level.setBlockAndUpdate(pos, state.setValue(RACK, true).setValue(FACING, player.getDirection().getOpposite()));
                Helpers.playPlaceSound(level, pos, state);
                return InteractionResult.sidedSuccess(level.isClientSide);
            }
            else if (FluidHelpers.transferBetweenBlockEntityAndItem(stack, barrel, player, hand))
            {
                return InteractionResult.SUCCESS;
            }
            else if (!level.isClientSide() && player instanceof ServerPlayer serverPlayer)
            {
                Helpers.openScreen(serverPlayer, barrel, barrel.getBlockPos());
            }
            return InteractionResult.SUCCESS;
        }
        return InteractionResult.PASS;
    }
    
}
