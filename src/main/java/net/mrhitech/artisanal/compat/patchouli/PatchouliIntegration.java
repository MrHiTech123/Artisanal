package net.mrhitech.artisanal.compat.patchouli;

import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blocks.TFCBlockStateProperties;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.devices.QuernBlock;
import net.dries007.tfc.common.blocks.wood.Wood;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.MultiBlock;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.ArtisanalTags;
import vazkii.patchouli.api.IMultiblock;
import vazkii.patchouli.api.PatchouliAPI;

import java.util.Optional;
import java.util.function.Function;

public class PatchouliIntegration {
    
    public static void registerMultiBlocks() {
        registerMultiblock("juicing_apparatus", PatchouliIntegration::juicingApparatus);
    }
    
    private static IMultiblock juicingApparatus(PatchouliAPI.IPatchouliAPI api) {
        IMultiblock multiblock = api.makeMultiblock(new String[][] {
                {"Q"},
                {"0"},
                {"A"}
        },
        'Q', api.stateMatcher(TFCBlocks.QUERN.get().defaultBlockState().setValue(TFCBlockStateProperties.HAS_HANDSTONE, true)),
                '0', api.stateMatcher(TFCBlocks.WOODS.get(Wood.SEQUOIA).get(Wood.BlockType.BARREL).get().defaultBlockState()),
                'A', api.airMatcher()
                
        );
        
        sneakIntoMultiblock(multiblock).ifPresent(access -> {
            access.getBlockEntity(new BlockPos(0, 2, 0), TFCBlockEntities.QUERN.get()).ifPresent(quern -> {
                quern.setHandstoneFromOutsideWorld();
            });
        });
        
        return multiblock;
        
    }
    
    
    private static void registerMultiblock(String name, Function<PatchouliAPI.IPatchouliAPI, IMultiblock> factory)
    {
        final PatchouliAPI.IPatchouliAPI api = PatchouliAPI.get();
        api.registerMultiblock(new ResourceLocation(Artisanal.MOD_ID, name), factory.apply(api));
    }
    
    private static Optional<BlockGetter> sneakIntoMultiblock(IMultiblock multiblock)
    {
        if (multiblock instanceof BlockGetter access)
        {
            return Optional.of(access);
        }
        return Optional.empty();
    }
}
