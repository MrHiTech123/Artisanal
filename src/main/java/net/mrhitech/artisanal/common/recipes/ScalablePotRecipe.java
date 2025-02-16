package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import net.dries007.tfc.common.blockentities.PotBlockEntity;
import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.common.recipes.PotRecipe;
import net.dries007.tfc.common.recipes.SimplePotRecipe;
import net.dries007.tfc.common.recipes.ingredients.FluidStackIngredient;
import net.dries007.tfc.common.recipes.outputs.ItemStackProvider;
import net.dries007.tfc.util.JsonHelpers;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.fluids.capability.IFluidHandler;

import java.util.ArrayList;
import java.util.List;

public class ScalablePotRecipe extends SimplePotRecipe {
    
    public ScalablePotRecipe(ResourceLocation id, List<Ingredient> itemIngredients, FluidStackIngredient fluidIngredient, int duration, float minTemp, FluidStack outputFluid, List<ItemStackProvider> outputProviders)
    {
        super(id, itemIngredients, fluidIngredient, duration, minTemp, outputFluid, outputProviders);
    }
    
    @Override
    public Output getOutput(PotBlockEntity.PotInventory inventory)
    {
        int amountWasInPot = inventory.getFluidHandler().getFluidInTank(0).getAmount();
        return new ScalableOutput(outputFluid, outputProviders, fluidIngredient, amountWasInPot);
    }
    
    public RecipeSerializer<?> getSerializer() {
        return ArtisanalRecipeSerializers.SCALABLE_POT.get();
    }
    
    
    record ScalableOutput(FluidStack stack, List<ItemStackProvider> providers, FluidStackIngredient inputFluid, int amountWasInPot) implements Output {
        @Override
        public void onFinish(PotBlockEntity.PotInventory inventory) {
            int ingredientAmount = inputFluid.amount();
            // scaleFactor only takes the fluid amount into account, and should only be used in fluid-only recipes
            int scaleFactor = amountWasInPot / ingredientAmount;
            
            int maxItemsBase = providers.size();
            int maxItems = maxItemsBase * scaleFactor;
            
            for (int currentSlot = 0; currentSlot < Math.min(maxItems, inventory.getSlots() - PotBlockEntity.SLOT_EXTRA_INPUT_START); ++currentSlot) {
                final int i = currentSlot % maxItemsBase;
                final ItemStack input = inventory.getStackInSlot(i);
                inventory.setStackInSlot(currentSlot + PotBlockEntity.SLOT_EXTRA_INPUT_START, providers.get(i).getSingleStack(input));
            }
            FluidStack toFill = stack.copy();
            if (!toFill.isEmpty()) {
                toFill.setAmount(toFill.getAmount() * scaleFactor);
            }
            
            inventory.drain(FluidHelpers.BUCKET_VOLUME, IFluidHandler.FluidAction.EXECUTE);
            inventory.fill(toFill, IFluidHandler.FluidAction.EXECUTE);
        }
    }
    
    public static class Serializer extends PotRecipe.Serializer<ScalablePotRecipe> {
        
        @Override
        public void toNetwork(FriendlyByteBuf buffer, ScalablePotRecipe recipe) {
            super.toNetwork(buffer, recipe);
            buffer.writeFluidStack(recipe.outputFluid);
            buffer.writeVarInt(recipe.outputProviders.size());
            recipe.outputProviders.forEach(provider -> provider.toNetwork(buffer));
        }
        
        @Override
        protected ScalablePotRecipe fromJson(ResourceLocation recipeId, JsonObject json, List<Ingredient> ingredients, FluidStackIngredient fluidIngredient, int duration, float minTemp)
        {
            final FluidStack output = json.has("fluid_output") ? JsonHelpers.getFluidStack(json, "fluid_output") : FluidStack.EMPTY;
            final List<ItemStackProvider> stacks = new ArrayList<>(5);
            
            boolean anyProvidersDependOnInput = false;
            if (json.has("item_output"))
            {
                final JsonArray array = json.getAsJsonArray("item_output");
                for (JsonElement element : array)
                {
                    final ItemStackProvider provider = ItemStackProvider.fromJson(element.getAsJsonObject());
                    stacks.add(provider);
                    anyProvidersDependOnInput |= provider.dependsOnInput();
                }
            }
            if (stacks.size() > 5)
            {
                throw new JsonParseException("Cannot have more than five item stack outputs for pot recipe.");
            }
            if (anyProvidersDependOnInput && stacks.size() != ingredients.size())
            {
                throw new JsonParseException("At least one output is an ItemStackProvider that depends on the input. This is only allowed if there are (1) equal number of inputs and outputs, and (2) All inputs and outputs are the same");
            }
            return new ScalablePotRecipe(recipeId, ingredients, fluidIngredient, duration, minTemp, output, stacks);
        }
        
        @Override
        protected ScalablePotRecipe fromNetwork(ResourceLocation recipeId, FriendlyByteBuf buffer, List<Ingredient> ingredients, FluidStackIngredient fluidIngredient, int duration, float minTemp)
        {
            final FluidStack fluid = buffer.readFluidStack();
            final int size = buffer.readVarInt();
            List<ItemStackProvider> stacks = new ArrayList<>(size);
            if (size > 0)
            {
                for (int i = 0; i < size; i++)
                {
                    stacks.add(ItemStackProvider.fromNetwork(buffer));
                }
            }
            return new ScalablePotRecipe(recipeId, ingredients, fluidIngredient, duration, minTemp, fluid, stacks);
        }
        
        
    }
    
    
    
}
