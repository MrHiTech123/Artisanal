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
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModLoadingContext;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.client.event.RegisterColorHandlersEvent;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.neoforged.neoforge.common.NeoForge;

import java.util.function.Predicate;

public class ClientEventHandler {
    public static void init() {
        final IEventBus bus = NeoForge.EVENT_BUS;
        
        bus.addListener(ClientEventHandler::clientSetup);
        bus.addListener(ClientEventHandler::registerColorHandlerItems);
        bus.addListener(ClientEventHandler::registerEntityRenderers);
        bus.addListener(ClientEventHandler::onMenuRegister);
        //bus.addListener(ClientEventHandler::registerOverlays);
        
    }
    
    
    public static void onMenuRegister(RegisterMenuScreensEvent event) {
        event.register(ArtisanalContainerTypes.DISTILLERY.get(), DistilleryScreen::new);
    }
    
    @SuppressWarnings("deprecation")
    public static void clientSetup(FMLClientSetupEvent event) {
        
        event.enqueueWork(() -> {
            ArtisanalBlocks.DRUMS.values().forEach(map -> ItemProperties.register(map.get().asItem(), Helpers.identifier("sealed"), (stack, level, entity, unused) -> stack.hasTag() ? 1.0f : 0f));
            
        });
            
        
        final RenderType translucent = RenderType.translucent();
        final RenderType cutoutMipped = RenderType.cutoutMipped();
        final Predicate<RenderType> ghostBlock = rt -> rt == cutoutMipped || rt == Sheets.translucentCullBlockSheet();
        
        for (Metal metal : Metal.values()) {
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
    
    public static void registerOverlays(RegisterGuiLayersEvent overlaysEvent) {
        overlaysEvent.registerAbove(VanillaGuiOverlay.HELMET.id(), "lab_goggles_overlay", RenderingHelpers::renderLabGogglesOverWorldIfWorn);
    }
    
    
}
