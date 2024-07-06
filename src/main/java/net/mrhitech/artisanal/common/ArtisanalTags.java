package net.mrhitech.artisanal.common;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalTags {
    public static class ITEMS {
        public static final TagKey<Item> CRAFTING_CATALYSTS = create("crafting_catalysts");
        
        private static TagKey<Item> create(String id) {
            return TagKey.create(Registries.ITEM, new ResourceLocation(Artisanal.MOD_ID, id));
        }
    }
}
