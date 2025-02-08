package net.mrhitech.artisanal.mixin;

import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraftforge.common.capabilities.CapabilityProvider;
import net.mrhitech.artisanal.util.IBlockEntityAccessor;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Mutable;
import org.spongepowered.asm.mixin.Shadow;

@Mixin(BlockEntity.class)
public class BlockEntityAccessor implements IBlockEntityAccessor {
    @Final
    @Mutable
    @Shadow
    private BlockEntityType<?> type;
    
    public void set$Type(BlockEntityType<?> f_type) {
        type = f_type;
        System.out.println("Type being set banana");
    }
}
