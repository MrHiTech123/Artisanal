package net.mrhitech.artisanal.common.block;


import net.dries007.tfc.util.Helpers;
import net.minecraft.core.registries.Registries;
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
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;

import java.util.Map;

public class ArtisanalBlocks {
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, Artisanal.MOD_ID);
    
    public static final Map<Waterlikes, RegistryObject<LiquidBlock>> WATERLIKES = Helpers.mapOfKeys(Waterlikes.class, fluid ->
            BLOCKS.register("fluid/" + fluid.getId(), () -> new LiquidBlock(ArtisanalFluids.WATERLIKES.get(fluid).source(), BlockBehaviour.Properties.copy(Blocks.WATER))));
    
    public static void register(IEventBus bus) {
        BLOCKS.register(bus);
    }
    
    
    
}
