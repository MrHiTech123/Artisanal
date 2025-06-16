package net.mrhitech.artisanal.common.event;

import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.mixin.BlockEntityTypeAccessor;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Stream;

public class ArtisanalSetupEvents {
    public static void init() {
        final IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        
        bus.addListener(ArtisanalSetupEvents::setup);
    }
    
    private static void setup(FMLCommonSetupEvent event) {
        event.enqueueWork(ArtisanalSetupEvents::modifyBlockEntityTypes);
    }
    private static void modifyBlockEntityTypes() {
        modifyBlockEntityType(TFCBlockEntities.BARREL.get(), ArtisanalBlocks.DRUMS.values().stream().map(RegistryObject::get));
    }
    private static void modifyBlockEntityType(BlockEntityType<?> type, Stream<Block> extraBlocks)
    {
        Set<Block> blocks = ((BlockEntityTypeAccessor) type).accessor$getValidBlocks();
        blocks = new HashSet<>(blocks);
        blocks.addAll(extraBlocks.toList());
        ((BlockEntityTypeAccessor) type).accessor$setValidBlocks(blocks);
    }
}