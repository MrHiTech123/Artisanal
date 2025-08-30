package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonObject;
import net.dries007.tfc.common.TFCEffects;
import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blocks.TFCBlockStateProperties;
import net.dries007.tfc.common.recipes.BarrelRecipe;
import net.dries007.tfc.common.recipes.InstantBarrelRecipe;
import net.dries007.tfc.common.recipes.RecipeSerializerImpl;
import net.dries007.tfc.common.recipes.inventory.BarrelInventory;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.util.ArtisanalHelpers;
import net.mrhitech.artisanal.util.IBarrelInventoryMixin;
import org.jetbrains.annotations.Nullable;

import javax.annotation.ParametersAreNonnullByDefault;
import java.util.List;

@ParametersAreNonnullByDefault
public class SpraysAcidInEyesInstantBarrelRecipe extends InstantBarrelRecipe {
    
    public SpraysAcidInEyesInstantBarrelRecipe(ResourceLocation id, Builder builder) {
        super(id, builder);
    }
    
    
    private static boolean topObstructed(BarrelBlockEntity barrel) {
        
        if (barrel.getBlockState().getValue(TFCBlockStateProperties.SEALED)) {
            return true;
        }
        
        Level level = barrel.getLevel();
        if (level == null) return true;
        BlockPos pos = barrel.getBlockPos();
        BlockPos oneAbove = new BlockPos(pos.getX(), pos.getY() + 1, pos.getZ());
        
        if (level.getBlockState(oneAbove).getBlock().equals(Blocks.AIR)) {
            return true;
        }
        
        return false;
    }
    
    private static boolean wearingSafetyGoggles(Player player) {
        
        for (ItemStack armor : player.getArmorSlots()) {
            if (Helpers.isItem(armor.getItem(), ArtisanalTags.ITEMS.SAFETY_GOGGLES)) {
                return true;
            }
        }
        
        return false;
        
    }
    
    private static void blindPlayer(Player player) {
        MobEffectInstance acidBlindness = 
                new MobEffectInstance(TFCEffects.INK.get(), MobEffectInstance.INFINITE_DURATION);
        player.addEffect(acidBlindness);
    }
    
    private static void maybeBlindPlayer(Player player) {
        if (!wearingSafetyGoggles(player)) {
            blindPlayer(player);
        }
    }
    
    @Override
    public void assembleOutputs(BarrelInventory inventory) {
        super.assembleOutputs(inventory);
        if (inventory instanceof BarrelBlockEntity.BarrelInventory barrelBlockEntityInventory) {
            BarrelBlockEntity barrel = ((IBarrelInventoryMixin)barrelBlockEntityInventory).artisanal$getBlockEntity();
            
            if (barrel == null) return;
            if (topObstructed(barrel)) return;
            
            
            Level level = barrel.getLevel();
            BlockPos pos = barrel.getBlockPos();
            BlockPos twoAbove = new BlockPos(pos.getX(), pos.getY() + 2, pos.getZ());
            
            if (level == null) return;
            List<Player> playersNearby = ArtisanalHelpers.playersNear(level, twoAbove, 5, 8);
            
            for (Player player : playersNearby) {
                maybeBlindPlayer(player);
            }
        }
    }
    
    @Override
    public RecipeSerializer<?> getSerializer() {
        return ArtisanalRecipeSerializers.SPRAYS_ACID_IN_EYES_INSTANT_BARREL_RECIPE.get();
    }
    
    public static class Serializer extends RecipeSerializerImpl<SpraysAcidInEyesInstantBarrelRecipe> {
        public Serializer() {
        }

        public SpraysAcidInEyesInstantBarrelRecipe fromJson(ResourceLocation recipeId, JsonObject json) {
            BarrelRecipe.Builder builder = Builder.fromJson(json);
            return new SpraysAcidInEyesInstantBarrelRecipe(recipeId, builder);
        }

        public @Nullable SpraysAcidInEyesInstantBarrelRecipe fromNetwork(ResourceLocation recipeId, FriendlyByteBuf buffer) {
            BarrelRecipe.Builder builder = Builder.fromNetwork(buffer);
            return new SpraysAcidInEyesInstantBarrelRecipe(recipeId, builder);
        }

        public void toNetwork(FriendlyByteBuf buffer, SpraysAcidInEyesInstantBarrelRecipe recipe) {
            Builder.toNetwork(recipe, buffer);
        }
    }
    
}
