package net.mrhitech.artisanal.common.loot;


import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import net.dries007.tfc.util.registry.RegistryHolder;
import net.mrhitech.artisanal.Artisanal;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

import java.util.function.Supplier;

public class ArtisanalLootModifiers {
    public static final DeferredRegister<MapCodec<? extends IGlobalLootModifier>> LOOT_MODIFIER_SERIALIZERS = DeferredRegister.create(
            NeoForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, Artisanal.MOD_ID);
    
    public static final GLMId<? extends IGlobalLootModifier> ADD_ITEM_STACK_MIN_MAX = glmSerializer("add_itemstack_min_max", AddItemStackMinMaxModifier.CODEC);
    public static final GLMId<? extends IGlobalLootModifier> ADD_FAT = glmSerializer("add_fat", AddFatModifier.CODEC);
    
    
    private static <T extends IGlobalLootModifier> GLMId<T> glmSerializer(String id, MapCodec<T> modifier)
    {
        return new GLMId<>(LOOT_MODIFIER_SERIALIZERS.register(id, () -> modifier));
    }
    
    public record GLMId<T extends IGlobalLootModifier>(DeferredHolder<MapCodec<? extends IGlobalLootModifier>, MapCodec<T>> holder)
        implements RegistryHolder<MapCodec<? extends IGlobalLootModifier>, MapCodec<T>> {}
    
    public static void register(IEventBus bus) {LOOT_MODIFIER_SERIALIZERS.register(bus);}
}
