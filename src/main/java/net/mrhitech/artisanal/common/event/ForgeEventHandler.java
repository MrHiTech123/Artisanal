package net.mrhitech.artisanal.common.event;

import net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity;
import net.dries007.tfc.util.events.StartFireEvent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.MissingMappingsEvent;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.common.item.CanMetal;


@Mod.EventBusSubscriber(modid = Artisanal.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public class ForgeEventHandler {
    private static void remapItems(MissingMappingsEvent event) {
        for (MissingMappingsEvent.Mapping<Item> itemMapping : event.getMappings(Registries.ITEM, Artisanal.MOD_ID)) {
            String itemName = itemMapping.getKey().getPath();
            if (itemName.equals("dry_bagasse")) {
                itemMapping.remap(ArtisanalItems.BAGASSE.get());
            }
            else if (itemName.equals("wet_bagasse")) {
                itemMapping.remap(ArtisanalItems.BAGASSE.get());
            }
            else if (itemName.equals("metal/tin_can")) {
                itemMapping.remap(ArtisanalItems.CANS.get(CanMetal.TIN).get());
            }
            else if (itemName.equals("metal/sealed_tin_can")) {
                itemMapping.remap(ArtisanalItems.SEALED_CANS.get(CanMetal.TIN).get());
            }
            else if (itemName.equals("metal/sterilized_tin_can")) {
                itemMapping.remap(ArtisanalItems.STERILIZED_CANS.get(CanMetal.TIN).get());
            }
            else if (itemName.equals("metal/dirty_tin_can")) {
                itemMapping.remap(ArtisanalItems.DIRTY_CANS.get(CanMetal.TIN).get());
            }
            else if (itemName.equals("metal/dented_tin_can")) {
                itemMapping.remap(ArtisanalItems.DENTED_CANS.get(CanMetal.TIN).get());
            }
            else if (itemName.equals("metal/dirty_dented_tin_can")) {
                itemMapping.remap(ArtisanalItems.DIRTY_DENTED_CANS.get(CanMetal.TIN).get());
            }
            
            
        }
    }
    
    @SubscribeEvent
    public static void onFireStart(StartFireEvent event) {
        Level level = event.getLevel();
        BlockPos pos = event.getPos();
        BlockState state = event.getState();
        Block block = state.getBlock();
        
        if (ArtisanalBlocks.DISTILLERIES.values().stream().map(RegistryObject::get).toList().contains(block)) {
            final BlockEntity entity = level.getBlockEntity(pos);
            
            if (entity instanceof AbstractFirepitBlockEntity<?> firepit && firepit.light(state)) {
                event.setCanceled(true);
            }
        }
    }
    
    @SubscribeEvent
    public static void onMissingMapping(MissingMappingsEvent event) {
        remapItems(event);
    }
}
