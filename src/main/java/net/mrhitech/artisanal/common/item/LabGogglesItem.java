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
    
    private static final ResourceLocation LAB_GOGGLES_OVERLAY_TEXTURE = new ResourceLocation(Artisanal.MOD_ID, "textures/gui/overlay/lab_goggles.png");
    
    private static boolean wearingLabGoggles(Player player) {
        for (ItemStack armor : player.getArmorSlots()) {
            if (armor.getItem() instanceof LabGogglesItem) {
                return true;
            }
        }
        
        return false;
    }
    
    
    private static void renderTextureOverlay(GuiGraphics graphics, ResourceLocation location, float alpha)
    {
        final Minecraft mc = Minecraft.getInstance();
        final int screenWidth = mc.getWindow().getGuiScaledWidth();
        final int screenHeight = mc.getWindow().getGuiScaledHeight();

        RenderSystem.disableDepthTest();
        RenderSystem.depthMask(false);
        graphics.setColor(1.0F, 1.0F, 1.0F, alpha);
        graphics.blit(location, 0, 0, -90, 0.0F, 0.0F, screenWidth, screenHeight, screenWidth, screenHeight);
        RenderSystem.depthMask(true);
        RenderSystem.enableDepthTest();
        graphics.setColor(1.0F, 1.0F, 1.0F, 1.0F);
    }
    
    private static void renderLabGogglesOverWorldIfWorn(ForgeGui gui, GuiGraphics graphics, float partialTicks, int width, int height) {
        if (!Minecraft.getInstance().options.getCameraType().isFirstPerson()) return;
        
        LocalPlayer player = Minecraft.getInstance().player;
        
        if (player == null) return;
        
        if (wearingLabGoggles(player)) {
            renderTextureOverlay(graphics, LAB_GOGGLES_OVERLAY_TEXTURE, 1f);
        }
        
        
    }
    
    
    public static void registerOverlay(RegisterGuiOverlaysEvent overlaysEvent) {
        overlaysEvent.registerAbove(VanillaGuiOverlay.HELMET.id(), "lab_goggles_overlay", LabGogglesItem::renderLabGogglesOverWorldIfWorn);
    }
    
    
}
