package net.mrhitech.artisanal.common.blockentities;

import net.dries007.tfc.common.blocks.wood.Wood;
import net.dries007.tfc.util.Metal;
import net.dries007.tfc.util.registry.RegistrationHelpers;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

import java.util.Arrays;
import java.util.Map;
import java.util.function.Predicate;
import java.util.function.Supplier;
import java.util.stream.Stream;

public class ArtisanalBlockEntities {
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, Artisanal.MOD_ID);
    
    public static final RegistryObject<BlockEntityType<DistilleryBlockEntity>> DISTILLERY = register(
            "distillery",
            DistilleryBlockEntity::new,
            metalBlocks(ArtisanalBlocks.DISTILLERIES, ArtisanalItems::hasDistilleries)
    );
    
    public static void register(IEventBus eventBus) {
        BLOCK_ENTITIES.register(eventBus);
    }
    
    private static <T extends BlockEntity> RegistryObject<BlockEntityType<T>> register(String name, BlockEntityType.BlockEntitySupplier<T> factory, Supplier<? extends Block> block)
    {
        return RegistrationHelpers.register(BLOCK_ENTITIES, name, factory, block);
    }

    private static <T extends BlockEntity> RegistryObject<BlockEntityType<T>> register(String name, BlockEntityType.BlockEntitySupplier<T> factory, Stream<? extends Supplier<? extends Block>> blocks)
    {
        return RegistrationHelpers.register(BLOCK_ENTITIES, name, factory, blocks);
    }
    
    private static Stream<? extends Supplier<? extends Block>> metalBlocks(Map<Metal.Default, RegistryObject<Block>> type) {
        return metalBlocks(type, Metal.Default::hasTools);
    }
    
    private static Stream<? extends Supplier<? extends Block>> metalBlocks(Map<Metal.Default, RegistryObject<Block>> type, Predicate<Metal.Default> requiredTrue)
    {
        return Arrays.stream(Metal.Default.values()).filter(requiredTrue).map(type::get);
    }
    
}