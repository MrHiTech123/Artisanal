package net.mrhitech.artisanal.common.recipes.outputs;

import com.google.gson.JsonObject;
import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodData;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.capabilities.heat.HeatCapability;
import net.dries007.tfc.common.recipes.outputs.AddHeatModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.util.JsonHelpers;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.world.item.ItemStack;

import java.util.concurrent.atomic.AtomicReference;

public record InheritDecayModifier(float decayMultiplier) implements ItemStackModifier {
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        AtomicReference<Float> baseDecayMod = new AtomicReference<Float>( -(float) 1.0);
        
        input.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
            baseDecayMod.set(cap.getData().decayModifier());
        });
        
        
        stack.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
            if (cap instanceof FoodHandler.Dynamic inHandler) {
                FoodData replacedData = FoodData.create(
                        inHandler.getData().hunger(),
                        inHandler.getData().water(),
                        inHandler.getData().saturation(),
                        inHandler.getData().nutrients(),
                        baseDecayMod.get() * decayMultiplier
                );
                if (baseDecayMod.get() != -1.0) {
                    inHandler.setFood(replacedData);
                }
                
            }
        });
        
        return stack;
    }
    
    public Serializer serializer() {
        return Serializer.INSTANCE;
    }
    
    
    public enum Serializer implements ItemStackModifier.Serializer<InheritDecayModifier>
    {
        INSTANCE;
        
        @Override
        public InheritDecayModifier fromJson(JsonObject json)
        {
            final float decayMultiplier = JsonHelpers.getAsFloat(json, "decay_multiplier");
            return new InheritDecayModifier(decayMultiplier);
        }
        
        @Override
        public InheritDecayModifier fromNetwork(FriendlyByteBuf buffer)
        {
            final float decayMultiplier = buffer.readFloat();
            return new InheritDecayModifier(decayMultiplier);
        }
        
        @Override
        public void toNetwork(InheritDecayModifier modifier, FriendlyByteBuf buffer)
        {
            buffer.writeFloat(modifier.decayMultiplier);
        }
    }
    
}
