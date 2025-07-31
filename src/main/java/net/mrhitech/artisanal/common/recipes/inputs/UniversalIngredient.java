package net.mrhitech.artisanal.common.recipes.inputs;

import com.google.gson.JsonObject;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraftforge.common.crafting.IIngredientSerializer;
import net.minecraftforge.registries.ForgeRegistries;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import org.jetbrains.annotations.Nullable;

import java.util.Arrays;
import java.util.Optional;
import java.util.function.Supplier;
import java.util.stream.Stream;

public class UniversalIngredient extends Ingredient {
    
    // private static final Supplier<Stream<ItemValue>> allItems = () -> ForgeRegistries.ITEMS.getKeys().stream().map(resourceLocation -> 
    //             new Ingredient.ItemValue(
    //                     new ItemStack(Optional.ofNullable(ForgeRegistries.ITEMS.getValue(resourceLocation)).orElse(Items.AIR))
    //             ));
    
    private static final Supplier<Stream<ItemValue>> noItems = () -> Stream.of(new Ingredient.ItemValue(new ItemStack(ArtisanalItems.DEBUG_ANY_ITEM.get())));
    
    protected UniversalIngredient() {
        super(noItems.get());
    }
    
    @Override
    public boolean test(@Nullable ItemStack stack) {
        return true;
    }

    @Override
    public IIngredientSerializer<?> getSerializer() {
        return Serializer.INSTANCE;
    }
    
    public enum Serializer implements IIngredientSerializer<UniversalIngredient> {
        INSTANCE;
        
        
        @Override
        public UniversalIngredient parse(FriendlyByteBuf buffer) {
            return new UniversalIngredient();
        }
        
        @Override
        public UniversalIngredient parse(JsonObject json) {
            return new UniversalIngredient();
        }
        
        @Override
        public void write(FriendlyByteBuf buffer, UniversalIngredient ingredient) {}
    }
}
