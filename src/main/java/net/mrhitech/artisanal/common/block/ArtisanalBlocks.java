package net.mrhitech.artisanal.common.block;


import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.wood.Wood;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Metal;
import net.dries007.tfc.util.registry.RegistrationHelpers;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.blockentities.ArtisanalBlockEntities;
import net.mrhitech.artisanal.common.fluids.Waterlikes;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

import javax.annotation.Nullable;
import java.util.Locale;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;

public class ArtisanalBlocks {
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, Artisanal.MOD_ID);
    
    public static final Map<Waterlikes, RegistryObject<LiquidBlock>> WATERLIKES = Helpers.mapOfKeys(Waterlikes.class, fluid ->
            register("fluid/" + fluid.getId(), () -> new LiquidBlock(ArtisanalFluids.WATERLIKES.get(fluid).source(), BlockBehaviour.Properties.copy(Blocks.WATER))));
    
    public static final Map<DrumMetal, RegistryObject<Block>> DRUMS = Helpers.mapOfKeys(DrumMetal.class, drumMetal -> 
            register(
                    "metal/drum/" + drumMetal.getMetal().name().toLowerCase(Locale.ROOT),
                    () -> new DrumBlock(
                            ExtendedProperties.of(TFCBlocks.METALS.get(drumMetal.getMetal())
                                    .get(Metal.BlockType.BLOCK).get())
                                    .blockEntity(TFCBlockEntities.BARREL)
                                    .serverTicks(BarrelBlockEntity::serverTick), 
                            drumMetal.getUsableFluids()
                    ),
                    new Item.Properties().rarity(drumMetal.getMetal().getRarity())
            ));
    
    public static final Map<Wood, RegistryObject<Block>> DISTILLERIES = Helpers.mapOfKeys(Wood.class, woodType ->
            register(
                    "wood/barrel/" + woodType.name().toLowerCase(Locale.ROOT),
                    () -> new DistilleryBlock(
                            ExtendedProperties.of(TFCBlocks.FIREPIT.get()).blockEntity(ArtisanalBlockEntities.DISTILLERY)
                    ),
                    new Item.Properties()
            )
    );
    
    
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
        return RegistrationHelpers.registerBlock(BLOCKS, ArtisanalItems.ITEMS, name, blockSupplier, blockItemFactory);
    }
    
    
    
}
