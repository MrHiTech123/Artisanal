package net.mrhitech.artisanal.common.event;

import net.minecraft.network.chat.Component;
import net.minecraft.server.packs.PackLocationInfo;
import net.minecraft.server.packs.PackSelectionConfig;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.repository.Pack;
import net.minecraft.server.packs.repository.PackSource;
import net.mrhitech.artisanal.Artisanal;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.AddPackFindersEvent;
import net.neoforged.neoforge.resource.ResourcePackLoader;
import net.neoforged.neoforgespi.language.IModFileInfo;

import java.util.Optional;

public class ArtisanalEvents {
    
    public static void init() {
        IEventBus bus = NeoForge.EVENT_BUS;
        
        bus.addListener(ArtisanalEvents::onPackFinder);
    }
    
    public static void onPackFinder(AddPackFindersEvent event)
    {
        if (event.getPackType() == PackType.CLIENT_RESOURCES)
        {
            final IModFileInfo info = ModList.get().getModFileById(Artisanal.MOD_ID);
            assert info != null;

            Artisanal.LOGGER.info("Injecting firmalife override pack");
            event.addRepositorySource(consumer ->
                consumer.accept(Pack.readMetaAndCreate(new PackLocationInfo("artisanal_data", Component.literal("Artisanal Resources"), PackSource.BUILT_IN, Optional.empty()), ResourcePackLoader.createPackForMod(info), PackType.CLIENT_RESOURCES, new PackSelectionConfig(true, Pack.Position.TOP, false)))
            );
        }
    }
}
