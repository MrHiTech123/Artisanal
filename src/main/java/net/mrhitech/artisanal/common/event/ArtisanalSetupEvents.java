package net.mrhitech.artisanal.common.event;

import net.dries007.tfc.common.blockentities.PotBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.container.PotContainer;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.mixin.BlockEntityTypeAccessor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.registries.DeferredHolder;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Stream;

public class ArtisanalSetupEvents {
    public static void init(IEventBus bus) {
        
        bus.addListener(ArtisanalSetupEvents::setup);
    }
    
    private static void setup(FMLCommonSetupEvent event) {
        event.enqueueWork(ArtisanalSetupEvents::modifyBlockEntityTypes);
    }
    private static void modifyBlockEntityTypes() {
        modifyBlockEntityType(TFCBlockEntities.BARREL.get(), ArtisanalBlocks.DRUMS.values().stream().map(DeferredHolder::get));
    }
    private static void modifyBlockEntityType(BlockEntityType<?> type, Stream<Block> extraBlocks)
    {
        Set<Block> blocks = ((BlockEntityTypeAccessor) type).accessor$getValidBlocks();
        blocks = new HashSet<>(blocks);
        blocks.addAll(extraBlocks.toList());
        ((BlockEntityTypeAccessor) type).accessor$setValidBlocks(blocks);
    }
}