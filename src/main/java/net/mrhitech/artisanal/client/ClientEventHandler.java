package net.mrhitech.artisanal.client;

import net.dries007.tfc.client.model.ContainedFluidModel;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.util.Helpers;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraftforge.client.event.RegisterColorHandlersEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

public class ClientEventHandler {
    public static void init() {
        final IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        bus.addListener(ClientEventHandler::clientSetup);
        bus.addListener(ClientEventHandler::registerColorHandlerItems);
    }
    
    public static void clientSetup(FMLClientSetupEvent event) {
        
        event.enqueueWork(() -> {
            ArtisanalBlocks.DRUMS.values().forEach(map -> ItemProperties.register(map.get().asItem(), Helpers.identifier("sealed"), (stack, level, entity, unused) -> stack.hasTag() ? 1.0f : 0f));
        });
        
    }
    
    public static void registerColorHandlerItems(RegisterColorHandlersEvent.Item event) {
        ArtisanalItems.FLUID_BUCKETS.values().forEach(reg -> event.register(new ContainedFluidModel.Colors(), reg.get()));
        
    }
}
