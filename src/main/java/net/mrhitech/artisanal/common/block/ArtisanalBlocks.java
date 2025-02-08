package net.mrhitech.artisanal.common.block;


import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.devices.BarrelBlock;
import net.dries007.tfc.common.items.TFCItems;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Metal;
import net.dries007.tfc.util.registry.RegistrationHelpers;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.Waterlikes;
import net.mrhitech.artisanal.common.blockentity.ArtisanalBlockEntities;
import net.mrhitech.artisanal.common.blockentity.DrumBlockEntity;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;

import javax.annotation.Nullable;
import java.util.Locale;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;

public class ArtisanalBlocks {
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, Artisanal.MOD_ID);
    
    public static final Map<Waterlikes, RegistryObject<LiquidBlock>> WATERLIKES = Helpers.mapOfKeys(Waterlikes.class, fluid ->
            register("fluid/" + fluid.getId(), () -> new LiquidBlock(ArtisanalFluids.WATERLIKES.get(fluid).source(), BlockBehaviour.Properties.copy(Blocks.WATER))));
    
    public static final Map<Metal.Default, RegistryObject<Block>> DRUMS = Helpers.mapOfKeys(Metal.Default.class, metal -> 
            register("metal/drum/" + metal.name().toLowerCase(Locale.ROOT), () -> new DrumBlock(ExtendedProperties.of(Blocks.IRON_BLOCK).blockEntity(ArtisanalBlockEntities.DRUM).serverTicks(DrumBlockEntity::serverTick))));
    
    
    public static void register(IEventBus bus) {
        BLOCKS.register(bus);
    }
    
    private static <T extends Block> RegistryObject<T> registerNoItem(String name, Supplier<T> blockSupplier)
    {
        return register(name, blockSupplier, (Function<T, ? extends BlockItem>) null);
    }
    
    private static <T extends Block> RegistryObject<T> register(String name, Supplier<T> blockSupplier)
    {
        return register(name, blockSupplier, block -> new BlockItem(block, new Item.Properties()));
    }
    
    private static <T extends Block> RegistryObject<T> register(String name, Supplier<T> blockSupplier, Item.Properties blockItemProperties)
    {
        return register(name, blockSupplier, block -> new BlockItem(block, blockItemProperties));
    }
    
    private static <T extends Block> RegistryObject<T> register(String name, Supplier<T> blockSupplier, @Nullable Function<T, ? extends BlockItem> blockItemFactory)
    {
        return RegistrationHelpers.registerBlock(BLOCKS, TFCItems.ITEMS, name, blockSupplier, blockItemFactory);
    }
    
    
    
}
