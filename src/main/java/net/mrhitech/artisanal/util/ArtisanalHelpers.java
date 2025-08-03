package net.mrhitech.artisanal.util;

import net.dries007.tfc.common.fluids.FluidRegistryObject;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.material.Fluid;
import net.minecraft.world.phys.AABB;
import net.minecraftforge.common.util.Lazy;
import net.minecraftforge.fluids.FluidType;
import net.minecraftforge.fluids.ForgeFlowingFluid;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import org.apache.commons.lang3.mutable.Mutable;
import org.apache.commons.lang3.mutable.MutableObject;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

public class ArtisanalHelpers {
    
    public static List<Player> playersNear(Level level, BlockPos pos, int maxDistance) {
        List<Player> toReturn = new ArrayList<>();
        
        AABB area = new AABB(
                new BlockPos(pos.getX() - maxDistance, pos.getY() - maxDistance, pos.getZ() - maxDistance),
                new BlockPos(pos.getX() + maxDistance, pos.getY() + maxDistance, pos.getZ() + maxDistance)
        );
        
        for (Player player : level.players()) {
            if (area.contains(player.position())) {
                toReturn.add(player);
            }
        }
        
        return toReturn;
        
    }
    
}
