package net.mrhitech.artisanal;

import com.mojang.logging.LogUtils;
import net.minecraft.client.Minecraft;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.EventBus;
import net.neoforged.fml.ModLoadingContext;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.mrhitech.artisanal.client.ClientEventHandler;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.blockentities.ArtisanalBlockEntities;
import net.mrhitech.artisanal.common.container.ArtisanalContainerTypes;
import net.mrhitech.artisanal.common.creative.ArtisanalCreativeTabs;
import net.mrhitech.artisanal.common.event.ArtisanalEvents;
import net.mrhitech.artisanal.common.event.ArtisanalSetupEvents;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.common.loot.ArtisanalLootModifiers;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeSerializers;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeTypes;
import net.mrhitech.artisanal.common.recipes.inputs.ArtisanalItemIngredients;
import net.mrhitech.artisanal.common.recipes.outputs.ArtisanalItemStackModifiers;
import net.mrhitech.artisanal.compat.patchouli.PatchouliIntegration;
import net.mrhitech.artisanal.config.ArtisanalServerConfig;
import net.mrhitech.artisanal.util.advancements.ArtisanalAdvancements;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import org.slf4j.Logger;

// The value here should match an entry in the META-INF/mods.toml file
@Mod(Artisanal.MOD_ID)
public class Artisanal
{
    // Define mod id in a common place for everything to reference
    public static final String MOD_ID = "artisanal";
    // Directly reference a slf4j logger
    public static final Logger LOGGER = LogUtils.getLogger();
    public Artisanal(IEventBus modEventBus, ModContainer modContainer)
    {
        
        ArtisanalAdvancements.registerTriggers();
        ArtisanalItems.register(modEventBus);
        ArtisanalBlocks.register(modEventBus);
        ArtisanalBlockEntities.register(modEventBus);
        ArtisanalSetupEvents.init();
        ArtisanalFluids.register(modEventBus);
        ArtisanalLootModifiers.register(modEventBus);
        modContainer.registerConfig(ModConfig.Type.SERVER, ArtisanalServerConfig.SPEC);
        ArtisanalContainerTypes.register(modEventBus);
        ArtisanalRecipeSerializers.register(modEventBus);
        ArtisanalRecipeTypes.register(modEventBus);
        ArtisanalItemStackModifiers.registerItemStackModifiers();
        ArtisanalItemIngredients.registerIngredientTypes();
        ArtisanalEvents.init();
        
        if (FMLEnvironment.dist == Dist.CLIENT) {
            ClientEventHandler.init();
        }
        
        // Register the commonSetup method for modloading
        modEventBus.addListener(this::commonSetup);

        // Register ourselves for server and other game events we are interested in
        NeoForge.EVENT_BUS.register(this);

        // Register the item to a creative tab
        modEventBus.addListener(this::addCreative);
    }

    private void commonSetup(final FMLCommonSetupEvent event)
    {
        // Some common setup code
        LOGGER.info("HELLO FROM COMMON SETUP");
        PatchouliIntegration.registerMultiBlocks();
    }

    // Add the example block item to the building blocks tab
    private void addCreative(BuildCreativeModeTabContentsEvent event)
    {
        ArtisanalCreativeTabs.AddCreative(event);
    }

    // You can use SubscribeEvent and let the Event Bus discover methods to call
    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event)
    {
        // Do something when the server starts
        LOGGER.info("HELLO from server starting");
    }

    // You can use EventBusSubscriber to automatically register all static methods in the class annotated with @SubscribeEvent
    @EventBusSubscriber(modid = MOD_ID, value = Dist.CLIENT)
    public static class ClientModEvents
    {
        @SubscribeEvent
        public static void onClientSetup(FMLClientSetupEvent event)
        {
            // Some client setup code
            LOGGER.info("HELLO FROM CLIENT SETUP");
            LOGGER.info("MINECRAFT NAME >> {}", Minecraft.getInstance().getUser().getName());
        }
    }
}
