package net.mrhitech.artisanal.common.recipes.inputs;

import com.google.gson.JsonObject;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraftforge.common.crafting.IIngredientSerializer;
import org.jetbrains.annotations.Nullable;

import java.util.Arrays;

public class UniversalIngredient extends Ingredient {
    
    private static final Ingredient.Value[] emptyIngredientValueArr = new Ingredient.Value[]{};
    
    protected UniversalIngredient() {
        super(Arrays.stream(emptyIngredientValueArr));
    }
    
    @Override
    public boolean test(@Nullable ItemStack stack) {
        return true;
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
