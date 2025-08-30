package net.mrhitech.artisanal.common;

import net.dries007.tfc.TerraFirmaCraft;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.material.Fluid;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalTags {
    public static class ITEMS {
        public static final TagKey<Item> CRAFTING_CATALYSTS = create("crafting_catalysts");
        public static final TagKey<Item> METAL_RODS = create("rods/metal");
        public static final TagKey<Item> TFC_BARRELS = create(TerraFirmaCraft.MOD_ID, "barrels");
        public static final TagKey<Item> DISTILLERIES = create("metal/distilleries");
        public static final TagKey<Item> FATS = create("fats");
        public static final TagKey<Item> SAFETY_GOGGLES = create("safety_goggles");
        
        private static TagKey<Item> create(String modId, String itemId) {
            return TagKey.create(Registries.ITEM, new ResourceLocation(modId, itemId));
        }
        private static TagKey<Item> create(String id) {
            return create(Artisanal.MOD_ID, id);
        }
    }
    
    public static final class BLOCKS {
        public static final TagKey<Block> TFC_BARRELS = create(TerraFirmaCraft.MOD_ID, "barrels");
        
        private static TagKey<Block> create(String modId, String itemId) {
            return TagKey.create(Registries.BLOCK, new ResourceLocation(modId, itemId));
        }
        private static TagKey<Block> create(String id) {
            return create(Artisanal.MOD_ID, id);
        }
    }
    
    public static class FLUIDS {
        public static final TagKey<Fluid> USABLE_IN_DRUM = create("usable_in_drum");
        public static final TagKey<Fluid> USABLE_IN_LAVA_DRUM = create("usable_in_lava_drum");
        public static final TagKey<Fluid> WATER_VISION = create("water_vision");
        
        private static TagKey<Fluid> create(String modId, String itemId) {
            return TagKey.create(Registries.FLUID, new ResourceLocation(modId, itemId));
        }
        private static TagKey<Fluid> create(String id) {
            return create(Artisanal.MOD_ID, id);
        }
    }
}
