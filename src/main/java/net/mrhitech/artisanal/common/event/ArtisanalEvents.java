package net.mrhitech.artisanal.common.event;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.metadata.pack.PackMetadataSection;
import net.minecraft.server.packs.repository.Pack;
import net.minecraft.server.packs.repository.PackSource;
import net.minecraft.world.item.Item;
import net.minecraftforge.event.AddPackFindersEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.forgespi.locating.IModFile;
import net.minecraftforge.registries.MissingMappingsEvent;
import net.minecraftforge.resource.PathPackResources;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.nio.file.Path;

public class ArtisanalEvents {
    
    public static void init() {
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        
        bus.addListener(ArtisanalEvents::onPackFinder);
    }
    
    public static void onPackFinder(AddPackFindersEvent event)
    {
        try
        {
            if (event.getPackType() == PackType.CLIENT_RESOURCES)
            {
                final IModFile modFile = ModList.get().getModFileById(Artisanal.MOD_ID).getFile();
                final Path resourcePath = modFile.getFilePath();
                try (PathPackResources pack = new PathPackResources(modFile.getFileName() + ":overload", true, resourcePath){
                    
                    private final IModFile file = ModList.get().getModFileById(Artisanal.MOD_ID).getFile();
                    
                    @NotNull
                    @Override
                    protected Path resolve(String @NotNull ... paths)
                    {
                        return file.findResource(paths);
                    }
                })
                {
                    final PackMetadataSection metadata = pack.getMetadataSection(PackMetadataSection.TYPE);
                    if (metadata != null)
                    {
                        Artisanal.LOGGER.info("Injecting firmalife override pack");
                        event.addRepositorySource(consumer ->
                                consumer.accept(Pack.readMetaAndCreate("artisanal_data", Component.literal("Artisanal Resources"), true, id -> pack, PackType.CLIENT_RESOURCES, Pack.Position.TOP, PackSource.BUILT_IN))
                        );
                    }
                }
                
            }
        }
        catch (IOException e)
        {
            throw new RuntimeException(e);
        }
    }
}
