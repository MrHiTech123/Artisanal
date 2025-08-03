package net.mrhitech.artisanal.common.fluids;

import com.mojang.blaze3d.shaders.FogShape;
import com.mojang.blaze3d.systems.RenderSystem;
import net.dries007.tfc.common.fluids.ExtendedFluidType;
import net.dries007.tfc.common.fluids.FluidTypeClientProperties;
import net.minecraft.client.Camera;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.FogRenderer;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.BlockAndTintGetter;
import net.minecraft.world.level.material.FluidState;
import net.minecraftforge.client.extensions.common.IClientFluidTypeExtensions;
import org.jetbrains.annotations.NotNull;
import org.joml.Vector3f;
import java.awt.Color;

import javax.annotation.Nullable;
import java.util.function.Consumer;

public class ArtisanalFluidType extends ExtendedFluidType {
    private final FluidTypeClientProperties clientProperties;
    private final Vector3f color;
    private final float shaderFogStart;
    private final float shaderFogEnd;
    
    public ArtisanalFluidType(Properties properties, FluidTypeClientProperties clientProperties, Vector3f color, float shaderFogStart, float shaderFogEnd) {
        super(properties, clientProperties);
        this.clientProperties = clientProperties;
        this.color = color;
        this.shaderFogStart = shaderFogStart;
        this.shaderFogEnd = shaderFogEnd;
    }
    
        @Override
    public void initializeClient(Consumer<IClientFluidTypeExtensions> consumer) {
        consumer.accept(new IClientFluidTypeExtensions() {
            @Override
            public int getTintColor() {
                return clientProperties.tintColor();
            }
            
            @Override
            public int getTintColor(FluidState state, BlockAndTintGetter getter, BlockPos pos) {
                return clientProperties.tintColorFunction().applyAsInt(getter, pos);
            }
            
            @Override
            public ResourceLocation getStillTexture() {
                return clientProperties.stillTexture();
            }
            
            @Override
            public ResourceLocation getFlowingTexture() {
                return clientProperties.flowingTexture();
            }
            
            @Override
            @Nullable
            public ResourceLocation getOverlayTexture() {
                return clientProperties.overlayTexture();
            }
            
            @Override
            @Nullable
            public ResourceLocation getRenderOverlayTexture(Minecraft minecraft) {
                return clientProperties.renderOverlayTexture();
            }
            
            @Override
            public @NotNull Vector3f modifyFogColor(Camera camera, float partialTick, ClientLevel level, int renderDistance, float darkenWorldAmount, Vector3f fluidFogColor) {
                return color;
            }
            
            @Override
            public void modifyFogRender(Camera camera, FogRenderer.FogMode mode, float renderDistance, float partialTick, float nearDistance, float farDistance, FogShape shape) {
                RenderSystem.setShaderFogStart(shaderFogStart);
                RenderSystem.setShaderFogEnd(shaderFogEnd);
            }
        });
    }
}
