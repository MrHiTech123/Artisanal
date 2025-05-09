package net.mrhitech.artisanal.common.event;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.MissingMappingsEvent;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.item.ArtisanalItems;


@Mod.EventBusSubscriber(modid = Artisanal.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public class ForgeEventHandler {
    private static void remapItems(MissingMappingsEvent event) {
        for (MissingMappingsEvent.Mapping<Item> itemMapping : event.getMappings(Registries.ITEM, Artisanal.MOD_ID)) {
            String itemName = itemMapping.getKey().getPath();
            if (itemName.equals("dry_bagasse")) {
                itemMapping.remap(ArtisanalItems.BAGASSE.get());
            }
            if (itemName.equals("wet_bagasse")) {
                itemMapping.remap(ArtisanalItems.BAGASSE.get());
            }
        }
    }
    
    @SubscribeEvent
    public static void onMissingMapping(MissingMappingsEvent event) {
        remapItems(event);
    }
}
