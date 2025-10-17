package net.mrhitech.artisanal.util;

import com.mojang.realmsclient.dto.BackupList;
import net.dries007.tfc.common.TFCDamageSources;
import net.dries007.tfc.common.TFCEffects;
import net.dries007.tfc.util.Helpers;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageSources;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.util.advancements.ArtisanalAdvancements;

import java.util.function.Supplier;

public class SulfuricAcidEffects {
    public static boolean wearingSafetyGoggles(Player player) {
        
        if (player.isCreative()) return true;
        
        for (ItemStack armor : player.getArmorSlots()) {
            if (Helpers.isItem(armor.getItem(), ArtisanalTags.ITEMS.EYE_PROTECTION)) {
                return true;
            }
        }
        
        return false;
        
    }
    
    private static final Supplier<MobEffectInstance> BLINDNESS_EFFECT = () -> new MobEffectInstance(TFCEffects.INK.get(), MobEffectInstance.INFINITE_DURATION);
    
    public static void blindPlayer(Player player) {
        MobEffectInstance acidBlindness = BLINDNESS_EFFECT.get();
        player.addEffect(acidBlindness);
        
        if (player instanceof ServerPlayer serverPlayer) {
            ArtisanalAdvancements.BLINDED_BY_ACID.trigger(serverPlayer);
        }
    }
    
    public static void dealAcidDamage(Player player) {
        // Todo add
    }
    
    public static void getAcidInEyes(Player player) {
        if (!player.getActiveEffects().contains(BLINDNESS_EFFECT.get())) {
            dealAcidDamage(player);
        }
        blindPlayer(player);
    }
    
    public static void sprayAcidAtPlayerEyes(Player player) {
        if (!wearingSafetyGoggles(player)) {
            getAcidInEyes(player);
        }
    }
}
