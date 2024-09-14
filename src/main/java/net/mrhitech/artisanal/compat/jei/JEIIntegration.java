package net.mrhitech.artisanal.compat.jei;

import mezz.jei.api.IModPlugin;
import mezz.jei.api.JeiPlugin;
import mezz.jei.api.helpers.IGuiHelper;
import mezz.jei.api.recipe.RecipeType;
import mezz.jei.api.registration.IGuiHandlerRegistration;
import mezz.jei.api.registration.IRecipeCatalystRegistration;
import mezz.jei.api.registration.IRecipeCategoryRegistration;
import mezz.jei.api.registration.IRecipeRegistration;
import net.dries007.tfc.client.ClientHelpers;
import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.items.TFCItems;
import net.dries007.tfc.common.recipes.PotRecipe;
import net.dries007.tfc.common.recipes.TFCRecipeTypes;
import net.dries007.tfc.util.Helpers;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.Container;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Recipe;
import net.mrhitech.artisanal.Artisanal;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeSerializers;
import net.mrhitech.artisanal.common.recipes.ArtisanalRecipeTypes;
import net.mrhitech.artisanal.common.recipes.JuicingRecipe;
import net.mrhitech.artisanal.compat.jei.category.JuicingRecipeCategory;
import net.mrhitech.artisanal.compat.jei.category.ScalablePotRecipeCategory;

import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;

@JeiPlugin
public class JEIIntegration implements IModPlugin {
    
    private static <C extends Container, T extends Recipe<C>> List<T> recipes(net.minecraft.world.item.crafting.RecipeType<T> type)
    {
        return ClientHelpers.getLevelOrThrow().getRecipeManager().getAllRecipesFor(type);
    }
    
    private static <C extends Container, T extends Recipe<C>> List<T> recipes(net.minecraft.world.item.crafting.RecipeType<T> type, Predicate<T> filter)
    {
        return recipes(type).stream().filter(filter).collect(Collectors.toList());
    }
    
    public static final RecipeType<PotRecipe> SCALABLE_POT = RecipeType.create(Artisanal.MOD_ID, "scalable_pot", PotRecipe.class);
    public static final RecipeType<JuicingRecipe> JUICING = RecipeType.create(Artisanal.MOD_ID, "juicing", JuicingRecipe.class);
    
    @Override
    public ResourceLocation getPluginUid() {
        return new ResourceLocation(Artisanal.MOD_ID, "jei");
    }
    
    @Override
    public void registerCategories(IRecipeCategoryRegistration registry) {
        final IGuiHelper gui = registry.getJeiHelpers().getGuiHelper();
        
        registry.addRecipeCategories(
                new ScalablePotRecipeCategory(SCALABLE_POT, gui),
                new JuicingRecipeCategory(JUICING, gui)
        );
    }
    
    @Override
    public void registerRecipes(IRecipeRegistration registry) {
        registry.addRecipes(SCALABLE_POT, recipes(TFCRecipeTypes.POT.get(), recipe -> (recipe.getSerializer() == ArtisanalRecipeSerializers.SCALABLE_POT.get())));
        registry.addRecipes(JUICING, recipes(ArtisanalRecipeTypes.JUICING.get(), recipe -> (recipe.getSerializer() == ArtisanalRecipeSerializers.JUICING_RECIPE.get())));
    }
    
    @Override
    public void registerRecipeCatalysts(IRecipeCatalystRegistration registry) {
        registry.addRecipeCatalyst(new ItemStack(TFCItems.POT.get()), SCALABLE_POT);
        registry.addRecipeCatalyst(new ItemStack(TFCBlocks.QUERN.get()), JUICING);
        registry.addRecipeCatalyst(new ItemStack(TFCItems.HANDSTONE.get()), JUICING);
        for (Item item : Helpers.allItems(ArtisanalTags.ITEMS.TFC_BARRELS).toList()) {
            registry.addRecipeCatalyst(new ItemStack(item), JUICING);
        }
    }
    
    
    
}
