package net.mrhitech.artisanal.common.container;


import net.dries007.tfc.common.container.Container;
import net.minecraft.network.chat.Component;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.MenuType;
import net.neoforged.neoforge.registries.DeferredHolder;

public class ArtisanalContainerProviders {
    MenuProvider DISTILLERY = createProvider(ArtisanalContainerTypes.DISTILLERY, "artisanal.screen.distillery");
    
    public static <T extends Container> MenuProvider createProvider(DeferredHolder<MenuType<?>, MenuType<T>> menuTypeSupplier, String translationKey) {
        return new SimpleMenuProvider((windowId, inv, player) -> Container.create(menuTypeSupplier.get(), windowId, player.getInventory()), Component.translatable(translationKey));
    }
    
}
