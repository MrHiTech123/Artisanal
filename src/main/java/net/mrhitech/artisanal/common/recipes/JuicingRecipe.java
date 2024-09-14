package net.mrhitech.artisanal.common.recipes;

import net.dries007.tfc.common.recipes.ISimpleRecipe;
import net.dries007.tfc.common.recipes.SimpleItemRecipe;
import net.dries007.tfc.common.recipes.inventory.ItemStackInventory;
import net.dries007.tfc.util.collections.IndirectHashCollection;
import net.minecraft.core.RegistryAccess;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;
import net.minecraftforge.fluids.FluidStack;

public class JuicingRecipe extends SimpleFluidRecipe {
    
    public static final IndirectHashCollection<Item, JuicingRecipe> CACHE = IndirectHashCollection.createForRecipe(JuicingRecipe::getValidItems, ArtisanalRecipeTypes.JUICING);
    
    
    public static JuicingRecipe getRecipe(Level world, ItemStackInventory wrapper)
    {
        for (JuicingRecipe recipe : CACHE.getAll(wrapper.getStack().getItem()))
        {
            if (recipe.matches(wrapper, world))
            {
                return recipe;
            }
        }
        return null;
    }
    
    public JuicingRecipe(ResourceLocation id, Ingredient ingredient, FluidStack result)
    {
        super(id, ingredient, result);
    }
    
    
    
    public ItemStack getResultItem(RegistryAccess access) {
        return ItemStack.EMPTY;
    }
    
    public FluidStack getResultFluid() {
        return this.result.copy();
    }
    
    @Override
    public RecipeSerializer getSerializer() {
        return ArtisanalRecipeSerializers.JUICING_RECIPE.get();
    }
    
    public RecipeType<?> getType() {
        return ArtisanalRecipeTypes.JUICING.get();
    }
    
    
    
}
