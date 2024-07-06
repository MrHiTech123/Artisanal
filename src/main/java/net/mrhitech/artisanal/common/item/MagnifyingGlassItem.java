package net.mrhitech.artisanal.common.item;

import net.dries007.tfc.client.TFCSounds;
import net.dries007.tfc.common.TFCTags;
import net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blocks.TFCBlocks;
import net.dries007.tfc.common.blocks.devices.FirepitBlock;
import net.dries007.tfc.common.capabilities.Capabilities;
import net.dries007.tfc.common.items.FirestarterItem;
import net.dries007.tfc.config.TFCConfig;
import net.dries007.tfc.util.advancements.TFCAdvancements;
import net.dries007.tfc.util.events.StartFireEvent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.dries007.tfc.util.Helpers;
import net.minecraftforge.items.IItemHandlerModifiable;

import javax.swing.plaf.basic.BasicComboBoxUI;
import java.util.ArrayList;
import java.util.List;


public class MagnifyingGlassItem extends FirestarterItem {
    public MagnifyingGlassItem(Item.Properties properties) {
        super(properties);
    }
    
    @Override
    public void onUseTick(Level level, LivingEntity livingEntityIn, ItemStack stack, int countLeft) {
        if (livingEntityIn instanceof Player player) {
            final BlockHitResult result = getPlayerPOVHitResult(level, player, ClipContext.Fluid.NONE);
            final BlockPos targetPos = result.getBlockPos();
            final BlockPos targetAbovePos = targetPos.above();
            final BlockPos playerAbovePos = player.getOnPos().above();
            
            double chance = TFCConfig.SERVER.fireStarterChance.get() * 
                    (rainingAtEither(level, targetAbovePos, playerAbovePos)? 0 : 1) * 
                    (eitherCanSeeSky(level, targetAbovePos, playerAbovePos)? 1 : 0) * 
                    (itsDay(level)? 1 : 0);
            
            if (chance == 0) {
                return;
            }
            
            if (level.isClientSide()) {
                Vec3 location = result.getLocation();
                makeEffects(level, player, location.x(), location.y(), location.z(), countLeft, getUseDuration(stack), level.random);
            }
            
            else if (countLeft == 1) {
                if (FirepitBlock.canSurvive(level, targetAbovePos)) {
                    final List<ItemEntity> items = level.getEntitiesOfClass(ItemEntity.class, new AABB(targetAbovePos.getX() - 0.5, targetAbovePos.getY(), targetAbovePos.getZ() - 0.5, targetAbovePos.getX() + 1.5, targetAbovePos.getY() + 1, targetAbovePos.getZ() + 1.5));
                    final List<ItemEntity> usableItems = new ArrayList<>();
                    int sticks = 1, kindling = 0;
                    
                    ItemEntity logEntity = null;
                    
                    for (ItemEntity entity : items) {
                        ItemStack foundStack = entity.getItem();
                        Item foundItem = foundStack.getItem();
                        int itemCount = foundStack.getCount();
                        if (Helpers.isItem(foundItem, TFCTags.Items.FIREPIT_STICKS))
                        {
                            sticks += itemCount;
                            usableItems.add(entity);
                        }
                        else if (Helpers.isItem(foundItem, TFCTags.Items.FIREPIT_KINDLING))
                        {
                            kindling += itemCount;
                            usableItems.add(entity);
                        }
                        else if (logEntity == null && Helpers.isItem(foundItem, TFCTags.Items.FIREPIT_LOGS))
                        {
                            logEntity = entity;
                        }
                    }
                    if (sticks >= 3 && logEntity != null) {
                        final float kindlingModifier = Math.min(0.1F * (float) kindling, 0.5F);
                        if (level.random.nextFloat() < chance + kindlingModifier) {
                            usableItems.forEach(Entity::kill);
                            logEntity.kill();
                            
                            ItemStack initialLog = logEntity.getItem().copy();
                            initialLog.setCount(1);
                            
                            final BlockState state = TFCBlocks.FIREPIT.get().defaultBlockState().setValue(FirepitBlock.AXIS, player.getDirection().getAxis());
                            level.setBlock(targetAbovePos, state, 3);
                            
                            level.getBlockEntity(targetAbovePos, TFCBlockEntities.FIREPIT.get()).ifPresent(firepit -> firepit.getCapability(Capabilities.ITEM).ifPresent(cap -> {
                                if (cap instanceof IItemHandlerModifiable modifiableInventory) {
                                    modifiableInventory.setStackInSlot(AbstractFirepitBlockEntity.SLOT_FUEL_CONSUME, initialLog);
                                }
                                firepit.light(state);
                            }));
                            if (player instanceof ServerPlayer serverPlayer)
                            {
                                TFCAdvancements.FIREPIT_CREATED.trigger(serverPlayer, state);
                            }
                        }
                        return;
                    }
                }
                StartFireEvent.startFire(level, targetPos, level.getBlockState(targetPos), result.getDirection(), player, stack);
                
            }
            
            
        }
    }
    
    @Override
    public UseAnim getUseAnimation(ItemStack stack)
    {
        return UseAnim.BOW;
    }
    
    public boolean itsDay(Level level) {
        float daySeconds = level.getTimeOfDay(0);
        return daySeconds < 0.25 || daySeconds > 0.75;
    }
    
    public boolean eitherCanSeeSky(Level level, BlockPos pos1, BlockPos pos2) {
        return level.canSeeSky(pos1) || level.canSeeSky(pos2);
    }
    public boolean rainingAtEither(Level level, BlockPos pos1, BlockPos pos2) {
        return level.isRainingAt(pos1) || level.isRainingAt(pos2);
    }
    
    @Override
    public int getUseDuration(ItemStack stack) {
        return 20;
    }
    
    private void makeEffects(Level world, Player player, double x, double y, double z, int countLeft, int total, RandomSource random)
    {
        int count = total - countLeft;
        if (random.nextFloat() + 0.3 < count / (double) total)
        {
            world.addParticle(ParticleTypes.SMOKE, x, y, z, 0.0F, 0.1F, 0.0F);
        }
        if (countLeft < 5 && random.nextFloat() + 0.3 < count / (double) total)
        {
            world.addParticle(ParticleTypes.FLAME, x, y, z, 0.0F, 0.1F, 0.0F);
        }
    }
    
}
