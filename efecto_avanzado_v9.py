"""
Advanced Multi-Effect Overlay v9.0 - MEGA EDITION
Efectos visuales profesionales con múltiples categorías
+ 17 MODOS DE OPERACIÓN ÚNICOS
+ 42 efectos diferentes con física única
+ Paletas de colores vibrantes
+ Rendimiento optimizado
"""

from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QTimer, QPoint, QPointF, pyqtSignal, QObject
from PyQt6.QtGui import (QPainter, QColor, QPen, QIcon, QPixmap, 
                         QRadialGradient, QBrush, QPainterPath, QLinearGradient)
from pynput import mouse
from pynput import keyboard
import sys
import math
import random
from dataclasses import dataclass
from typing import List
from enum import Enum
import ctypes
from ctypes import wintypes
import json
import os

# Constantes de Windows API para forzar ventana arriba de TODO
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040

# ============================================================================
# EFECTOS Y CONFIGURACIÓN
# ============================================================================

class EffectType(Enum):
    """Tipos de efectos disponibles - 30+ EFECTOS"""
    # Efectos de Agua (4)
    WATER = ("water", "💧 Agua Cristalina", 0)
    OCEAN = ("ocean", "🌊 Olas del Océano", 0)
    ICE = ("ice", "🧊 Hielo Congelado", 0)
    BUBBLE = ("bubble", "🫧 Burbujas", 0)
    
    # Efectos de Fuego (4)
    FIRE = ("fire", "🔥 Fuego Ardiente", 1)
    LAVA = ("lava", "🌋 Lava Volcánica", 1)
    INFERNO = ("inferno", "🔥 Infierno", 1)
    EMBER = ("ember", "✨ Brasas", 1)
    
    # Efectos Mágicos (5)
    SPARKLE = ("sparkle", "✨ Chispas Mágicas", 2)
    MAGIC = ("magic", "🔮 Magia Arcana", 2)
    STARS = ("stars", "⭐ Estrellas", 2)
    FAIRY = ("fairy", "🧚 Polvo de Hada", 2)
    MYSTIC = ("mystic", "🌟 Místico", 2)
    
    # Efectos Naturales (5)
    SNOW = ("snow", "❄️ Nieve", 3)
    SMOKE = ("smoke", "💨 Humo", 3)
    LEAF = ("leaf", "🍃 Hojas de Otoño", 3)
    CHERRY = ("cherry", "🌸 Flor de Cerezo", 3)
    POISON = ("poison", "☠️ Veneno Tóxico", 3)
    
    # Efectos Electrónicos (4)
    NEON = ("neon", "🌈 Neón", 4)
    PLASMA = ("plasma", "⚡ Plasma", 4)
    LIGHTNING = ("lightning", "⚡ Relámpago", 4)
    CYBER = ("cyber", "🤖 Cibernético", 4)
    
    # Efectos Preciosos (5)
    GOLD = ("gold", "🟡 Oro Brillante", 5)
    SILVER = ("silver", "⚪ Plata Metálica", 5)
    DIAMOND = ("diamond", "💎 Diamante", 5)
    RUBY = ("ruby", "💎 Rubí", 5)
    EMERALD = ("emerald", "💎 Esmeralda", 5)
    
    # Efectos Cósmicos (4)
    GALAXY = ("galaxy", "🌌 Galaxia", 6)
    NEBULA = ("nebula", "🌠 Nebulosa", 6)
    AURORA = ("aurora", "🌌 Aurora Boreal", 6)
    METEOR = ("meteor", "☄️ Meteoro", 6)
    
    # Efectos Especiales (4)
    RAINBOW = ("rainbow", "🌈 Arcoíris", 7)
    BLOOD = ("blood", "🩸 Sangre", 7)
    TOXIC = ("toxic", "☢️ Radiactivo", 7)
    MATRIX = ("matrix", "💚 Matrix", 7)
    
    # Colores Puros (8) - NUEVA CATEGORÍA
    RED = ("red", "🔴 Rojo Puro", 8)
    BLUE = ("blue", "🔵 Azul Puro", 8)
    GREEN = ("green", "🟢 Verde Puro", 8)
    YELLOW = ("yellow", "🟡 Amarillo Puro", 8)
    PURPLE = ("purple", "🟣 Morado Puro", 8)
    ORANGE = ("orange", "🟠 Naranja Puro", 8)
    PINK = ("pink", "🩷 Rosa Puro", 8)
    WHITE = ("white", "⚪ Blanco Puro", 8)
    
    def __init__(self, type_id: str, display_name: str, category: int):
        self.type_id = type_id
        self.display_name = display_name
        self.category = category

class EffectMode(Enum):
    """16 MODOS DE OPERACIÓN - MEGA EDICIÓN"""
    # Modos Básicos
    CLICK_ONLY = ("click", "🖱️ Solo Clic", "Gran splash al hacer clic")
    FOLLOW_MOUSE = ("follow", "👆 Seguir Cursor", "Rastro continuo al mover")
    TRAIL = ("trail", "✨ Rastro de Luz", "Estela luminosa del cursor")
    BURST = ("burst", "💥 Explosión", "Múltiples partículas en clic")
    RIPPLE_ONLY = ("ripple", "〰️ Solo Ondas", "Solo ondas expansivas")
    MINIMAL = ("minimal", "⚪ Minimalista", "Efecto sutil y ligero")
    DOUBLE_CLICK = ("double_click", "👆👆 Solo Doble Clic", "Efecto solo con doble clic")
    
    # Modos Nuevos - Interactivos
    DRAG_PAINT = ("drag_paint", "🖱️ Arrastrar y Pintar", "Efectos mientras arrastras el mouse")
    RANDOM = ("random", "🎲 Aleatorio", "Efecto aleatorio en cada clic")
    COMBO = ("combo", "💥 Modo Combo", "Multiplicador por clics rápidos")
    AUTO_FIRE = ("auto_fire", "⏱️ Automático", "Efectos automáticos continuos")
    
    # Modos Creativos
    FIREWORKS = ("fireworks", "🎆 Fuegos Artificiales", "Explosiones aleatorias constantes")
    ORBITAL = ("orbital", "🌀 Orbital", "Partículas orbitan el cursor")
    LIGHTNING = ("lightning_mode", "⚡ Tormenta", "Rayos entre clics recientes")
    MIRROR = ("mirror", "🎭 Espejo", "Efectos en posición simétrica")
    
    # Modos Especiales
    KEYBOARD = ("keyboard", "⌨️ Teclado", "Efectos al escribir")
    RIGHT_CLICK_ONLY = ("right_only", "🖱️ Solo Clic Derecho", "Ignora clic izquierdo")
    
    def __init__(self, mode_id: str, display_name: str, description: str):
        self.mode_id = mode_id
        self.display_name = display_name
        self.description = description

class IntensityLevel(Enum):
    VERY_LOW = ("very_low", 80, 6, 0.6)
    LOW = ("low", 60, 10, 0.8)
    MEDIUM = ("medium", 40, 15, 1.0)
    HIGH = ("high", 20, 22, 1.3)
    VERY_HIGH = ("very_high", 10, 30, 1.6)
    
    def __init__(self, name: str, min_distance: int, particles: int, scale: float):
        self.level_name = name
        self.min_distance = min_distance
        self.particle_count = particles
        self.scale_factor = scale

