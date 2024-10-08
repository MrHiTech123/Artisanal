package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.Metal;
import net.minecraft.world.item.*;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.Waterlikes;
import net.mrhitech.artisanal.common.fluids.ArtisanalFluids;

import java.util.Map;

public class ArtisanalItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, Artisanal.MOD_ID);

    public static final Map<Waterlikes, RegistryObject<Item>> FLUID_BUCKETS = Helpers.mapOfKeys(Waterlikes.class, fluid ->
            ITEMS.register("bucket/" + fluid.getId(), () -> new BucketItem(ArtisanalFluids.WATERLIKES.get(fluid).source(), new Item.Properties().craftRemainder(Items.BUCKET).stacksTo(1))));
    
    
    public static final RegistryObject<Item> SUET = ITEMS.register("suet", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> PORK_FAT = ITEMS.register("pork_fat", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> BEAR_FAT = ITEMS.register("bear_fat", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> POULTRY_FAT = ITEMS.register("poultry_fat", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SOAP = ITEMS.register("soap", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> TRIMMED_FEATHER = ITEMS.register("trimmed_feather", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SOAKED_FEATHER = ITEMS.register("soaked_feather", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> TEMPERED_FEATHER = ITEMS.register("tempered_feather", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> QUILL = ITEMS.register("quill", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> CLEANED_SUGARCANE = ITEMS.register("food/cleaned_sugarcane", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    public static final RegistryObject<Item> WET_BAGASSE = ITEMS.register("wet_bagasse", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DRY_BAGASSE = ITEMS.register("dry_bagasse", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> PERISHABLE_SUGAR = ITEMS.register("perishable_sugar", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> NON_PERISHABLE_SUGAR = ITEMS.register("non_perishable_sugar", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> MILK_FLAKES = ITEMS.register("milk_flakes", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> POWDERED_MILK = ITEMS.register("powdered_milk", () -> new Item(new Item.Properties()));
    
    public static final Map<MagnifyingGlassMetal, RegistryObject<Item>> MAGNIFYING_GLASSES = Helpers.mapOfKeys(MagnifyingGlassMetal.class, metal ->
            ITEMS.register("metal/magnifying_glass/" + metal.getSerializedName(), () -> new MagnifyingGlassItem(new Item.Properties().stacksTo(1))));
    
    public static final Map<MagnifyingGlassMetal, RegistryObject<Item>> MAGNIFYING_GLASS_FRAMES = Helpers.mapOfKeys(MagnifyingGlassMetal.class, metal ->
            ITEMS.register("metal/magnifying_glass_frame/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    
    public static final RegistryObject<Item> TINPLATE = ITEMS.register("metal/tinplate", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> TIN_CAN = ITEMS.register("metal/tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SEALED_TIN_CAN = ITEMS.register("metal/sealed_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> STERILIZED_TIN_CAN = ITEMS.register("metal/sterilized_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DIRTY_TIN_CAN = ITEMS.register("metal/dirty_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DENTED_TIN_CAN = ITEMS.register("metal/dented_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DIRTY_DENTED_TIN_CAN = ITEMS.register("metal/dirty_dented_tin_can", () -> new Item(new Item.Properties()));
    
    public static final Map<Metal.Default, RegistryObject<Item>> CAN_OPENERS = Helpers.mapOfKeys(Metal.Default.class,
            metal -> Metal.ItemType.AXE.has(metal),
            metal -> ITEMS.register("metal/can_opener/" + metal.getSerializedName(), () -> new TieredItem(metal.toolTier(), new Item.Properties().defaultDurability(metal.toolTier().getUses()))));
    
    public static final Map<Metal.Default, RegistryObject<Item>> CIRCLE_BLADES = Helpers.mapOfKeys(Metal.Default.class,
            metal -> Metal.ItemType.AXE.has(metal),
            metal -> ITEMS.register("metal/circle_blade/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    
    public static final Map<SteelMetal, RegistryObject<Item>> STRIKERS = Helpers.mapOfKeys(SteelMetal.class, metal ->
            ITEMS.register("metal/striker/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    
    public static final Map<SteelMetal, RegistryObject<Item>> FLINT_ANDS = Helpers.mapOfKeys(SteelMetal.class, metal -> !metal.equals(SteelMetal.STEEL), metal ->
            ITEMS.register("metal/flint_and/" + metal.getSerializedName(), () -> new FlintAndSteelItem(new Item.Properties().durability(metal.getTier().getUses()))));
    
    public static final RegistryObject<Item> DIRTY_JAR = ITEMS.register("dirty_jar", () -> new Item(new Item.Properties()));
    
    
    public static final RegistryObject<Item> DIRTY_SMALL_POT = ITEMS.register("ceramic/dirty_small_pot", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SMALL_POT = ITEMS.register("ceramic/small_pot", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> UNFIRED_SMALL_POT = ITEMS.register("ceramic/unfired_small_pot", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> CLOSED_SMALL_POT = ITEMS.register("ceramic/closed_small_pot", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> DIRTY_BOWL = ITEMS.register("dirty_bowl", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> FRUIT_MASH = ITEMS.register("food/fruit_mash", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    
    public static void register(IEventBus bus) {
        ITEMS.register(bus);
    }

}
