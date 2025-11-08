package net.mrhitech.artisanal.common.item;

import com.mojang.blaze3d.systems.RenderSystem;
import net.dries007.tfc.TerraFirmaCraft;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.client.event.RegisterGuiOverlaysEvent;
import net.minecraftforge.client.gui.overlay.ForgeGui;
import net.minecraftforge.client.gui.overlay.IGuiOverlay;
import net.minecraftforge.client.gui.overlay.VanillaGuiOverlay;
import net.mrhitech.artisanal.Artisanal;

public class LabGogglesItem extends ArmorItem {
    
    public LabGogglesItem(ArmorMaterial material, Properties properties) {
        super(material, Type.HELMET, properties);
    }
    
    public static final ResourceLocation OVERLAY_TEXTURE = new ResourceLocation(Artisanal.MOD_ID, "textures/gui/overlay/lab_goggles.png");
    
    public static boolean wearingLabGoggles(Player player) {
        for (ItemStack armor : player.getArmorSlots()) {
            if (armor.getItem() instanceof LabGogglesItem) {
                return true;
            }
        }
        
        return false;
    }
    
    
    
    
    
    
    
    
}
