package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonObject;
import net.dries007.tfc.common.recipes.ISimpleRecipe;
import net.dries007.tfc.common.recipes.RecipeSerializerImpl;
import net.dries007.tfc.common.recipes.WeldingRecipe;
import net.dries007.tfc.common.recipes.ingredients.FluidStackIngredient;
import net.dries007.tfc.common.recipes.ingredients.ItemStackIngredient;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackProvider;
import net.dries007.tfc.util.JsonHelpers;
import net.dries007.tfc.util.collections.IndirectHashCollection;
import net.minecraft.core.NonNullList;
import net.minecraft.core.RegistryAccess;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.CraftingTableBlock;
import net.minecraftforge.fluids.FluidStack;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.annotation.ParametersAreNonnullByDefault;
import java.util.Arrays;
import java.util.Collection;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;


@ParametersAreNonnullByDefault
public class DistilleryRecipe implements ISimpleRecipe<DistilleryBlockEntity.DistilleryInventory> {
    
    private final ResourceLocation id;
    private final Ingredient itemStackIngredient;
    private final FluidStackIngredient fluidStackIngredient;
    private final ItemStackProvider resultItemStack;
    private final FluidStack resultFluidStack;
    private final ItemStackProvider leftoverItemStack;
    private final FluidStack leftoverFluidStack;
    private final int minTemp;
    private final int duration;
    
    
    public DistilleryRecipe(
            ResourceLocation id, 
            Ingredient itemStackIngredient, 
            FluidStackIngredient fluidStackIngredient, 
            ItemStackProvider outputItemStack, 
            FluidStack outputFluidStack,
            ItemStackProvider leftoverItemStack,
            FluidStack leftoverFluidStack,
            int minTemp,
            int duration
    ) {
        this.id = id;
        this.itemStackIngredient = itemStackIngredient;
        this.fluidStackIngredient = fluidStackIngredient;
        this.resultItemStack = outputItemStack;
        this.resultFluidStack = outputFluidStack;
        this.leftoverItemStack = leftoverItemStack;
        this.leftoverFluidStack = leftoverFluidStack;
        this.minTemp = minTemp;
        this.duration = duration;
    }
    
    @Override
    public boolean matches(DistilleryBlockEntity.DistilleryInventory distilleryInventory, Level level) {
        return itemStackIngredient.test(distilleryInventory.getStackInSlot(0)) &&
                fluidStackIngredient.test(distilleryInventory.getFluidInTank(0));
    }
    
    public static Optional<DistilleryRecipe> fromInventory(Level level, DistilleryBlockEntity.DistilleryInventory inventory) {
        return level.getRecipeManager().getRecipeFor(ArtisanalRecipeTypes.DISTILLERY.get(), inventory, level);
    }
    
    
    public Ingredient getIngredientItem() {
        return itemStackIngredient;
    }
    
    public FluidStackIngredient getIngredientFluid() {
        return fluidStackIngredient;
    }
    
    @Override
    public ItemStack getResultItem(RegistryAccess pRegistryAccess) {
        throw new RuntimeException("This version of getResultItem should not be running; why would we need registry access!?");
        // return getResultItem(ItemStack.EMPTY);
        CraftingTableBlock
    }
    
    public Optional<ItemStack> getResultItem(ItemStack input) {
        return Optional.of(resultItemStack.getStack(input));
    }
    
    
    public Optional<FluidStack> getResultFluid() {
        return Optional.of(resultFluidStack.copy());
    }
    
    public Optional<ItemStack> getLeftoverItem(ItemStack input) {
        return Optional.of(leftoverItemStack.getStack(input));
    }
    
    public Optional<FluidStack> getLeftoverFluid() {
        return Optional.of(leftoverFluidStack.copy());
    }
    
    public boolean isHotEnough(float distilleryTemp) {
        return distilleryTemp >= minTemp;
    }
    
    public int getDuration() {
        return duration;
    }
    
    
    @Override
    public ResourceLocation getId() {
        return id;
    }
    
    @Override
    public RecipeSerializer<?> getSerializer() {
        return ArtisanalRecipeSerializers.DISTILLERY.get();
    }
    
    @Override
    public RecipeType<?> getType() {
        return ArtisanalRecipeTypes.DISTILLERY.get();
    }
    
    public static <T> Function<T, JsonObject> nullIfArgIsNull(Function<T, JsonObject> function) {
        return arg -> (arg == null)? null : function.apply(arg);
    }
    
    public static class Serializer extends RecipeSerializerImpl<DistilleryRecipe> {
        @Override
        public @NotNull DistilleryRecipe fromJson(ResourceLocation id, JsonObject json) {
            Ingredient itemStackIngredient = json.has("input_item")? Ingredient.fromJson(JsonHelpers.get(json, "input_item")) : Ingredient.EMPTY;
            FluidStackIngredient fluidStackIngredient = json.has("input_fluid")? FluidStackIngredient.fromJson(GsonHelper.getAsJsonObject(json, "input_fluid", null)) : FluidStackIngredient.EMPTY;
            ItemStackProvider resultItemStack = json.has("result_item")? ItemStackProvider.fromJson(GsonHelper.getAsJsonObject(json, "result_item")) : ItemStackProvider.empty();
            FluidStack resultFluidStack = json.has("result_fluid")? JsonHelpers.getFluidStack(GsonHelper.getAsJsonObject(json, "result_fluid")) : FluidStack.EMPTY;
            ItemStackProvider leftoverItemStack = json.has("leftover_item")? ItemStackProvider.fromJson(GsonHelper.getAsJsonObject(json, "leftover_item")) : ItemStackProvider.empty();
            FluidStack leftoverFluidStack = json.has("leftover_fluid")? JsonHelpers.getFluidStack(GsonHelper.getAsJsonObject(json, "leftover_fluid")) : FluidStack.EMPTY;
            int minTemp = json.get("min_temp").getAsInt();
            int durationTicks = json.get("duration").getAsInt();
            
            return new DistilleryRecipe(
                    id,
                    itemStackIngredient,
                    fluidStackIngredient,
                    resultItemStack,
                    resultFluidStack,
                    leftoverItemStack,
                    leftoverFluidStack,
                    minTemp,
                    durationTicks
            );
            
        }
        
        @Override
        public @Nullable DistilleryRecipe fromNetwork(ResourceLocation id, FriendlyByteBuf buffer) {
            Ingredient itemStackIngredient = Ingredient.fromNetwork(buffer);
            FluidStackIngredient fluidStackIngredient = FluidStackIngredient.fromNetwork(buffer);
            ItemStackProvider resultItemStack = ItemStackProvider.fromNetwork(buffer);
            FluidStack resultFluidStack = FluidStack.readFromPacket(buffer);
            ItemStackProvider leftoverItemStack = ItemStackProvider.fromNetwork(buffer);
            FluidStack leftoverFluidStack = FluidStack.readFromPacket(buffer);
            int minTemp = buffer.readVarInt();
            int durationTicks = buffer.readVarInt();
            
            return new DistilleryRecipe(
                    id,
                    itemStackIngredient,
                    fluidStackIngredient,
                    resultItemStack,
                    resultFluidStack,
                    leftoverItemStack,
                    leftoverFluidStack,
                    minTemp,
                    durationTicks
            );
        }
        
        @Override
        public void toNetwork(FriendlyByteBuf buffer, DistilleryRecipe recipe) {
            recipe.itemStackIngredient.toNetwork(buffer);
            recipe.fluidStackIngredient.toNetwork(buffer);
            buffer.writeVarInt(recipe.minTemp);
            buffer.writeVarInt(recipe.duration);
            
        }
    }
    
    
}
