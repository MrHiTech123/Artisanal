package net.mrhitech.artisanal.common.recipes.outputs;

import net.dries007.tfc.common.capabilities.food.FoodCapability;
import net.dries007.tfc.common.capabilities.food.FoodHandler;
import net.dries007.tfc.common.recipes.outputs.ItemStackModifier;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.List;

public enum RemoveButterModifier implements ItemStackModifier.SingleInstance<RemoveButterModifier> {
    INSTANCE;
    
    public static final ResourceLocation BUTTER = new ResourceLocation("firmalife", "food/butter");
    
    public ItemStack apply(ItemStack stack, ItemStack input) {
        
        stack.getCapability(FoodCapability.CAPABILITY).ifPresent(cap -> {
            if (cap instanceof FoodHandler.Dynamic inHandler) {
                
                List<ItemStack> ingredients = inHandler.getIngredients();
                
                for (int i = 0; i < ingredients.size(); ++i) {
                    ItemStack ingredient = ingredients.get(i);
                    ResourceLocation ingredientLocation = ForgeRegistries.ITEMS.getKey(ingredient.getItem());
                    
                    if (ingredientLocation != null && 
                            ingredientLocation.equals(BUTTER)
                    ) {
                        ingredients.remove(i);
                        --i;
                    }
                }
            }
        });
        
        
        return stack;
    }
    
    public RemoveButterModifier instance() {
        return INSTANCE;
    }
    
    
    
}
