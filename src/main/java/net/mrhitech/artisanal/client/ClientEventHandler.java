package net.mrhitech.artisanal.client;

import net.dries007.tfc.client.model.ContainedFluidModel;
import net.minecraftforge.client.event.RegisterColorHandlersEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

public class ClientEventHandler {
    public static void init() {
        final IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        bus.addListener(ClientEventHandler::registerColorHandlerItems);
    }
    
    public static void registerColorHandlerItems(RegisterColorHandlersEvent.Item event) {
        ArtisanalItems.FLUID_BUCKETS.values().forEach(reg -> event.register(new ContainedFluidModel.Colors(), reg.get()));
        
    }
}
