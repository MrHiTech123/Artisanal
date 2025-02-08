package net.mrhitech.artisanal.common.creative;

import net.dries007.tfc.common.TFCCreativeTabs;
import net.dries007.tfc.util.Metal;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.mrhitech.artisanal.common.Waterlikes;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.common.item.MagnifyingGlassMetal;
import net.mrhitech.artisanal.common.item.SteelMetal;

public class ArtisanalCreativeTabs {
    public static void AddCreative(BuildCreativeModeTabContentsEvent event) {
        
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            event.accept(ArtisanalItems.ANIMAL_FAT);
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
            
            event.accept(ArtisanalItems.PERISHABLE_SUGAR);
            event.accept(ArtisanalItems.NON_PERISHABLE_SUGAR);
        }
        
        if (event.getTabKey() == TFCCreativeTabs.FLORA.tab().getKey()) {
            event.accept(ArtisanalItems.WET_BAGASSE);
            event.accept(ArtisanalItems.DRY_BAGASSE);
        }
        
        if (event.getTabKey() == TFCCreativeTabs.FOOD.tab().getKey()) {
            event.accept(ArtisanalItems.CLEANED_SUGARCANE);
            event.accept(ArtisanalItems.FRUIT_MASH);
            event.accept(ArtisanalItems.CARROT_MASH);
            event.accept(ArtisanalItems.TOMATO_MASH);
            event.accept(ArtisanalItems.MILK_FLAKES);
            event.accept(ArtisanalItems.GOAT_MILK_FLAKES);
            event.accept(ArtisanalItems.YAK_MILK_FLAKES);
            event.accept(ArtisanalItems.POWDERED_MILK);
            event.accept(ArtisanalItems.POWDERED_GOAT_MILK);
            event.accept(ArtisanalItems.POWDERED_YAK_MILK);
            
            
            event.accept(ArtisanalItems.DIRTY_JAR);
            
            event.accept(ArtisanalItems.DIRTY_SMALL_POT);
            event.accept(ArtisanalItems.SMALL_POT);
            event.accept(ArtisanalItems.UNFIRED_SMALL_POT);
            event.accept(ArtisanalItems.CLOSED_SMALL_POT);
            
            event.accept(ArtisanalItems.DIRTY_BOWL);
        }
        
        if (event.getTabKey() == TFCCreativeTabs.METAL.tab().getKey()) {
            for (MagnifyingGlassMetal metal : MagnifyingGlassMetal.values()) {
                event.accept(ArtisanalItems.MAGNIFYING_GLASSES.get(metal));
                event.accept(ArtisanalItems.MAGNIFYING_GLASS_FRAMES.get(metal));
            }
            event.accept(ArtisanalItems.TINPLATE);
            event.accept(ArtisanalItems.TIN_CAN);
            event.accept(ArtisanalItems.SEALED_TIN_CAN);
            event.accept(ArtisanalItems.STERILIZED_TIN_CAN);
            event.accept(ArtisanalItems.DIRTY_TIN_CAN);
            event.accept(ArtisanalItems.DENTED_TIN_CAN);
            event.accept(ArtisanalItems.DIRTY_DENTED_TIN_CAN);
            
            for (Metal.Default metal : Metal.Default.values()) {
                if (Metal.ItemType.AXE.has(metal)) {
                    event.accept(ArtisanalItems.CAN_OPENERS.get(metal));
                    event.accept(ArtisanalItems.CIRCLE_BLADES.get(metal));
                }
            }
            
            for (SteelMetal metal : SteelMetal.values()) {
                event.accept(ArtisanalItems.STRIKERS.get(metal));
                if (!metal.equals(SteelMetal.STEEL)) {
                    event.accept(ArtisanalItems.FLINT_AND_STEELS.get(metal));
                }
            }
            
        }
        if (event.getTabKey() == TFCCreativeTabs.ROCKS.tab().getKey()) {
            event.accept(ArtisanalItems.FLINT_AND_PYRITE.get());
            event.accept(ArtisanalItems.FLINT_AND_CUT_PYRITE.get());
        }
    }
}
