package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Metal;
import net.minecraft.world.item.*;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.fluids.Waterlikes;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

import java.util.Locale;
import java.util.Map;
import java.util.function.Supplier;

public class ArtisanalItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(Artisanal.MOD_ID);

    public static final Map<Waterlikes, DeferredItem<Item>> FLUID_BUCKETS = Helpers.mapOf(Waterlikes.class, fluid ->
            register("bucket/" + fluid.getId(), () ->
                    new BucketItem(ArtisanalFluids.WATERLIKES.get(fluid).getSource(), new Item.Properties().craftRemainder(Items.BUCKET).stacksTo(1))));
    
    public static final DeferredItem<Item> ANIMAL_FAT = register("animal_fat", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> SUET = register("suet", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> PORK_FAT = register("pork_fat", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> BEAR_FAT = register("bear_fat", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> POULTRY_FAT = register("poultry_fat", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> SOAP = register("soap", () -> new Item(new Item.Properties()));
    
    public static final DeferredItem<Item> TRIMMED_FEATHER = register("trimmed_feather", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> SOAKED_FEATHER = register("soaked_feather", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> TEMPERED_FEATHER = register("tempered_feather", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> QUILL = register("quill", () -> new Item(new Item.Properties()));
    
    public static final DeferredItem<Item> CLEANED_SUGARCANE = register("food/cleaned_sugarcane", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    public static final DeferredItem<Item> BAGASSE = register("bagasse", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> PERISHABLE_SUGAR = register("perishable_sugar", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> NON_PERISHABLE_SUGAR = register("non_perishable_sugar", () -> new Item(new Item.Properties()));
    
    public static final DeferredItem<Item> MILK_FLAKES = register("milk_flakes", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> GOAT_MILK_FLAKES = register("goat_milk_flakes", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> YAK_MILK_FLAKES = register("yak_milk_flakes", () -> new Item(new Item.Properties()));
    
    public static final DeferredItem<Item> POWDERED_MILK = register("powdered_milk", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> POWDERED_GOAT_MILK = register("powdered_goat_milk", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> POWDERED_YAK_MILK = register("powdered_yak_milk", () -> new Item(new Item.Properties()));
    
    
    public static final Map<MagnifyingGlassMetal, DeferredItem<Item>> MAGNIFYING_GLASSES = Helpers.mapOf(MagnifyingGlassMetal.class, metal ->
            register("metal/magnifying_glass/" + metal.getSerializedName(), () -> new MagnifyingGlassItem(new Item.Properties().stacksTo(1))));
    
    public static final Map<MagnifyingGlassMetal, DeferredItem<Item>> MAGNIFYING_GLASS_FRAMES = Helpers.mapOf(MagnifyingGlassMetal.class, metal ->
            register("metal/magnifying_glass_frame/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    
    public static final DeferredItem<Item> TINPLATE = register("metal/tinplate", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> STAINLESS_STEELPLATE = register("metal/stainless_steelplate", () -> new Item(new Item.Properties()));
    
    public static final Map<CanMetal, DeferredItem<Item>> CANS = Helpers.mapOf(CanMetal.class, metal -> 
            register("metal/can/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    public static final Map<CanMetal, DeferredItem<Item>> SEALED_CANS = Helpers.mapOf(CanMetal.class, metal -> 
            register("metal/can/" + metal.getSerializedName() + "_sealed", () -> new Item(new Item.Properties())));
    public static final Map<CanMetal, DeferredItem<Item>> STERILIZED_CANS = Helpers.mapOf(CanMetal.class, metal -> 
            register("metal/can/" + metal.getSerializedName() + "_sterilized", () -> new Item(new Item.Properties())));
    public static final Map<CanMetal, DeferredItem<Item>> DIRTY_CANS = Helpers.mapOf(CanMetal.class, metal -> 
            register("metal/can/" + metal.getSerializedName() + "_dirty", () -> new Item(new Item.Properties())));
    public static final Map<CanMetal, DeferredItem<Item>> DENTED_CANS = Helpers.mapOf(CanMetal.class, metal -> 
            register("metal/can/" + metal.getSerializedName() + "_dented", () -> new Item(new Item.Properties())));
    public static final Map<CanMetal, DeferredItem<Item>> DIRTY_DENTED_CANS = Helpers.mapOf(CanMetal.class, metal -> 
            register("metal/can/" + metal.getSerializedName() + "_dirty_dented", () -> new Item(new Item.Properties())));
    
    public static final Map<Metal, DeferredItem<Item>> CAN_OPENERS = Helpers.mapOf(Metal.class,
            Metal.ItemType.AXE::has,
            metal -> register("metal/can_opener/" + metal.getSerializedName(), () -> new TieredItem(metal.toolTier(), new Item.Properties().durability(metal.toolTier().getUses()).rarity(metal.rarity()))));
    
    public static final Map<Metal, DeferredItem<Item>> CIRCLE_BLADES = Helpers.mapOf(Metal.class,
            Metal.ItemType.AXE::has,
            metal -> register("metal/circle_blade/" + metal.getSerializedName(), () -> new Item(new Item.Properties().rarity(metal.rarity()))));
    
    public static final Map<Metal, DeferredItem<Item>> BRICK_MOLDS = Helpers.mapOf(Metal.class,
            Metal.ItemType.AXE::has,
            metal -> register("metal/brick_mold/" + metal.getSerializedName(), () -> new Item(new Item.Properties().durability(metal.toolTier().getUses()).rarity(metal.rarity()))));
    
    public static final Map<SteelMetal, DeferredItem<Item>> STRIKERS = Helpers.mapOf(SteelMetal.class, metal ->
            register("metal/striker/" + metal.getSerializedName(), () -> new Item(new Item.Properties().rarity(metal.getRarity()))));
    
    public static final Map<SteelMetal, DeferredItem<Item>> FLINT_AND_STEELS = Helpers.mapOf(SteelMetal.class, metal -> !metal.equals(SteelMetal.STEEL), metal ->
            register("metal/flint_and/" + metal.getSerializedName(), () -> new FlintAndSteelItem(new Item.Properties().durability(metal.getTier().getUses()).rarity(metal.getRarity()))));
    
    public static final DeferredItem<Item> FLINT_AND_PYRITE = register("stone/flint_and/pyrite", () -> new FlintAndSteelItem(new Item.Properties().durability(70)));
    public static final DeferredItem<Item> FLINT_AND_CUT_PYRITE = register("stone/flint_and/cut_pyrite", () -> new FlintAndSteelItem(new Item.Properties().durability(70)));
    
    
    public static final DeferredItem<Item> DIRTY_JAR = register("dirty_jar", () -> new Item(new Item.Properties()));
    
    
    public static final DeferredItem<Item> DIRTY_SMALL_POT = register("ceramic/dirty_small_pot", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> SMALL_POT = register("ceramic/small_pot", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> UNFIRED_SMALL_POT = register("ceramic/unfired_small_pot", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> CLOSED_SMALL_POT = register("ceramic/closed_small_pot", () -> new Item(new Item.Properties()));
    
    public static final DeferredItem<Item> DIRTY_BOWL = register("dirty_bowl", () -> new Item(new Item.Properties()));
    
    public static final DeferredItem<Item> FRUIT_MASH = register("food/fruit_mash", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    
    public static final DeferredItem<Item> CARROT_MASH = register("food/carrot_mash", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    public static final DeferredItem<Item> TOMATO_MASH = register("food/tomato_mash", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    
    public static final Map<PicklableMetal, DeferredItem<Item>> PICKLED_DOUBLE_SHEETS = Helpers.mapOf(PicklableMetal.class, (metal) ->
            register("metal/pickled_double_sheet/" + metal.getMetal().name().toLowerCase(Locale.ROOT),
                    () -> new Item(new Item.Properties().rarity(metal.getMetal().rarity()))));
    
    public static final DeferredItem<Item> DIRTY_BURLAP_CLOTH = register("dirty_burlap_cloth", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> DIRTY_SILK_CLOTH = register("dirty_silk_cloth", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> DIRTY_WOOL_CLOTH = register("dirty_wool_cloth", () -> new Item(new Item.Properties()));
    
    
    public static final Map<Metal, DeferredItem<Item>> DISTILLERY_SPOUTS = Helpers.mapOf(Metal.class, ArtisanalItems::hasDistilleries, metal -> 
            register("metal/distillery_spout/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    public static final Map<Metal, DeferredItem<Item>> DISTILLERIES = Helpers.mapOf(Metal.class, ArtisanalItems::hasDistilleries, metal ->
            register("metal/distillery/" + metal.getSerializedName(), () -> new DistilleryItem(new Item.Properties(), metal)));
    
    public static final DeferredItem<Item> CINNABAR_POWDER = register("powder/cinnabar", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> BITUMEN = register("bitumen", () -> new Item(new Item.Properties()));
    
    
    public static final DeferredItem<Item> LEATHER_STRAP = register("leather_strap", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> LAB_GOGGLES_FRAME = register("lab_goggles_frame", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> LAB_GOGGLES_LENS = register("lab_goggles_lens", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> LAB_GOGGLES = register("lab_goggles", () -> new LabGogglesItem(ArtisanalArmorMaterials.LAB, new Item.Properties()));
    
    
    
    
    
    
    
    
    public static final DeferredItem<Item> DEBUG_ANY_ITEM = register("debug/any_item", () -> new Item(new Item.Properties()));
    public static final DeferredItem<Item> DEBUG_WHATEVER_FOOD_WAS_INSIDE_THE_CAN = register("debug/whatever_food_was_inside_the_can", () -> new Item(new Item.Properties()));
    
    
    public static <T extends Item> DeferredItem<T> register(String name, Supplier<T> supplier) {
        return ITEMS.register(name, supplier);
    }
    
    public static void register(IEventBus bus) {
        ITEMS.register(bus);
    }
    
    public static boolean hasDistilleries(Metal metal) {
        return Metal.ItemType.AXE_HEAD.has(metal) || metal == Metal.CAST_IRON || metal == Metal.BRASS;
    }

}
