package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.common.items.BarrelBlockItem;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;

public class DrumBlockItem extends BarrelBlockItem {
    
    public DrumBlockItem(Block block, Properties properties) {
        super(block, properties);
    }
    
    @Override
    public InteractionResult useOn(UseOnContext context) {
        return super.useOn(context);
    }
    
}
