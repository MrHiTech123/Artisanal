package net.mrhitech.artisanal.common.recipes.outputs;


import com.google.gson.JsonObject;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.items.TFCItems;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.dries007.tfc.util.Helpers;
import net.dries007.tfc.util.JsonHelpers;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.material.Fluids;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.fluids.capability.IFluidHandler;
import net.minecraftforge.fluids.capability.IFluidHandlerItem;


public record OutputFluidItemIngredientModifier(FluidStack outFluidParam) implements ItemStackModifier {
    
    
    
    @Override
    public ItemStack apply(ItemStack formerOutputItem, ItemStack fluidItemIngredient) {
        ItemStack output = fluidItemIngredient.copy();
        // The amount specified in the output fluid is the MAXIMUM fluid that can be output.
        // The amount of fluid that must be in the fluid item ingredient is the MINUMUM fluid that can be output.
        
        FluidStack outFluid = outFluidParam.copy();
        
        IFluidHandlerItem fluidHandler = Helpers.getCapability(output, Capabilities.FLUID_ITEM);
        
        if (fluidHandler == null) {
            return !output.isEmpty() ? output : new ItemStack(TFCItems.JUG.get());
        }
        
        
        
        int amountInFluidItemIngredient = fluidHandler.getFluidInTank(0).getAmount();
        outFluid.setAmount(Math.min(outFluid.getAmount(), amountInFluidItemIngredient));
        
        fluidHandler.drain(Integer.MAX_VALUE, IFluidHandler.FluidAction.EXECUTE);
        fluidHandler.fill(outFluid, IFluidHandler.FluidAction.EXECUTE);
        return !output.isEmpty() ? output : new ItemStack(TFCItems.JUG.get());
    }
    
    @Override
    public Serializer serializer() {
        return Serializer.CHANGE_FLUID_NBT;
    }
    
    public record Serializer() implements ItemStackModifier.Serializer<OutputFluidItemIngredientModifier> {
        
        static final Serializer CHANGE_FLUID_NBT = new Serializer();
        
        @Override
        public OutputFluidItemIngredientModifier fromJson(JsonObject json) {
            final FluidStack outFluid = JsonHelpers.getFluidStack(json, "fluid");
            return new OutputFluidItemIngredientModifier(!outFluid.isEmpty() ? outFluid : defaultFluid());
        }
        
        @Override
        public OutputFluidItemIngredientModifier fromNetwork(FriendlyByteBuf buffer) {
            final FluidStack outFluid = FluidStack.readFromPacket(buffer);
            return new OutputFluidItemIngredientModifier(!outFluid.isEmpty() ? outFluid : defaultFluid());
        }
        
        @Override
        public void toNetwork(OutputFluidItemIngredientModifier modifier, FriendlyByteBuf buffer) {
            modifier.outFluidParam.writeToPacket(buffer);
        }
        
        public static FluidStack defaultFluid() {
            return new FluidStack(Fluids.WATER, 1000);
        }
    }
    
    
}