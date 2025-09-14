package net.mrhitech.artisanal.common.item;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraftforge.common.Tags;
import net.mrhitech.artisanal.Artisanal;
import org.jetbrains.annotations.NotNull;

import javax.annotation.ParametersAreNonnullByDefault;

@ParametersAreNonnullByDefault
public enum ArtisanalArmorMaterials implements ArmorMaterial {
    
    LAB("lab", 552, 0, 0, SoundEvents.ARMOR_EQUIP_LEATHER, Ingredient.of(Tags.Items.LEATHER), 0, 0);
    
    private final String name;
    private final int durability;
    private final int defense;
    private final int enchantmentValue;
    private final SoundEvent equipSound;
    private final Ingredient repairIngredient;
    private final int toughness;
    private final int knockbackResistance;
    
    ArtisanalArmorMaterials(
            String name,
            int durability,
            int defense,
            int enchantmentValue,
            SoundEvent equipSound,
            Ingredient repairIngredient,
            int toughness,
            int knockbackResistance
    ) {
        this.name = name;
        this.durability = durability;
        this.defense = defense;
        this.enchantmentValue = enchantmentValue;
        this.equipSound = equipSound;
        this.repairIngredient = repairIngredient;
        this.toughness = toughness;
        this.knockbackResistance = knockbackResistance;
    }
    
    @Override
    public int getDurabilityForType(ArmorItem.Type pType) {
        return durability;
    }
    
    @Override
    public int getDefenseForType(ArmorItem.Type pType) {
        return defense;
    }
    
    @Override
    public int getEnchantmentValue() {
        return enchantmentValue;
    }
    
    @Override
    public @NotNull SoundEvent getEquipSound() {
        return equipSound;
    }
    
    @Override
    public @NotNull Ingredient getRepairIngredient() {
        return repairIngredient;
    }
    
    @Override
    public @NotNull String getName() {
        return Artisanal.MOD_ID + ":" + name;
    }
    
    @Override
    public float getToughness() {
        return toughness;
    }
    
    @Override
    public float getKnockbackResistance() {
        return knockbackResistance;
    }
}