# Paletas de colores ULTRA VIBRANTES - 30+ EFECTOS
class EffectColors:
    # AGUA (4)
    WATER = {
        'primary': QColor(0, 191, 255),
        'secondary': QColor(64, 224, 255),
        'accent': QColor(135, 206, 250),
        'highlight': QColor(240, 248, 255)
    }
    OCEAN = {
        'primary': QColor(0, 105, 148),
        'secondary': QColor(0, 150, 199),
        'accent': QColor(72, 209, 204),
        'highlight': QColor(127, 255, 212)
    }
    ICE = {
        'primary': QColor(175, 238, 238),
        'secondary': QColor(173, 216, 230),
        'accent': QColor(224, 255, 255),
        'highlight': QColor(240, 255, 255)
    }
    BUBBLE = {
        'primary': QColor(147, 196, 125),
        'secondary': QColor(207, 226, 243),
        'accent': QColor(219, 242, 255),
        'highlight': QColor(255, 255, 255)
    }
    
    # FUEGO (4)
    FIRE = {
        'primary': QColor(255, 69, 0),
        'secondary': QColor(255, 140, 0),
        'accent': QColor(255, 215, 0),
        'highlight': QColor(255, 255, 224)
    }
    LAVA = {
        'primary': QColor(139, 0, 0),
        'secondary': QColor(255, 69, 0),
        'accent': QColor(255, 140, 0),
        'highlight': QColor(255, 215, 0)
    }
    INFERNO = {
        'primary': QColor(178, 34, 34),
        'secondary': QColor(220, 20, 60),
        'accent': QColor(255, 99, 71),
        'highlight': QColor(255, 160, 122)
    }
    EMBER = {
        'primary': QColor(205, 92, 92),
        'secondary': QColor(233, 150, 122),
        'accent': QColor(255, 160, 122),
        'highlight': QColor(255, 228, 181)
    }
    
    # MÁGICO (5)
    SPARKLE = {
        'primary': QColor(255, 215, 0),
        'secondary': QColor(255, 255, 0),
        'accent': QColor(255, 250, 205),
        'highlight': QColor(255, 255, 255)
    }
    MAGIC = {
        'primary': QColor(138, 43, 226),
        'secondary': QColor(186, 85, 211),
        'accent': QColor(218, 112, 214),
        'highlight': QColor(255, 240, 255)
    }
    STARS = {
        'primary': QColor(255, 255, 100),
        'secondary': QColor(255, 245, 157),
        'accent': QColor(255, 250, 205),
        'highlight': QColor(255, 255, 255)
    }
    FAIRY = {
        'primary': QColor(255, 105, 180),
        'secondary': QColor(255, 182, 193),
        'accent': QColor(255, 218, 224),
        'highlight': QColor(255, 240, 245)
    }
    MYSTIC = {
        'primary': QColor(75, 0, 130),
        'secondary': QColor(148, 0, 211),
        'accent': QColor(186, 85, 211),
        'highlight': QColor(221, 160, 221)
    }
    
    # NATURAL (5)
    SNOW = {
        'primary': QColor(230, 240, 255),
        'secondary': QColor(240, 248, 255),
        'accent': QColor(248, 252, 255),
        'highlight': QColor(255, 255, 255)
    }
    SMOKE = {
        'primary': QColor(105, 105, 105),
        'secondary': QColor(128, 128, 128),
        'accent': QColor(169, 169, 169),
        'highlight': QColor(211, 211, 211)
    }
    LEAF = {
        'primary': QColor(255, 140, 0),
        'secondary': QColor(218, 165, 32),
        'accent': QColor(240, 230, 140),
        'highlight': QColor(255, 248, 220)
    }
    CHERRY = {
        'primary': QColor(255, 182, 193),
        'secondary': QColor(255, 192, 203),
        'accent': QColor(255, 218, 224),
        'highlight': QColor(255, 240, 245)
    }
    POISON = {
        'primary': QColor(0, 128, 0),
        'secondary': QColor(50, 205, 50),
        'accent': QColor(124, 252, 0),
        'highlight': QColor(173, 255, 47)
    }
    
    # ELECTRÓNICO (4)
    NEON = {
        'primary': QColor(255, 0, 255),
        'secondary': QColor(0, 255, 255),
        'accent': QColor(255, 255, 0),
        'highlight': QColor(255, 255, 255)
    }
    PLASMA = {
        'primary': QColor(138, 43, 226),
        'secondary': QColor(0, 255, 255),
        'accent': QColor(255, 0, 255),
        'highlight': QColor(255, 255, 255)
    }
    LIGHTNING = {
        'primary': QColor(135, 206, 250),
        'secondary': QColor(173, 216, 230),
        'accent': QColor(255, 255, 255),
        'highlight': QColor(240, 248, 255)
    }
    CYBER = {
        'primary': QColor(0, 255, 255),
        'secondary': QColor(64, 224, 208),
        'accent': QColor(127, 255, 212),
        'highlight': QColor(224, 255, 255)
    }
    
    # PRECIOSO (5)
    GOLD = {
        'primary': QColor(255, 215, 0),
        'secondary': QColor(255, 223, 0),
        'accent': QColor(255, 239, 146),
        'highlight': QColor(255, 250, 205)
    }
    SILVER = {
        'primary': QColor(192, 192, 192),
        'secondary': QColor(211, 211, 211),
        'accent': QColor(220, 220, 220),
        'highlight': QColor(245, 245, 245)
    }
    DIAMOND = {
        'primary': QColor(185, 242, 255),
        'secondary': QColor(200, 245, 255),
        'accent': QColor(225, 250, 255),
        'highlight': QColor(255, 255, 255)
    }
    RUBY = {
        'primary': QColor(224, 17, 95),
        'secondary': QColor(244, 67, 54),
        'accent': QColor(255, 87, 87),
        'highlight': QColor(255, 138, 128)
    }
    EMERALD = {
        'primary': QColor(0, 201, 87),
        'secondary': QColor(0, 230, 118),
        'accent': QColor(105, 240, 174),
        'highlight': QColor(178, 255, 218)
    }
    
    # CÓSMICO (4)
    GALAXY = {
        'primary': QColor(75, 0, 130),
        'secondary': QColor(138, 43, 226),
        'accent': QColor(218, 112, 214),
        'highlight': QColor(255, 192, 203)
    }
    NEBULA = {
        'primary': QColor(255, 0, 128),
        'secondary': QColor(128, 0, 255),
        'accent': QColor(0, 191, 255),
        'highlight': QColor(255, 255, 255)
    }
    AURORA = {
        'primary': QColor(0, 255, 127),
        'secondary': QColor(64, 224, 208),
        'accent': QColor(127, 255, 212),
        'highlight': QColor(224, 255, 255)
    }
    METEOR = {
        'primary': QColor(255, 140, 0),
        'secondary': QColor(255, 165, 0),
        'accent': QColor(255, 200, 124),
        'highlight': QColor(255, 239, 213)
    }
    
    # ESPECIAL (4)
    RAINBOW = {
        'primary': QColor(255, 0, 0),
        'secondary': QColor(255, 127, 0),
        'accent': QColor(255, 255, 0),
        'highlight': QColor(255, 255, 255)
    }
    BLOOD = {
        'primary': QColor(139, 0, 0),
        'secondary': QColor(178, 34, 34),
        'accent': QColor(220, 20, 60),
        'highlight': QColor(255, 99, 71)
    }
    TOXIC = {
        'primary': QColor(0, 255, 0),
        'secondary': QColor(50, 205, 50),
        'accent': QColor(124, 252, 0),
        'highlight': QColor(173, 255, 47)
    }
    MATRIX = {
        'primary': QColor(0, 128, 0),
        'secondary': QColor(0, 255, 0),
        'accent': QColor(144, 238, 144),
        'highlight': QColor(193, 255, 193)
    }
    
    # COLORES PUROS (8) - NUEVA CATEGORÍA
    RED = {
        'primary': QColor(255, 0, 0),
        'secondary': QColor(255, 80, 80),
        'accent': QColor(255, 120, 120),
        'highlight': QColor(255, 180, 180)
    }
    BLUE = {
        'primary': QColor(0, 0, 255),
        'secondary': QColor(80, 80, 255),
        'accent': QColor(120, 120, 255),
        'highlight': QColor(180, 180, 255)
    }
    GREEN = {
        'primary': QColor(0, 255, 0),
        'secondary': QColor(80, 255, 80),
        'accent': QColor(120, 255, 120),
        'highlight': QColor(180, 255, 180)
    }
    YELLOW = {
        'primary': QColor(255, 255, 0),
        'secondary': QColor(255, 255, 80),
        'accent': QColor(255, 255, 120),
        'highlight': QColor(255, 255, 180)
    }
    PURPLE = {
        'primary': QColor(180, 0, 255),
        'secondary': QColor(200, 80, 255),
        'accent': QColor(220, 120, 255),
        'highlight': QColor(235, 180, 255)
    }
    ORANGE = {
        'primary': QColor(255, 165, 0),
        'secondary': QColor(255, 185, 80),
        'accent': QColor(255, 200, 120),
        'highlight': QColor(255, 220, 180)
    }
    PINK = {
        'primary': QColor(255, 20, 147),
        'secondary': QColor(255, 105, 180),
        'accent': QColor(255, 150, 200),
        'highlight': QColor(255, 200, 230)
    }
    WHITE = {
        'primary': QColor(255, 255, 255),
        'secondary': QColor(245, 245, 245),
        'accent': QColor(235, 235, 235),
        'highlight': QColor(220, 220, 220)
    }

# ============================================================================
# CONFIGURACIÓN DE FRAGMENTOS - MODIFICA AQUÍ
# ============================================================================
class FragmentConfig:
    """Configuración global de fragmentos de explosión"""
    
    # CANTIDAD de fragmentos (multiplicador de intensidad)
    # Valores recomendados: 1=pocos, 2=normal, 3=muchos, 4=masivo
    MULTIPLIER = 4
    
    # VELOCIDAD de los fragmentos (mín, máx)
    # Valores: (2, 4)=lentos, (6, 12)=normales, (10, 20)=rápidos
    SPEED_MIN = 2
    SPEED_MAX = 4
    
    # TAMAÑO de los fragmentos (mín, máx)
    # Valores: (2, 4)=pequeños, (5, 9)=medianos, (8, 15)=grandes
    SIZE_MIN = 5
    SIZE_MAX = 12
    
    # ÁNGULO de dispersión (0 a X * pi)
    # 1 = semicírculo, 2 = círculo completo
    ANGLE_RANGE = 10
    
    # VELOCIDAD DE ROTACIÓN (mín, máx en grados/frame)
    ROTATION_MIN = -25
    ROTATION_MAX = 25

class AnimationConfig:
    FPS = 60
    FRAME_TIME = 1000 // FPS
    RIPPLE_SPEED = 3.0
    MAX_RIPPLE_RADIUS = 120
    RIPPLE_COUNT = 6
    PARTICLE_GRAVITY = 0.4
    PARTICLE_FADE_RATE = 10
    SPLASH_RADIUS = 80

# ============================================================================
# CLASES DE EFECTOS
# ============================================================================

@dataclass
class EffectSplash:
    x: float
    y: float
    radius: float = 1.0
    max_radius: float = AnimationConfig.SPLASH_RADIUS
    opacity: int = 255
    effect_type: EffectType = EffectType.WATER
    
    def update(self) -> None:
        if self.effect_type == EffectType.SMOKE:
            speed = 5.0
        elif self.effect_type in [EffectType.LIGHTNING, EffectType.PLASMA]:
            speed = 12.0
        else:
            speed = 8.0
            
        self.radius += speed
        progress = self.radius / self.max_radius
        self.opacity = int(255 * (1 - progress ** 0.5))
        
    def is_active(self) -> bool:
        return self.radius < self.max_radius and self.opacity > 0

