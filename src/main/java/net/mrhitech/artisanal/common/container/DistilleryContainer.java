package net.mrhitech.artisanal.common.container;

import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.container.BlockEntityContainer;
import net.dries007.tfc.common.container.CallbackSlot;
import net.dries007.tfc.common.container.PotContainer;
import net.dries007.tfc.util.Helpers;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;
import net.mrhitech.artisanal.common.blockentities.ArtisanalBlockEntities;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;

import static net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity.SLOT_FUEL_CONSUME;
import static net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity.SLOT_FUEL_INPUT;

public class DistilleryContainer extends BlockEntityContainer<DistilleryBlockEntity> {
    
    public static DistilleryContainer create(DistilleryBlockEntity distillery, Inventory playerInv, int windowId) {
        return new DistilleryContainer(distillery, windowId).init(playerInv, 20);
    }
    
    private DistilleryContainer(DistilleryBlockEntity distillery, int windowId) {
        super(ArtisanalContainerTypes.DISTILLERY.get(), windowId, distillery);
        
        addDataSlots(distillery.getSyncableData());
    }
    
    @Override
    protected boolean moveStack(ItemStack stack, int slotIndex) {
        return switch (typeOf(slotIndex)) {
            case MAIN_INVENTORY, HOTBAR -> Helpers.isItem(stack, TFCTags.Items.FIREPIT_FUEL)?
                    !moveItemStackTo(stack, SLOT_FUEL_CONSUME, SLOT_FUEL_INPUT + 1, false)
                    : blockEntity.hasRecipeStarted() || moveItemStackTo(stack, DistilleryBlockEntity.SLOT_INPUT_ITEM, DistilleryBlockEntity.SLOT_INPUT_ITEM + 1, false);
            case CONTAINER -> !moveItemStackTo(stack, containerSlots, slots.size(), false);
        };
    }
    
    @Override
    protected void addContainerSlots() {
        
        blockEntity.getCapability(Capabilities.ITEM).ifPresent(handler -> {
            // Fuel 
            for (int i = 0; i < 4; i++) {
                addSlot(new CallbackSlot(blockEntity, handler, i, 8, 70 - 18 * i));
            }
            
            addSlot(new CallbackSlot(blockEntity, handler, DistilleryBlockEntity.SLOT_INPUT_ITEM, 101, 63));
            addSlot(new CallbackSlot(blockEntity, handler, DistilleryBlockEntity.SLOT_OUTPUT_ITEM, 101, 27));
        });
        
        
    }
}
