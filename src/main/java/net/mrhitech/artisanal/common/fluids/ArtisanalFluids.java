package net.mrhitech.artisanal.common.fluids;

import net.dries007.tfc.common.fluids.*;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.registry.RegistrationHelpers;
import net.minecraft.core.registries.Registries;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.pathfinder.PathType;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.SoundActions;
import net.neoforged.neoforge.fluids.BaseFlowingFluid;
import net.neoforged.neoforge.fluids.FluidType;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import org.joml.Vector3f;

import java.util.Map;
import java.util.function.Consumer;
import java.util.function.Function;
import java.awt.Color;

@SuppressWarnings("unchecked")
public class ArtisanalFluids {
    public static final DeferredRegister FLUID_TYPES = DeferredRegister.create(NeoForgeRegistries.Keys.FLUID_TYPES, Artisanal.MOD_ID);
    public static final DeferredRegister FLUIDS = DeferredRegister.create(Registries.FLUID, Artisanal.MOD_ID);
    
    public static final int ALPHA_MASK = 0xFF000000;
    
    public static final Map<Waterlikes, FluidHolder<FlowingFluid>> WATERLIKES = Helpers.mapOf(Waterlikes.class, fluid ->
        register(
            fluid.getId(),
            properties -> properties
                    .block(ArtisanalBlocks.WATERLIKES.get(fluid))
                    .bucket(ArtisanalItems.FLUID_BUCKETS.get(fluid)),
            waterLike()
                    .descriptionId("fluid.artisanal." + fluid.getId())
                    .canConvertToSource(false),
            MixingFluid.Source::new,
            MixingFluid.Flowing::new,
            fluid.getColor(),
            fluid.getShaderFogStart(),
            fluid.getShaderFogEnd()
        )
    );
    
    
    
    private static FluidType.Properties waterLike()
    {
        return FluidType.Properties.create()
                .adjacentPathType(PathType.WATER)
                .sound(SoundActions.BUCKET_FILL, SoundEvents.BUCKET_FILL)
                .sound(SoundActions.BUCKET_EMPTY, SoundEvents.BUCKET_EMPTY)
                .canConvertToSource(true)
                .canDrown(true)
                .canExtinguish(true)
                .canHydrate(true)
                .canPushEntity(true)
                .canSwim(true)
                .supportsBoating(true);
    }
    
    private static <F extends FlowingFluid> FluidHolder<F> register(String name, Consumer<BaseFlowingFluid.Properties> builder, FluidType.Properties typeProperties, Function<BaseFlowingFluid.Properties, F> sourceFactory, Function<BaseFlowingFluid.Properties, F> flowingFactory, Vector3f color, float shaderFogStart, float shaderFogEnd)
    {
        // Names `metal/foo` to `metal/flowing_foo`
        final int index = name.lastIndexOf('/');
        final String flowingName = index == -1 ? "flowing_" + name : name.substring(0, index) + "/flowing_" + name.substring(index + 1);
        
        return RegistrationHelpers.registerFluid(FLUID_TYPES, FLUIDS, name, name, flowingName, builder, () -> new ArtisanalFluidType(typeProperties, color, shaderFogStart, shaderFogEnd), sourceFactory, flowingFactory);
    }
    
    public static void register(IEventBus bus) {
        FLUIDS.register(bus);
        FLUID_TYPES.register(bus);
    }
    
    
}