@dataclass
class EffectRipple:
    x: float
    y: float
    radius: float = 1.0
    speed: float = AnimationConfig.RIPPLE_SPEED
    max_radius: float = AnimationConfig.MAX_RIPPLE_RADIUS
    opacity: int = 255
    intensity: float = 1.0
    effect_type: EffectType = EffectType.WATER
    
    def update(self) -> None:
        self.radius += self.speed * self.intensity
        progress = self.radius / self.max_radius
        eased_progress = 1 - (1 - progress) ** 2
        self.opacity = int(255 * (1 - eased_progress))
        
    def is_active(self) -> bool:
        return self.radius < self.max_radius and self.opacity > 0

@dataclass
class EffectParticle:
    x: float
    y: float
    vx: float
    vy: float
    life: int = 255
    size: int = 3
    rotation: float = 0.0
    rotation_speed: float = 0.0
    effect_type: EffectType = EffectType.WATER
    color_shift: float = 0.0
    is_fragment: bool = False  # Indica si es un fragmento irregular de explosión
    
    @classmethod
    def create(cls, x: float, y: float, effect_type: EffectType, is_click: bool = True) -> 'EffectParticle':
        angle = random.uniform(0, 2 * math.pi)
        
        if effect_type in [EffectType.FIRE, EffectType.LAVA]:
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed * 0.3
            vy = -random.uniform(4, 10)
            size = random.randint(3, 7)
        elif effect_type == EffectType.SMOKE:
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed * 0.5
            vy = -random.uniform(2, 5)
            size = random.randint(5, 12)
        elif effect_type == EffectType.SNOW:
            vx = random.uniform(-2, 2)
            vy = random.uniform(1, 3)
            size = random.randint(2, 5)
        elif effect_type in [EffectType.SPARKLE, EffectType.STARS]:
            speed = random.uniform(6, 14)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.randint(1, 3)
        elif effect_type in [EffectType.NEON, EffectType.PLASMA, EffectType.LIGHTNING]:
            speed = random.uniform(4, 9)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            size = random.randint(2, 5)
        elif effect_type in [EffectType.MAGIC]:
            speed = random.uniform(3, 7)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2
            size = random.randint(3, 6)
        elif effect_type == EffectType.OCEAN:
            speed = random.uniform(4, 10)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed * 0.7
            size = random.randint(3, 6)
        else:
            speed = random.uniform(5, 12) if is_click else random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed + (random.uniform(-4, -1) if is_click else random.uniform(-2, 0))
            size = random.randint(2, 5) if is_click else random.randint(1, 3)
        
        return cls(
            x=x, y=y, vx=vx, vy=vy, size=size,
            rotation=random.uniform(0, 360),
            rotation_speed=random.uniform(-8, 8),
            effect_type=effect_type,
            color_shift=random.uniform(0, 360)
        )
    
    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy
        
        if self.effect_type in [EffectType.FIRE, EffectType.LAVA]:
            self.vy -= 0.2
            self.vx *= 0.95
        elif self.effect_type == EffectType.SMOKE:
            self.vy -= 0.15
            self.vx *= 0.98
            self.size += 0.1
        elif self.effect_type == EffectType.SNOW:
            self.vy += 0.1
            self.vx *= 0.99
        elif self.effect_type in [EffectType.MAGIC]:
            self.vy -= 0.1
            self.vx *= 0.96
        elif self.effect_type == EffectType.OCEAN:
            self.vy += 0.2
            self.vx *= 0.98
        else:
            self.vy += AnimationConfig.PARTICLE_GRAVITY
            self.vx *= 0.97
        
        self.rotation += self.rotation_speed
        self.color_shift += 5
        self.life -= AnimationConfig.PARTICLE_FADE_RATE
        
    def is_active(self) -> bool:
        return self.life > 0

@dataclass
class TrailDrop:
    x: float
    y: float
    vy: float = 0.0
    life: int = 255
    size: int = 2
    effect_type: EffectType = EffectType.WATER
    is_fragment: bool = False
    
    def update(self) -> None:
        self.y += self.vy
        self.vy += 0.5
        self.life -= 5
        
    def is_active(self) -> bool:
        return self.life > 0

class GlobalMouseSignals(QObject):
    click = pyqtSignal(int, int, bool)  # x, y, is_right_click
    move = pyqtSignal(int, int)

# ============================================================================
# OVERLAY PRINCIPAL
# ============================================================================

