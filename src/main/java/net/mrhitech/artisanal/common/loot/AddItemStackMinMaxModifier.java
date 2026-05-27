package net.mrhitech.artisanal.common.loot;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.common.loot.LootModifier;
import org.jetbrains.annotations.NotNull;

import java.util.Random;

public class AddItemStackMinMaxModifier extends LootModifier {
    public static final MapCodec<AddItemStackMinMaxModifier> CODEC = RecordCodecBuilder.mapCodec(
            inst -> LootModifier.codecStart(inst)
            .and(ItemStack.CODEC.fieldOf("item").forGetter(m -> m.item))
            .and(Codec.INT.fieldOf("min").forGetter(m -> m.min))
            .and(Codec.INT.fieldOf("max").forGetter(m -> m.max))
            .apply(inst, AddItemStackMinMaxModifier::new));
    
    protected final ItemStack item;
    protected final int min;
    protected final int max;
    protected Random rand = new Random();
    
    
    public AddItemStackMinMaxModifier(LootItemCondition[] conditionsIn, ItemStack f_item, int f_min, int f_max) {
        super(conditionsIn);
        this.item = f_item;
        this.min = f_min;
        this.max = f_max;
    }
    
    @Override
    protected @NotNull ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> objectArrayList, LootContext lootContext) {
        for (LootItemCondition condition : this.conditions) {
            if (!condition.test(lootContext)) {
                return objectArrayList;
            }
        }
        objectArrayList.add(new ItemStack(item.getItem(), rand.nextInt(min, max + 1)));
        
        return objectArrayList;
    }
    
    @Override
    public @NotNull MapCodec<? extends IGlobalLootModifier> codec() {
        return CODEC;
    }
}
