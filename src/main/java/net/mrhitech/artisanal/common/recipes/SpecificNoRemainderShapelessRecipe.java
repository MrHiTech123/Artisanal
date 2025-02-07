package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import net.dries007.tfc.common.recipes.AdvancedShapelessRecipe;
import net.dries007.tfc.common.recipes.RecipeHelpers;
import net.dries007.tfc.common.recipes.RecipeSerializerImpl;
import net.dries007.tfc.common.recipes.outputs.ItemStackProvider;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.JsonHelpers;
import net.minecraft.core.NonNullList;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.inventory.CraftingContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.Arrays;
import java.util.Iterator;

public class SpecificNoRemainderShapelessRecipe extends AdvancedShapelessRecipe {
    
    public SpecificNoRemainderShapelessRecipe(ResourceLocation id, String group, ItemStackProvider result, NonNullList<Ingredient> ingredients, @Nullable Ingredient primaryIngredient) {
        super(id, group, result, ingredients, primaryIngredient);
    }
    
    @Override
    public @NotNull NonNullList<ItemStack> getRemainingItems(CraftingContainer pContainer) {
        NonNullList<ItemStack> toReturn = NonNullList.withSize(pContainer.getContainerSize(), ItemStack.EMPTY);
        
        for(int i = 0; i < toReturn.size(); ++i) {
            ItemStack item = pContainer.getItem(i);
            if (primaryIngredient != null &&
                    Arrays.stream(primaryIngredient.getItems())
                            .map(ItemStack::getItem).anyMatch(item.getItem()::equals)) {
                toReturn.set(i, ItemStack.EMPTY);
            }
            else if (item.hasCraftingRemainingItem()) {
                toReturn.set(i, item.getCraftingRemainingItem());
            }
        }
        
        return toReturn;
    }
    
    
    public RecipeSerializer<?> getSerializer() {
        return ArtisanalRecipeSerializers.SPECIFIC_NO_REMAINDER_SHAPELESS.get();
    }
    
    public static class Serializer extends RecipeSerializerImpl<SpecificNoRemainderShapelessRecipe> {
        public Serializer() {
        }
        
        public SpecificNoRemainderShapelessRecipe fromJson(ResourceLocation id, JsonObject json) {
            String group = JsonHelpers.getAsString(json, "group", "");
            NonNullList<Ingredient> ingredients = RecipeHelpers.itemsFromJson(JsonHelpers.getAsJsonArray(json, "ingredients"));
            if (!ingredients.isEmpty() && ingredients.size() <= 9) {
                ItemStackProvider result = ItemStackProvider.fromJson(JsonHelpers.getAsJsonObject(json, "result"));
                Ingredient primaryIngredient = json.has("primary_ingredient") ? Ingredient.fromJson(json.get("primary_ingredient")) : null;
                return new SpecificNoRemainderShapelessRecipe(id, group, result, ingredients, primaryIngredient);
            } else {
                throw new JsonParseException("ingredients should be 1 to 9 ingredients long, it was: " + ingredients.size());
            }
        }
        
        public @Nullable SpecificNoRemainderShapelessRecipe fromNetwork(ResourceLocation id, FriendlyByteBuf buffer) {
            String group = buffer.readUtf();
            int size = buffer.readVarInt();
            NonNullList<Ingredient> ingredients = NonNullList.withSize(size, Ingredient.EMPTY);
            
            for(int j = 0; j < ingredients.size(); ++j) {
                ingredients.set(j, Ingredient.fromNetwork(buffer));
            }
            
            ItemStackProvider result = ItemStackProvider.fromNetwork(buffer);
            Ingredient primaryIngredient = (Ingredient) Helpers.decodeNullable(buffer, Ingredient::fromNetwork);
            return new SpecificNoRemainderShapelessRecipe(id, group, result, ingredients, primaryIngredient);
        }
        
        public void toNetwork(FriendlyByteBuf buffer, SpecificNoRemainderShapelessRecipe recipe) {
            buffer.writeUtf(recipe.getGroup());
            buffer.writeVarInt(recipe.getIngredients().size());
            Iterator var3 = recipe.getIngredients().iterator();
            
            while(var3.hasNext()) {
                Ingredient ingredient = (Ingredient)var3.next();
                ingredient.toNetwork(buffer);
            }
            
            recipe.result.toNetwork(buffer);
            Helpers.encodeNullable(recipe.primaryIngredient, buffer, Ingredient::toNetwork);
        }
    }
}
