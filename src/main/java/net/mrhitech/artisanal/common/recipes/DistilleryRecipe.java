package net.mrhitech.artisanal.common.recipes;

import com.google.gson.JsonObject;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.dries007.tfc.common.recipes.ISimpleRecipe;
import net.dries007.tfc.common.recipes.PotRecipe;
import net.dries007.tfc.common.recipes.RecipeSerializerImpl;
import net.dries007.tfc.common.recipes.WeldingRecipe;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackProvider;
import net.dries007.tfc.util.collections.IndirectHashCollection;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.core.RegistryAccess;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeHolder;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.CraftingTableBlock;
import net.mrhitech.artisanal.common.blockentities.DistilleryBlockEntity;
import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.crafting.SizedFluidIngredient;
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
    
    public static final MapCodec<DistilleryRecipe> CODEC = RecordCodecBuilder.mapCodec(instance -> instance.group(
            Ingredient.CODEC.fieldOf("input_item").forGetter(c -> c.itemStackIngredient),
            SizedFluidIngredient.FLAT_CODEC.fieldOf("input_fluid").forGetter(c -> c.fluidStackIngredient),
            ItemStackProvider.CODEC.fieldOf("result_item").forGetter(c -> c.resultItemStack),
            FluidStack.CODEC.fieldOf("result_fluid").forGetter(c -> c.resultFluidStack),
            ItemStackProvider.CODEC.fieldOf("leftover_item").forGetter(c -> c.leftoverItemStack),
            FluidStack.CODEC.fieldOf("leftover_fluid").forGetter(c -> c.leftoverFluidStack),
            Codec.INT.fieldOf("min_temp").forGetter(c -> c.minTemp),
            Codec.INT.fieldOf("duration").forGetter(c -> c.duration)
    ).apply(instance, DistilleryRecipe::new));
    
    
    protected final Ingredient itemStackIngredient;
    protected final SizedFluidIngredient fluidStackIngredient;
    protected final ItemStackProvider resultItemStack;
    protected final FluidStack resultFluidStack;
    protected final ItemStackProvider leftoverItemStack;
    protected final FluidStack leftoverFluidStack;
    protected final int minTemp;
    protected final int duration;
    
    
    public DistilleryRecipe(
            Ingredient itemStackIngredient, 
            SizedFluidIngredient fluidStackIngredient, 
            ItemStackProvider outputItemStack, 
            FluidStack outputFluidStack,
            ItemStackProvider leftoverItemStack,
            FluidStack leftoverFluidStack,
            int minTemp,
            int duration
    ) {
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
        return itemStackIngredient.test(distilleryInventory.getStackInSlot(DistilleryBlockEntity.SLOT_INPUT_ITEM)) &&
                fluidStackIngredient.test(distilleryInventory.getFluidInTank(DistilleryBlockEntity.TANK_INPUT_FLUID));
    }
    
    @Override
    public @NotNull ItemStack assemble(DistilleryBlockEntity.DistilleryInventory distilleryInventory, HolderLookup.Provider provider) {
        return ItemStack.EMPTY;
    }
    
    public static Optional<DistilleryRecipe> fromInventory(Level level, DistilleryBlockEntity.DistilleryInventory inventory) {
        return level.getRecipeManager().getRecipeFor(ArtisanalRecipeTypes.DISTILLERY.get(), inventory, level).map(RecipeHolder::value);
    }
    
    public Ingredient getIngredientItem() {
        return itemStackIngredient;
    }
    
    public SizedFluidIngredient getIngredientFluid() {
        return fluidStackIngredient;
    }
    
    
    @Override
    public @NotNull ItemStack getResultItem(HolderLookup.Provider registries) {
        return getResultItem().orElseGet(() -> ItemStack.EMPTY);
        // throw new RuntimeException("This version of getResultItem should not be running; why would we need registry access!?");
        // return getResultItem(ItemStack.EMPTY);
    }
    
    private int scaleOfInputItem(ItemStack inputItem) {
        if (itemStackIngredient.isEmpty() || inputItem.isEmpty()) {
            return Integer.MAX_VALUE;
        }
        else {
            // TODO: Check if works
            return inputItem.getCount() / itemStackIngredient.getItems()[0].getCount();
        }
    }
    
    private int scaleOfInputFluid(FluidStack inputFluid) {
        if (fluidStackIngredient.amount() == 0 || inputFluid.isEmpty()) {
            return Integer.MAX_VALUE;
        }
        else {
            return inputFluid.getAmount() / fluidStackIngredient.amount();
        }
    }
    
    private int scaleOfInput(ItemStack inputItem, FluidStack inputFluid) {
        int toReturn = Math.min(scaleOfInputItem(inputItem), scaleOfInputFluid(inputFluid));
        if (toReturn == Integer.MAX_VALUE) {
            toReturn = 1;
        }
        return toReturn;
    }
    
    private ItemStack scaleResult(ItemStack unscaledResult, int scale) {
        return new ItemStack(unscaledResult.getItem(), unscaledResult.getCount() * scale);
    }
    
    private FluidStack scaleResult(FluidStack unscaledResult, int scale) {
        return new FluidStack(unscaledResult.getFluid(), unscaledResult.getAmount() * scale);
    }
    
    public Optional<ItemStack> getResultItem() {
        return getResultItem(ItemStack.EMPTY, FluidStack.EMPTY);
    }
    
    public Optional<FluidStack> getResultFluid() {
        return getResultFluid(ItemStack.EMPTY, FluidStack.EMPTY);
    }
    
    public Optional<ItemStack> getLeftoverItem() {
        return getLeftoverItem(ItemStack.EMPTY, FluidStack.EMPTY);
    }
    
    public Optional<FluidStack> getLeftoverFluid() {
        return getLeftoverFluid(ItemStack.EMPTY, FluidStack.EMPTY);
    }
    
    
    
    
    public Optional<ItemStack> getResultItem(ItemStack inputItem, FluidStack inputFluid) {
        ItemStack unscaledResult = resultItemStack.getStack(inputItem);
        
        int scale = scaleOfInput(inputItem, inputFluid);
        ItemStack scaledResult = scaleResult(unscaledResult, scale);
        
        return Optional.of(scaledResult);
    }
    
    
    public Optional<FluidStack> getResultFluid(ItemStack inputItem, FluidStack inputFluid) {
        FluidStack unscaledResult = resultFluidStack.copy();
        
        int scale = scaleOfInput(inputItem, inputFluid);
        FluidStack scaledResult = scaleResult(unscaledResult, scale);
        
        return Optional.of(scaledResult);
    }
    
    public Optional<ItemStack> getLeftoverItem(ItemStack inputItem, FluidStack inputFluid) {
        ItemStack unscaledResult = leftoverItemStack.getStack(inputItem);
        
        int scale = scaleOfInput(inputItem, inputFluid);
        ItemStack scaledResult = scaleResult(unscaledResult, scale);
        
        return Optional.of(scaledResult);
    }
    
    public Optional<FluidStack> getLeftoverFluid(ItemStack inputItem, FluidStack inputFluid) {
        FluidStack unscaledResult = leftoverFluidStack.copy();
        
        int scale = scaleOfInput(inputItem, inputFluid);
        FluidStack scaledResult = scaleResult(unscaledResult, scale);
        
        return Optional.of(scaledResult);
    }
    
    public boolean isHotEnough(float distilleryTemp) {
        return distilleryTemp >= minTemp;
    }
    
    public int getDuration() {
        return duration;
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
    
    
    
    // public static class Serializer extends RecipeSerializerImpl<DistilleryRecipe> {
    //     @Override
    //     public @NotNull DistilleryRecipe fromJson(ResourceLocation id, JsonObject json) {
    //         Ingredient itemStackIngredient = json.has("input_item")? Ingredient.fromJson(json.getAsJsonObject("input_item")) : ItemStackIngredient.EMPTY;
    //         Ingredient fluidStackIngredient = json.has("input_fluid")? Ingredient.fromJson(json.getAsJsonObject("input_fluid")) : Ingredient.EMPTY;
    //         ItemStackProvider resultItemStack = json.has("result_item")? ItemStackProvider.fromJson(GsonHelper.getAsJsonObject(json, "result_item")) : ItemStackProvider.empty();
    //         FluidStack resultFluidStack = json.has("result_fluid")? JsonHelpers.getFluidStack(GsonHelper.getAsJsonObject(json, "result_fluid")) : FluidStack.EMPTY;
    //         ItemStackProvider leftoverItemStack = json.has("leftover_item")? ItemStackProvider.fromJson(GsonHelper.getAsJsonObject(json, "leftover_item")) : ItemStackProvider.empty();
    //         FluidStack leftoverFluidStack = json.has("leftover_fluid")? JsonHelpers.getFluidStack(GsonHelper.getAsJsonObject(json, "leftover_fluid")) : FluidStack.EMPTY;
    //         int minTemp = json.get("min_temp").getAsInt();
    //         int durationTicks = json.get("duration").getAsInt();
    //        
    //         return new DistilleryRecipe(
    //                 id,
    //                 itemStackIngredient,
    //                 fluidStackIngredient,
    //                 resultItemStack,
    //                 resultFluidStack,
    //                 leftoverItemStack,
    //                 leftoverFluidStack,
    //                 minTemp,
    //                 durationTicks
    //         );
    //        
    //     }
    //    
    //     @Override
    //     public @Nullable DistilleryRecipe fromNetwork(ResourceLocation id, FriendlyByteBuf buffer) {
    //         Ingredient itemStackIngredient = Ingredient.fromNetwork(buffer);
    //         Ingredient fluidStackIngredient = Ingredient.fromNetwork(buffer);
    //         ItemStackProvider resultItemStack = ItemStackProvider.fromNetwork(buffer);
    //         FluidStack resultFluidStack = FluidStack.readFromPacket(buffer);
    //         ItemStackProvider leftoverItemStack = ItemStackProvider.fromNetwork(buffer);
    //         FluidStack leftoverFluidStack = FluidStack.readFromPacket(buffer);
    //         int minTemp = buffer.readVarInt();
    //         int durationTicks = buffer.readVarInt();
    //        
    //         return new DistilleryRecipe(
    //                 id,
    //                 itemStackIngredient,
    //                 fluidStackIngredient,
    //                 resultItemStack,
    //                 resultFluidStack,
    //                 leftoverItemStack,
    //                 leftoverFluidStack,
    //                 minTemp,
    //                 durationTicks
    //         );
    //     }
    //    
    //     @Override
    //     public void toNetwork(FriendlyByteBuf buffer, DistilleryRecipe recipe) {
    //         recipe.itemStackIngredient.toNetwork(buffer);
    //         recipe.fluidStackIngredient.toNetwork(buffer);
    //         recipe.resultItemStack.toNetwork(buffer);
    //         recipe.resultFluidStack.writeToPacket(buffer);
    //         recipe.leftoverItemStack.toNetwork(buffer);
    //         recipe.leftoverFluidStack.writeToPacket(buffer);
    //         buffer.writeVarInt(recipe.minTemp);
    //         buffer.writeVarInt(recipe.duration);
    //        
    //     }
    // }
    
    
}
