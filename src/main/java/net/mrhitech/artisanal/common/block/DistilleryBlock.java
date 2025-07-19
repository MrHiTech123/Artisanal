package net.mrhitech.artisanal.common.block;

import net.dries007.tfc.client.particle.TFCParticles;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.devices.FirepitBlock;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.common.items.FluidContainerItem;
import net.dries007.tfc.common.items.JugItem;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
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
import net.mrhitech.artisanal.common.blockentities.ArtisanalBlockEntities;

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
    
    
    
    
    @Override
    public InteractionResult use(BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult result) {
        
        return level.getBlockEntity(pos, ArtisanalBlockEntities.DISTILLERY.get()).map(distillery -> {
            final ItemStack playerHeldStack = player.getItemInHand(hand);
            
            if (player.isShiftKeyDown() && playerHeldStack.isEmpty()) {
                System.out.println("Give player the distillery item");
                
            }
            
            
            // if (FluidHelpers.transferBetweenBlockEntityAndItem(playerHeldStack, distillery, player, hand)) {
            //    
            // }
            
            return InteractionResult.sidedSuccess(level.isClientSide);
        }).orElse(InteractionResult.PASS);
        
        
    }
    
}
