package net.mrhitech.artisanal.mixin;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blockentities.BarrelInventoryCallback;
import net.dries007.tfc.common.blockentities.TickableInventoryBlockEntity;
import net.dries007.tfc.common.recipes.inventory.BarrelInventory;
import net.dries007.tfc.util.calendar.ICalendarTickable;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.common.util.INBTSerializable;
import net.minecraftforge.items.IItemHandlerModifiable;
import net.mrhitech.artisanal.util.IBarrelBlockEntityAccessor;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.gen.Accessor;


@Mixin(BarrelBlockEntity.class)
public abstract class BarrelBlockEntityAccessor extends TickableInventoryBlockEntity<BarrelBlockEntity.BarrelInventory> implements ICalendarTickable, BarrelInventoryCallback, IBarrelBlockEntityAccessor {
    protected BarrelBlockEntityAccessor(BlockEntityType<?> type, BlockPos pos, BlockState state, InventoryFactory<BarrelBlockEntity.BarrelInventory> inventory, Component defaultName) {
        super(type, pos, state, inventory, defaultName);
    }
    
    public BarrelBlockEntity.BarrelInventory getInventory() {
        return inventory;
    }
}
