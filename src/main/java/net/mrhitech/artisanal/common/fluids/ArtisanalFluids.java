package net.mrhitech.artisanal.common.fluids;

import net.dries007.tfc.common.fluids.*;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.registry.RegistrationHelpers;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.pathfinder.BlockPathTypes;
import net.minecraftforge.common.SoundActions;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fluids.FluidType;
import net.minecraftforge.fluids.ForgeFlowingFluid;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.block.ArtisanalBlocks;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

import java.util.Map;
import java.util.function.Consumer;
import java.util.function.Function;

@SuppressWarnings("unchecked")
public class ArtisanalFluids {
    public static final DeferredRegister FLUID_TYPES = DeferredRegister.create(ForgeRegistries.Keys.FLUID_TYPES, Artisanal.MOD_ID);
    public static final DeferredRegister FLUIDS = DeferredRegister.create(ForgeRegistries.FLUIDS, Artisanal.MOD_ID);
    
    public static final int ALPHA_MASK = 0xFF000000;
    
    public static final Map<Waterlikes, FluidRegistryObject<FlowingFluid>> WATERLIKES = Helpers.mapOfKeys(Waterlikes.class, fluid ->
            register(
            fluid.getId(),
            properties -> properties
                    .block(ArtisanalBlocks.WATERLIKES.get(fluid))
                    .bucket(ArtisanalItems.FLUID_BUCKETS.get(fluid)),
            waterLike()
                    .descriptionId("fluid.artisanal." + fluid.getId())
                    .canConvertToSource(false),
            new FluidTypeClientProperties(fluid.getColor(), TFCFluids.WATER_STILL, TFCFluids.WATER_FLOW, TFCFluids.WATER_OVERLAY, null),
            MixingFluid.Source::new,
            MixingFluid.Flowing::new
    ));
    
    
    
    private static FluidType.Properties waterLike()
    {
        return FluidType.Properties.create()
                .adjacentPathType(BlockPathTypes.WATER)
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
    
    private static <F extends FlowingFluid> FluidRegistryObject<F> register(String name, Consumer<ForgeFlowingFluid.Properties> builder, FluidType.Properties typeProperties, FluidTypeClientProperties clientProperties, Function<ForgeFlowingFluid.Properties, F> sourceFactory, Function<ForgeFlowingFluid.Properties, F> flowingFactory)
    {
        // Names `metal/foo` to `metal/flowing_foo`
        final int index = name.lastIndexOf('/');
        final String flowingName = index == -1 ? "flowing_" + name : name.substring(0, index) + "/flowing_" + name.substring(index + 1);
        
        return RegistrationHelpers.registerFluid(FLUID_TYPES, FLUIDS, name, name, flowingName, builder, () -> new ExtendedFluidType(typeProperties, clientProperties), sourceFactory, flowingFactory);
    }
    
    public static void register(IEventBus bus) {
        FLUIDS.register(bus);
        FLUID_TYPES.register(bus);
    }
    
    
}
