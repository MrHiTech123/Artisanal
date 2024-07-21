package net.mrhitech.artisanal.common.recipes.outputs;

import com.google.gson.JsonObject;
import net.dries007.tfc.common.capabilities.heat.HeatCapability;
import net.dries007.tfc.common.recipes.outputs.AddHeatModifier;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.util.JsonHelpers;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.world.item.ItemStack;

public record CapHeatModifier(float max_temp) implements ItemStackModifier {
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        stack.getCapability(HeatCapability.CAPABILITY).ifPresent(cap -> {
            if (cap.getTemperature() > max_temp) {
                cap.setTemperature(max_temp);
            }
        });
        
        return stack;
    }
    
    public Serializer serializer() {
        return Serializer.INSTANCE;
    }
    
    
    public enum Serializer implements ItemStackModifier.Serializer<CapHeatModifier>
    {
        INSTANCE;
        
        @Override
        public CapHeatModifier fromJson(JsonObject json)
        {
            final float max_temp = JsonHelpers.getAsFloat(json, "max_temp");
            return new CapHeatModifier(max_temp);
        }
        
        @Override
        public CapHeatModifier fromNetwork(FriendlyByteBuf buffer)
        {
            final float max_temp = buffer.readFloat();
            return new CapHeatModifier(max_temp);
        }
        
        @Override
        public void toNetwork(CapHeatModifier modifier, FriendlyByteBuf buffer)
        {
            buffer.writeFloat(modifier.max_temp);
        }
    }
    
}
