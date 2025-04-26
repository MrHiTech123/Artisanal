package net.mrhitech.artisanal.common.block;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.devices.BarrelBlock;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluid;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.mixin.BarrelInventoryAccessor;
import net.mrhitech.artisanal.util.IBarrelBlockEntityMixin;
import org.jetbrains.annotations.Nullable;


public class DrumBlock extends BarrelBlock {
    
    private final TagKey<Fluid> usableFluids;
    
    public DrumBlock(ExtendedProperties properties, TagKey<Fluid> usableFluids) {
        super(properties);
        this.usableFluids = usableFluids;
    }
    
    @Override
    public @Nullable BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        BlockEntity entity = super.newBlockEntity(pos, state);
        if (entity instanceof BarrelBlockEntity barrel) {
            modifyBlockEntity(barrel);
            barrel.getBlockState().getBlock();
        }
        
        return entity;
    }
    
    private static void modifyBlockEntity(BarrelBlockEntity barrel) {
        ((IBarrelBlockEntityMixin)barrel).enableDrumFluids();
    }
    
    
    
    public TagKey<Fluid> getUsableFluids() {
        return usableFluids;
    }
    
    //
    // public static void modifyBlockEntity(BarrelBlockEntity barrel) {
    //     ((BarrelInventoryAccessor)((IBarrelBlockEntityMixin)barrel).getInventory()).getTank().setValidator(
    //             fluid -> Helpers.isFluid(fluid.getFluid(), ArtisanalTags.FLUIDS.USABLE_IN_DRUM));
    // }
}
