package net.mrhitech.artisanal.common.loot;

import com.google.common.base.Suppliers;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraftforge.common.loot.IGlobalLootModifier;
import net.minecraftforge.common.loot.LootModifier;
import net.minecraftforge.registries.ForgeRegistries;
import org.jetbrains.annotations.NotNull;

import java.util.Random;
import java.util.function.Supplier;

public class AddItemStackMinMaxModifier extends LootModifier {
    public static final Supplier<Codec<AddItemStackMinMaxModifier>> CODEC = Suppliers.memoize(()
            -> RecordCodecBuilder.create(inst -> codecStart(inst)
            .and(ForgeRegistries.ITEMS.getCodec().fieldOf("item").forGetter(m -> m.item))
            .and(Codec.INT.fieldOf("min").forGetter(m -> m.min))
            .and(Codec.INT.fieldOf("max").forGetter(m -> m.max))
            .apply(inst, AddItemStackMinMaxModifier::new)));
    
    protected final Item item;
    protected final int min;
    protected final int max;
    protected Random rand = new Random();
    
    
    public AddItemStackMinMaxModifier(LootItemCondition[] conditionsIn, Item f_item, int f_min, int f_max) {
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
        objectArrayList.add(new ItemStack(item, rand.nextInt(min, max + 1)));
        
        return objectArrayList;
    }
    
    @Override
    public Codec<? extends IGlobalLootModifier> codec() {
        return null;
    }
}
