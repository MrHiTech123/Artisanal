package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.util.Metal;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;

public class DistilleryItem extends Item {
    
    protected Metal.Default metal;
    
    public DistilleryItem(Properties pProperties, Metal.Default metal) {
        super(pProperties);
        this.metal = metal;
    }
    
    @Override
    public InteractionResult onItemUseFirst(ItemStack stack, UseOnContext context) {
        Player player = context.getPlayer();
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        AbstractFirepitBlockEntity<?> firepit = level.getBlockEntity(pos, TFCBlockEntities.FIREPIT.get()).orElse(null);
        if (firepit != null && !(player != null && player.isShiftKeyDown())) {
            if (!level.isClientSide) {
                Block newBlock = ArtisanalBlocks.DISTILLERIES.get(metal).get();
                BlockState state = level.getBlockState(pos);
                AbstractFirepitBlockEntity.convertTo(level, pos, state, firepit, newBlock);
                if (!(player != null && player.isCreative())) stack.shrink(1);
            }
            return InteractionResult.sidedSuccess(level.isClientSide);
        }
        return InteractionResult.PASS;
    }
}
