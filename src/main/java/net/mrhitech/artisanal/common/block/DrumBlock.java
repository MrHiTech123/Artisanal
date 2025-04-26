package net.mrhitech.artisanal.common.block;

import net.dries007.tfc.common.blockentities.BarrelBlockEntity;
import net.dries007.tfc.common.blocks.ExtendedProperties;
import net.dries007.tfc.common.blocks.devices.BarrelBlock;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.util.Helpers;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.NoteBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.common.Tags;
import net.minecraftforge.fluids.capability.IFluidHandler;
import net.mrhitech.artisanal.common.ArtisanalTags;
import net.mrhitech.artisanal.util.IBarrelBlockEntityMixin;
import net.mrhitech.artisanal.util.advancements.ArtisanalAdvancements;
import org.jetbrains.annotations.Nullable;

import javax.annotation.ParametersAreNonnullByDefault;


public class DrumBlock extends BarrelBlock {
    
    private final TagKey<Fluid> usableFluids;
    
    public DrumBlock(ExtendedProperties properties, TagKey<Fluid> usableFluids) {
        super(properties);
        this.usableFluids = usableFluids;
    }
    
    private static void modifyBlockEntity(BarrelBlockEntity barrel) {
        ((IBarrelBlockEntityMixin)barrel).enableDrumFluids();
    }
    
    
    
    public TagKey<Fluid> getUsableFluids() {
        return usableFluids;
    }
    
    @Override
    @ParametersAreNonnullByDefault
    public void attack(BlockState state, Level level, BlockPos pos, Player player) {
        if (state.getValue(SEALED)) {
            BlockEntity entity = level.getBlockEntity(pos);
            if (entity instanceof BarrelBlockEntity barrel) {
                if (
                        Helpers.isItem(player.getMainHandItem(), Tags.Items.RODS_WOODEN) || 
                        Helpers.isItem(player.getMainHandItem(), ArtisanalTags.ITEMS.METAL_RODS)
                ) {
                    IFluidHandler tank = Helpers.getCapability(barrel, Capabilities.FLUID);
                    if (tank != null) {
                        float fill = (float)tank.getFluidInTank(0).getAmount() / tank.getTankCapacity(0);
                        int note = Mth.ceil(fill * 24.0F);
                        level.playSeededSound(
                                null,
                                pos.getX(),
                                pos.getY(),
                                pos.getZ(),
                                SoundEvents.ANVIL_LAND,
                                SoundSource.RECORDS,
                                1.0F,
                                NoteBlock.getPitchFromNote(note),
                                level.random.nextLong()
                        );
                        
                        if (player instanceof ServerPlayer serverPlayer) {
                            ArtisanalAdvancements.PLAY_DRUM.trigger(serverPlayer);
                        }
                    }
                }
            }
        }
    }
}
