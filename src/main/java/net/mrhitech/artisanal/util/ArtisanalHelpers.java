package net.mrhitech.artisanal.util;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

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
