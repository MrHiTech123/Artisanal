package net.mrhitech.artisanal.client;

import net.dries007.tfc.client.model.ContainedFluidModel;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Metal;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.MenuScreens;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.ItemBlockRenderTypes;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.client.event.RegisterColorHandlersEvent;
import net.minecraftforge.client.event.RegisterGuiOverlaysEvent;
import net.minecraftforge.client.gui.overlay.ForgeGui;
import net.minecraftforge.client.gui.overlay.VanillaGuiOverlay;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.mrhitech.artisanal.client.render.blockentity.DistilleryBlockEntityRenderer;
import net.mrhitech.artisanal.client.screen.DistilleryScreen;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.blockentities.ArtisanalBlockEntities;
import net.mrhitech.artisanal.common.container.ArtisanalContainerTypes;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;
import net.mrhitech.artisanal.common.fluids.Waterlikes;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.common.item.LabGogglesItem;
import net.mrhitech.artisanal.util.RenderingHelpers;

import java.util.function.Predicate;

public class ClientEventHandler {
    public static void init() {
        final IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        
        bus.addListener(ClientEventHandler::clientSetup);
        bus.addListener(ClientEventHandler::registerColorHandlerItems);
        bus.addListener(ClientEventHandler::registerEntityRenderers);
        //bus.addListener(ClientEventHandler::registerOverlays);
        
    }
    
    @SuppressWarnings("deprecation")
    public static void clientSetup(FMLClientSetupEvent event) {
        
        event.enqueueWork(() -> {
            ArtisanalBlocks.DRUMS.values().forEach(map -> ItemProperties.register(map.get().asItem(), Helpers.identifier("sealed"), (stack, level, entity, unused) -> stack.hasTag() ? 1.0f : 0f));
            
            MenuScreens.register(ArtisanalContainerTypes.DISTILLERY.get(), DistilleryScreen::new);
        });
        
        final RenderType translucent = RenderType.translucent();
        final RenderType cutoutMipped = RenderType.cutoutMipped();
        final Predicate<RenderType> ghostBlock = rt -> rt == cutoutMipped || rt == Sheets.translucentCullBlockSheet();
        
        for (Metal.Default metal : Metal.Default.values()) {
            if (!ArtisanalItems.hasDistilleries(metal)) continue;
            ItemBlockRenderTypes.setRenderLayer(
                    ArtisanalBlocks.DISTILLERIES.get(metal).get(), 
                    ghostBlock
            );
        }
        
        for (Waterlikes waterlike : Waterlikes.values()) {
            if (waterlike.isTransparent()) {
                ItemBlockRenderTypes.setRenderLayer(ArtisanalFluids.WATERLIKES.get(waterlike).getSource(), translucent);
                ItemBlockRenderTypes.setRenderLayer(ArtisanalFluids.WATERLIKES.get(waterlike).getFlowing(), translucent);
            }
        }
    }
    
    public static void registerColorHandlerItems(RegisterColorHandlersEvent.Item event) {
        ArtisanalItems.FLUID_BUCKETS.values().forEach(reg -> event.register(new ContainedFluidModel.Colors(), reg.get()));
    }
    
    public static void registerEntityRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerBlockEntityRenderer(ArtisanalBlockEntities.DISTILLERY.get(), ctx -> new DistilleryBlockEntityRenderer());
    }
    
    public static void registerOverlays(RegisterGuiOverlaysEvent overlaysEvent) {
        overlaysEvent.registerAbove(VanillaGuiOverlay.HELMET.id(), "lab_goggles_overlay", RenderingHelpers::renderLabGogglesOverWorldIfWorn);
    }
    
    
}
