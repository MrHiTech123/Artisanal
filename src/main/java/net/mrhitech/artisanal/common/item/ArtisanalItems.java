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
import java.util.function.Supplier;

public class ArtisanalItems {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, Artisanal.MOD_ID);

    public static final Map<Waterlikes, RegistryObject<Item>> FLUID_BUCKETS = Helpers.mapOfKeys(Waterlikes.class, fluid ->
            register("bucket/" + fluid.getId(), () -> new BucketItem(ArtisanalFluids.WATERLIKES.get(fluid).source(), new Item.Properties().craftRemainder(Items.BUCKET).stacksTo(1))));
    
    
    public static final RegistryObject<Item> SUET = register("suet", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> PORK_FAT = register("pork_fat", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> BEAR_FAT = register("bear_fat", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> POULTRY_FAT = register("poultry_fat", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SOAP = register("soap", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> TRIMMED_FEATHER = register("trimmed_feather", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SOAKED_FEATHER = register("soaked_feather", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> TEMPERED_FEATHER = register("tempered_feather", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> QUILL = register("quill", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> CLEANED_SUGARCANE = register("food/cleaned_sugarcane", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    public static final RegistryObject<Item> WET_BAGASSE = register("wet_bagasse", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DRY_BAGASSE = register("dry_bagasse", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> PERISHABLE_SUGAR = register("perishable_sugar", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> NON_PERISHABLE_SUGAR = register("non_perishable_sugar", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> MILK_FLAKES = register("milk_flakes", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> GOAT_MILK_FLAKES = register("goat_milk_flakes", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> YAK_MILK_FLAKES = register("yak_milk_flakes", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> POWDERED_MILK = register("powdered_milk", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> POWDERED_GOAT_MILK = register("powdered_goat_milk", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> POWDERED_YAK_MILK = register("powdered_yak_milk", () -> new Item(new Item.Properties()));
    
    
    public static final Map<MagnifyingGlassMetal, RegistryObject<Item>> MAGNIFYING_GLASSES = Helpers.mapOfKeys(MagnifyingGlassMetal.class, metal ->
            register("metal/magnifying_glass/" + metal.getSerializedName(), () -> new MagnifyingGlassItem(new Item.Properties().stacksTo(1))));
    
    public static final Map<MagnifyingGlassMetal, RegistryObject<Item>> MAGNIFYING_GLASS_FRAMES = Helpers.mapOfKeys(MagnifyingGlassMetal.class, metal ->
            register("metal/magnifying_glass_frame/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    
    public static final RegistryObject<Item> TINPLATE = register("metal/tinplate", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> TIN_CAN = register("metal/tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SEALED_TIN_CAN = register("metal/sealed_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> STERILIZED_TIN_CAN = register("metal/sterilized_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DIRTY_TIN_CAN = register("metal/dirty_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DENTED_TIN_CAN = register("metal/dented_tin_can", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> DIRTY_DENTED_TIN_CAN = register("metal/dirty_dented_tin_can", () -> new Item(new Item.Properties()));
    
    public static final Map<Metal.Default, RegistryObject<Item>> CAN_OPENERS = Helpers.mapOfKeys(Metal.Default.class,
            metal -> Metal.ItemType.AXE.has(metal),
            metal -> register("metal/can_opener/" + metal.getSerializedName(), () -> new TieredItem(metal.toolTier(), new Item.Properties().defaultDurability(metal.toolTier().getUses()))));
    
    public static final Map<Metal.Default, RegistryObject<Item>> CIRCLE_BLADES = Helpers.mapOfKeys(Metal.Default.class,
            metal -> Metal.ItemType.AXE.has(metal),
            metal -> register("metal/circle_blade/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    
    public static final Map<SteelMetal, RegistryObject<Item>> STRIKERS = Helpers.mapOfKeys(SteelMetal.class, metal ->
            register("metal/striker/" + metal.getSerializedName(), () -> new Item(new Item.Properties())));
    
    public static final Map<SteelMetal, RegistryObject<Item>> FLINT_ANDS = Helpers.mapOfKeys(SteelMetal.class, metal -> !metal.equals(SteelMetal.STEEL), metal ->
            register("metal/flint_and/" + metal.getSerializedName(), () -> new FlintAndSteelItem(new Item.Properties().durability(metal.getTier().getUses()))));
    
    public static final RegistryObject<Item> DIRTY_JAR = register("dirty_jar", () -> new Item(new Item.Properties()));
    
    
    public static final RegistryObject<Item> DIRTY_SMALL_POT = register("ceramic/dirty_small_pot", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> SMALL_POT = register("ceramic/small_pot", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> UNFIRED_SMALL_POT = register("ceramic/unfired_small_pot", () -> new Item(new Item.Properties()));
    public static final RegistryObject<Item> CLOSED_SMALL_POT = register("ceramic/closed_small_pot", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> DIRTY_BOWL = register("dirty_bowl", () -> new Item(new Item.Properties()));
    
    public static final RegistryObject<Item> FRUIT_MASH = register("food/fruit_mash", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    
    public static final RegistryObject<Item> CARROT_MASH = register("food/carrot_mash", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    public static final RegistryObject<Item> TOMATO_MASH = register("food/tomato_mash", () -> new Item(new Item.Properties().food(ArtisanalFoods.BLANK_FOOD)));
    
    
    public static <T extends Item> RegistryObject<T> register(String name, Supplier<T> supplier) {
        return ITEMS.register(name, supplier);
    }
    
    public static void register(IEventBus bus) {
        ITEMS.register(bus);
    }

}