class AdvancedMultiEffectOverlay(QWidget):
    
    def __init__(self):
        super().__init__()
        
        # Archivo de configuración
        self.config_file = os.path.join(os.path.expanduser('~'), 'effect_overlay_config.json')
        
        # Cargar configuración guardada o usar valores predeterminados
        self._load_config()
        
        self.splashes: List[EffectSplash] = []
        self.ripples: List[EffectRipple] = []
        self.particles: List[EffectParticle] = []
        self.trail_drops: List[TrailDrop] = []
        
        self.last_drop_pos = None
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Variables para detectar doble clic
        self.last_click_time = 0
        self.last_click_pos = (0, 0)
        self.double_click_threshold = 0.3  # 300ms para detectar doble clic
        self.double_click_distance = 10  # 10 píxeles de tolerancia
        
        # Variables para modo DRAG_PAINT
        self.is_dragging = False
        self.drag_last_pos = None
        
        # Variables para modo COMBO
        self.combo_multiplier = 1.0
        self.combo_last_click = 0
        self.combo_timeout = 2.0  # segundos
        self.combo_click_history = []
        
        # Variables para modo LIGHTNING
        self.lightning_history = []  # Historial de clics para rayos
        self.lightning_max_history = 5
        
        # Variables para modo ORBITAL
        self.orbital_particles_cache = []
        
        # Lista de clics recientes para varios modos
        self.recent_clicks = []
        
        self.signals = GlobalMouseSignals()
        self.signals.click.connect(self._handle_click)
        self.signals.move.connect(self._handle_move)
        
        self._setup_window()
        self._setup_animation()
        self._setup_system_tray()
        self._start_mouse_listener()
        self._start_keyboard_listener()
        
    def _setup_window(self) -> None:
        # Flags para estar sobre TODO (incluyendo menú inicio y barra de tareas)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.X11BypassWindowManagerHint |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.BypassWindowManagerHint
        )
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # Cubrir TODAS las pantallas
        total_geometry = QApplication.primaryScreen().virtualGeometry()
        self.setGeometry(total_geometry)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        
        # Asegurar que esté arriba de TODO
        self.raise_()
        self.activateWindow()
        
    def _setup_animation(self) -> None:
        # Timer principal de animación
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._update_effects)
        self.animation_timer.start(AnimationConfig.FRAME_TIME)
        
        # Timer para mantener la ventana siempre arriba (cada 50ms para mayor agresividad)
        self.top_timer = QTimer(self)
        self.top_timer.timeout.connect(self._keep_on_top)
        self.top_timer.start(50)
        
        # Timer para modos automáticos (AUTO_FIRE, FIREWORKS)
        self.auto_timer = QTimer(self)
        # self.auto_timer.timeout.connect(self._auto_effects_tick)  # TEMPORALMENTE DESHABILITADO
        self.auto_fire_interval = 1000  # 1 segundo por defecto
        
        # Timer para modo ORBITAL
        self.orbital_timer = QTimer(self)
        # self.orbital_timer.timeout.connect(self._orbital_tick)  # TEMPORALMENTE DESHABILITADO
        # self.orbital_timer.start(50)  # 50ms para suavidad
        
    def _setup_system_tray(self) -> None:
        """Configura el icono y menú de la bandeja del sistema"""
        icon = self._create_tray_icon()
        self.tray_icon = QSystemTrayIcon(icon, self)
        
        menu = QMenu()
        menu.installEventFilter(self)
        
        # ============ ESTADO ============
        self.action_toggle = menu.addAction("🟢 Activo")
        self.action_toggle.triggered.connect(self._toggle_effect)
        
        menu.addSeparator()
        menu.addAction("─── CONFIGURACIÓN ───").setEnabled(False)
        menu.addSeparator()
        
        # ============ BOTONES DEL MOUSE ============
        mouse_menu = menu.addMenu("🖱️  Botones del Mouse")
        mouse_menu.installEventFilter(self)
        
        # Clic Izquierdo
        left_submenu = mouse_menu.addMenu("👈 Clic Izquierdo")
        left_submenu.installEventFilter(self)
        self._add_effects_to_menu(left_submenu, is_right_click=False)
        
        # Clic Derecho - CON TODOS LOS EFECTOS ORGANIZADOS
        right_submenu = mouse_menu.addMenu("👉 Clic Derecho")
        right_submenu.installEventFilter(self)
        self.right_click_actions = {}
        self._add_right_click_effects_to_menu(right_submenu)
        # Marcar el efecto por defecto (se hará en _load_config después)
        
        menu.addSeparator()
        
        # ============ MODO & INTENSIDAD ============
        mode_menu = menu.addMenu("⚙️  Modo de Operación")
        mode_menu.installEventFilter(self)
        self.mode_actions = {}
        for mode in EffectMode:
            action = mode_menu.addAction(mode.display_name)
            action.setToolTip(mode.description)
            action.triggered.connect(lambda checked, m=mode: self._set_mode(m))
            self.mode_actions[mode] = action
        self.mode_actions[EffectMode.CLICK_ONLY].setText("● " + EffectMode.CLICK_ONLY.display_name)
        
        intensity_menu = menu.addMenu("📊 Intensidad")
        intensity_menu.installEventFilter(self)
        self.action_very_low = intensity_menu.addAction("○ Muy Baja")
        self.action_very_low.triggered.connect(lambda: self._set_intensity(IntensityLevel.VERY_LOW))
        self.action_low = intensity_menu.addAction("○ Baja")
        self.action_low.triggered.connect(lambda: self._set_intensity(IntensityLevel.LOW))
        self.action_medium = intensity_menu.addAction("● Media")
        self.action_medium.triggered.connect(lambda: self._set_intensity(IntensityLevel.MEDIUM))
        self.action_high = intensity_menu.addAction("○ Alta")
        self.action_high.triggered.connect(lambda: self._set_intensity(IntensityLevel.HIGH))
        self.action_very_high = intensity_menu.addAction("○ Muy Alta")
        self.action_very_high.triggered.connect(lambda: self._set_intensity(IntensityLevel.VERY_HIGH))
        
        menu.addSeparator()
        
        # ============ OPCIONES ADICIONALES ============
        self.action_fragments = menu.addAction("💥 Fragmentos de Explosión: ON")
        self.action_fragments.triggered.connect(self._toggle_fragments)
        
        self.action_keyboard = menu.addAction("⌨️ Teclado Combinado: OFF")
        self.action_keyboard.triggered.connect(self._toggle_keyboard_effects)
        
        self.action_startup = menu.addAction("🚀 Iniciar con Windows")
        self.action_startup.triggered.connect(self._toggle_startup)
        self._update_startup_status()
        
        # Actualizar UI según configuración cargada
        self._update_ui_from_config()
        
        menu.addSeparator()
        menu.addAction("─── SISTEMA ───").setEnabled(False)
        menu.addSeparator()
        menu.addAction("ℹ️  Acerca de").triggered.connect(self._show_about)
        menu.addAction("❌ Salir").triggered.connect(self._quit_application)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
        self.tray_icon.setToolTip("Advanced Multi Effect Overlay v9.0 - MEGA EDITION")
    
    def _add_effects_to_menu(self, parent_menu, is_right_click=False):
        """Agrega todos los efectos a un menú de forma organizada"""
        self.effect_actions = {}
        
        # Agua (4)
        water_menu = parent_menu.addMenu("💦 Agua")
        water_menu.installEventFilter(self)
        for eff in [EffectType.WATER, EffectType.OCEAN, EffectType.ICE, EffectType.BUBBLE]:
            action = water_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Fuego (4)
        fire_menu = parent_menu.addMenu("🔥 Fuego")
        fire_menu.installEventFilter(self)
        for eff in [EffectType.FIRE, EffectType.LAVA, EffectType.INFERNO, EffectType.EMBER]:
            action = fire_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Mágicos (5)
        magic_menu = parent_menu.addMenu("✨ Mágico")
        magic_menu.installEventFilter(self)
        for eff in [EffectType.SPARKLE, EffectType.MAGIC, EffectType.STARS, EffectType.FAIRY, EffectType.MYSTIC]:
            action = magic_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Naturales (5)
        nature_menu = parent_menu.addMenu("� Natural")
        nature_menu.installEventFilter(self)
        for eff in [EffectType.SNOW, EffectType.SMOKE, EffectType.LEAF, EffectType.CHERRY, EffectType.POISON]:
            action = nature_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Electrónicos (4)
        elec_menu = parent_menu.addMenu("⚡ Electrónico")
        elec_menu.installEventFilter(self)
        for eff in [EffectType.NEON, EffectType.PLASMA, EffectType.LIGHTNING, EffectType.CYBER]:
            action = elec_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Preciosos (5)
        precious_menu = parent_menu.addMenu("💎 Precioso")
        precious_menu.installEventFilter(self)
        for eff in [EffectType.GOLD, EffectType.SILVER, EffectType.DIAMOND, EffectType.RUBY, EffectType.EMERALD]:
            action = precious_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Cósmicos (4)
        cosmic_menu = parent_menu.addMenu("🌌 Cósmico")
        cosmic_menu.installEventFilter(self)
        for eff in [EffectType.GALAXY, EffectType.NEBULA, EffectType.AURORA, EffectType.METEOR]:
            action = cosmic_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Especiales (4)
        special_menu = parent_menu.addMenu("🌈 Especial")
        special_menu.installEventFilter(self)
        for eff in [EffectType.RAINBOW, EffectType.BLOOD, EffectType.TOXIC, EffectType.MATRIX]:
            action = special_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        # Colores Puros (8) - NUEVA CATEGORÍA
        colors_menu = parent_menu.addMenu("🎨 Colores Puros")
        colors_menu.installEventFilter(self)
        for eff in [EffectType.RED, EffectType.BLUE, EffectType.GREEN, EffectType.YELLOW, 
                    EffectType.PURPLE, EffectType.ORANGE, EffectType.PINK, EffectType.WHITE]:
            action = colors_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_effect_type(e))
            action.hovered.connect(lambda e=eff: self._on_menu_hover(e))
            self.effect_actions[eff] = action
        
        self.effect_actions[EffectType.WATER].setText("● " + EffectType.WATER.display_name)
    
    def _add_right_click_effects_to_menu(self, parent_menu):
        """Agrega todos los efectos al menú de clic derecho de forma organizada"""
        # Agua (4)
        water_menu = parent_menu.addMenu("💦 Agua")
        water_menu.installEventFilter(self)
        for eff in [EffectType.WATER, EffectType.OCEAN, EffectType.ICE, EffectType.BUBBLE]:
            action = water_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Fuego (4)
        fire_menu = parent_menu.addMenu("🔥 Fuego")
        fire_menu.installEventFilter(self)
        for eff in [EffectType.FIRE, EffectType.LAVA, EffectType.INFERNO, EffectType.EMBER]:
            action = fire_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Mágicos (5)
        magic_menu = parent_menu.addMenu("✨ Mágico")
        magic_menu.installEventFilter(self)
        for eff in [EffectType.SPARKLE, EffectType.MAGIC, EffectType.STARS, EffectType.FAIRY, EffectType.MYSTIC]:
            action = magic_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Naturales (5)
        nature_menu = parent_menu.addMenu("🍃 Natural")
        nature_menu.installEventFilter(self)
        for eff in [EffectType.SNOW, EffectType.SMOKE, EffectType.LEAF, EffectType.CHERRY, EffectType.POISON]:
            action = nature_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Electrónicos (4)
        elec_menu = parent_menu.addMenu("⚡ Electrónico")
        elec_menu.installEventFilter(self)
        for eff in [EffectType.NEON, EffectType.PLASMA, EffectType.LIGHTNING, EffectType.CYBER]:
            action = elec_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Preciosos (5)
        precious_menu = parent_menu.addMenu("💎 Precioso")
        precious_menu.installEventFilter(self)
        for eff in [EffectType.GOLD, EffectType.SILVER, EffectType.DIAMOND, EffectType.RUBY, EffectType.EMERALD]:
            action = precious_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Cósmicos (4)
        cosmic_menu = parent_menu.addMenu("🌌 Cósmico")
        cosmic_menu.installEventFilter(self)
        for eff in [EffectType.GALAXY, EffectType.NEBULA, EffectType.AURORA, EffectType.METEOR]:
            action = cosmic_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Especiales (4)
        special_menu = parent_menu.addMenu("🌈 Especial")
        special_menu.installEventFilter(self)
        for eff in [EffectType.RAINBOW, EffectType.BLOOD, EffectType.TOXIC, EffectType.MATRIX]:
            action = special_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
        # Colores Puros (8) - NUEVA CATEGORÍA TAMBIÉN EN CLIC DERECHO
        colors_menu = parent_menu.addMenu("🎨 Colores Puros")
        colors_menu.installEventFilter(self)
        for eff in [EffectType.RED, EffectType.BLUE, EffectType.GREEN, EffectType.YELLOW,
                    EffectType.PURPLE, EffectType.ORANGE, EffectType.PINK, EffectType.WHITE]:
            action = colors_menu.addAction(eff.display_name)
            action.triggered.connect(lambda checked, e=eff: self._set_right_click_effect(e))
            self.right_click_actions[eff] = action
        
    def _create_tray_icon(self) -> QIcon:
        pixmap = QPixmap(128, 128)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Arcoíris vibrante
        for i in range(12):
            angle = i * 30
            hue = i * 30
            color = QColor.fromHsv(hue, 255, 255)
            painter.setPen(QPen(color, 6))
            painter.drawArc(24, 24, 80, 80, angle * 16, 30 * 16)
        
        # Centro ultra brillante
        gradient = QRadialGradient(64, 64, 35)
        gradient.setColorAt(0, QColor(255, 255, 255, 255))
        gradient.setColorAt(0.5, QColor(255, 215, 0, 200))
        gradient.setColorAt(1, QColor(138, 43, 226, 150))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(39, 39, 50, 50)
        
        painter.end()
        return QIcon(pixmap)
        
    def _start_mouse_listener(self) -> None:
        def on_click(x, y, button, pressed):
            # SOPORTE PARA AMBOS BOTONES: Izquierdo Y Derecho
            if self.is_active:
                if pressed:  # Botón presionado
                    if button == mouse.Button.left:
                        self.signals.click.emit(x, y, False)  # False = clic izquierdo
                        self.is_dragging = True
                        self.drag_last_pos = (x, y)
                    elif button == mouse.Button.right:
                        self.signals.click.emit(x, y, True)   # True = clic derecho
                        self.is_dragging = True
                        self.drag_last_pos = (x, y)
                else:  # Botón soltado
                    self.is_dragging = False
                    self.drag_last_pos = None
                
        def on_move(x, y):
            if self.is_active:
                self.signals.move.emit(x, y)
        
        self.mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
        self.mouse_listener.start()
    
    def _start_keyboard_listener(self) -> None:
        """Inicia listener de teclado para modo KEYBOARD"""
        def on_press(key):
            # Solo crear efectos si está activo Y (modo KEYBOARD o efectos de teclado combinables habilitados)
            if self.is_active and (self.effect_mode == EffectMode.KEYBOARD or self.keyboard_effects_enabled):
                # Crear efecto en la posición actual del cursor del mouse
                x = self.mouse_x
                y = self.mouse_y
                
                # EFECTO ALEATORIO EN CADA TECLA
                random_effect = random.choice(list(EffectType))
                
                # Crear efecto pequeño con color aleatorio
                for _ in range(8):  # Más partículas para mejor visibilidad
                    self.particles.append(EffectParticle.create(x, y, random_effect, is_click=False))
                
                # Agregar mini ripple con color aleatorio
                self.ripples.append(EffectRipple(
                    x=x, y=y,
                    intensity=0.6,
                    max_radius=50,
                    effect_type=random_effect
                ))
        
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.keyboard_listener.start()
        
    def _handle_click(self, x: int, y: int, is_right_click: bool) -> None:
        import time
        
        # Modo RIGHT_CLICK_ONLY: ignorar clics izquierdos
        if self.effect_mode == EffectMode.RIGHT_CLICK_ONLY and not is_right_click:
            return
        
        # Usar efecto alternativo para clic derecho
        effect_to_use = self.right_click_effect if is_right_click else self.current_effect
        
        # Modo RANDOM: elegir efecto aleatorio
        if self.effect_mode == EffectMode.RANDOM:
            all_effects = list(EffectType)
            effect_to_use = random.choice(all_effects)
        
        # Detectar doble clic
        current_time = time.time()
        time_diff = current_time - self.last_click_time
        distance = math.sqrt((x - self.last_click_pos[0])**2 + (y - self.last_click_pos[1])**2)
        
        is_double_click = (time_diff < self.double_click_threshold and 
                          distance < self.double_click_distance)
        
        # Actualizar last click  
        self.last_click_time = current_time
        self.last_click_pos = (x, y)
        
        # Agregar a historial para LIGHTNING
        self.recent_clicks.append({'x': x, 'y': y, 'time': current_time, 'effect': effect_to_use})
        if len(self.recent_clicks) > 10:
            self.recent_clicks.pop(0)
        
        # Modo COMBO: actualizar multiplicador
        if self.effect_mode == EffectMode.COMBO:
            if time_diff < self.combo_timeout:
                self.combo_multiplier = min(self.combo_multiplier + 0.5, 10.0)
            else:
                self.combo_multiplier = 1.0
            self.combo_last_click = current_time
        
        # En modo DOUBLE_CLICK, solo activar con doble clic
        if self.effect_mode == EffectMode.DOUBLE_CLICK:
            if is_double_click:
                self._create_big_splash(x, y, effect_to_use)
            return
        
        # En modo DRAG_PAINT, no crear efectos en clic (solo en drag)
        if self.effect_mode == EffectMode.DRAG_PAINT:
            return
        
        # Ejecutar efecto según el modo
        if self.effect_mode == EffectMode.CLICK_ONLY:
            self._create_big_splash(x, y, effect_to_use)
        elif self.effect_mode == EffectMode.BURST:
            self._create_burst(x, y, effect_to_use)
        elif self.effect_mode == EffectMode.RIPPLE_ONLY:
            self._create_ripples_only(x, y, effect_to_use)
        elif self.effect_mode == EffectMode.MINIMAL:
            self._create_minimal(x, y, effect_to_use)
        elif self.effect_mode == EffectMode.COMBO:
            # _create_combo_splash no implementado aún - usar básico con multiplicador visual
            for _ in range(int(self.combo_multiplier)):
                self._create_big_splash(x + random.randint(-10, 10), y + random.randint(-10, 10), effect_to_use)
        elif self.effect_mode == EffectMode.MIRROR:
            # _create_mirror_effect no implementado - crear dos efectos simétricos
            screen = QApplication.primaryScreen().geometry()
            center_x = screen.width() / 2
            self._create_big_splash(x, y, effect_to_use)
            mirror_x = center_x + (center_x - x)
            self._create_big_splash(mirror_x, y, effect_to_use)
        elif self.effect_mode == EffectMode.LIGHTNING:
            # _create_lightning_effect no implementado - usar básico
            self._create_big_splash(x, y, effect_to_use)
        elif self.effect_mode in [EffectMode.RANDOM, EffectMode.RIGHT_CLICK_ONLY, 
                                   EffectMode.AUTO_FIRE, EffectMode.FIREWORKS, 
                                   EffectMode.ORBITAL]:
            self._create_big_splash(x, y, effect_to_use)
        else:
            self._create_big_splash(x, y, effect_to_use)
            
    def _handle_move(self, x: int, y: int) -> None:
        self.mouse_x = x
        self.mouse_y = y
        
        # Modo DRAG_PAINT: efectos mientras arrastras
        if self.effect_mode == EffectMode.DRAG_PAINT and self.is_dragging:
            if self.drag_last_pos is not None:
                distance = math.sqrt((x - self.drag_last_pos[0])**2 + (y - self.drag_last_pos[1])**2)
                if distance >= 15:  # Cada 15 píxeles
                    effect = self.current_effect
                    for _ in range(3):  # Crear múltiples partículas
                        self.particles.append(EffectParticle.create(x, y, effect, is_click=False))
                    self.drag_last_pos = (x, y)
            return
        
        # Modos originales
        if self.effect_mode == EffectMode.FOLLOW_MOUSE:
            if self.last_drop_pos is None:
                self.last_drop_pos = (x, y)
                return
                
            dx = x - self.last_drop_pos[0]
            dy = y - self.last_drop_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance >= self.intensity_level.min_distance:
                self._create_trail_effect(x, y)
                self.last_drop_pos = (x, y)
        elif self.effect_mode == EffectMode.TRAIL:
            self._create_light_trail(x, y)
        elif self.effect_mode == EffectMode.CLICK_ONLY:
            if random.random() < 0.005:
                self._create_subtle_ripple(x, y)
                
    def _create_big_splash(self, x: float, y: float, effect_type: EffectType = None) -> None:
        if effect_type is None:
            effect_type = self.current_effect
        self.splashes.append(EffectSplash(x=x, y=y, effect_type=effect_type))
        
        intensity = random.uniform(1.0, 1.3)
        self.ripples.append(EffectRipple(
            x=x, y=y, 
            intensity=intensity,
            max_radius=AnimationConfig.MAX_RIPPLE_RADIUS * intensity,
            effect_type=effect_type
        ))
        
        # MUCHAS MÁS PARTÍCULAS al hacer clic (4x en lugar de 2x)
        particle_count = self.intensity_level.particle_count * 4
        for _ in range(random.randint(particle_count, particle_count + 15)):
            self.particles.append(EffectParticle.create(x, y, effect_type, is_click=True))
        
        # AGREGAR FRAGMENTOS/CACHOS que explotan (solo si está activado)
        if self.fragments_enabled:
            fragment_count = self.intensity_level.particle_count * FragmentConfig.MULTIPLIER
            for _ in range(fragment_count):
                angle = random.uniform(0, FragmentConfig.ANGLE_RANGE * math.pi)
                speed = random.uniform(FragmentConfig.SPEED_MIN, FragmentConfig.SPEED_MAX)
                size = random.randint(FragmentConfig.SIZE_MIN, FragmentConfig.SIZE_MAX)
                self.particles.append(EffectParticle(
                    x=x, y=y,
                    vx=math.cos(angle) * speed,
                    vy=math.sin(angle) * speed,
                    life=255,
                    size=size,
                    rotation=random.uniform(0, 360),
                    rotation_speed=random.uniform(FragmentConfig.ROTATION_MIN, FragmentConfig.ROTATION_MAX),
                    effect_type=effect_type,
                    color_shift=random.uniform(0, 360),
                    is_fragment=True  # MARCADO COMO FRAGMENTO
                ))
            
    def _create_trail_effect(self, x: float, y: float) -> None:
        self.ripples.append(EffectRipple(
            x=x, y=y, 
            intensity=0.6,
            max_radius=60,
            effect_type=self.current_effect
        ))
        
        num_particles = max(2, self.intensity_level.particle_count // 3)
        for _ in range(num_particles):
            self.particles.append(EffectParticle.create(x, y, self.current_effect, is_click=False))
            
        if random.random() < 0.3:
            self.trail_drops.append(TrailDrop(x=x, y=y, size=random.randint(2, 4), effect_type=self.current_effect))
            
    def _create_subtle_ripple(self, x: float, y: float) -> None:
        self.ripples.append(EffectRipple(
            x=x, y=y, 
            intensity=0.3,
            max_radius=40,
            effect_type=self.current_effect
        ))
    
    def _on_menu_hover(self, effect: EffectType) -> None:
        """Crea efecto visual sutil cuando pasas el mouse por un efecto del menú"""
        if self.is_active:
            # Obtener posición actual del mouse
            from PyQt6.QtGui import QCursor
            pos = QCursor.pos()
            # Crear ondas sutiles del efecto que está siendo resaltado
            old_effect = self.current_effect
            self.current_effect = effect  # Temporalmente cambiar al efecto hover
            self._create_subtle_ripple(pos.x(), pos.y())
            self.current_effect = old_effect  # Restaurar efecto original
    
    def _create_burst(self, x: float, y: float, effect_type: EffectType = None) -> None:
        """Modo Burst: Explosión de partículas"""
        if effect_type is None:
            effect_type = self.current_effect
        count = self.intensity_level.particle_count * 3
        for _ in range(count):
            self.particles.append(EffectParticle.create(x, y, effect_type, is_click=True))
    
    def _create_ripples_only(self, x: float, y: float, effect_type: EffectType = None) -> None:
        """Modo Ripple: Solo ondas, sin partículas"""
        if effect_type is None:
            effect_type = self.current_effect
        for i in range(3):
            self.ripples.append(EffectRipple(
                x=x, y=y,
                radius=i * 20,
                intensity=1.0 - i * 0.2,
                max_radius=120,
                effect_type=effect_type
            ))
    
    def _create_minimal(self, x: float, y: float, effect_type: EffectType = None) -> None:
        """Modo Minimal: Efecto ultra ligero"""
        if effect_type is None:
            effect_type = self.current_effect
        self.ripples.append(EffectRipple(x=x, y=y, max_radius=60, effect_type=effect_type))
        for _ in range(3):
            self.particles.append(EffectParticle.create(x, y, effect_type, is_click=True))
    
    def _create_light_trail(self, x: float, y: float) -> None:
        """Modo Trail: Estela de luz"""
        if len(self.particles) < 80:
            self.particles.append(EffectParticle.create(x, y, self.current_effect, is_click=False))
    
    def _keep_on_top(self) -> None:
        """Mantiene el overlay siempre visible sobre TODO (incluso menú inicio)"""
        if self.is_active:
            try:
                # Obtener el handle de la ventana
                hwnd = int(self.winId())
                
                # Usar SetWindowPos de Windows para forzar HWND_TOPMOST
                ctypes.windll.user32.SetWindowPos(
                    hwnd,
                    HWND_TOPMOST,
                    0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
                )
            except:
                # Fallback a métodos de Qt
                self.raise_()
                self.activateWindow()
        
    def _update_effects(self) -> None:
        for splash in self.splashes:
            splash.update()
        self.splashes = [s for s in self.splashes if s.is_active()]
        
        for ripple in self.ripples:
            ripple.update()
        self.ripples = [r for r in self.ripples if r.is_active()]
        
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_active()]
        
        for drop in self.trail_drops:
            drop.update()
        self.trail_drops = [d for d in self.trail_drops if d.is_active()]
        
        if self.splashes or self.ripples or self.particles or self.trail_drops:
            self.update()
            
    def _get_colors(self, effect_type: EffectType) -> dict:
        color_map = {
            # Agua
            EffectType.WATER: EffectColors.WATER,
            EffectType.OCEAN: EffectColors.OCEAN,
            EffectType.ICE: EffectColors.ICE,
            EffectType.BUBBLE: EffectColors.BUBBLE,
            # Fuego
            EffectType.FIRE: EffectColors.FIRE,
            EffectType.LAVA: EffectColors.LAVA,
            EffectType.INFERNO: EffectColors.INFERNO,
            EffectType.EMBER: EffectColors.EMBER,
            # Mágico
            EffectType.SPARKLE: EffectColors.SPARKLE,
            EffectType.MAGIC: EffectColors.MAGIC,
            EffectType.STARS: EffectColors.STARS,
            EffectType.FAIRY: EffectColors.FAIRY,
            EffectType.MYSTIC: EffectColors.MYSTIC,
            # Natural
            EffectType.SNOW: EffectColors.SNOW,
            EffectType.SMOKE: EffectColors.SMOKE,
            EffectType.LEAF: EffectColors.LEAF,
            EffectType.CHERRY: EffectColors.CHERRY,
            EffectType.POISON: EffectColors.POISON,
            # Electrónico
            EffectType.NEON: EffectColors.NEON,
            EffectType.PLASMA: EffectColors.PLASMA,
            EffectType.LIGHTNING: EffectColors.LIGHTNING,
            EffectType.CYBER: EffectColors.CYBER,
            # Precioso
            EffectType.GOLD: EffectColors.GOLD,
            EffectType.SILVER: EffectColors.SILVER,
            EffectType.DIAMOND: EffectColors.DIAMOND,
            EffectType.RUBY: EffectColors.RUBY,
            EffectType.EMERALD: EffectColors.EMERALD,
            # Cósmico
            EffectType.GALAXY: EffectColors.GALAXY,
            EffectType.NEBULA: EffectColors.NEBULA,
            EffectType.AURORA: EffectColors.AURORA,
            EffectType.METEOR: EffectColors.METEOR,
            # Especial
            EffectType.RAINBOW: EffectColors.RAINBOW,
            EffectType.BLOOD: EffectColors.BLOOD,
            EffectType.TOXIC: EffectColors.TOXIC,
            EffectType.MATRIX: EffectColors.MATRIX,
            # Colores Puros
            EffectType.RED: EffectColors.RED,
            EffectType.BLUE: EffectColors.BLUE,
            EffectType.GREEN: EffectColors.GREEN,
            EffectType.YELLOW: EffectColors.YELLOW,
            EffectType.PURPLE: EffectColors.PURPLE,
            EffectType.ORANGE: EffectColors.ORANGE,
            EffectType.PINK: EffectColors.PINK,
            EffectType.WHITE: EffectColors.WHITE
        }
        return color_map.get(effect_type, EffectColors.WATER)
            
    def paintEvent(self, event) -> None:
        if not self.is_active:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        for splash in self.splashes:
            self._draw_splash(painter, splash)
        
        for ripple in self.ripples:
            self._draw_ripple(painter, ripple)
            
        for particle in self.particles:
            self._draw_particle(painter, particle)
            
        for drop in self.trail_drops:
            self._draw_trail_drop(painter, drop)
            
    def _draw_splash(self, painter: QPainter, splash: EffectSplash) -> None:
        colors = self._get_colors(splash.effect_type)
        
        gradient = QRadialGradient(splash.x, splash.y, splash.radius)
        center_color = QColor(*colors['highlight'].getRgb()[:3], splash.opacity)
        edge_color = QColor(*colors['primary'].getRgb()[:3], 0)
        
        gradient.setColorAt(0.7, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.85, center_color)
        gradient.setColorAt(1.0, edge_color)
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(splash.x, splash.y), splash.radius, splash.radius)
        
    def _draw_ripple(self, painter: QPainter, ripple: EffectRipple) -> None:
        colors = self._get_colors(ripple.effect_type)
        
        for i in range(AnimationConfig.RIPPLE_COUNT):
            offset = i * 12
            current_radius = ripple.radius - offset
            
            if current_radius <= 0:
                continue
                
            opacity_factor = max(0, 1 - i / AnimationConfig.RIPPLE_COUNT)
            current_opacity = int(ripple.opacity * opacity_factor)
            
            t = i / AnimationConfig.RIPPLE_COUNT
            
            if ripple.effect_type in [EffectType.NEON, EffectType.PLASMA]:
                hue = int((i * 60 + ripple.radius) % 360)
                color = QColor.fromHsv(hue, 255, 255, current_opacity)
            elif ripple.effect_type == EffectType.LIGHTNING:
                color = colors['accent'] if i % 2 == 0 else colors['secondary']
                color = QColor(*color.getRgb()[:3], current_opacity)
            else:
                color = QColor(
                    int(colors['primary'].red() + (colors['secondary'].red() - colors['primary'].red()) * t),
                    int(colors['primary'].green() + (colors['secondary'].green() - colors['primary'].green()) * t),
                    int(colors['primary'].blue() + (colors['secondary'].blue() - colors['primary'].blue()) * t),
                    current_opacity
                )
            
            width = max(1, 4 - i)
            painter.setPen(QPen(color, width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawEllipse(QPointF(ripple.x, ripple.y), current_radius, current_radius)
        
        if ripple.radius < 20:
            center_opacity = int(ripple.opacity * 0.9)
            center_color = QColor(*colors['highlight'].getRgb()[:3], center_opacity)
            
            gradient = QRadialGradient(ripple.x, ripple.y, 8)
            gradient.setColorAt(0, center_color)
            gradient.setColorAt(1, QColor(center_color.red(), center_color.green(), center_color.blue(), 0))
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(QPointF(ripple.x, ripple.y), 8, 8)
            
    def _draw_particle(self, painter: QPainter, particle: EffectParticle) -> None:
        colors = self._get_colors(particle.effect_type)
        opacity = max(0, particle.life)
        
        if particle.effect_type in [EffectType.FIRE, EffectType.LAVA]:
            t = particle.life / 255
            if particle.effect_type == EffectType.LAVA:
                color = QColor(int(139 + (255-139) * (1-t)), int(69 * t), 0, opacity)
            else:
                color = QColor(255, int(69 + 186 * t), 0, opacity)
        elif particle.effect_type in [EffectType.SPARKLE, EffectType.STARS]:
            color = QColor(*colors['highlight'].getRgb()[:3], opacity)
        elif particle.effect_type in [EffectType.NEON, EffectType.PLASMA]:
            hue = int(particle.color_shift % 360)
            color = QColor.fromHsv(hue, 255, 255, opacity)
        elif particle.effect_type == EffectType.MAGIC:
            hue = int((280 + particle.color_shift) % 360)
            color = QColor.fromHsv(hue, 200, 255, opacity)
        else:
            color = QColor(*colors['accent'].getRgb()[:3], opacity)
        
        painter.save()
        painter.translate(particle.x, particle.y)
        painter.rotate(particle.rotation)
        
        # Si la partícula es un fragmento y están habilitados, dibujarla como forma irregular
        if particle.is_fragment and self.fragments_enabled:
            # FRAGMENTOS IRREGULARES (como cachos de vidrio/cristal)
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            
            # Crear forma irregular (triángulo/polígono)
            path = QPainterPath()
            sides = random.choice([3, 4, 5])  # 3=triángulo, 4=cuadrado irregular, 5=pentágono
            points = []
            for i in range(sides):
                angle = (i * 360 / sides) * math.pi / 180
                # Distancia irregular para cada punto
                dist = particle.size * random.uniform(0.6, 1.2)
                points.append(QPointF(math.cos(angle) * dist, math.sin(angle) * dist))
            
            if points:
                path.moveTo(points[0])
                for point in points[1:]:
                    path.lineTo(point)
                path.closeSubpath()
                painter.fillPath(path, QBrush(color))
        elif particle.effect_type in [EffectType.STARS]:
            # Dibujar estrella
            painter.setPen(Qt.PenStyle.NoPen)
            gradient = QRadialGradient(0, 0, particle.size)
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(QBrush(gradient))
            
            path = QPainterPath()
            points = []
            for i in range(5):
                outer_angle = (i * 144 - 90) * math.pi / 180
                inner_angle = ((i * 144 - 90) + 72) * math.pi / 180
                points.append(QPointF(math.cos(outer_angle) * particle.size, 
                                     math.sin(outer_angle) * particle.size))
                points.append(QPointF(math.cos(inner_angle) * particle.size * 0.4, 
                                     math.sin(inner_angle) * particle.size * 0.4))
            
            path.moveTo(points[0])
            for point in points[1:]:
                path.lineTo(point)
            path.closeSubpath()
            painter.fillPath(path, QBrush(gradient))
        else:
            # Partículas pequeñas normales (círculos con gradiente)
            gradient = QRadialGradient(0, 0, particle.size)
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(QPointF(0, 0), particle.size, particle.size * 0.7)
        
        painter.restore()
        
    def _draw_trail_drop(self, painter: QPainter, drop: TrailDrop) -> None:
        colors = self._get_colors(drop.effect_type)
        opacity = max(0, drop.life)
        color = QColor(*colors['primary'].getRgb()[:3], opacity)
        
        gradient = QRadialGradient(drop.x, drop.y, drop.size * 1.5)
        gradient.setColorAt(0, color)
        gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QPointF(drop.x, drop.y), drop.size, drop.size * 1.5)
        
    def _toggle_effect(self) -> None:
        self.is_active = not self.is_active
        
        if self.is_active:
            self.action_toggle.setText("● Efecto Activo")
            self.tray_icon.setToolTip("Advanced Multi Effect Overlay - Activo")
        else:
            self.action_toggle.setText("○ Efecto Desactivado")
            self.tray_icon.setToolTip("Advanced Multi Effect Overlay - Desactivado")
            self.splashes.clear()
            self.ripples.clear()
            self.particles.clear()
            self.trail_drops.clear()
            self.update()
    
    def _toggle_fragments(self) -> None:
        """Toggle fragmentos de explosión on/off"""
        self.fragments_enabled = not self.fragments_enabled
        
        if self.fragments_enabled:
            self.action_fragments.setText("💥 Fragmentos de Explosión: ON")
            self.tray_icon.showMessage(
                "Fragmentos Activados",
                "Los fragmentos de explosión están ACTIVADOS",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            self.action_fragments.setText("💥 Fragmentos de Explosión: OFF")
            self.tray_icon.showMessage(
                "Fragmentos Desactivados", 
                "Los fragmentos de explosión están DESACTIVADOS",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        self._save_config()  # Guardar configuración
    
    def _toggle_keyboard_effects(self) -> None:
        """Toggle efectos de teclado combinables on/off"""
        self.keyboard_effects_enabled = not self.keyboard_effects_enabled
        
        if self.keyboard_effects_enabled:
            self.action_keyboard.setText("⌨️ Teclado Combinado: ON")
            self.tray_icon.showMessage(
                "Teclado Combinado Activado",
                "Los efectos de teclado ahora funcionan con cualquier modo",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            self.action_keyboard.setText("⌨️ Teclado Combinado: OFF")
            self.tray_icon.showMessage(
                "Teclado Combinado Desactivado",
                "Los efectos de teclado solo funcionarán en el modo Teclado",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        self._save_config()  # Guardar configuración
    
    def _set_effect_type(self, effect: EffectType) -> None:
        self.current_effect = effect
        
        for eff, action in self.effect_actions.items():
            if eff == effect:
                action.setText("● " + eff.display_name)
            else:
                action.setText("○ " + eff.display_name)
        
        self.tray_icon.setToolTip(f"Efecto Actual: {effect.display_name}")
        self._save_config()  # Guardar configuración
    
    def _set_mode(self, mode: EffectMode) -> None:
        self.effect_mode = mode
        self.last_drop_pos = None
        
        # Detener todos los timers automáticos
        self.auto_timer.stop()
        
        # Activar timer según modo
        if mode == EffectMode.AUTO_FIRE:
            self.auto_timer.start(self.auto_fire_interval)  # 1 segundo
        elif mode == EffectMode.FIREWORKS:
            self.auto_timer.start(2000)  # 2 segundos
        
        for m, action in self.mode_actions.items():
            if m == mode:
                action.setText("● " + m.display_name)
            else:
                action.setText("○ " + m.display_name)
        
        self.tray_icon.setToolTip(f"Modo: {mode.display_name}")
        self._save_config()  # Guardar configuración
    
    def _set_intensity(self, level: IntensityLevel) -> None:
        self.intensity_level = level
        self._update_intensity_ui()
        self._save_config()  # Guardar configuración
    
    def _update_intensity_ui(self) -> None:
        """Actualiza la UI de intensidad según el nivel actual"""
        level = self.intensity_level
        self.action_very_low.setText("○ Muy Baja" if level != IntensityLevel.VERY_LOW else "● Muy Baja")
        self.action_low.setText("○ Baja" if level != IntensityLevel.LOW else "● Baja")
        self.action_medium.setText("○ Media" if self.intensity_level != IntensityLevel.MEDIUM else "● Media")
        self.action_high.setText("○ Alta" if self.intensity_level != IntensityLevel.HIGH else "● Alta")
        self.action_very_high.setText("○ Muy Alta" if self.intensity_level != IntensityLevel.VERY_HIGH else "● Muy Alta")
    
    def _is_startup_enabled(self) -> bool:
        """Verifica si el programa está configurado para iniciar con Windows"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "EffectOverlay")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except:
            return False
    
    def _enable_startup(self) -> None:
        """Agrega el programa al inicio de Windows"""
        try:
            import winreg
            import sys
            import os
            
            # Obtener la ruta completa del script
            if getattr(sys, 'frozen', False):
                app_path = sys.executable
            else:
                app_path = f'pythonw "{os.path.abspath(sys.argv[0])}"'
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "EffectOverlay", 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error al habilitar inicio: {e}")
            return False
    
    def _disable_startup(self) -> None:
        """Remueve el programa del inicio de Windows"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, "EffectOverlay")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Error al deshabilitar inicio: {e}")
            return False
    
    def _toggle_startup(self) -> None:
        """Alterna el inicio automático con Windows"""
        if self._is_startup_enabled():
            if self._disable_startup():
                self.action_startup.setText("🚀 Iniciar con Windows")
        else:
            if self._enable_startup():
                self.action_startup.setText("✅ Iniciar con Windows")
    
    def _update_startup_status(self) -> None:
        """Actualiza el estado visual del menú de inicio"""
        if self._is_startup_enabled():
            self.action_startup.setText("✅ Iniciar con Windows")
        else:
            self.action_startup.setText("🚀 Iniciar con Windows")
    
    def _show_about(self) -> None:
        from PyQt6.QtWidgets import QMessageBox
        
        msg = QMessageBox()
        msg.setWindowTitle("Advanced Multi Effect Overlay v9.0 - MEGA EDITION")
        msg.setIcon(QMessageBox.Icon.Information)
        
        info_text = """VERSIÓN v9.0 - MEGA EDITION

🆕 NOVEDAD: SOPORTE PARA CLIC DERECHO E IZQUIERDO
Ahora puedes crear efectos con AMBOS botones del mouse!

42 EFECTOS VISUALES ORGANIZADOS POR CATEGORÍAS:
• Agua (4): Cristalina, Océano, Hielo, Burbujas
• Fuego (4): Fuego, Lava, Infierno, Brasas
• Mágicos (5): Chispas, Magia, Estrellas, Hadas, Místico
• Naturales (5): Nieve, Humo, Hojas, Cerezos, Veneno
• Electrónicos (4): Neón, Plasma, Relámpago, Cyber
• Preciosos (5): Oro, Plata, Diamante, Rubí, Esmeralda
• Cósmicos (4): Galaxia, Nebulosa, Aurora, Meteoro
• Especiales (4): Arcoíris, Sangre, Tóxico, Matrix
• Colores Puros (8): Rojo, Azul, Verde, Amarillo, Morado, Naranja, Rosa, Blanco

17 MODOS DE OPERACIÓN:
... (y el resto de modos)

✅ GUARDADO AUTOMÁTICO
Tu configuración se guarda automáticamente y se restaura al reiniciar

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Creado por: ING Victor Maldonado
Versión: 9.0 MEGA EDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        msg.setText(info_text)
        msg.exec()
    
    def _set_right_click_effect(self, effect: EffectType) -> None:
        """Cambia el efecto que se usa con el botón derecho"""
        self.right_click_effect = effect
        
        # Actualizar marcas en el menú
        for eff, action in self.right_click_actions.items():
            if eff == effect:
                action.setText("● " + eff.display_name)
            else:
                action.setText("○ " + eff.display_name)
        
        self.tray_icon.setToolTip(f"Botón Derecho: {effect.display_name}")
        self._save_config()  # Guardar configuración
    
    def _save_config(self) -> None:
        """Guarda la configuración actual en un archivo JSON"""
        try:
            config = {
                'is_active': self.is_active,
                'effect_mode': self.effect_mode.mode_id,
                'intensity_level': self.intensity_level.level_name,
                'current_effect': self.current_effect.type_id,
                'right_click_effect': self.right_click_effect.type_id,
                'fragments_enabled': self.fragments_enabled,
                'keyboard_effects_enabled': getattr(self, 'keyboard_effects_enabled', False)
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def _load_config(self) -> None:
        """Carga la configuración desde el archivo JSON o usa valores predeterminados"""
        # Valores predeterminados
        self.is_active = True
        self.effect_mode = EffectMode.CLICK_ONLY
        self.intensity_level = IntensityLevel.MEDIUM
        self.current_effect = EffectType.WATER
        self.right_click_effect = EffectType.GOLD
        self.fragments_enabled = True
        self.keyboard_effects_enabled = False
        
        # Intentar cargar configuración guardada
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Cargar valores guardados
                self.is_active = config.get('is_active', True)
                self.fragments_enabled = config.get('fragments_enabled', True)
                self.keyboard_effects_enabled = config.get('keyboard_effects_enabled', False)
                
                # Cargar modo
                mode_id = config.get('effect_mode', 'click')
                for mode in EffectMode:
                    if mode.mode_id == mode_id:
                        self.effect_mode = mode
                        break
                
                # Cargar intensidad
                intensity_name = config.get('intensity_level', 'medium')
                for level in IntensityLevel:
                    if level.level_name == intensity_name:
                        self.intensity_level = level
                        break
                
                # Cargar efecto actual
                effect_id = config.get('current_effect', 'water')
                for effect in EffectType:
                    if effect.type_id == effect_id:
                        self.current_effect = effect
                        break
                
                # Cargar efecto clic derecho
                right_effect_id = config.get('right_click_effect', 'gold')
                for effect in EffectType:
                    if effect.type_id == right_effect_id:
                        self.right_click_effect = effect
                        break
                
                print(f"✓ Configuración cargada desde: {self.config_file}")
                print(f"  - Efecto: {self.current_effect.display_name}")
                print(f"  - Modo: {self.effect_mode.display_name}")
                print(f"  - Intensidad: {self.intensity_level.level_name}")
                print(f"  - Clic Derecho: {self.right_click_effect.display_name}")
                print(f"  - Fragmentos: {'ON' if self.fragments_enabled else 'OFF'}")
                print(f"  - Teclado Combinado: {'ON' if self.keyboard_effects_enabled else 'OFF'}")
        except Exception as e:
            print(f"No se pudo cargar configuración (usando valores predeterminados): {e}")
    
    def _update_ui_from_config(self) -> None:
        """Actualiza todos los elementos de UI según la configuración cargada"""
        # Actualizar estado activo/inactivo
        if self.is_active:
            self.action_toggle.setText("🟢 Activo")
        else:
            self.action_toggle.setText("🔴 Desactivado")
        
        # Actualizar fragmentos
        self.action_fragments.setText(f"💥 Fragmentos de Explosión: {'ON' if self.fragments_enabled else 'OFF'}")
        
        # Actualizar teclado combinado
        self.action_keyboard.setText(f"⌨️ Teclado Combinado: {'ON' if self.keyboard_effects_enabled else 'OFF'}")
        
        # Actualizar efecto izquierdo
        for eff, action in self.effect_actions.items():
            if eff == self.current_effect:
                action.setText("● " + eff.display_name)
            else:
                action.setText("○ " + eff.display_name)
        
        # Actualizar efecto derecho
        for eff, action in self.right_click_actions.items():
            if eff == self.right_click_effect:
                action.setText("● " + eff.display_name)
            else:
                action.setText("○ " + eff.display_name)
        
        # Actualizar modo
        for m, action in self.mode_actions.items():
            if m == self.effect_mode:
                action.setText("● " + m.display_name)
            else:
                action.setText("○ " + m.display_name)
        
        # Actualizar intensidad
        self._update_intensity_ui()
        
        # Actualizar fragmentos
        if self.fragments_enabled:
            self.action_fragments.setText("💥 Fragmentos de Explosión: ON")
        else:
            self.action_fragments.setText("💥 Fragmentos de Explosión: OFF")
    
    def _quit_application(self) -> None:
        self._save_config()  # Guardar antes de salir
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()
        self.tray_icon.hide()
        QApplication.quit()

import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        # Re-ejecutar el script con privilegios de administrador
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("Advanced Multi Effect Overlay")
    app.setApplicationVersion("8.0")
    
    overlay = AdvancedMultiEffectOverlay()
    overlay.show()
    
    print("\n" + "="*70)
    print(" ADVANCED MULTI EFFECT OVERLAY v8.0 - RIGHT CLICK EDITION ".center(70))
    print("="*70)
    print("\n[!] 42 EFECTOS DISPONIBLES (34 efectos + 8 colores puros)")
    print("\n[+] CONTROLES:")
    print("   - Clic IZQUIERDO -> Gran efecto")
    print("   - Clic DERECHO -> Gran efecto (configurable)")
    print("   - Clic derecho en icono de bandeja -> Menú completo")
    print("\n[OK] GUARDADO AUTOMATICO DE CONFIGURACION")
    print("   Tu configuración se guarda automáticamente y se restaura al reiniciar")
    print("\n[!] REQUIERE PRIVILEGIOS DE ADMINISTRADOR PARA VISIBILIDAD TOTAL")
    print("="*70 + "\n")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    # run_as_admin()  # Comentado para evitar loop de elevación
    main()
    
    def _create_combo_splash(self, x: float, y: float, effect_type: EffectType) -> None:
        """Modo COMBO: Splash con multiplicador"""
        # TamaÃ±o y cantidad segÃºn multiplicador
        scale = self.combo_multiplier
        particle_count = int(self.intensity_level.particle_count * 4 * scale)
        
        # Splash mÃ¡s grande
        self.splashes.append(EffectSplash(
            x=x, y=y, 
            max_radius=AnimationConfig.SPLASH_RADIUS * scale,
            effect_type=effect_type
        ))
        
        # Ondas mÃ¡s intensas
        self.ripples.append(EffectRipple(
            x=x, y=y,
            intensity=scale,
            max_radius=AnimationConfig.MAX_RIPPLE_RADIUS * scale,
            effect_type=effect_type
        ))
        
        # Muchas mÃ¡s partÃ­culas
        for _ in range(min(particle_count, 300)):  # LÃ­mite de 300
            self.particles.append(EffectParticle.create(x, y, effect_type, is_click=True))
    
    def _create_mirror_effect(self, x: float, y: float, effect_type: EffectType) -> None:
        """Modo MIRROR: Efecto en posiciÃ³n y su espejo"""
        screen = QApplication.primaryScreen().geometry()
        center_x = screen.width() / 2
        center_y = screen.height() / 2
        
        # Efecto original
        self._create_big_splash(x, y, effect_type)
        
        # Espejo horizontal
        mirror_x = center_x + (center_x - x)
        self._create_big_splash(mirror_x, y, effect_type)
    
    def _create_lightning_effect(self, x: float, y: float, effect_type: EffectType) -> None:
        """Modo LIGHTNING: Efectos con rayos entre clics recientes"""
        import time
        current_time = time.time()
        
        # Efecto principal
        self._create_big_splash(x, y, effect_type)
        
        # Crear "rayos" hacia clics recientes (Ãºltimos 3 segundos)
        for click in self.recent_clicks[-5:]:
            if current_time - click['time'] < 3.0:
                # Crear partÃ­culas a lo largo de la lÃ­nea
                steps = 10
                for i in range(steps):
                    t = i / steps
                    ray_x = click['x'] + (x - click['x']) * t
                    ray_y = click['y'] + (y - click['y']) * t
                    self.particles.append(EffectParticle.create(ray_x, ray_y, effect_type, is_click=False))
    
    def _auto_effects_tick(self) -> None:
        """Timer tick para modos AUTO_FIRE y FIREWORKS"""
        if not self.is_active:
            return
            
        screen = QApplication.primaryScreen().geometry()
        
        if self.effect_mode == EffectMode.AUTO_FIRE:
            # Efectos en posiciones aleatorias
            x = random.randint(100, screen.width() - 100)
            y = random.randint(100, screen.height() - 100)
            self._create_big_splash(x, y, self.current_effect)
            
        elif self.effect_mode == EffectMode.FIREWORKS:
            # MÃºltiples explosiones simultÃ¡neas
            for _ in range(random.randint(2, 4)):
                x = random.randint(100, screen.width() - 100)
                y = random.randint(100, screen.height() - 100)
                effect = random.choice(list(EffectType))
                self._create_burst(x, y, effect)
    
    def _orbital_tick(self) -> None:
        """Timer tick para modo ORBITAL"""
        if not self.is_active or self.effect_mode != EffectMode.ORBITAL:
            return
        
        # Crear partÃ­culas que orbitan alrededor del cursor
        import time
        t = time.time()
        radius = 80
        
        for i in range(8):  # 8 partÃ­culas orbitando
            angle = (t * 2 + i * (360 / 8)) * math.pi / 180
            x = self.mouse_x + math.cos(angle) * radius
            y = self.mouse_y + math.sin(angle) * radius
            
            if len(self.particles) < 200:  # LÃ­mite
                particle = EffectParticle.create(x, y, self.current_effect, is_click=False)
                particle.life = 50  # Vida muy corta
                self.particles.append(particle)
