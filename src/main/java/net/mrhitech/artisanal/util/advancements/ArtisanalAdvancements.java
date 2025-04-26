package net.mrhitech.artisanal.util.advancements;

import net.dries007.tfc.util.advancements.BlockActionTrigger;
import net.dries007.tfc.util.advancements.EntityActionTrigger;
import net.dries007.tfc.util.advancements.GenericTrigger;
import net.minecraft.advancements.CriteriaTriggers;
import net.minecraft.resources.ResourceLocation;
import net.mrhitech.artisanal.Artisanal;

public class ArtisanalAdvancements {
    
    public static void registerTriggers() {}
    
    public static final GenericTrigger JUICING = registerGeneric("juicing");
    public static final GenericTrigger PLAY_DRUM = registerGeneric("play_drum");
    
    
    public static BlockActionTrigger registerBlock(String name)
    {
        return CriteriaTriggers.register(new BlockActionTrigger(new ResourceLocation(Artisanal.MOD_ID, name)));
    }

    public static GenericTrigger registerGeneric(String name)
    {
        return CriteriaTriggers.register(new GenericTrigger(new ResourceLocation(Artisanal.MOD_ID, name)));
    }

    public static EntityActionTrigger registerEntity(String name)
    {
        return CriteriaTriggers.register(new EntityActionTrigger(new ResourceLocation(Artisanal.MOD_ID, name)));
    }
}
