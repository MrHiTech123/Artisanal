package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.blockentities.QuernBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blockentities.TickableInventoryBlockEntity;
import net.dries007.tfc.common.blockentities.rotation.RotationSinkBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.items.ItemStackHandler;
import net.mrhitech.artisanal.util.JuicingHandler;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(value = QuernBlockEntity.class, remap = false)
public abstract class QuernBlockEntityMixin extends TickableInventoryBlockEntity<ItemStackHandler> implements RotationSinkBlockEntity  {
    
    @Inject(method = "finishGrinding", at = @At("HEAD"))
    private void finishGrindingInject(CallbackInfo info) {
        ItemStack inputStack = ((ItemStackHandler)this.inventory).getStackInSlot(1);
        JuicingHandler.handle(inputStack, this.level, this.getBlockPos());
    }
    
    public QuernBlockEntityMixin(BlockPos pos, BlockState state) {
        super((BlockEntityType) TFCBlockEntities.QUERN.get(), pos, state, defaultInventory(3), null);
    }
    
    
    
}
