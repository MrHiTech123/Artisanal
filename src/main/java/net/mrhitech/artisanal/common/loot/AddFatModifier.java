package net.mrhitech.artisanal.common.loot;

import com.google.common.base.Suppliers;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.dries007.tfc.util.Helpers;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraftforge.registries.ForgeRegistries;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.common.item.ArtisanalItems;
import net.mrhitech.artisanal.config.ArtisanalServerConfig;
import org.jetbrains.annotations.NotNull;

import java.util.function.Supplier;

public class AddFatModifier extends AddItemStackMinMaxModifier{
    public static final Supplier<Codec<AddFatModifier>> CODEC = Suppliers.memoize(()
            -> RecordCodecBuilder.create(inst -> codecStart(inst)
            .and(ForgeRegistries.ITEMS.getCodec().fieldOf("item").forGetter(m -> m.item))
            .and(Codec.INT.fieldOf("min").forGetter(m -> m.min))
            .and(Codec.INT.fieldOf("max").forGetter(m -> m.max))
            .apply(inst, AddFatModifier::new)));
    
    public AddFatModifier(LootItemCondition[] conditionsIn, Item f_item, int f_min, int f_max) {
        super(conditionsIn, f_item, f_min, f_max);
    }
    
    protected @NotNull ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> objectArrayList, LootContext lootContext) {
        super.doApply(objectArrayList, lootContext);
        
        if (!ArtisanalServerConfig.GENERIC_ANIMAL_FAT.get()) {
            return objectArrayList;
        }
        
        ItemStack removedFatStack = new ItemStack(Items.AIR);
        for (ItemStack stack : objectArrayList) {
            if (Helpers.isItem(stack.getItem(), ArtisanalTags.ITEMS.FATS) 
                    && !stack.getItem().equals(ArtisanalItems.ANIMAL_FAT.get())) {
                removedFatStack = stack;
            }
        }
        
        
        if (objectArrayList.remove(removedFatStack)) {
            objectArrayList.add(
                    new ItemStack(ArtisanalItems.ANIMAL_FAT.get(), removedFatStack.getCount())
            );
        }
        
        return objectArrayList;
        
        
        
    }
}
