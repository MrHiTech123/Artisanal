package net.mrhitech.artisanal.common.block.devices;

import net.dries007.tfc.client.TFCSounds;
import net.dries007.tfc.client.particle.TFCParticles;
import net.dries007.tfc.common.TFCDamageSources;
import net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.devices.FirepitBlock;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.common.items.Powder;
import net.dries007.tfc.common.items.TFCItems;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraftforge.items.ItemHandlerHelper;
import net.mrhitech.artisanal.common.blockentities.ArtisanalBlockEntities;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

public class DistilleryBlock extends FirepitBlock {
    
    
    public DistilleryBlock(ExtendedProperties properties) {
        super(properties);
    }
    
    private boolean shouldRenderBoiling() {
        return false;
    }
    
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        super.animateTick(state, level, pos, random);
        
        level.getBlockEntity(pos, ArtisanalBlockEntities.DISTILLERY.get()).ifPresent(distillery -> {
            if (!shouldRenderBoiling()) return;
            
            // TODO: Figure out position of bubbles
            double x = pos.getX();
            double y = pos.getY();
            double z = pos.getZ();
            
            for (int i = 0; i < random.nextInt(4, 9); ++i) {
                level.addParticle(TFCParticles.BUBBLE.get(), false, x + random.nextFloat() * 0.375 - 0.1875, y + 0.625, z + random.nextFloat() * 0.375 - 0.1875, 0, 0.05D, 0);
            }
            
            level.addParticle(TFCParticles.STEAM.get(), false, x, y + 0.8, z, Helpers.triangle(random), 0.5, Helpers.triangle(random));
            level.playLocalSound(x, y, z, SoundEvents.WATER_AMBIENT, SoundSource.BLOCKS, 1.0F, random.nextFloat() * 0.7F + 0.4F, false);
            
        });
    }
    
    
    private void giveAshToPlayer(DistilleryBlockEntity distillery, Player player, Level level, BlockPos pos) {
        ItemHandlerHelper.giveItemToPlayer(player, new ItemStack(TFCItems.POWDERS.get(Powder.WOOD_ASH).get(), distillery.getAsh()));
        distillery.setAsh(0);
        Helpers.playSound(level, pos, SoundEvents.SAND_BREAK);
    }
    
    private void givePotToPlayer(Player player, Level level, BlockPos pos, BlockState state, DistilleryBlockEntity distillery) {
        ItemHandlerHelper.giveItemToPlayer(player, new ItemStack(ArtisanalItems.DISTILLERY.get()));
        AbstractFirepitBlockEntity.convertTo(level, pos, state, distillery, TFCBlocks.FIREPIT.get());
    }
    
    @Override
    public InteractionResult use(BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult result) {
        
        return level.getBlockEntity(pos, ArtisanalBlockEntities.DISTILLERY.get()).map(distillery -> {
            final ItemStack playerHeldStack = player.getItemInHand(hand);
            
            
            if (player.isShiftKeyDown() && playerHeldStack.isEmpty()) {
                if (distillery.getAsh() >= 0) {
                    if (!distillery.isBoiling()) {
                        giveAshToPlayer(distillery, player, level, pos);
                    }
                }
                else {
                    givePotToPlayer(player, level, pos, state, distillery);
                }
                
                if (distillery.isBoiling()) {
                    TFCDamageSources.pot(player, 1f);
                    Helpers.playSound(level, pos, TFCSounds.ITEM_COOL.get());
                }
                
                return InteractionResult.sidedSuccess(level.isClientSide);
            }
            else if (!distillery.isBoiling() && FluidHelpers.transferBetweenBlockEntityAndItem(playerHeldStack, distillery, player, hand)) {
                distillery.setAndUpdateSlots(-1);
                distillery.markForSync();
                return InteractionResult.sidedSuccess(level.isClientSide);
            }
            else {
                if (tryInsertLog(player, playerHeldStack, distillery, result.getLocation().y - pos.getY() < 0.6)) {
                    return InteractionResult.sidedSuccess(level.isClientSide);
                }
                if (player instanceof ServerPlayer serverPlayer) {
                    Helpers.openScreen(serverPlayer, distillery, pos);
                }
                return InteractionResult.sidedSuccess(level.isClientSide);
            }
        }).orElse(InteractionResult.PASS);
        
        
    }
    
}
