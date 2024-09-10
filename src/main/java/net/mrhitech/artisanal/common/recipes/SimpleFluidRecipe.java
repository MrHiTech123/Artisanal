//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonObject;
import java.util.Arrays;
import java.util.Collection;
import java.util.stream.Collectors;

import net.dries007.tfc.common.fluids.FluidHelpers;
import net.dries007.tfc.common.recipes.ISimpleRecipe;
import net.dries007.tfc.common.recipes.RecipeSerializerImpl;
import net.dries007.tfc.common.recipes.inventory.ItemStackInventory;
import net.dries007.tfc.common.recipes.outputs.ItemStackProvider;
import net.dries007.tfc.util.JsonHelpers;
import net.minecraft.core.RegistryAccess;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.Level;
import net.minecraftforge.fluids.FluidStack;
import org.jetbrains.annotations.Nullable;

public abstract class SimpleFluidRecipe implements ISimpleRecipe<ItemStackInventory> {
    protected final ResourceLocation id;
    protected final Ingredient ingredient;
    protected final FluidStack result;
    
    public SimpleFluidRecipe(ResourceLocation id, Ingredient ingredient, FluidStack result) {
        this.id = id;
        this.ingredient = ingredient;
        this.result = result;
    }
    
    public Collection<Item> getValidItems() {
        return (Collection)Arrays.stream(this.getIngredient().getItems()).map(ItemStack::getItem).collect(Collectors.toSet());
    }
    
    public boolean matches(ItemStackInventory wrapper, Level level) {
        return this.getIngredient().test(wrapper.getStack());
    }
    
    public FluidStack getResultFluid(@Nullable RegistryAccess access) {
        return FluidStack.EMPTY;
    }
    
    public FluidStack getResult() {
        return this.result.copy();
    }
    
    public ResourceLocation getId() {
        return this.id;
    }
    
    public boolean isSpecial() {
        return false;
    }
    
    public ItemStack assemble(ItemStackInventory wrapper, RegistryAccess access) {
        return ItemStack.EMPTY;
    }
    
    public FluidStack assembleFluid() {
        return this.result.copy();
    }
    
    public Ingredient getIngredient() {
        return this.ingredient;
    }
    
    public static class Serializer<R extends SimpleFluidRecipe> extends RecipeSerializerImpl<R> {
        private final Factory<R> factory;
        
        public Serializer(Factory<R> factory) {
            this.factory = factory;
        }
        
        public R fromJson(ResourceLocation recipeId, JsonObject json) {
            Ingredient ingredient = Ingredient.fromJson(JsonHelpers.get(json, "ingredient"));
            FluidStack result = JsonHelpers.getFluidStack(GsonHelper.getAsJsonObject(json, "result"));
            return this.factory.create(recipeId, ingredient, result);
        }
        
        public @Nullable R fromNetwork(ResourceLocation recipeId, FriendlyByteBuf buffer) {
            Ingredient ingredient = Ingredient.fromNetwork(buffer);
            FluidStack result = FluidStack.readFromPacket(buffer);
            return this.factory.create(recipeId, ingredient, result);
        }
        
        public void toNetwork(FriendlyByteBuf buffer, R recipe) {
            recipe.getIngredient().toNetwork(buffer);
            recipe.getResult().writeToPacket(buffer);
        }
        
        public interface Factory<R extends SimpleFluidRecipe> {
            R create(ResourceLocation var1, Ingredient var2, FluidStack var3);
        }
    }
}
