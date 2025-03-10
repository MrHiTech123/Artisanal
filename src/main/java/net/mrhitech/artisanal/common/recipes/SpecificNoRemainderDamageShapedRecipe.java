package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import net.dries007.tfc.common.recipes.AdvancedShapedRecipe;
import net.dries007.tfc.common.recipes.DamageInputsCraftingRecipe;
import net.dries007.tfc.common.recipes.RecipeHelpers;
import net.dries007.tfc.common.recipes.RecipeSerializerImpl;
import net.dries007.tfc.common.recipes.outputs.ItemStackProvider;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.JsonHelpers;
import net.minecraft.core.NonNullList;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.inventory.CraftingContainer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeSerializer;
import org.jetbrains.annotations.NotNull;

import java.util.Map;

public class SpecificNoRemainderDamageShapedRecipe extends AdvancedShapedRecipe {
    
    private int inputSlot;
    private ItemStackProvider result;
    public SpecificNoRemainderDamageShapedRecipe(ResourceLocation id, String group, int width, int height, NonNullList<Ingredient> recipeItems, ItemStackProvider result, int inputSlot) {
        super(id, group, width, height, recipeItems, result, inputSlot);
        this.result = result;
        this.inputSlot = inputSlot;
    }
    
    @Override
    public @NotNull NonNullList<ItemStack> getRemainingItems(CraftingContainer inventory) {
        NonNullList<ItemStack> toReturn = NonNullList.withSize(inventory.getContainerSize(), ItemStack.EMPTY);
        
        RecipeHelpers.setCraftingInput(inventory); //Maybe delete?
        final int matchSlot = RecipeHelpers.translateMatch(this, inputSlot, inventory);
        
        
        for(int i = 0; i < toReturn.size(); ++i) {
            ItemStack stack = inventory.getItem(i);
            if (i == matchSlot) {
                toReturn.set(i, ItemStack.EMPTY);
            }
            else if (stack.isDamageableItem())
            {
                toReturn.set(i, Helpers.damageCraftingItem(stack, 1).copy());
            }
            else if (DamageAndCatalystRecipe.isUnbreakable(stack)) // unbreakable items are not damageable, but should still be able to be used in crafting
            {
                toReturn.set(i, stack.copy());
            }
            else if (stack.hasCraftingRemainingItem()) {
                toReturn.set(i, stack.getCraftingRemainingItem());
            }
        }
        
        return toReturn;
    }
    
    
    public RecipeSerializer<?> getSerializer() {
        return ArtisanalRecipeSerializers.SPECIFIC_NO_REMAINDER_DAMAGE_SHAPED.get();
    }
    
    public static class Serializer extends RecipeSerializerImpl<SpecificNoRemainderDamageShapedRecipe>
    {
        @Override
        public SpecificNoRemainderDamageShapedRecipe fromJson(ResourceLocation recipeId, JsonObject json)
        {
            final String group = GsonHelper.getAsString(json, "group", "");
            final Map<String, Ingredient> keys = RecipeHelpers.keyFromJson(GsonHelper.getAsJsonObject(json, "key"));
            final String[] pattern = RecipeHelpers.shrink(RecipeHelpers.patternFromJson(GsonHelper.getAsJsonArray(json, "pattern")));
            final int width = pattern[0].length();
            final int height = pattern.length;
            final NonNullList<Ingredient> recipeItems = RecipeHelpers.dissolvePattern(pattern, keys, width, height);
            final ItemStackProvider providerResult = ItemStackProvider.fromJson(JsonHelpers.getAsJsonObject(json, "result"));
            final int inputRow = JsonHelpers.getAsInt(json, "input_row");
            final int inputCol = JsonHelpers.getAsInt(json, "input_column");
            if (inputRow < 0 || inputRow >= height)
            {
                throw new JsonParseException("input_row must be in the range [0, height)");
            }
            if (inputCol < 0 || inputCol >= width)
            {
                throw new JsonParseException("input_column must be in the range [0, width)");
            }
            final int inputSlot = RecipeHelpers.dissolveRowColumn(inputRow, inputCol, width);
            return new SpecificNoRemainderDamageShapedRecipe(recipeId, group, width, height, recipeItems, providerResult, inputSlot);
        }
        
        @Override
        public SpecificNoRemainderDamageShapedRecipe fromNetwork(ResourceLocation recipeId, FriendlyByteBuf buffer)
        {
            final int width = buffer.readVarInt();
            final int height = buffer.readVarInt();
            final String group = buffer.readUtf();
            final NonNullList<Ingredient> recipeItems = NonNullList.withSize(width * height, Ingredient.EMPTY);
            
            for (int k = 0; k < recipeItems.size(); ++k)
            {
                recipeItems.set(k, Ingredient.fromNetwork(buffer));
            }
            
            final ItemStackProvider provider = ItemStackProvider.fromNetwork(buffer);
            final int inputSlot = buffer.readVarInt();
            return new SpecificNoRemainderDamageShapedRecipe(recipeId, group, width, height, recipeItems, provider, inputSlot);
        }
        
        @Override
        public void toNetwork(FriendlyByteBuf buffer, SpecificNoRemainderDamageShapedRecipe recipe)
        {
            buffer.writeVarInt(recipe.getWidth());
            buffer.writeVarInt(recipe.getHeight());
            buffer.writeUtf(recipe.getGroup());
            
            for (Ingredient ingredient : recipe.getIngredients())
            {
                ingredient.toNetwork(buffer);
            }
            
            recipe.result.toNetwork(buffer);
            buffer.writeVarInt(recipe.inputSlot);
        }
    }
}
