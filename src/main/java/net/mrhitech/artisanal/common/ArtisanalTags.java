package net.mrhitech.artisanal.common;

import net.dries007.tfc.TerraFirmaCraft;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalTags {
    public static class ITEMS {
        public static final TagKey<Item> CRAFTING_CATALYSTS = create("crafting_catalysts");
        public static final TagKey<Item> USED_IN_JUICING = create("used_in_juicing");
        public static final TagKey<Item> TFC_BARRELS = create(TerraFirmaCraft.MOD_ID, "barrels");
        
        private static TagKey<Item> create(String modId, String itemId) {
            return TagKey.create(Registries.ITEM, new ResourceLocation(modId, itemId));
        }
        private static TagKey<Item> create(String id) {
            return create(Artisanal.MOD_ID, id);
        }
    }
}
