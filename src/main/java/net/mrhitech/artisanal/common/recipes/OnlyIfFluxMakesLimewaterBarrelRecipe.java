package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonObject;
import net.dries007.tfc.common.recipes.BarrelRecipe;
import net.dries007.tfc.common.recipes.InstantBarrelRecipe;
import net.dries007.tfc.common.recipes.RecipeSerializerImpl;
import net.dries007.tfc.common.recipes.inventory.BarrelInventory;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.level.Level;
import net.mrhitech.artisanal.config.ArtisanalServerConfig;
import org.jetbrains.annotations.Nullable;

public class OnlyIfFluxMakesLimewaterBarrelRecipe extends InstantBarrelRecipe {
    
    public OnlyIfFluxMakesLimewaterBarrelRecipe(ResourceLocation id, Builder builder) {
        super(id, builder);
    }
    
    @Override
    public boolean matches(BarrelInventory container, @Nullable Level level) {
        if (ArtisanalServerConfig.SPEC.isLoaded() && !ArtisanalServerConfig.FLUX_MAKES_LIMEWATER.get()) {
            return false;
        }
        return super.matches(container, level);
        
    }
    
    public RecipeSerializer getSerializer() {
        return ArtisanalRecipeSerializers.ONLY_IF_FLUX_MAKES_LIMEWATER_BARREL.get();
    }
    
    public static class Serializer extends RecipeSerializerImpl<OnlyIfFluxMakesLimewaterBarrelRecipe> {
        public Serializer() {
        }
        
        public OnlyIfFluxMakesLimewaterBarrelRecipe fromJson(ResourceLocation recipeId, JsonObject json) {
            BarrelRecipe.Builder builder = Builder.fromJson(json);
            return new OnlyIfFluxMakesLimewaterBarrelRecipe(recipeId, builder);
        }
        
        public @Nullable OnlyIfFluxMakesLimewaterBarrelRecipe fromNetwork(ResourceLocation recipeId, FriendlyByteBuf buffer) {
            BarrelRecipe.Builder builder = Builder.fromNetwork(buffer);
            return new OnlyIfFluxMakesLimewaterBarrelRecipe(recipeId, builder);
        }
        
        public void toNetwork(FriendlyByteBuf buffer, OnlyIfFluxMakesLimewaterBarrelRecipe recipe) {
            Builder.toNetwork(recipe, buffer);
        }
    }
    
}
