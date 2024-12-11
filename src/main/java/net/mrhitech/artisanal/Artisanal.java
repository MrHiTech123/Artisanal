package net.mrhitech.artisanal;

import com.mojang.logging.LogUtils;
import net.minecraft.client.Minecraft;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.event.server.ServerStartingEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLEnvironment;
import net.minecraftforge.registries.ForgeRegistries;
import net.mrhitech.artisanal.client.ClientEventHandler;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.creative.ArtisanalCreativeTabs;
import net.mrhitech.artisanal.common.event.ArtisanalEvents;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.common.loot.ArtisanalLootModifiers;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeSerializers;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeTypes;
import net.mrhitech.artisanal.common.recipes.outputs.ArtisanalItemStackModifiers;
import net.mrhitech.artisanal.compat.patchouli.PatchouliIntegration;
import org.slf4j.Logger;

// The value here should match an entry in the META-INF/mods.toml file
@Mod(Artisanal.MOD_ID)
public class Artisanal
{
    // Define mod id in a common place for everything to reference
    public static final String MOD_ID = "artisanal";
    // Directly reference a slf4j logger
    public static final Logger LOGGER = LogUtils.getLogger();
    public Artisanal()
    {
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();

        ArtisanalItems.register(modEventBus);
        ArtisanalBlocks.register(modEventBus);
        ArtisanalFluids.register(modEventBus);
        ArtisanalLootModifiers.register(modEventBus);
        ArtisanalRecipeSerializers.register(modEventBus);
        ArtisanalRecipeTypes.register(modEventBus);
        ArtisanalItemStackModifiers.registerItemStackModifiers();
        ArtisanalEvents.init();
        if (FMLEnvironment.dist == Dist.CLIENT) {
            ClientEventHandler.init();
        }
        
        // Register the commonSetup method for modloading
        modEventBus.addListener(this::commonSetup);

        // Register ourselves for server and other game events we are interested in
        MinecraftForge.EVENT_BUS.register(this);

        // Register the item to a creative tab
        modEventBus.addListener(this::addCreative);
    }

    private void commonSetup(final FMLCommonSetupEvent event)
    {
        // Some common setup code
        LOGGER.info("HELLO FROM COMMON SETUP");
        LOGGER.info("DIRT BLOCK >> {}", ForgeRegistries.BLOCKS.getKey(Blocks.DIRT));
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
    @Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
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
