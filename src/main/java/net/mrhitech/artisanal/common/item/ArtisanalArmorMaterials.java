package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.registry.HolderHolder;
import net.minecraft.Util;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;
import net.mrhitech.artisanal.Artisanal;
import net.neoforged.neoforge.common.Tags;
import net.neoforged.neoforge.registries.DeferredRegister;
import org.jetbrains.annotations.NotNull;

import javax.annotation.ParametersAreNonnullByDefault;
import java.util.EnumMap;
import java.util.List;

@ParametersAreNonnullByDefault
public class ArtisanalArmorMaterials {
    
    public static final DeferredRegister<ArmorMaterial> ARMOR_MATERIALS = DeferredRegister.create(Registries.ARMOR_MATERIAL, Artisanal.MOD_ID);

    
    
    public static final Id LAB = register("lab", SoundEvents.ARMOR_EQUIP_LEATHER,552, 552, 552, 552, 0, 0, 0, 0, 0, 0, 0);
    
    private static Id register(
        String name,
        Holder<SoundEvent> equipSound,
        int feetDamage, int legDamage, int chestDamage, int headDamage,
        int feetReduction, int legReduction, int chestReduction, int headReduction,
        int enchantability, float toughness, float knockbackResistance
    ) {
        return new Id(ARMOR_MATERIALS.register(name, () -> new ArmorMaterial(
            Util.make(new EnumMap<>(ArmorItem.Type.class), map -> {
                map.put(ArmorItem.Type.BOOTS, feetReduction);
                map.put(ArmorItem.Type.LEGGINGS, legReduction);
                map.put(ArmorItem.Type.CHESTPLATE, chestReduction);
                map.put(ArmorItem.Type.HELMET, headReduction);
                map.put(ArmorItem.Type.BODY, chestReduction);
            }),
            enchantability,
            equipSound,
            () -> Ingredient.EMPTY,
            List.of(new ArmorMaterial.Layer(Helpers.identifier(name))),
            toughness,
            knockbackResistance
        )), feetDamage, legDamage, chestDamage, headDamage);
    }

    public record Id(
        Holder<ArmorMaterial> holder,
        int feetDamage,
        int legDamage,
        int chestDamage,
        int headDamage
    ) {}
    
    
}
