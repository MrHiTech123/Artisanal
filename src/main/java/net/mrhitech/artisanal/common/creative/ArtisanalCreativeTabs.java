package net.mrhitech.artisanal.common.creative;

import net.dries007.tfc.common.TFCCreativeTabs;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.mrhitech.artisanal.common.Waterlikes;
import net.mrhitech.artisanal.common.item.ArtisanalItems;

public class ArtisanalCreativeTabs {
    public static void AddCreative(BuildCreativeModeTabContentsEvent event) {
        
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            event.accept(ArtisanalItems.SUET);
            event.accept(ArtisanalItems.PORK_FAT);
            event.accept(ArtisanalItems.POULTRY_FAT);
            event.accept(ArtisanalItems.SOAP);
            
            event.accept(ArtisanalItems.TRIMMED_FEATHER);
            event.accept(ArtisanalItems.SOAKED_FEATHER);
            event.accept(ArtisanalItems.TEMPERED_FEATHER);
            event.accept(ArtisanalItems.QUILL);
            
            event.accept(ArtisanalItems.WET_BAGASSE);
            event.accept(ArtisanalItems.DRY_BAGASSE);
            
            event.accept(ArtisanalItems.MILK_FLAKES);
            event.accept(ArtisanalItems.POWDERED_MILK);
            
            
        }
        
        if (event.getTabKey() == TFCCreativeTabs.MISC.tab().getKey()) {
            for (Waterlikes fluid : Waterlikes.values()) {
                event.accept(ArtisanalItems.FLUID_BUCKETS.get(fluid));
            }
            event.accept(ArtisanalItems.SUET);
            event.accept(ArtisanalItems.PORK_FAT);
            event.accept(ArtisanalItems.BEAR_FAT);
            event.accept(ArtisanalItems.POULTRY_FAT);
            event.accept(ArtisanalItems.SOAP);
            
            event.accept(ArtisanalItems.TRIMMED_FEATHER);
            event.accept(ArtisanalItems.SOAKED_FEATHER);
            event.accept(ArtisanalItems.TEMPERED_FEATHER);
            event.accept(ArtisanalItems.QUILL);
        }
        
        if (event.getTabKey() == TFCCreativeTabs.FLORA.tab().getKey()) {
            event.accept(ArtisanalItems.WET_BAGASSE);
            event.accept(ArtisanalItems.DRY_BAGASSE);
        }
        
        if (event.getTabKey() == TFCCreativeTabs.FOOD.tab().getKey()) {
            event.accept(ArtisanalItems.CLEANED_SUGARCANE);
            event.accept(ArtisanalItems.MILK_FLAKES);
            event.accept(ArtisanalItems.POWDERED_MILK);
        }
        
        if (event.getTabKey() == TFCCreativeTabs.MISC.tab().getKey()) {
            event.accept(ArtisanalItems.PERISHABLE_SUGAR);
            event.accept(ArtisanalItems.NON_PERISHABLE_SUGAR);
        }
    }
}
