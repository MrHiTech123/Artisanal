package net.mrhitech.artisanal.common.block.devices;

import net.dries007.tfc.client.TFCSounds;
import net.dries007.tfc.client.particle.TFCParticles;
import net.dries007.tfc.common.TFCDamageTypes;
import net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.devices.FirepitBlock;
import net.dries007.tfc.common.container.ItemStackContainerProvider;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.common.items.Powder;
import net.dries007.tfc.common.items.TFCItems;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Metal;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.mrhitech.artisanal.common.blockentities.ArtisanalBlockEntities;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;
import net.mrhitech.artisanal.common.container.ArtisanalContainerTypes;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;
import net.neoforged.neoforge.fluids.capability.templates.FluidTank;
import net.neoforged.neoforge.items.ItemHandlerHelper;

public class DistilleryBlock extends FirepitBlock {
    
    private static final VoxelShape DISTILLERY_SHAPE = Shapes.or(BASE_SHAPE, box(2, 0, 2, 14, 16, 14));
    
    protected Metal metal;
    
    public DistilleryBlock(ExtendedProperties properties, Metal metal) {
        super(properties, DISTILLERY_SHAPE);
        this.metal = metal;
    }
    
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        super.animateTick(state, level, pos, random);
        
        level.getBlockEntity(pos, ArtisanalBlockEntities.DISTILLERY.get()).ifPresent(distillery -> {
            if (!distillery.shouldRenderAsBoiling()) return;
            
            // TODO: Figure out position of bubbles
            double x = pos.getX();
            double y = pos.getY();
            double z = pos.getZ();
            
            // for (int i = 0; i < random.nextInt(4, 9); ++i) {
            //     level.addParticle(TFCParticles.BUBBLE.get(), false, x + random.nextFloat() * 0.375 - 0.1875, y + 0.625, z + random.nextFloat() * 0.375 - 0.1875, 0, 0.05D, 0);
            // }
            //
            
            
            // level.addParticle(TFCParticles.STEAM.get(), false, x, y + 0.8, z, Helpers.triangle(random), 0.5, Helpers.triangle(random));
            if (!distillery.getFluidInTank(DistilleryBlockEntity.TANK_INPUT_FLUID).isEmpty()) {
                level.playLocalSound(x, y, z, SoundEvents.WATER_AMBIENT, SoundSource.BLOCKS, 1.0F, random.nextFloat() * 0.7F + 0.4F, false);
            }
            
        });
    }
    
    
    private void giveAshToPlayer(DistilleryBlockEntity distillery, Player player, Level level, BlockPos pos) {
        ItemHandlerHelper.giveItemToPlayer(player, new ItemStack(TFCItems.POWDERS.get(Powder.WOOD_ASH).get(), distillery.getAsh()));
        distillery.setAsh(0);
        Helpers.playSound(level, pos, SoundEvents.SAND_BREAK);
    }
    
    private void giveDistilleryToPlayer(Player player, Level level, BlockPos pos, BlockState state, DistilleryBlockEntity distillery) {
        ItemHandlerHelper.giveItemToPlayer(player, new ItemStack(ArtisanalItems.DISTILLERIES.get(metal).get()));
        AbstractFirepitBlockEntity.convertTo(level, pos, state, distillery, TFCBlocks.FIREPIT.get());
    }
    
    private ItemInteractionResult openGui(Player player, DistilleryBlockEntity distillery, Level level, BlockPos pos) {
        if (player instanceof ServerPlayer serverPlayer) {
            ArtisanalContainerTypes.openScreen(serverPlayer, distillery, pos);
        }
        return ItemInteractionResult.sidedSuccess(level.isClientSide);
    }
    
    
    
    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hitResult) {
        return level.getBlockEntity(pos, ArtisanalBlockEntities.DISTILLERY.get()).map(distillery -> {
            final ItemStack playerHeldStack = player.getItemInHand(hand);
            
            
            if (player.isShiftKeyDown() && playerHeldStack.isEmpty()) {
                if (distillery.getAsh() > 0) {
                    if (!distillery.isBoiling()) {
                        giveAshToPlayer(distillery, player, level, pos);
                    }
                }
                else {
                    giveDistilleryToPlayer(player, level, pos, state, distillery);
                }
                
                if (distillery.isBoiling()) {
                    TFCDamageTypes.pot(player, 1f);
                    Helpers.playSound(level, pos, TFCSounds.ITEM_COOL.get());
                }
                
                return ItemInteractionResult.sidedSuccess(level.isClientSide);
            }
            else if (
                    !distillery.isBoiling() && 
                    playerHeldStack.getCapability(Capabilities.FluidHandler.ITEM) != null
            ) {
                
                IFluidHandler cap = playerHeldStack.getCapability(Capabilities.FluidHandler.ITEM);
                assert cap != null;
                
                FluidTank outputTank = distillery.getOutputTank();
                if (!outputTank.getFluid().isEmpty()) {
                    FluidStack transferStack = outputTank.drain(outputTank.getCapacity(), IFluidHandler.FluidAction.EXECUTE);
                    int amountFilled = cap.fill(transferStack, IFluidHandler.FluidAction.EXECUTE);
                    
                    if (amountFilled != 0) {
                        FluidHelpers.playTransferSound(level, pos, transferStack, FluidHelpers.Transfer.FILL);
                    }
                    
                    FluidStack toAddBackToOutputTank = new FluidStack(transferStack.getFluid(), transferStack.getAmount() - amountFilled);
                    outputTank.fill(toAddBackToOutputTank, IFluidHandler.FluidAction.EXECUTE);
                }
                else if (FluidHelpers.transferBetweenBlockEntityAndItem(playerHeldStack, distillery, player, hand)) {
                    distillery.setAndUpdateSlots(-1);
                    distillery.markForSync();
                }
                else {
                    openGui(player, distillery, level, pos);
                }
                
                
                return ItemInteractionResult.sidedSuccess(level.isClientSide);
            }
            else {
                if (tryInsertLog(player, playerHeldStack, distillery, hitResult.getLocation().y - pos.getY() < 0.6)) {
                    return ItemInteractionResult.sidedSuccess(level.isClientSide);
                }
                return openGui(player, distillery, level, pos);
            }
        }).orElse(ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION);
        
        
    }
    
}
