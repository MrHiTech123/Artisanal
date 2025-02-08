package net.mrhitech.artisanal.common.blockentity;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.mixin.BarrelInventoryAccessor;
import net.mrhitech.artisanal.util.IBlockEntityAccessor;
import org.jetbrains.annotations.Nullable;

public class DrumBlockEntity extends BarrelBlockEntity {
    public DrumBlockEntity(BlockPos pos, BlockState state) {
        super(pos, state);
        ((IBlockEntityAccessor)this).set$Type(ArtisanalBlockEntities.DRUM.get());
        ((BarrelInventoryAccessor)inventory).getTank().setValidator(
                (stack) -> Helpers.isFluid(stack.getFluid(), ArtisanalTags.FLUIDS.USABLE_IN_DRUM)
        );
    }

    @Nullable
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new DrumBlockEntity(pos, state);
    }
}
