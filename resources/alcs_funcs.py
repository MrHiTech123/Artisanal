# Credit to AlcatrazEscapee and EERussianGuy, the devs of TerraFirmaCraft!
# Licensed under EUPL v1.2

from enum import Enum, auto
from typing import Dict, List, Set, NamedTuple, Sequence, Optional, Tuple, Any, Union, Literal, get_args
from mcresources import ResourceManager, utils, loot_tables, RecipeContext, ItemContext, BlockContext, advancements
from mcresources.type_definitions import ResourceIdentifier, Json, JsonObject, VerticalAnchor

class Size(Enum):
    tiny = auto()
    very_small = auto()
    small = auto()
    normal = auto()
    large = auto()
    very_large = auto()
    huge = auto()


class Weight(Enum):
    very_light = auto()
    light = auto()
    medium = auto()
    heavy = auto()
    very_heavy = auto()


class Category(Enum):
    fruit = auto()
    vegetable = auto()
    grain = auto()
    bread = auto()
    dairy = auto()
    meat = auto()
    cooked_meat = auto()
    other = auto()

class Rules(Enum):
    hit_any = 'hit_any'
    hit_not_last = 'hit_not_last'
    hit_last = 'hit_last'
    hit_second_last = 'hit_second_last'
    hit_third_last = 'hit_third_last'
    draw_any = 'draw_any'
    draw_last = 'draw_last'
    draw_not_last = 'draw_not_last'
    draw_second_last = 'draw_second_last'
    draw_third_last = 'draw_third_last'
    punch_any = 'punch_any'
    punch_last = 'punch_last'
    punch_not_last = 'punch_not_last'
    punch_second_last = 'punch_second_last'
    punch_third_last = 'punch_third_last'
    bend_any = 'bend_any'
    bend_last = 'bend_last'
    bend_not_last = 'bend_not_last'
    bend_second_last = 'bend_second_last'
    bend_third_last = 'bend_third_last'
    upset_any = 'upset_any'
    upset_last = 'upset_last'
    upset_not_last = 'upset_not_last'
    upset_second_last = 'upset_second_last'
    upset_third_last = 'upset_third_last'
    shrink_any = 'shrink_any'
    shrink_last = 'shrink_last'
    shrink_not_last = 'shrink_not_last'
    shrink_second_last = 'shrink_second_last'
    shrink_third_last = 'shrink_third_last'

#  Work under Copyright. Licensed under the EUPL.
#  See the project README.md and LICENSE.txt for more information.

from typing import Dict, List, Set, NamedTuple, Sequence, Optional, Tuple, Any


class Rock(NamedTuple):
    category: str
    sand: str


class MetalItem(NamedTuple):
    type: str
    smelt_amount: int
    parent_model: str
    tag: Optional[str]
    mold: bool
    durability: bool


class Ore(NamedTuple):
    metal: Optional[str]
    graded: bool
    required_tool: str
    tag: str
    dye_color: Optional[str] = None


class OreGrade(NamedTuple):
    grind_amount: int


class Vein(NamedTuple):
    ore: str  # The name of the ore (as found in ORES)
    vein_type: str  # Either 'cluster', 'pipe' or 'disc'
    rarity: int
    size: int
    min_y: int
    max_y: int
    density: float
    grade: tuple[int, int, int]  # (poor, normal, rich) weights
    rocks: tuple[str, ...]  # Rock, or rock categories
    biomes: str | None
    height: int
    radius: int
    deposits: bool
    indicator_rarity: int  # Above-ground indicators
    underground_rarity: int  # Underground indicators
    underground_count: int
    project: bool | None  # Project to surface
    project_offset: bool | None  # Project offset
    near_lava: bool | None

    @staticmethod
    def new(
        ore: str,
        rarity: int,
        size: int,
        min_y: int,
        max_y: int,
        density: float,
        rocks: tuple[str, ...],

        vein_type: str = 'cluster',
        grade: tuple[int, int, int] = (),
        biomes: str = None,
        height: int = 2,  # For disc type veins, `size` is the width
        radius: int = 5,  # For pipe type veins, `size` is the height
        deposits: bool = False,
        indicator: int = 12,  # Indicator rarity
        deep_indicator: tuple[int, int] = (1, 0),  # Pair of (rarity, count) for underground indicators
        project: str | bool = None,  # Projects to surface. Either True or 'offset'
        near_lava: bool | None = None,
    ):
        assert 0 < density < 1
        assert isinstance(rocks, tuple), 'Forgot the trailing comma in a single element tuple: %s' % repr(rocks)
        assert vein_type in ('cluster', 'disc', 'pipe')
        assert project is None or project is True or project == 'offset'

        underground_rarity, underground_count = deep_indicator
        return Vein(ore, 'tfc:%s_vein' % vein_type, rarity, size, min_y, max_y, density, grade, rocks, biomes, height, radius, deposits, indicator, underground_rarity, underground_count, None if project is None else True, None if project != 'offset' else True, near_lava)

    def config(self) -> dict[str, Any]:
        cfg = {
            'rarity': self.rarity,
            'density': self.density,
            'min_y': self.min_y,
            'max_y': self.max_y,
            'project': self.project,
            'project_offset': self.project_offset,
            'biomes': self.biomes,
            'near_lava': self.near_lava,
        }
        if self.vein_type == 'tfc:cluster_vein':
            cfg.update(size=self.size)
        elif self.vein_type == 'tfc:pipe_vein':
            cfg.update(min_skew=5, max_skew=13, min_slant=0, max_slant=2, sign=0, height=self.size, radius=self.radius)
        else:
            cfg.update(size=self.size, height=self.height)
        return cfg


class Plant(NamedTuple):
    clay: bool
    min_temp: float
    max_temp: float
    min_rain: float
    max_rain: float
    type: str
    worldgen: bool = True


class Wood(NamedTuple):
    temp: float
    duration: int


class Berry(NamedTuple):
    min_temp: float
    max_temp: float
    min_rain: float
    max_rain: float
    type: str
    min_forest: str
    max_forest: str


class Fruit(NamedTuple):
    min_temp: float
    max_temp: float
    min_rain: float
    max_rain: float


class Crop(NamedTuple):
    type: str
    stages: int
    nutrient: str
    min_temp: float
    max_temp: float
    min_rain: float
    max_rain: float
    min_hydration: int
    max_hydration: int
    min_forest: Optional[str]
    max_forest: Optional[str]


class Metal(NamedTuple):
    tier: int
    types: Set[str]  # One of 'part', 'tool', 'armor', 'utility'
    heat_capacity_base: float  # Do not access directly, use one of specific or ingot heat capacity.
    melt_temperature: float
    melt_metal: Optional[str]

    def specific_heat_capacity(self) -> float: return round(300 / self.heat_capacity_base) / 100_000
    def ingot_heat_capacity(self) -> float: return 1 / self.heat_capacity_base


POTTERY_MELT = 1400 - 1
POTTERY_HEAT_CAPACITY = 1.2  # Heat Capacity

HORIZONTAL_DIRECTIONS: List[str] = ['east', 'west', 'north', 'south']

ROCK_CATEGORIES = ('sedimentary', 'metamorphic', 'igneous_extrusive', 'igneous_intrusive')
ROCK_CATEGORY_ITEMS = ('axe', 'hammer', 'hoe', 'javelin', 'knife', 'shovel')

TOOL_TAGS: Dict[str, str] = {
    # Rock
    'axe': 'axes',
    'hammer': 'hammers',
    'hoe': 'hoes',
    'javelin': 'javelins',
    'knife': 'knives',
    'shovel': 'shovels',
    # Metal Only
    'pickaxe': 'pickaxes',
    'chisel': 'chisels',
    'mace': 'maces',
    'sword': 'swords',
    'saw': 'saws',
    'propick': 'propicks',
    'scythe': 'scythes',
    'shears': 'shears',
    'tuyere': 'tuyeres'
}

ROCKS: Dict[str, Rock] = {
    'granite': Rock('igneous_intrusive', 'white'),
    'diorite': Rock('igneous_intrusive', 'white'),
    'gabbro': Rock('igneous_intrusive', 'black'),
    'shale': Rock('sedimentary', 'black'),
    'claystone': Rock('sedimentary', 'brown'),
    'limestone': Rock('sedimentary', 'white'),
    'conglomerate': Rock('sedimentary', 'green'),
    'dolomite': Rock('sedimentary', 'black'),
    'chert': Rock('sedimentary', 'yellow'),
    'chalk': Rock('sedimentary', 'white'),
    'rhyolite': Rock('igneous_extrusive', 'red'),
    'basalt': Rock('igneous_extrusive', 'red'),
    'andesite': Rock('igneous_extrusive', 'red'),
    'dacite': Rock('igneous_extrusive', 'yellow'),
    'quartzite': Rock('metamorphic', 'white'),
    'slate': Rock('metamorphic', 'yellow'),
    'phyllite': Rock('metamorphic', 'brown'),
    'schist': Rock('metamorphic', 'green'),
    'gneiss': Rock('metamorphic', 'green'),
    'marble': Rock('metamorphic', 'yellow')
}
METALS: Dict[str, Metal] = {
    'bismuth': Metal(1, {'part'}, 0.14, 270, None),
    'bismuth_bronze': Metal(2, {'part', 'tool', 'armor', 'utility'}, 0.35, 985, None),
    'black_bronze': Metal(2, {'part', 'tool', 'armor', 'utility'}, 0.35, 1070, None),
    'bronze': Metal(2, {'part', 'tool', 'armor', 'utility'}, 0.35, 950, None),
    'brass': Metal(2, {'part'}, 0.35, 930, None),
    'copper': Metal(1, {'part', 'tool', 'armor', 'utility'}, 0.35, 1080, None),
    'gold': Metal(1, {'part'}, 0.6, 1060, None),
    'nickel': Metal(1, {'part'}, 0.48, 1453, None),
    'rose_gold': Metal(1, {'part'}, 0.35, 960, None),
    'silver': Metal(1, {'part'}, 0.48, 961, None),
    'tin': Metal(1, {'part'}, 0.14, 230, None),
    'zinc': Metal(1, {'part'}, 0.21, 420, None),
    'sterling_silver': Metal(1, {'part'}, 0.35, 950, None),
    'wrought_iron': Metal(3, {'part', 'tool', 'armor', 'utility'}, 0.35, 1535, 'cast_iron'),
    'cast_iron': Metal(1, {'part'}, 0.35, 1535, None),
    'pig_iron': Metal(3, set(), 0.35, 1535, None),
    'steel': Metal(4, {'part', 'tool', 'armor', 'utility'}, 0.35, 1540, None),
    'black_steel': Metal(5, {'part', 'tool', 'armor', 'utility'}, 0.35, 1485, None),
    'blue_steel': Metal(6, {'part', 'tool', 'armor', 'utility'}, 0.35, 1540, None),
    'red_steel': Metal(6, {'part', 'tool', 'armor', 'utility'}, 0.35, 1540, None),
    'weak_steel': Metal(4, set(), 0.35, 1540, None),
    'weak_blue_steel': Metal(5, set(), 0.35, 1540, None),
    'weak_red_steel': Metal(5, set(), 0.35, 1540, None),
    'high_carbon_steel': Metal(3, set(), 0.35, 1540, 'pig_iron'),
    'high_carbon_black_steel': Metal(4, set(), 0.35, 1540, 'weak_steel'),
    'high_carbon_blue_steel': Metal(5, set(), 0.35, 1540, 'weak_blue_steel'),
    'high_carbon_red_steel': Metal(5, set(), 0.35, 1540, 'weak_red_steel'),
    'unknown': Metal(0, set(), 0.5, 400, None)
}
METAL_BLOCKS: Dict[str, MetalItem] = {
    'anvil': MetalItem('utility', 1400, 'tfc:block/anvil', None, False, False),
    'block': MetalItem('part', 100, 'block/block', None, False, False),
    'block_slab': MetalItem('part', 50, 'block/block', None, False, False),
    'block_stairs': MetalItem('part', 75, 'block/block', None, False, False),
    'bars': MetalItem('utility', 25, 'item/generated', None, False, False),
    'chain': MetalItem('utility', 6, 'tfc:block/chain', None, False, False),
    'lamp': MetalItem('utility', 100, 'tfc:block/lamp', None, False, False),
    'trapdoor': MetalItem('utility', 200, 'tfc:block/trapdoor', None, False, False)
}
METAL_ITEMS: Dict[str, MetalItem] = {
    'ingot': MetalItem('all', 100, 'item/generated', 'forge:ingots', True, False),
    'double_ingot': MetalItem('part', 200, 'item/generated', 'forge:double_ingots', False, False),
    'sheet': MetalItem('part', 200, 'item/generated', 'forge:sheets', False, False),
    'double_sheet': MetalItem('part', 400, 'item/generated', 'forge:double_sheets', False, False),
    'rod': MetalItem('part', 50, 'item/handheld_rod', 'forge:rods', False, False),
    'unfinished_lamp': MetalItem('utility', 100, 'item/generated', None, False, False),

    'tuyere': MetalItem('tool', 400, 'item/generated', None, False, True),
    'fish_hook': MetalItem('tool', 200, 'item/generated', None, False, False),
    'fishing_rod': MetalItem('tool', 200, 'item/generated', 'forge:fishing_rods', False, True),
    'pickaxe': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'pickaxe_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'shovel': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'shovel_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'axe': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'axe_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'hoe': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'hoe_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'chisel': MetalItem('tool', 100, 'tfc:item/handheld_flipped', None, False, True),
    'chisel_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'sword': MetalItem('tool', 200, 'item/handheld', None, False, True),
    'sword_blade': MetalItem('tool', 200, 'item/generated', None, True, False),
    'mace': MetalItem('tool', 200, 'item/handheld', None, False, True),
    'mace_head': MetalItem('tool', 200, 'item/generated', None, True, False),
    'saw': MetalItem('tool', 100, 'tfc:item/handheld_flipped', None, False, True),
    'saw_blade': MetalItem('tool', 100, 'item/generated', None, True, False),
    'javelin': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'javelin_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'hammer': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'hammer_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'propick': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'propick_head': MetalItem('tool', 100, 'item/generated', None, True, False),
    'knife': MetalItem('tool', 100, 'tfc:item/handheld_flipped', None, False, True),
    'knife_blade': MetalItem('tool', 100, 'item/generated', None, True, False),
    'scythe': MetalItem('tool', 100, 'item/handheld', None, False, True),
    'scythe_blade': MetalItem('tool', 100, 'item/generated', None, True, False),
    'shears': MetalItem('tool', 200, 'item/handheld', None, False, True),

    'unfinished_helmet': MetalItem('armor', 400, 'item/generated', None, False, False),
    'helmet': MetalItem('armor', 600, 'item/generated', None, False, True),
    'unfinished_chestplate': MetalItem('armor', 400, 'item/generated', None, False, False),
    'chestplate': MetalItem('armor', 800, 'item/generated', None, False, True),
    'unfinished_greaves': MetalItem('armor', 400, 'item/generated', None, False, False),
    'greaves': MetalItem('armor', 600, 'item/generated', None, False, True),
    'unfinished_boots': MetalItem('armor', 200, 'item/generated', None, False, False),
    'boots': MetalItem('armor', 400, 'item/generated', None, False, True),
    'horse_armor': MetalItem('armor', 1200, 'item/generated', None, False, False),

    'shield': MetalItem('tool', 400, 'item/handheld', None, False, True)
}
METAL_ITEMS_AND_BLOCKS: Dict[str, MetalItem] = {**METAL_ITEMS, **METAL_BLOCKS}
METAL_TOOL_HEADS = ('chisel', 'hammer', 'hoe', 'javelin', 'knife', 'mace', 'pickaxe', 'propick', 'saw', 'scythe', 'shovel', 'sword', 'axe')

ORES: Dict[str, Ore] = {
    'native_copper': Ore('copper', True, 'copper', 'copper', 'orange'),
    'native_gold': Ore('gold', True, 'copper', 'gold'),
    'hematite': Ore('cast_iron', True, 'copper', 'iron', 'red'),
    'native_silver': Ore('silver', True, 'copper', 'silver', 'light_gray'),
    'cassiterite': Ore('tin', True, 'copper', 'tin', 'gray'),
    'bismuthinite': Ore('bismuth', True, 'copper', 'bismuth', 'green'),
    'garnierite': Ore('nickel', True, 'bronze', 'nickel', 'brown'),
    'malachite': Ore('copper', True, 'copper', 'copper', 'green'),
    'magnetite': Ore('cast_iron', True, 'copper', 'iron', 'gray'),
    'limonite': Ore('cast_iron', True, 'copper', 'iron', 'yellow'),
    'sphalerite': Ore('zinc', True, 'copper', 'zinc', 'gray'),
    'tetrahedrite': Ore('copper', True, 'copper', 'copper', 'gray'),
    'bituminous_coal': Ore(None, False, 'copper', 'coal'),
    'lignite': Ore(None, False, 'copper', 'coal'),
    'gypsum': Ore(None, False, 'copper', 'gypsum'),
    'graphite': Ore(None, False, 'copper', 'graphite'),
    'sulfur': Ore(None, False, 'copper', 'sulfur'),
    'cinnabar': Ore(None, False, 'bronze', 'redstone'),
    'cryolite': Ore(None, False, 'bronze', 'redstone'),
    'saltpeter': Ore(None, False, 'copper', 'saltpeter'),
    'sylvite': Ore(None, False, 'copper', 'sylvite'),
    'borax': Ore(None, False, 'copper', 'borax'),
    'halite': Ore(None, False, 'bronze', 'halite'),
    'amethyst': Ore(None, False, 'steel', 'amethyst'),  # Mohs: 7
    'diamond': Ore(None, False, 'black_steel', 'diamond'),  # Mohs: 10
    'emerald': Ore(None, False, 'steel', 'emerald'),  # Mohs: 7.5-8
    'lapis_lazuli': Ore(None, False, 'wrought_iron', 'lapis'),  # Mohs: 5-6
    'opal': Ore(None, False, 'wrought_iron', 'opal'),  # Mohs: 5.5-6.5
    'pyrite': Ore(None, False, 'copper', 'pyrite'),
    'ruby': Ore(None, False, 'black_steel', 'ruby'),  # Mohs: 9
    'sapphire': Ore(None, False, 'black_steel', 'sapphire'),  # Mohs: 9
    'topaz': Ore(None, False, 'steel', 'topaz')  # Mohs: 8
}
ORE_GRADES: Dict[str, OreGrade] = {
    'normal': OreGrade(5),
    'poor': OreGrade(3),
    'rich': OreGrade(7)
}
DEFAULT_FORGE_ORE_TAGS: Tuple[str, ...] = ('coal', 'diamond', 'emerald', 'gold', 'iron', 'lapis', 'netherite_scrap', 'quartz', 'redstone')

POOR = 70, 25, 5  # = 1550
NORMAL = 35, 40, 25  # = 2400
RICH = 15, 25, 60  # = 2550

ORE_VEINS: dict[str, Vein] = {
    # Copper
    # Native - only in IE, only surface, and common to compensate for the y-level getting cut off.
    # Malachite + Tetrahedrite - Sed + MM, can spawn in larger deposits, hence more common. Tetrahedrite also spawns at high altitude MM
    # All copper have high indicator rarity because it's necessary early on
    'surface_native_copper': Vein.new('native_copper', 24, 20, 40, 130, 0.25, ('igneous_extrusive',), grade=POOR, deposits=True, indicator=14),
    'surface_malachite': Vein.new('malachite', 32, 20, 40, 130, 0.25, ('marble', 'limestone', 'chalk', 'dolomite'), grade=POOR, indicator=14),
    'surface_tetrahedrite': Vein.new('tetrahedrite', 7, 20, 90, 170, 0.25, ('metamorphic',), grade=POOR, indicator=8),

    'normal_malachite': Vein.new('malachite', 45, 30, -30, 70, 0.5, ('marble', 'limestone', 'chalk', 'dolomite'), grade=NORMAL, indicator=25),
    'normal_tetrahedrite': Vein.new('tetrahedrite', 40, 30, -30, 70, 0.5, ('metamorphic',), grade=NORMAL, indicator=25),

    # Native Gold - IE and II at all y levels, larger deeper
    'normal_native_gold': Vein.new('native_gold', 90, 15, 0, 70, 0.25, ('igneous_extrusive', 'igneous_intrusive'), grade=NORMAL, indicator=40),
    'rich_native_gold': Vein.new('native_gold', 50, 40, -80, 20, 0.5, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 4)),

    # In the same area as native gold deposits, pyrite veins - vast majority pyrite, but some native gold - basically troll veins
    'fake_native_gold': Vein.new('pyrite', 16, 15, -50, 70, 0.35, ('igneous_extrusive', 'igneous_intrusive'), indicator=0),

    # Silver - black bronze (T2 with gold), or for black steel. Rare and small in uplift mountains via high II or plentiful near bottom of world
    'surface_native_silver': Vein.new('native_silver', 15, 10, 90, 180, 0.2, ('granite', 'diorite'), grade=POOR),
    'normal_native_silver': Vein.new('native_silver', 25, 25, -80, 20, 0.6, ('granite', 'diorite', 'gneiss', 'schist'), grade=RICH, indicator=0, deep_indicator=(1, 9)),

    # Tin - bronze T2, rare situation (II uplift mountain) but common and rich.
    'surface_cassiterite': Vein.new('cassiterite', 5, 15, 80, 180, 0.4, ('igneous_intrusive',), grade=NORMAL, deposits=True),

    # Bismuth - bronze T2 surface via Sed, deep and rich via II
    'surface_bismuthinite': Vein.new('bismuthinite', 32, 20, 40, 130, 0.3, ('sedimentary',), grade=POOR, indicator=14),
    'normal_bismuthinite': Vein.new('bismuthinite', 45, 40, -80, 20, 0.6, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 4)),

    # Zinc - bronze T2, requires different source from bismuth, surface via IE, or deep via II
    'surface_sphalerite': Vein.new('sphalerite', 30, 20, 40, 130, 0.3, ('igneous_extrusive',), grade=POOR),
    'normal_sphalerite': Vein.new('sphalerite', 45, 40, -80, 20, 0.6, ('igneous_intrusive',), grade=RICH, indicator=0, deep_indicator=(1, 5)),

    # Iron - both surface via IE and Sed. IE has one, Sed has two, so the two are higher rarity
    'surface_hematite': Vein.new('hematite', 45, 20, 10, 90, 0.4, ('igneous_extrusive',), grade=NORMAL, indicator=24),
    'surface_magnetite': Vein.new('magnetite', 90, 20, 10, 90, 0.4, ('sedimentary',), grade=NORMAL, indicator=24),
    'surface_limonite': Vein.new('limonite', 90, 20, 10, 90, 0.4, ('sedimentary',), grade=NORMAL, indicator=24),

    # Nickel - only deep spawning II. Extra veins in gabbro
    'normal_garnierite': Vein.new('garnierite', 25, 18, -80, 0, 0.3, ('igneous_intrusive',), grade=NORMAL),
    'gabbro_garnierite': Vein.new('garnierite', 20, 30, -80, 0, 0.6, ('gabbro',), grade=RICH, indicator=0, deep_indicator=(1, 7)),

    # Graphite - for steel, found in low MM. Along with Kao, which is high altitude sed (via clay deposits)
    'graphite': Vein.new('graphite', 20, 20, -30, 60, 0.4, ('gneiss', 'marble', 'quartzite', 'schist')),

    # Coal, spawns roughly based on IRL grade (lignite -> bituminous -> anthracite), big flat discs
    'lignite': Vein.new('lignite', 160, 40, -20, -8, 0.85, ('sedimentary',), vein_type='disc', height=2, project='offset'),
    'bituminous_coal': Vein.new('bituminous_coal', 210, 50, -35, -12, 0.9, ('sedimentary',), vein_type='disc', height=3, project='offset'),

    # Sulfur spawns near lava level in any low-level rock, common, but small veins
    'sulfur': Vein.new('sulfur', 4, 18, -64, -45, 0.25, ('igneous_intrusive', 'metamorphic'), vein_type='disc', height=5, near_lava=True),

    # Redstone: Cryolite is deep II, cinnabar is deep MM, both are common enough within these rocks but rare to find
    'cryolite': Vein.new('cryolite', 16, 18, -70, -10, 0.7, ('granite', 'diorite')),
    'cinnabar': Vein.new('cinnabar', 14, 18, -70, 10, 0.6, ('quartzite', 'phyllite', 'gneiss', 'schist')),

    # Misc minerals - all spawning in discs, mostly in sedimentary rock. Rare, but all will spawn together
    # Gypsum is decorative, so more common, and Borax is sad, so more common (but smaller)
    # Veins that spawn in all sedimentary are rarer than those that don't
    'saltpeter': Vein.new('saltpeter', 110, 35, 40, 100, 0.4, ('sedimentary',), vein_type='disc', height=5),
    'sylvite': Vein.new('sylvite', 60, 35, 40, 100, 0.35, ('shale', 'claystone', 'chert'), vein_type='disc', height=5),
    'borax': Vein.new('borax', 40, 23, 40, 100, 0.2, ('claystone', 'limestone', 'shale'), vein_type='disc', height=3),
    'gypsum': Vein.new('gypsum', 70, 25, 40, 100, 0.3, ('sedimentary',), vein_type='disc', height=5),
    'halite': Vein.new('halite', 110, 35, -45, -12, 0.85, ('sedimentary',), vein_type='disc', height=4, project='offset'),

    # Gems - these are all fairly specific but since we don't have a gameplay need for gems they can be a bit niche
    'lapis_lazuli': Vein.new('lapis_lazuli', 30, 30, -20, 80, 0.12, ('limestone', 'marble')),

    'diamond': Vein.new('diamond', 30, 60, -64, 100, 0.15, ('gabbro',), vein_type='pipe', radius=5),
    'emerald': Vein.new('emerald', 80, 60, -64, 100, 0.15, ('igneous_intrusive',), vein_type='pipe', radius=5),

    'amethyst': Vein.new('amethyst', 25, 8, 40, 60, 0.2, ('sedimentary', 'metamorphic'), vein_type='disc', biomes='#tfc:is_river', height=4),
    'opal': Vein.new('opal', 25, 8, 40, 60, 0.2, ('sedimentary', 'igneous_extrusive'), vein_type='disc', biomes='#tfc:is_river', height=4),
}

ALL_MINERALS = ('bituminous_coal', 'lignite', 'graphite', 'cinnabar', 'cryolite', 'saltpeter', 'sulfur', 'sylvite', 'borax', 'gypsum', 'lapis_lazuli', 'halite', 'diamond', 'emerald', 'sulfur', 'amethyst', 'opal')

DEPOSIT_RARES: Dict[str, str] = {
    'granite': 'topaz',
    'diorite': 'emerald',
    'gabbro': 'diamond',
    'shale': 'borax',
    'claystone': 'amethyst',
    'limestone': 'lapis_lazuli',
    'conglomerate': 'lignite',
    'dolomite': 'amethyst',
    'chert': 'ruby',
    'chalk': 'sapphire',
    'rhyolite': 'pyrite',
    'basalt': 'pyrite',
    'andesite': 'pyrite',
    'dacite': 'pyrite',
    'quartzite': 'opal',
    'slate': 'pyrite',
    'phyllite': 'pyrite',
    'schist': 'pyrite',
    'gneiss': 'gypsum',
    'marble': 'lapis_lazuli'
}

ROCK_BLOCK_TYPES = ('raw', 'hardened', 'bricks', 'cobble', 'gravel', 'smooth', 'mossy_cobble', 'mossy_bricks', 'cracked_bricks', 'chiseled', 'spike', 'loose', 'pressure_plate', 'button')
ROCK_BLOCKS_IN_JSON = ('raw', 'hardened', 'cobble', 'gravel', 'spike', 'loose')
CUTTABLE_ROCKS = ('raw', 'bricks', 'cobble', 'smooth', 'mossy_cobble', 'mossy_bricks', 'cracked_bricks')
ROCK_SPIKE_PARTS = ('base', 'middle', 'tip')
SAND_BLOCK_TYPES = ('brown', 'white', 'black', 'red', 'yellow', 'green', 'pink')
SANDSTONE_BLOCK_TYPES = ('raw', 'smooth', 'cut')
SOIL_BLOCK_TYPES = ('dirt', 'grass', 'grass_path', 'clay', 'clay_grass', 'farmland', 'rooted_dirt', 'mud', 'mud_bricks', 'drying_bricks', 'muddy_roots')
SOIL_BLOCK_VARIANTS = ('silt', 'loam', 'sandy_loam', 'silty_loam')
KAOLIN_CLAY_TYPES = ('red', 'pink', 'white')
SOIL_BLOCK_TAGS: Dict[str, List[str]] = {
    'grass': ['grass'],
    'dirt': ['dirt'],
    'rooted_dirt': ['dirt'],
    'clay_grass': ['clay_grass', 'grass', 'clay'],
    'clay': ['clay'],
    'mud': ['mud'],
    'grass_path': ['paths'],
    'farmland': ['farmland'],
    'muddy_roots': ['dirt'],
    'mud_bricks': ['mud_bricks']
}
ORE_DEPOSITS = ('native_copper', 'cassiterite', 'native_silver', 'native_gold')
GEMS = ('amethyst', 'diamond', 'emerald', 'lapis_lazuli', 'opal', 'pyrite', 'ruby', 'sapphire', 'topaz')
TRIM_MATERIALS = (*GEMS, 'rose_gold', 'gold', 'silver', 'sterling_silver', 'bismuth')
MISC_GROUNDCOVER = ('bone', 'clam', 'driftwood', 'mollusk', 'mussel', 'pinecone', 'seaweed', 'stick', 'dead_grass', 'feather', 'flint', 'guano', 'humus', 'rotten_flesh', 'salt_lick', 'sea_urchin', 'pumice')
COLORS = ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black')
SIMPLE_FLUIDS = ('brine', 'curdled_milk', 'limewater', 'lye', 'milk_vinegar', 'olive_oil', 'olive_oil_water', 'tallow', 'tannin', 'vinegar')
ALCOHOLS = ('beer', 'cider', 'rum', 'sake', 'vodka', 'whiskey', 'corn_whiskey', 'rye_whiskey')

WOODS: Dict[str, Wood] = {
    'acacia': Wood(650, 1000),
    'ash': Wood(696, 1250),
    'aspen': Wood(611, 1000),
    'birch': Wood(652, 1750),
    'blackwood': Wood(720, 1750),
    'chestnut': Wood(651, 1500),
    'douglas_fir': Wood(707, 1500),
    'hickory': Wood(762, 2000),
    'kapok': Wood(645, 1000),
    'mangrove': Wood(655, 1000),
    'maple': Wood(745, 2000),
    'oak': Wood(728, 2250),
    'palm': Wood(730, 1250),
    'pine': Wood(627, 1250),
    'rosewood': Wood(640, 1500),
    'sequoia': Wood(612, 1750),
    'spruce': Wood(608, 1500),
    'sycamore': Wood(653, 1750),
    'white_cedar': Wood(625, 1500),
    'willow': Wood(603, 1000)
}

# DO NOT EDIT DIRECTLY - Imported directly from spreadsheet
# https://docs.google.com/spreadsheets/d/1Ghw3dCmVO5Gv0MMGBydUxox_nwLYmmcZkGSbbf0QSAE/
CROPS: Dict[str, Crop] = {
    # Grains
    'barley': Crop('default', 8, 'nitrogen', -8, 26, 70, 310, 18, 75, None, 'edge'),
    'oat': Crop('default', 8, 'phosphorus', 3, 40, 140, 400, 35, 100, None, 'edge'),
    'rye': Crop('default', 8, 'phosphorus', -11, 30, 100, 350, 25, 85, None, 'edge'),
    'maize': Crop('double', 6, 'phosphorus', 13, 40, 300, 500, 75, 100, None, 'edge'),
    'wheat': Crop('default', 8, 'phosphorus', -4, 35, 100, 400, 25, 100, None, 'edge'),
    'rice': Crop('default', 8, 'phosphorus', 15, 30, 100, 500, 25, 100, 'normal', None),
    # Vegetables
    'beet': Crop('default', 6, 'potassium', -5, 20, 70, 300, 18, 85, None, None),
    'cabbage': Crop('default', 6, 'nitrogen', -10, 27, 60, 280, 15, 65, None, None),
    'carrot': Crop('default', 5, 'potassium', 3, 30, 100, 400, 25, 100, None, None),
    'garlic': Crop('default', 5, 'nitrogen', -20, 18, 60, 310, 15, 75, None, None),
    'green_bean': Crop('double_stick', 8, 'nitrogen', 2, 35, 150, 410, 38, 100, 'normal', None),
    'melon': Crop('spreading', 8, 'phosphorus', 5, 37, 200, 500, 75, 100, 'normal', None),
    'potato': Crop('default', 7, 'potassium', -1, 37, 200, 410, 50, 100, None, None),
    'pumpkin': Crop('spreading', 8, 'phosphorus', 0, 30, 120, 390, 30, 80, None, None),
    'onion': Crop('default', 7, 'nitrogen', 0, 30, 100, 390, 25, 90, None, None),
    'soybean': Crop('default', 7, 'nitrogen', 8, 30, 160, 410, 40, 100, 'normal', None),
    'squash': Crop('default', 8, 'potassium', 5, 33, 90, 390, 23, 95, 'normal', None),
    'sugarcane': Crop('double', 8, 'potassium', 12, 38, 160, 500, 40, 100, None, None),
    'tomato': Crop('double_stick', 8, 'potassium', 0, 36, 120, 390, 30, 95, 'normal', None),
    'jute': Crop('double', 6, 'potassium', 5, 37, 100, 410, 25, 100, None, None),
    'papyrus': Crop('double', 6, 'potassium', 19, 37, 310, 500, 70, 100, None, None),
    'red_bell_pepper': Crop('pickable', 7, 'potassium', 16, 30, 190, 400, 25, 60, None, None),
    'yellow_bell_pepper': Crop('pickable', 7, 'potassium', 16, 30, 190, 400, 25, 60, None, None),
}

PLANTS: Dict[str, Plant] = {
    'athyrium_fern': Plant(True, -3.9, 15.7, 270, 500, 'standard'),
    'canna': Plant(True, 13.9, 40, 290, 500, 'standard'),
    'goldenrod': Plant(True, -12.9, -2.1, 75, 500, 'standard'),
    'pampas_grass': Plant(True, 10.4, 40, 0, 300, 'tall_grass'),
    'perovskia': Plant(True, -5.7, 13.9, 0, 280, 'dry'),

    'beachgrass': Plant(False, -8, 30, 190, 500, 'beach_grass', False),
    'bluegrass': Plant(False, -0.4, 13.9, 110, 280, 'short_grass', False),
    'bromegrass': Plant(False, 6.8, 21.1, 140, 360, 'short_grass', False),
    'fountain_grass': Plant(False, 3.2, 26.4, 75, 150, 'short_grass', False),
    'manatee_grass': Plant(False, 13.9, 40, 250, 500, 'grass_water', False),
    'orchard_grass': Plant(False, -30, 12.1, 75, 300, 'short_grass', False),
    'ryegrass': Plant(False, -18.2, 40, 150, 320, 'short_grass', False),
    'scutch_grass': Plant(False, 3.2, 40, 150, 500, 'short_grass', False),
    'star_grass': Plant(False, 5, 40, 50, 260, 'grass_water', False),
    'timothy_grass': Plant(False, -16.4, 17.5, 289, 500, 'short_grass', False),
    'raddia_grass': Plant(False, 19.3, 40, 330, 500, 'short_grass', False),

    'allium': Plant(False, -5.7, 1.4, 150, 400, 'standard'),
    'anthurium': Plant(False, 13.9, 40, 290, 500, 'standard'),
    'arrowhead': Plant(False, -5.7, 22.9, 180, 500, 'emergent_fresh'),
    'houstonia': Plant(False, -7.5, 12.1, 150, 500, 'standard'),
    'badderlocks': Plant(False, -12.9, 5, 150, 500, 'submerged_tall'),
    'cordgrass': Plant(False, -16.4, 22.9, 50, 500, 'emergent'),
    'barrel_cactus': Plant(False, 6.8, 19.3, 0, 85, 'cactus'),
    'blood_lily': Plant(True, 10.4, 19.3, 200, 500, 'standard'),
    'blue_orchid': Plant(False, 12.1, 40, 250, 390, 'standard'),
    'blue_ginger': Plant(False, 17.5, 26.4, 300, 450, 'standard'),
    'calendula': Plant(False, 6.8, 22.9, 130, 300, 'standard'),
    'cattail': Plant(False, -11.1, 22.9, 150, 500, 'emergent_fresh'),
    'laminaria': Plant(False, -18.2, 1.4, 100, 500, 'water'),
    'marigold': Plant(False, -3.9, 19.3, 50, 390, 'emergent_fresh'),
    'bur_reed': Plant(False, -11.1, 6.8, 250, 400, 'emergent_fresh'),
    'butterfly_milkweed': Plant(False, -11.1, 19.3, 75, 300, 'standard'),
    'black_orchid': Plant(False, 15.7, 40, 290, 410, 'standard'),
    'cobblestone_lichen': Plant(False, -30, 20, 25, 450, 'creeping'),
    'coontail': Plant(False, 5, 19.3, 250, 500, 'grass_water_fresh'),
    'dandelion': Plant(False, -16.4, 40, 120, 400, 'standard'),
    'dead_bush': Plant(False, -7.5, 40, 0, 120, 'dry'),
    'desert_flame': Plant(False, 3.2, 21.1, 40, 170, 'standard'),
    'duckweed': Plant(False, 12.1, 40, 0, 500, 'floating_fresh'),
    'eel_grass': Plant(False, 8.6, 40, 200, 500, 'grass_water_fresh'),
    'field_horsetail': Plant(False, -7.5, 21.1, 300, 500, 'standard'),
    'foxglove': Plant(False, -3.9, 17.5, 150, 300, 'tall_plant'),
    'grape_hyacinth': Plant(False, -5.7, 12.1, 150, 250, 'standard'),
    'green_algae': Plant(False, -20, 30, 215, 450, 'floating_fresh'),
    'gutweed': Plant(False, -2.1, 19.3, 100, 500, 'water'),
    'heliconia': Plant(False, 15.7, 40, 320, 500, 'standard'),
    'heather': Plant(False, -2.1, 8.6, 180, 380, 'standard'),
    'hibiscus': Plant(False, 12.1, 24.6, 260, 450, 'tall_plant'),
    'ivy': Plant(False, -4, 14, 90, 450, 'creeping'),
    'kangaroo_paw': Plant(False, 15.7, 40, 100, 300, 'standard'),
    'king_fern': Plant(False, 19.3, 40, 350, 500, 'tall_plant'),
    'labrador_tea': Plant(False, -12.9, 3.2, 200, 380, 'standard'),
    'lady_fern': Plant(False, -5.7, 10.4, 200, 500, 'standard'),
    'licorice_fern': Plant(False, 5, 12.1, 300, 400, 'epiphyte'),
    'artists_conk': Plant(False, -12, 21, 150, 420, 'epiphyte'),
    'lily_of_the_valley': Plant(False, -11.1, 15.7, 180, 415, 'standard'),
    'lilac': Plant(False, -5.7, 8.6, 150, 300, 'tall_plant'),
    'lotus': Plant(False, -0.4, 19.3, 0, 500, 'floating_fresh'),
    'maiden_pink': Plant(False, 5, 25, 100, 350, 'standard'),

    'meads_milkweed': Plant(False, -5.7, 5, 130, 380, 'standard'),
    'milfoil': Plant(False, -9.3, 22.9, 250, 500, 'water_fresh'),
    'morning_glory': Plant(False, -14, 19, 300, 500, 'creeping'),
    'philodendron': Plant(False, 16, 30, 380, 500, 'creeping'),
    'moss': Plant(False, -10, 30, 250, 450, 'creeping'),
    'nasturtium': Plant(False, 8.6, 22.9, 150, 380, 'standard'),
    'ostrich_fern': Plant(False, -9.3, 8.6, 290, 470, 'tall_plant'),
    'oxeye_daisy': Plant(False, -9.3, 12.1, 120, 300, 'standard'),
    'phragmite': Plant(False, -2.1, 19.3, 50, 250, 'emergent_fresh'),
    'pickerelweed': Plant(False, -9.3, 17.5, 200, 500, 'emergent_fresh'),
    'pistia': Plant(False, 8.6, 26.4, 0, 400, 'floating_fresh'),
    'poppy': Plant(False, -7.5, 15.7, 150, 250, 'standard'),
    'primrose': Plant(False, -3.9, 12.1, 150, 300, 'standard'),
    'pulsatilla': Plant(False, -5.7, 5, 50, 200, 'standard'),
    'red_algae': Plant(False, -20, 30, 215, 450, 'floating'),
    'red_sealing_wax_palm': Plant(False, 19.3, 40, 280, 500, 'tall_plant'),
    'reindeer_lichen': Plant(False, -30, -8, 50, 470, 'creeping'),
    'rose': Plant(True, -5, 20, 150, 300, 'tall_plant'),
    'sacred_datura': Plant(False, 6.8, 19.3, 75, 150, 'standard'),
    'sagebrush': Plant(False, -5.7, 15.7, 0, 120, 'dry'),
    'sago': Plant(False, -12.9, 19.3, 200, 500, 'water_fresh'),
    'saguaro_fruit': Plant(False, -18, 18, 200, 500, 'cactus_fruit', False),
    'sapphire_tower': Plant(False, 12.1, 22.9, 75, 200, 'tall_plant'),
    'sargassum': Plant(False, -5.7, 17.5, 0, 500, 'floating'),
    'sea_lavender': Plant(False, -5.7, 13.9, 300, 450, 'emergent'),
    'sea_palm': Plant(False, -18, 20, 10, 450, 'dry', False),
    'guzmania': Plant(False, 21.1, 40, 290, 480, 'epiphyte'),
    'silver_spurflower': Plant(False, 15.7, 24.6, 230, 400, 'standard'),
    'snapdragon_pink': Plant(False, 17.5, 24.6, 150, 300, 'standard'),
    'snapdragon_red': Plant(False, 13.9, 21.1, 150, 300, 'standard'),
    'snapdragon_white': Plant(False, 10.4, 17.5, 150, 300, 'standard'),
    'snapdragon_yellow': Plant(False, 8.6, 24.6, 150, 300, 'standard'),
    'strelitzia': Plant(False, 15.7, 26.4, 50, 300, 'standard'),
    'switchgrass': Plant(False, -2.1, 22.9, 110, 390, 'tall_grass'),
    'sword_fern': Plant(False, -7.5, 13.9, 100, 500, 'standard'),
    'tall_fescue_grass': Plant(False, -5.7, 12.1, 280, 430, 'tall_grass'),
    'toquilla_palm': Plant(False, 17.5, 40, 250, 500, 'tall_plant'),
    'trillium': Plant(False, -5.7, 10.4, 250, 500, 'standard'),
    'tropical_milkweed': Plant(False, 10.4, 24.6, 120, 300, 'standard'),
    'tulip_orange': Plant(False, 5, 12.1, 200, 400, 'standard'),
    'tulip_pink': Plant(False, -2.1, 5, 200, 400, 'standard'),
    'tulip_red': Plant(False, 3.2, 6.8, 200, 400, 'standard'),
    'tulip_white': Plant(False, -7.5, -0.4, 200, 400, 'standard'),
    'turtle_grass': Plant(False, 15.7, 40, 240, 500, 'grass_water'),
    'vriesea': Plant(False, 15.7, 40, 200, 400, 'epiphyte'),
    'water_canna': Plant(True, 13.9, 40, 150, 500, 'floating_fresh'),
    'water_lily': Plant(False, -7.5, 40, 0, 500, 'floating_fresh'),
    'water_taro': Plant(False, 13.9, 40, 260, 500, 'emergent_fresh'),
    'yucca': Plant(False, -0.4, 22.9, 0, 75, 'dry'),
}

SMALL_FLOWERS = ('allium', 'anthurium', 'black_orchid', 'blood_lily', 'blue_orchid', 'blue_ginger', 'butterfly_milkweed', 'calendula', 'canna', 'dandelion', 'desert_flame', 'goldenrod', 'grape_hyacinth', 'guzmania', 'kangaroo_paw', 'labrador_tea', 'lily_of_the_valley', 'lotus', 'nasturtium', 'oxeye_daisy', 'pistia', 'poppy', 'primrose', 'pulsatilla', 'rose', 'sacred_datura', 'sagebrush', 'sapphire_tower', 'sargassum', 'silver_spurflower', 'snapdragon_red', 'snapdragon_pink', 'snapdragon_white', 'snapdragon_yellow', 'strelitzia', 'trillium', 'tropical_milkweed', 'tulip_orange', 'tulip_red', 'tulip_pink', 'tulip_white', 'vriesea', 'water_lily', 'yucca')

TALL_FLOWERS = ('foxglove', 'hibiscus', 'lilac', 'toquilla_palm', 'marigold')

FLOWERPOT_CROSS_PLANTS = {
    'allium': 'allium_2',
    'anthurium': 'anthurium_0',
    'athyrium_fern': 'single',
    'black_orchid': 'black_orchid_0',
    'blood_lily': 'blood_lily_0',
    'blue_orchid': 'blue_orchid_1',
    'blue_ginger': 'blue_ginger_0',
    'butterfly_milkweed': 'potted',
    'calendula': 'calendula_3',
    'canna': 'canna_3',
    'dandelion': 'dandelion_2',
    'dead_bush': 'dead_bush0',
    'desert_flame': 'desert_flame_0',
    'field_horsetail': 'potted',
    'foxglove': 'item',
    'goldenrod': 'goldenrod_2',
    'grape_hyacinth': 'grape_hyacinth_1',
    'heliconia': 'heliconia_0',
    'heather': 'potted',
    'houstonia': 'houstonia_1',
    'kangaroo_paw': 'item',
    'labrador_tea': 'labrador_tea_4',
    'lady_fern': 'item',
    'lily_of_the_valley': 'lily_of_the_valley_3',
    'maiden_pink': 'potted',
    'meads_milkweed': 'meads_milkweed_3',
    'nasturtium': 'nasturtium_2',
    'ostrich_fern': 'ostrich_fern_3',
    'oxeye_daisy': 'oxeye_daisy_3',
    'perovskia': 'perovskia_3',
    'poppy': 'poppy_2',
    'primrose': 'primrose',
    'pulsatilla': 'pulsatilla_3',
    'rose': 'classic',
    'sacred_datura': 'sacred_datura_3',
    'sagebrush': 'sagebrush_4',
    'saguaro_fruit': 'saguaro_fruit_1',
    'sapphire_tower': 'potted',
    'silver_spurflower': 'silver_spurflower_2',
    'snapdragon_pink': 'snapdragon_pink_1',
    'snapdragon_red': 'snapdragon_red_1',
    'snapdragon_white': 'snapdragon_white_1',
    'snapdragon_yellow': 'snapdragon_yellow_1',
    'strelitzia': 'strelitzia_0',
    'sword_fern': 'potted',
    'toquilla_palm': 'potted',
    'trillium': 'trillium',
    'tropical_milkweed': 'tropical_milkweed_3',
    'tulip_orange': 'tulip_orange_1',
    'tulip_pink': 'tulip_pink_1',
    'tulip_red': 'tulip_red_1',
    'tulip_white': 'tulip_white_1',
    'yucca': 'potted'
}

SIMPLE_TALL_PLANTS = {
    'foxglove': 5
}
MISC_POTTED_PLANTS = ['barrel_cactus', 'morning_glory', 'moss', 'reindeer_lichen', 'rose', 'toquilla_palm', 'tree_fern', 'sea_palm', 'philodendron']

SIMPLE_STAGE_PLANTS: Dict[str, int] = {
    'allium': 8,
    'anthurium': 2,
    'black_orchid': 3,
    'blood_lily': 4,
    'blue_ginger': 2,
    'blue_orchid': 3,
    'butterfly_milkweed': 7,
    'desert_flame': 2,
    'heliconia': 3,
    'houstonia': 3,
    'goldenrod': 5,
    'grape_hyacinth': 4,
    'kangaroo_paw': 2,  # tinted
    'labrador_tea': 7,
    'lily_of_the_valley': 6,
    'meads_milkweed': 7,
    'nasturtium': 5,
    'oxeye_daisy': 6,
    'perovskia': 6,
    'poppy': 5,
    'primrose': 3,
    'pulsatilla': 6,
    'sacred_datura': 5,  # different
    'saguaro_fruit': 2,
    'silver_spurflower': 3,
    'strelitzia': 3,
    'trillium': 6,  # different
    'tropical_milkweed': 4,
    'yucca': 4
}

MODEL_PLANTS: List[str] = ['arundo', 'arundo_plant', 'athyrium_fern', 'dry_phragmite', 'dry_phragmite_plant', 'hanging_vines', 'hanging_vines_plant', 'spanish_moss', 'spanish_moss_plant', 'lady_fern', 'laminaria', 'liana', 'liana_plant', 'milfoil', 'sago', 'sword_fern', 'tree_fern', 'tree_fern_plant', 'winged_kelp', 'winged_kelp_plant', 'sea_palm']
SEAGRASS: List[str] = ['star_grass', 'manatee_grass', 'eel_grass', 'turtle_grass', 'coontail']

UNIQUE_PLANTS: List[str] = ['hanging_vines_plant', 'hanging_vines', 'spanish_moss', 'spanish_moss_plant', 'liana_plant', 'liana', 'tree_fern_plant', 'tree_fern', 'arundo_plant', 'arundo', 'dry_phragmite', 'dry_phragmite_plant', 'winged_kelp_plant', 'winged_kelp', 'leafy_kelp_plant', 'leafy_kelp', 'giant_kelp_plant', 'giant_kelp_flower', 'jungle_vines', 'saguaro', 'saguaro_plant']
BROWN_COMPOST_PLANTS: List[str] = ['hanging_vines', 'spanish_moss', 'liana', 'tree_fern', 'arundo', 'dry_phragmite', 'jungle_vines']
SEAWEED: List[str] = ['sago', 'gutweed', 'laminaria', 'milfoil']
CORALS: List[str] = ['tube', 'brain', 'bubble', 'fire', 'horn']
CORAL_BLOCKS: List[str] = ['dead_coral', 'dead_coral', 'dead_coral_fan', 'coral_fan', 'dead_coral_wall_fan', 'coral_wall_fan']

PLANT_COLORS: Dict[str, List[str]] = {
    'white': ['houstonia', 'oxeye_daisy', 'primrose', 'snapdragon_white', 'trillium', 'spanish_moss', 'tulip_white', 'water_lily', 'lily_of_the_valley'],
    'orange': ['butterfly_milkweed', 'canna', 'nasturtium', 'strelitzia', 'tulip_orange', 'water_canna', 'marigold'],
    'magenta': ['athyrium_fern', 'morning_glory', 'pulsatilla', 'lilac', 'silver_spurflower'],
    'light_blue': ['labrador_tea', 'sapphire_tower'],
    'yellow': ['calendula', 'dandelion', 'meads_milkweed', 'goldenrod', 'snapdragon_yellow', 'desert_flame'],
    'lime': ['moss'],
    'pink': ['foxglove', 'sacred_datura', 'tulip_pink', 'snapdragon_pink', 'hibiscus', 'lotus', 'maiden_pink'],
    'light_gray': ['yucca'],
    'purple': ['allium', 'black_orchid', 'perovskia', 'blue_ginger', 'pickerelweed', 'heather'],
    'blue': ['blue_orchid', 'grape_hyacinth'],
    'brown': ['field_horsetail', 'sargassum'],
    'green': ['barrel_cactus', 'reindeer_lichen'],
    'red': ['guzmania', 'poppy', 'rose', 'snapdragon_red', 'tropical_milkweed', 'tulip_red', 'vriesea', 'anthurium', 'blood_lily', 'heliconia', 'kangaroo_paw']
}

COLOR_COMBOS = [
    ('red', 'yellow', 'orange'),
    ('blue', 'white', 'light_blue'),
    ('purple', 'pink', 'magenta'),
    ('red', 'white', 'pink'),
    ('white', 'gray', 'light_gray'),
    ('white', 'black', 'gray'),
    ('green', 'white', 'lime'),
    ('green', 'blue', 'cyan'),
    ('red', 'blue', 'purple'),
    ('yellow', 'blue', 'green')
]

VESSEL_TYPES = {
    'blue': 'a',
    'brown': 'a',
    'gray': 'a',
    'light_gray': 'a',
    'magenta': 'a',
    'orange': 'a',
    'white': 'a',
    'pink': 'b',
    'cyan': 'b',
    'purple': 'b',
    'yellow': 'c',
    'black': 'c',
    'light_blue': 'c',
    'lime': 'c',
    'red': 'c',
    'green': 'd'
}

DISC_COLORS = {
    'yellow': '13',
    'orange': 'blocks',
    'lime': 'cat',
    'red': 'chirp',
    'green': 'far',
    'purple': 'mall',
    'magenta': 'mellohi',
    'cyan': 'otherside',
    'black': 'stal',
    'white': 'strad',
    'light_blue': 'wait',
    'blue': 'ward',
}

SIMPLE_BLOCKS = ('peat', 'aggregate', 'fire_bricks', 'fire_clay_block', 'smooth_mud_bricks')
SIMPLE_ITEMS = ('alabaster_brick', 'bone_needle', 'blank_disc', 'blubber', 'brass_mechanisms', 'burlap_cloth', 'compost', 'daub', 'dirty_jute_net', 'empty_jar', 'empty_jar_with_lid', 'fire_clay', 'goat_horn', 'gem_saw', 'glow_arrow', 'glue', 'hematitic_glass_batch', 'jacks', 'jar_lid',
                'jute', 'jute_fiber', 'jute_net', 'kaolin_clay', 'lamp_glass', 'lens', 'mortar', 'olive_paste', 'olivine_glass_batch', 'paddle', 'papyrus', 'papyrus_strip', 'pure_nitrogen', 'pure_phosphorus', 'pure_potassium', 'rotten_compost', 'sandpaper', 'silica_glass_batch', 'silk_cloth', 'soaked_papyrus_strip', 'soot', 'spindle',
                'stick_bunch', 'stick_bundle', 'straw', 'treated_hide', 'unrefined_paper', 'volcanic_glass_batch', 'wool', 'wool_cloth', 'wool_yarn', 'wrought_iron_grill')
GENERIC_POWDERS = {
    'charcoal': 'black',
    'coke': 'black',
    'graphite': 'blue',
    'kaolinite': 'pink',
    'sylvite': 'orange',
    'lapis_lazuli': 'blue'
}
POWDERS = ('flux', 'lime', 'salt', 'saltpeter', 'soda_ash', 'sulfur', 'wood_ash')
GLASSWORKING_POWDERS = ('soda_ash', 'sulfur', 'graphite', 'hematite', 'limonite', 'magnetite', 'native_gold', 'native_copper', 'malachite', 'tetrahedrite', 'cassiterite', 'garnierite', 'native_silver', 'amethyst', 'ruby', 'lapis_lazuli', 'pyrite', 'sapphire')
VANILLA_DYED_ITEMS = ('wool', 'carpet', 'bed', 'terracotta', 'banner', 'glazed_terracotta')
SIMPLE_POTTERY = ('bowl', 'fire_brick', 'pot', 'spindle_head', 'vessel')
SIMPLE_UNFIRED_POTTERY = ('brick', 'crucible', 'flower_pot', 'jug', 'pan', 'blowpipe')
GLASS_TYPES = ('silica', 'hematitic', 'olivine', 'volcanic')
VANILLA_TOOL_MATERIALS = ('netherite', 'diamond', 'iron', 'stone', 'wooden', 'golden')
SHORE_DECORATORS = ('driftwood', 'clam', 'mollusk', 'mussel', 'seaweed', 'sticks_shore', 'guano')
FOREST_DECORATORS = ('sticks_forest', 'pinecone', 'salt_lick', 'dead_grass', 'humus', 'rotten_flesh')
OCEAN_PLANT_TYPES = ('grass_water', 'floating', 'water', 'emergent', 'tall_water')
MISC_PLANT_FEATURES = ('hanging_vines', 'hanging_vines_cave', 'spanish_moss', 'saguaro_patch', 'jungle_vines', 'liana', 'moss_cover', 'reindeer_lichen_cover', 'morning_glory_cover', 'philodendron_cover', 'tree_fern', 'arundo')
SURFACE_GRASS_FEATURES = ('fountain_', 'orchard_', 'rye', 'scutch_', 'timothy_', 'brome', 'blue', 'raddia_')
UNDERGROUND_FEATURES = ('cave_column', 'cave_spike', 'large_cave_spike', 'water_spring', 'lava_spring', 'calcite', 'mega_calcite', 'icicle', 'underground_loose_rocks', 'underground_guano_patch')

# todo: bush hydration / rainfall separation and proper ranges
# When this gest updated, it needs to be updated in both the book (generate_book.py) and in the climate range (data.py) to use the new hydration and rainfall values
# Alternatively, we ditch rainfall and/or hydration entirely.
BERRIES: Dict[str, Berry] = {
    'blackberry': Berry(7, 24, 200, 500, 'spreading', 'none', 'edge'),
    'raspberry': Berry(5, 25, 200, 500, 'spreading', 'none', 'edge'),
    'blueberry': Berry(7, 29, 100, 400, 'spreading', 'none', 'edge'),
    'elderberry': Berry(10, 33, 100, 400, 'spreading', 'none', 'edge'),
    'bunchberry': Berry(15, 35, 200, 500, 'stationary', 'edge', 'old_growth'),
    'gooseberry': Berry(5, 27, 200, 500, 'stationary', 'edge', 'old_growth'),
    'snowberry': Berry(-7, 18, 200, 500, 'stationary', 'edge', 'old_growth'),
    'cloudberry': Berry(-2, 17, 80, 380, 'stationary', 'edge', 'old_growth'),
    'strawberry': Berry(5, 28, 100, 400, 'stationary', 'edge', 'old_growth'),
    'wintergreen_berry': Berry(-6, 17, 100, 400, 'stationary', 'edge', 'old_growth'),
    'cranberry': Berry(-5, 17, 250, 500, 'waterlogged', 'edge', 'old_growth')
}

FRUITS: Dict[str, Fruit] = {
    'banana': Fruit(17, 35, 280, 500),
    'cherry': Fruit(5, 25, 100, 350),
    'green_apple': Fruit(1, 25, 110, 280),
    'lemon': Fruit(10, 30, 180, 470),
    'olive': Fruit(5, 30, 150, 500),
    'orange': Fruit(15, 36, 250, 500),
    'peach': Fruit(4, 27, 60, 230),
    'plum': Fruit(15, 31, 250, 400),
    'red_apple': Fruit(1, 25, 100, 280)
}
JAR_FRUITS: List[str] = [*BERRIES.keys(), *FRUITS.keys(), 'pumpkin_chunks', 'melon_slice']
NORMAL_FRUIT_TREES: List[str] = [k for k in FRUITS.keys() if k != 'banana']

SIMPLE_FRESHWATER_FISH = ('bluegill', 'crappie', 'lake_trout', 'largemouth_bass', 'rainbow_trout', 'salmon', 'smallmouth_bass',)

GRAINS = ('barley', 'maize', 'oat', 'rice', 'rye', 'wheat')
GRAIN_SUFFIXES = ('', '_grain', '_flour', '_dough', '_bread', '_bread_sandwich', '_bread_jam_sandwich')
MISC_FOODS = ('beet', 'cabbage', 'carrot', 'garlic', 'green_bean', 'green_bell_pepper', 'onion', 'potato', 'baked_potato', 'red_bell_pepper', 'soybean', 'squash', 'tomato', 'yellow_bell_pepper', 'cheese', 'cooked_egg', 'boiled_egg', 'fresh_seaweed', 'dried_seaweed', 'dried_kelp', 'cattail_root', 'taro_root', 'sugarcane', 'cooked_rice', 'pumpkin_chunks', 'melon_slice')
MEATS = ('beef', 'pork', 'chicken', 'quail', 'mutton', 'bear', 'horse_meat', 'pheasant', 'turkey', 'peafowl', 'grouse', 'venison', 'wolf', 'rabbit', 'hyena', 'duck', 'chevon', 'gran_feline', 'camelidae', 'cod', 'tropical_fish', 'turtle', 'calamari', 'shellfish', *SIMPLE_FRESHWATER_FISH, 'frog_legs')
NUTRIENTS = ('grain', 'fruit', 'vegetables', 'protein', 'dairy')

SPAWN_EGG_ENTITIES = ('isopod', 'lobster', 'crayfish', 'cod', 'pufferfish', 'tropical_fish', 'jellyfish', 'orca', 'dolphin', 'manatee', 'penguin', 'frog', 'turtle', 'horseshoe_crab', 'polar_bear', 'grizzly_bear', 'black_bear', 'cougar', 'panther', 'lion', 'sabertooth', 'squid', 'octopoteuthis', 'pig', 'cow', 'goat', 'yak', 'alpaca', 'musk_ox', 'sheep', 'chicken', 'duck', 'quail', 'rabbit', 'fox', 'boar', 'donkey', 'mule', 'horse', 'deer', 'moose', 'boar', 'rat', 'cat', 'dog', 'wolf', 'panda', 'grouse', 'pheasant', 'turkey', 'ocelot', 'direwolf', 'hyena', 'tiger', 'crocodile', 'bongo', 'caribou', 'gazelle', 'wildebeest', 'peafowl', *SIMPLE_FRESHWATER_FISH)
BUCKETABLE_FISH = ('cod', 'pufferfish', 'tropical_fish', 'jellyfish', *SIMPLE_FRESHWATER_FISH)
LAND_PREDATORS = ('polar_bear', 'grizzly_bear', 'black_bear', 'cougar', 'panther', 'lion', 'sabertooth', 'wolf', 'direwolf', 'ocelot', 'tiger', 'hyena', 'crocodile')
AMPHIBIOUS_PREDATORS = 'crocodile'
OCEAN_PREDATORS = ('dolphin', 'orca')
OCEAN_PREY = ('isopod', 'lobster', 'crayfish', 'cod', 'tropical_fish', 'horseshoe_crab', *SIMPLE_FRESHWATER_FISH)
LIVESTOCK = ('pig', 'cow', 'goat', 'yak', 'alpaca', 'sheep', 'musk_ox', 'chicken', 'duck', 'quail', 'horse', 'mule', 'donkey')
LAND_PREY = ('rabbit', 'fox', 'turtle', 'penguin', 'frog', 'deer', 'bongo', 'panda', 'grouse', 'pheasant', 'turkey', 'ocelot', 'caribou', 'gazelle', 'peafowl')
LAND_NEUTRALS = ('boar', 'moose', 'wildebeest')

BLOCK_ENTITIES = ('log_pile', 'burning_log_pile', 'placed_item', 'pit_kiln', 'charcoal_forge', 'quern', 'scraping', 'crucible', 'bellows', 'composter', 'chest', 'trapped_chest', 'barrel', 'loom', 'sluice', 'tool_rack', 'sign', 'lamp', 'berry_bush', 'crop', 'firepit', 'pot', 'grill', 'pile', 'farmland', 'tick_counter', 'nest_box', 'bloomery', 'bloom', 'anvil', 'ingot_pile', 'sheet_pile', 'blast_furnace', 'large_vessel', 'powderkeg', 'bowl', 'hot_poured_glass', 'glass_basin', 'axle', 'hand_wheel', 'sewing_table')
TANNIN_WOOD_TYPES = ('oak', 'birch', 'chestnut', 'douglas_fir', 'hickory', 'maple', 'sequoia')

def spawner(entity: str, weight: int = 1, min_count: int = 1, max_count: int = 4) -> Dict[str, Any]:
    return {
        'type': entity,
        'weight': weight,
        'minCount': min_count,
        'maxCount': max_count
    }

SALT_MARSH_AMBIENT: Dict[str, Dict[str, Any]] = {
    'isopod': spawner('tfc:isopod'),
    'lobster': spawner('tfc:lobster'),
    'horseshoe_crab': spawner('tfc:horseshoe_crab'),
    'salmon': spawner('tfc:salmon')
}

OCEAN_AMBIENT: Dict[str, Dict[str, Any]] = {
    'isopod': spawner('tfc:isopod'),
    'lobster': spawner('tfc:lobster'),
    'horseshoe_crab': spawner('tfc:horseshoe_crab'),
    'cod': spawner('tfc:cod', weight=10),
    'pufferfish': spawner('tfc:pufferfish', max_count=2),
    'tropical_fish': spawner('tfc:tropical_fish', weight=10, max_count=6),
    'jellyfish': spawner('tfc:jellyfish', min_count=2, max_count=6)
}

OCEAN_CREATURES: Dict[str, Dict[str, Any]] = {
    'orca': spawner('tfc:orca', min_count=1, max_count=3),
    'dolphin': spawner('tfc:dolphin', min_count=1, max_count=3),
    'squid': spawner('tfc:squid', min_count=1, max_count=3, weight=2)
}

UNDERGROUND_WATER_CREATURES: Dict[str, Dict[str, Any]] = {
    'octopoteuthis': spawner('tfc:octopoteuthis', min_count=1, max_count=2)
}

LAKE_AMBIENT: Dict[str, Dict[str, Any]] = {
    **dict(('%s' % fish, spawner('tfc:%s' % fish, min_count=2, max_count=4, weight=10)) for fish in SIMPLE_FRESHWATER_FISH if 'trout' not in fish),
    'crayfish': spawner('tfc:crayfish', min_count=1, max_count=4, weight=5)
}

RIVER_AMBIENT: Dict[str, Dict[str, Any]] = {
    **dict(('%s' % fish, spawner('tfc:%s' % fish, min_count=2, max_count=4, weight=10)) for fish in SIMPLE_FRESHWATER_FISH if 'trout' in fish),
}

LAKE_CREATURES: Dict[str, Dict[str, Any]] = {
    'manatee': spawner('tfc:manatee', min_count=1, max_count=2)
}

SHORE_CREATURES: Dict[str, Dict[str, Any]] = {
    'penguin': spawner('tfc:penguin', min_count=2, max_count=5, weight=10),
    'turtle': spawner('tfc:turtle', min_count=2, max_count=5, weight=10)
}

LAND_CREATURES: Dict[str, Dict[str, Any]] = {
    'crocodile': spawner('tfc:crocodile', min_count=1, max_count=1, weight=20),
    'pig': spawner('tfc:pig', min_count=1, max_count=4),
    'cow': spawner('tfc:cow', min_count=1, max_count=4),
    'goat': spawner('tfc:goat', min_count=1, max_count=4),
    'yak': spawner('tfc:yak', min_count=1, max_count=4),
    'alpaca': spawner('tfc:alpaca', min_count=1, max_count=4),
    'sheep': spawner('tfc:sheep', min_count=1, max_count=4),
    'musk_ox': spawner('tfc:musk_ox', min_count=1, max_count=4),
    'chicken': spawner('tfc:chicken', min_count=2, max_count=6),
    'duck': spawner('tfc:duck', min_count=2, max_count=6),
    'quail': spawner('tfc:quail', min_count=2, max_count=6),
    'polar_bear': spawner('tfc:polar_bear', min_count=1, max_count=1, weight=2),
    'grizzly_bear': spawner('tfc:grizzly_bear', min_count=1, max_count=1, weight=2),
    'black_bear': spawner('tfc:black_bear', min_count=1, max_count=1, weight=2),
    'lion': spawner('tfc:lion', min_count=1, max_count=3, weight=2),
    'sabertooth': spawner('tfc:sabertooth', min_count=1, max_count=1, weight=2),
    'tiger': spawner('tfc:tiger', min_count=1, max_count=1, weight=2),
    'rabbit': spawner('tfc:rabbit', min_count=1, max_count=4, weight=3),
    'fox': spawner('tfc:fox', min_count=1, max_count=1),
    'panda': spawner('tfc:panda', min_count=3, max_count=5),
    'boar': spawner('tfc:boar', min_count=1, max_count=2, weight=2),
    'wildebeest': spawner('tfc:wildebeest', min_count=1, max_count=2, weight=2),
    'moose': spawner('tfc:moose', min_count=1, max_count=1),
    'bongo': spawner('tfc:bongo', min_count=2, max_count=4, weight=3),
    'caribou': spawner('tfc:caribou', min_count=2, max_count=4, weight=3),
    'deer': spawner('tfc:deer', min_count=2, max_count=4, weight=3),
    'gazelle': spawner('tfc:gazelle', min_count=2, max_count=4, weight=3),
    'grouse': spawner('tfc:grouse', min_count=2, max_count=4),
    'pheasant': spawner('tfc:pheasant', min_count=2, max_count=4),
    'turkey': spawner('tfc:turkey', min_count=2, max_count=4),
    'peafowl': spawner('tfc:peafowl', min_count=2, max_count=4),
    'wolf': spawner('tfc:wolf', min_count=6, max_count=9),
    'hyena': spawner('tfc:hyena', min_count=5, max_count=9),
    'direwolf': spawner('tfc:direwolf', min_count=3, max_count=7),
    'donkey': spawner('tfc:donkey', min_count=1, max_count=3),
    'horse': spawner('tfc:horse', min_count=1, max_count=3),
    'ocelot': spawner('tfc:ocelot', min_count=1, max_count=3),
    'frog': spawner('tfc:frog', min_count=2, max_count=4),
}

VANILLA_MONSTERS: Dict[str, Dict[str, Any]] = {
    'spider': spawner('minecraft:spider', weight=100, min_count=4, max_count=4),
    'zombie': spawner('minecraft:zombie', weight=95, min_count=4, max_count=4),
    'skeleton': spawner('minecraft:skeleton', weight=100, min_count=4, max_count=4),
    'creeper': spawner('minecraft:creeper', weight=100, min_count=4, max_count=4),
    'slime': spawner('minecraft:slime', weight=100, min_count=4, max_count=4),
}

DISABLED_VANILLA_RECIPES = ('flint_and_steel', 'turtle_helmet', 'campfire', 'bucket', 'composter', 'tinted_glass', 'glass_pane', 'enchanting_table', 'bowl', 'blaze_rod', 'bone_meal', 'flower_pot', 'painting', 'torch', 'soul_torch', 'sticky_piston', 'clock', 'compass', 'white_wool_from_string', 'hay_block', 'anvil', 'wheat', 'lapis_lazuli', 'leather_horse_armor', 'map', 'furnace', 'jack_o_lantern', 'melon_seeds', 'melon', 'pumpkin_pie', 'chest', 'barrel', 'trapped_chest', 'bricks', 'bookshelf', 'crafting_table', 'lectern', 'chest_minecart', 'rail', 'beetroot_soup', 'mushroom_stew', 'rabbit_stew_from_red_mushroom',
                            'rabbit_stew_from_brown_mushroom', 'suspicious_stew', 'scaffolding', 'bow', 'glass_bottle', 'fletching_table', 'shield', 'lightning_rod', 'fishing_rod', 'iron_door', 'iron_trapdoor', 'spyglass', 'slime_ball', 'smoker', 'soul_campfire', 'loom', 'lantern', 'soul_lantern', 'flower_banner_pattern', 'skull_banner_pattern', 'creeper_banner_pattern', 'mojang_banner_pattern')
ARMOR_SECTIONS = ('chestplate', 'leggings', 'boots', 'helmet')
TFC_ARMOR_SECTIONS = ('helmet', 'chestplate', 'greaves', 'boots')
VANILLA_ARMOR_TYPES = ('leather', 'golden', 'iron', 'diamond', 'netherite')
VANILLA_TOOLS = ('sword', 'shovel', 'pickaxe', 'axe', 'hoe')
MOB_ARMOR_METALS = ('copper', 'bronze', 'black_bronze', 'bismuth_bronze', 'wrought_iron')
MOB_TOOLS = ('axe', 'sword', 'javelin', 'mace', 'scythe')
STONE_MOB_TOOLS = ('axe', 'javelin')
TFC_BIOMES = ('badlands', 'inverted_badlands', 'canyons', 'low_canyons', 'plains', 'plateau', 'hills', 'rolling_hills', 'lake', 'lowlands', 'salt_marsh', 'mountains', 'volcanic_mountains', 'old_mountains', 'oceanic_mountains', 'volcanic_oceanic_mountains', 'ocean', 'ocean_reef', 'deep_ocean', 'deep_ocean_trench', 'river', 'shore', 'tidal_shore', 'mountain_river', 'volcanic_mountain_river', 'old_mountain_river', 'oceanic_mountain_river', 'volcanic_oceanic_mountain_river', 'mountain_lake', 'volcanic_mountain_lake', 'old_mountain_lake', 'oceanic_mountain_lake', 'volcanic_oceanic_mountain_lake', 'plateau_lake')
PAINTINGS = ('golden_field', 'hot_spring', 'lake', 'supports', 'volcano')
VANILLA_TRIMS = ('coast', 'sentry', 'dune', 'wild', 'ward', 'eye', 'vex', 'tide', 'snout', 'rib', 'spire', 'wayfinder', 'shaper', 'silence', 'raiser', 'host')

ALLOYS: Dict[str, Tuple[Tuple[str, float, float], ...]] = {
    'bismuth_bronze': (('zinc', 0.2, 0.3), ('copper', 0.5, 0.65), ('bismuth', 0.1, 0.2)),
    'black_bronze': (('copper', 0.5, 0.7), ('silver', 0.1, 0.25), ('gold', 0.1, 0.25)),
    'bronze': (('copper', 0.88, 0.92), ('tin', 0.08, 0.12)),
    'brass': (('copper', 0.88, 0.92), ('zinc', 0.08, 0.12)),
    'rose_gold': (('copper', 0.15, 0.3), ('gold', 0.7, 0.85)),
    'sterling_silver': (('copper', 0.2, 0.4), ('silver', 0.6, 0.8)),
    'weak_steel': (('steel', 0.5, 0.7), ('nickel', 0.15, 0.25), ('black_bronze', 0.15, 0.25)),
    'weak_blue_steel': (('black_steel', 0.5, 0.55), ('steel', 0.2, 0.25), ('bismuth_bronze', 0.1, 0.15), ('sterling_silver', 0.1, 0.15)),
    'weak_red_steel': (('black_steel', 0.5, 0.55), ('steel', 0.2, 0.25), ('brass', 0.1, 0.15), ('rose_gold', 0.1, 0.15))
}

# This is here because it's used all over, and it's easier to import with all constants
def lang(key: str, *args) -> str:
    return ((key % args) if len(args) > 0 else key).replace('_', ' ').replace('/', ' ').title()


def lang_enum(name: str, values: Sequence[str]) -> Dict[str, str]:
    return dict(('tfc.enum.%s.%s' % (name, value), lang(value)) for value in values)


VANILLA_OVERRIDE_LANG = {
    'item.minecraft.glow_ink_sac': 'Glowing Ink Sac',
    'item.minecraft.shield': 'Wooden Shield',
    'block.minecraft.bell': 'Golden Bell',
    'block.minecraft.slime_block': 'Glue Block',
    'block.minecraft.loom': 'Banner Loom',
    **dict(('item.minecraft.shield.%s' % color, '%s Wooden Shield' % lang(color)) for color in COLORS),
}

# This is here as it's used only once in a generic lang call by generate_resources.py
DEFAULT_LANG = {
    # Misc
    'death.attack.tfc.grill': '%1$s grilled themself to death',
    'death.attack.tfc.grill.player': '%1$s grilled themselves while trying to escape %2$s',
    'death.attack.tfc.pot': '%1$s boiled themselves into soup',
    'death.attack.tfc.pot.player': '%1$s boiled themself while trying to escape %2$s',
    'death.attack.tfc.dehydration': '%1$s dehydrated to death',
    'death.attack.tfc.dehydration.player': '%1$s dehydrated to death while trying to escape %2$s',
    'death.attack.tfc.coral': '%1$s impaled themself on a coral reef.',
    'death.attack.tfc.coral.player': '%1$s impaled themself on a coral reef while trying to escape %2$s',
    'death.attack.tfc.pluck': '%1$s was plucked to death.',
    'death.attack.tfc.pluck.player': '%1$s was plucked to death by %2$s, which is surprising, because people don\'t typically grow feathers.',
    'effect.tfc.pinned': 'Pinned',
    'effect.tfc.ink': 'Ink',
    'effect.tfc.glow_ink': 'Glowing Ink',
    'effect.tfc.overburdened': 'Overburdened',
    'effect.tfc.thirst': 'Thirst',
    'effect.tfc.exhausted': 'Exhausted',
    'tfc.key.place_block': 'Place Block',
    'tfc.key.cycle_chisel_mode': 'Cycle Chisel Mode',
    'tfc.key.stack_food': 'Stack Food',
    # Sounds
    'subtitles.block.tfc.crop.stick_add': 'Stick placed in farmland',
    'subtitles.block.tfc.bloomery.crackle': 'Bloomery crackles',
    'subtitles.block.tfc.quern.drag': 'Quern grinding',
    'subtitles.block.tfc.loom.weave': 'Loom clacking',
    'subtitles.block.tfc.bellows.blow': 'Air whooshing',
    'subtitles.block.tfc.tool_rack.place_item': 'Item placed on Tool Rack',
    'subtitles.block.tfc.wattle.dyed': 'Wattle stained',
    'subtitles.block.tfc.wattle.daubed': 'Wattle daubed',
    'subtitles.block.tfc.wattle.woven': 'Wattle woven',
    'subtitles.block.tfc.scribing_table.rename_item': 'Player scribbling',
    'subtitles.block.tfc.barrel.opened': 'Barrel opened',
    'subtitles.block.tfc.barrel.closed': 'Barrel closed',
    'subtitles.block.tfc.vessel.opened': 'Vessel opened',
    'subtitles.block.tfc.vessel.closed': 'Vessel closed',
    'subtitles.block.tfc.anvil.hit': 'Anvil clangs',
    'subtitles.block.tfc.barrel.drip': 'Barrel leaks water',
    'subtitles.item.tfc.fertilizer.use': 'Fertilizer spread',
    'subtitles.item.tfc.pan.use': 'Pan sifting',
    'subtitles.item.tfc.ceramic.break': 'Ceramics shattering',
    'subtitles.item.tfc.jug.blow': 'Jug whistles',
    'subtitles.item.tfc.knapping.clay': 'Clay squishes',
    'subtitles.item.tfc.knapping.leather': 'Leather scrapes',
    'subtitles.item.tfc.knapping.rock': 'Rock clacks',
    'subtitles.item.tfc.javelin.hit': 'Javelin stabs',
    'subtitles.item.tfc.javelin.hit_ground': 'Javelin vibrates',
    'subtitles.item.tfc.javelin.throw': 'Javelin clangs',
    'subtitles.item.tfc.cool': 'Something hisses',
    **dict(('subtitles.item.armor.equip_%s' % metal, '%s armor equips' % lang(metal)) for metal, data in METALS.items() if 'armor' in data.types),
    'subtitles.item.tfc.firestarter.use': 'Firestarter scratches',
    'subtitles.entity.tfc.alpaca.ambient': 'Alpaca bleats',
    'subtitles.entity.tfc.alpaca.hurt': 'Alpaca yelps',
    'subtitles.entity.tfc.alpaca.death': 'Alpaca dies',
    'subtitles.entity.tfc.yak.ambient': 'Yak grumbles',
    'subtitles.entity.tfc.yak.hurt': 'Yak groans',
    'subtitles.entity.tfc.yak.death': 'Yak dies',
    'subtitles.entity.tfc.musk_ox.ambient': 'Musk Ox pants',
    'subtitles.entity.tfc.musk_ox.hurt': 'Musk Ox bellows',
    'subtitles.entity.tfc.musk_ox.death': 'Musk Ox dies',
    'subtitles.entity.tfc.duck.ambient': 'Duck quacks',
    'subtitles.entity.tfc.duck.hurt': 'Duck quacks angrily',
    'subtitles.entity.tfc.duck.death': 'Duck dies',
    'subtitles.entity.tfc.penguin.ambient': 'Penguin quacks',
    'subtitles.entity.tfc.penguin.hurt': 'Penguin quacks angrily',
    'subtitles.entity.tfc.penguin.death': 'Penguin dies',
    'subtitles.entity.tfc.quail.ambient': 'Quail calls',
    'subtitles.entity.tfc.quail.hurt': 'Quail yelps',
    'subtitles.entity.tfc.quail.death': 'Quail dies',
    'subtitles.entity.tfc.bear.ambient': 'Bear groans',
    'subtitles.entity.tfc.bear.attack': 'Bear roars',
    'subtitles.entity.tfc.bear.hurt': 'Bear hurts',
    'subtitles.entity.tfc.bear.death': 'Bear dies',
    'subtitles.entity.tfc.bear.sleep': 'Bear snores',
    'subtitles.entity.tfc.cougar.death': 'Cougar dies',
    'subtitles.entity.tfc.cougar.attack': 'Cougar roars',
    'subtitles.entity.tfc.cougar.ambient': 'Cougar screams',
    'subtitles.entity.tfc.cougar.hurt': 'Cougar yowls',
    'subtitles.entity.tfc.cougar.sleep': 'Cougar snores',
    'subtitles.entity.tfc.lion.death': 'Lion dies',
    'subtitles.entity.tfc.lion.attack': 'Lion roars',
    'subtitles.entity.tfc.lion.ambient': 'Lion grunts',
    'subtitles.entity.tfc.lion.hurt': 'Lion roars',
    'subtitles.entity.tfc.lion.sleep': 'Lion snores',
    'subtitles.entity.tfc.sabertooth.death': 'Sabertooth dies',
    'subtitles.entity.tfc.sabertooth.attack': 'Sabertooth roars',
    'subtitles.entity.tfc.sabertooth.ambient': 'Sabertooth calls',
    'subtitles.entity.tfc.sabertooth.hurt': 'Sabertooth yowls',
    'subtitles.entity.tfc.sabertooth.sleep': 'Sabertooth snores',
    'subtitles.entity.tfc.tiger.death': 'Tiger dies',
    'subtitles.entity.tfc.tiger.attack': 'Tiger roars',
    'subtitles.entity.tfc.tiger.ambient': 'Tiger chuffs',
    'subtitles.entity.tfc.tiger.hurt': 'Tiger yowls',
    'subtitles.entity.tfc.tiger.sleep': 'Tiger snores',
    'subtitles.entity.tfc.crocodile.death': 'Crocodile dies',
    'subtitles.entity.tfc.crocodile.attack': 'Crocodile roars',
    'subtitles.entity.tfc.crocodile.ambient': 'Crocodile snorts',
    'subtitles.entity.tfc.crocodile.hurt': 'Crocodile roars',
    'subtitles.entity.tfc.crocodile.sleep': 'Crocodile snores',
    'subtitles.entity.tfc.bongo.death': 'Bongo dies',
    'subtitles.entity.tfc.bongo.ambient': 'Bongo brays',
    'subtitles.entity.tfc.bongo.hurt': 'Bongo yelps',
    'subtitles.entity.tfc.caribou.death': 'Caribou dies',
    'subtitles.entity.tfc.caribou.ambient': 'Caribou brays',
    'subtitles.entity.tfc.caribou.hurt': 'Caribou yelps',
    'subtitles.entity.tfc.deer.death': 'Deer dies',
    'subtitles.entity.tfc.deer.ambient': 'Deer brays',
    'subtitles.entity.tfc.deer.hurt': 'Deer yelps',
    'subtitles.entity.tfc.gazelle.death': 'Gazelle dies',
    'subtitles.entity.tfc.gazelle.ambient': 'Gazelle brays',
    'subtitles.entity.tfc.gazelle.hurt': 'Gazelle yelps',
    'subtitles.entity.tfc.moose.death': 'Moose dies',
    'subtitles.entity.tfc.moose.ambient': 'Moose brays',
    'subtitles.entity.tfc.moose.hurt': 'Moose yelps',
    'subtitles.entity.tfc.moose.attack': 'Moose groans',
    'subtitles.entity.tfc.boar.death': 'Boar dies',
    'subtitles.entity.tfc.boar.ambient': 'Boar oinks',
    'subtitles.entity.tfc.boar.hurt': 'Boar squeals',
    'subtitles.entity.tfc.boar.attack': 'Boar grunts',
    'subtitles.entity.tfc.wildbeest.death': 'Wildebeest dies',
    'subtitles.entity.tfc.wildebeest.ambient': 'Wildebeest grunts',
    'subtitles.entity.tfc.wildebeest.hurt': 'Wildebeest yelps',
    'subtitles.entity.tfc.wildebeest.attack': 'Wildebeest rams',
    'subtitles.entity.tfc.grouse.death': 'Grouse dies',
    'subtitles.entity.tfc.grouse.ambient': 'Grouse calls',
    'subtitles.entity.tfc.grouse.hurt': 'Grouse squeals',
    'subtitles.entity.tfc.pheasant.chick.ambient': 'Chick chirps',
    'subtitles.entity.tfc.pheasant.hurt': 'Pheasant crows',
    'subtitles.entity.tfc.pheasant.death': 'Pheasant dies',
    'subtitles.entity.tfc.pheasant.ambient': 'Pheasant calls',
    'subtitles.entity.tfc.turkey.death': 'Turkey dies',
    'subtitles.entity.tfc.turkey.ambient': 'Turkey gobbles',
    'subtitles.entity.tfc.turkey.hurt': 'Turkey yelps',
    'subtitles.entity.tfc.peafowl.death': 'Peacock dies',
    'subtitles.entity.tfc.peafowl.ambient': 'Peacock crows',
    'subtitles.entity.tfc.peafowl.hurt': 'Peacock yelps',
    'subtitles.entity.tfc.rat.death': 'Rat dies',
    'subtitles.entity.tfc.rat.ambient': 'Rat squeaks',
    'subtitles.entity.tfc.rat.hurt': 'Rat squeals',
    'subtitles.entity.tfc.rooster.cry': 'Rooster calls',
    'subtitles.entity.tfc.dog.ambient': 'Dog Barks',
    'subtitles.entity.tfc.dog.hurt': 'Dog Yelps',
    'subtitles.entity.tfc.dog.death': 'Dog Dies',
    'subtitles.entity.tfc.dog.attack': 'Dog Bites',
    'subtitles.entity.tfc.dog.sleep': 'Dog Snores',
    'subtitles.entity.tfc.tfc_wolf.ambient': 'Wolf barks',
    'subtitles.entity.tfc.tfc_wolf.hurt': 'Wolf yelps',
    'subtitles.entity.tfc.tfc_wolf.death': 'Wolf dies',
    'subtitles.entity.tfc.tfc_wolf.attack': 'Wolf bites',
    'subtitles.entity.tfc.tfc_wolf.sleep': 'Wolf snores',
    'subtitles.entity.tfc.hyena.ambient': 'Hyena laughs',
    'subtitles.entity.tfc.hyena.hurt': 'Hyena yelps',
    'subtitles.entity.tfc.hyena.death': 'Hyena dies',
    'subtitles.entity.tfc.hyena.attack': 'Hyena bites',
    'subtitles.entity.tfc.hyena.sleep': 'Hyena snores',
    'subtitles.entity.tfc.ramming.impact': 'Ram impacts',
    **dict(('subtitles.entity.tfc.%s.ambient' % fish, '%s splashes' % fish.title().replace('_', ' ')) for fish in (*SIMPLE_FRESHWATER_FISH, 'manatee', 'jellyfish')),
    **dict(('subtitles.entity.tfc.%s.flop' % fish, '%s flops' % fish.title().replace('_', ' ')) for fish in (*SIMPLE_FRESHWATER_FISH, 'manatee', 'jellyfish')),
    **dict(('subtitles.entity.tfc.%s.death' % fish, '%s dies' % fish.title().replace('_', ' ')) for fish in (*SIMPLE_FRESHWATER_FISH, 'manatee', 'jellyfish')),
    **dict(('subtitles.entity.tfc.%s.hurt' % fish, '%s hurts' % fish.title().replace('_', ' ')) for fish in (*SIMPLE_FRESHWATER_FISH, 'manatee', 'jellyfish')),
    'subtitles.generic.tfc.dirt_slide': 'Soil landslides',
    'subtitles.generic.tfc.rock_slide_long': 'Rock collapses',
    'subtitles.generic.tfc.rock_slide_long_fake': 'Rock creaks',
    'subtitles.generic.tfc.rock_slide_short': 'Rock crumbles',
    'subtitles.generic.tfc.rock_smash': 'Rock smashes',

    # Creative Tabs
    'tfc.creative_tab.earth': 'TFC Earth',
    'tfc.creative_tab.ores': 'TFC Ores',
    'tfc.creative_tab.rock': 'TFC Rock Stuffs',
    'tfc.creative_tab.metals': 'TFC Metal Stuffs',
    'tfc.creative_tab.wood': 'TFC Wooden Stuffs',
    'tfc.creative_tab.flora': 'TFC Flora',
    'tfc.creative_tab.devices': 'TFC Devices',
    'tfc.creative_tab.food': 'TFC Food',
    'tfc.creative_tab.misc': 'TFC Misc',
    'tfc.creative_tab.decorations': 'TFC Decorations',
    # Containers
    'tfc.screen.calendar': 'Calendar',
    'tfc.screen.nutrition': 'Nutrition',
    'tfc.screen.climate': 'Climate',
    'tfc.screen.knapping': 'Knapping',
    'tfc.screen.scribing_table': 'Rename Items',
    'tfc.screen.pet_command': 'Pet Commands',
    'tfc.screen.sewing_table': 'Sewing Table',
    # Tooltips
    'tfc.tooltip.forging': '§f - Can Work',
    'tfc.tooltip.welding': '§f - Can Weld',
    'tfc.tooltip.danger': '§f - Danger!!',
    'tfc.tooltip.anvil_plan': 'Plans',
    'tfc.tooltip.anvil_tier_required': 'Requires %s Anvil',
    'tfc.tooltip.calendar_days_years': '%d, %04d',
    'tfc.tooltip.calendar_hour_minute_month_day_year': '%s %s %d, %04d',
    'tfc.tooltip.calendar_season': 'Season : %s',
    'tfc.tooltip.calendar_day': 'Day : %s',
    'tfc.tooltip.calendar_birthday': '%s\'s Birthday!',
    'tfc.tooltip.calendar_date': 'Date : %s',
    'tfc.tooltip.climate_koppen_climate_classification': 'Climate: %s',
    'tfc.tooltip.climate_average_temperature': 'Avg. Temp: %s',
    'tfc.tooltip.climate_annual_rainfall': 'Annual Rainfall: %smm',
    'tfc.tooltip.climate_current_temp': 'Current Temp: %s',
    'tfc.tooltip.food_expiry_date': 'Expires on: %s',
    'tfc.tooltip.food_expiry_left': 'Expires in: %s',
    'tfc.tooltip.food_expiry_date_and_left': 'Expires on: %s (in %s)',
    'tfc.tooltip.food_infinite_expiry': 'Never expires',
    'tfc.tooltip.food_rotten': 'Rotten!',
    'tfc.tooltip.food_rotten_special': 'Ewwww, are you really thinking of eating that? It looks disgusting',
    'tfc.tooltip.nutrition': 'Nutrition:',
    'tfc.tooltip.nutrition_saturation': ' - Saturation: %s%%',
    'tfc.tooltip.nutrition_water': ' - Water: %s%%',
    'tfc.tooltip.nutrition_none': '- None!',
    'tfc.tooltip.hold_shift_for_nutrition_info': 'Hold (Shift) for Nutrition Info',
    'tfc.tooltip.salad': 'Salad',
    'tfc.tooltip.contents': 'Contents:',
    'tfc.tooltip.propick.found_very_large': 'Found a very large sample of %s',
    'tfc.tooltip.propick.found_large': 'Found a large sample of %s',
    'tfc.tooltip.propick.found_medium': 'Found a medium sample of %s',
    'tfc.tooltip.propick.found_small': 'Found a small sample of %s',
    'tfc.tooltip.propick.found_traces': 'Found traces of %s',
    'tfc.tooltip.propick.found': 'Found %s',
    'tfc.tooltip.propick.nothing': 'Found nothing.',
    'tfc.tooltip.propick.accuracy': 'Accuracy: %s%%',
    'tfc.tooltip.pan.contents': '§7Contains ',
    'tfc.tooltip.pan.water': 'You need to stand in water to be able to pan.',
    'tfc.tooltip.small_vessel.inventory_too_hot': 'Too hot to open!',
    'tfc.tooltip.small_vessel.alloy_solid': 'Contents have solidified!',
    'tfc.tooltip.small_vessel.alloy_molten': 'Contents are still liquid!',
    'tfc.tooltip.small_vessel.contents': 'Contents:',
    'tfc.tooltip.small_vessel.solid': ' - Solid.',
    'tfc.tooltip.small_vessel.molten': ' - Molten!',
    'tfc.tooltip.small_vessel.still_has_unmelted_items': 'Contains un-melted items!',
    'tfc.tooltip.mold.fluid_incompatible': 'This metal can\'t go in the mold!',
    'tfc.tooltip.food_trait.salted': 'Salted',
    'tfc.tooltip.food_trait.brined': 'Brined',
    'tfc.tooltip.food_trait.pickled': 'Pickled',
    'tfc.tooltip.food_trait.preserved': 'Preserved',
    'tfc.tooltip.food_trait.vinegar': 'Preserved in Vinegar',
    'tfc.tooltip.food_trait.charcoal_grilled': 'Charcoal Grilled',
    'tfc.tooltip.food_trait.wood_grilled': 'Wood Grilled',
    'tfc.tooltip.food_trait.wild': 'Wild',
    'tfc.tooltip.food_trait.burnt_to_a_crisp': 'Burnt to a crisp!',
    'tfc.tooltip.item_melts_into': '§7Melts into %s mB of §f%s§7 (at %s§7)',
    'tfc.tooltip.fuel_burns_at': '§7Burns at §f%s§7 for §f%s',
    'tfc.tooltip.time_delta_hours_minutes': '%s:%s',
    'tfc.tooltip.time_delta_days': '%s day(s)',
    'tfc.tooltip.time_delta_months_days': '%s month(s) and %s day(s)',
    'tfc.tooltip.time_delta_years_months_days': '%s year(s), %s month(s) and %s day(s)',
    'tfc.tooltip.temperature_celsius': '%s\u00b0C',
    'tfc.tooltip.temperature_fahrenheit': '%s\u00b0F',
    'tfc.tooltip.temperature_rankine': '%s\u00b0R',
    'tfc.tooltip.temperature_kelvin': '%s K',
    'tfc.tooltip.fluid_units': '%s mB',
    'tfc.tooltip.fluid_units_of': '%s mB of %s',
    'tfc.tooltip.fluid_units_and_capacity': '%s / %s mB',
    'tfc.tooltip.fluid_units_and_capacity_of': '%s / %s mB of %s',
    'tfc.tooltip.less_than_one_fluid_units': '< 1 mB',
    'tfc.tooltip.farmland.mature': '§aMature',
    'tfc.tooltip.farmland.hydration': '§1Hydration: §r%s%%',
    'tfc.tooltip.farmland.hydration_too_low': ' - §4Too low! §r(>%s%%)',
    'tfc.tooltip.farmland.hydration_too_high': ' - §4Too high! §r(<%s%%)',
    'tfc.tooltip.farmland.temperature': '§4Temperature: §r%s\u00b0C',
    'tfc.tooltip.farmland.temperature_too_low': ' - §4Too low! §r(>%s\u00b0C)',
    'tfc.tooltip.farmland.temperature_too_high': ' - §4Too high! §r(<%s\u00b0C)',
    'tfc.tooltip.farmland.just_right': ' - §2Good§r',
    'tfc.tooltip.farmland.nutrients': '§b(N) Nitrogen: §r%s%%, §6(P) Phosphorus: §r%s%%, §d(K) Potassium: §r%s%%',
    'tfc.tooltip.fruit_tree.done_growing': 'This block is done growing',
    'tfc.tooltip.fruit_tree.growing': 'This block could grow under the right conditions.',
    'tfc.tooltip.fruit_tree.sapling_wrong_month': 'Wrong season to grow a tree.',
    'tfc.tooltip.fruit_tree.sapling_splice': 'May be spliced',
    'tfc.tooltip.berry_bush.not_underwater': 'Must be underwater to grow!',
    'tfc.tooltip.fertilizer.nitrogen': '§b(N) Nitrogen: §r%s%%',
    'tfc.tooltip.fertilizer.phosphorus': '§6(P) Phosphorus: §r%s%%',
    'tfc.tooltip.fertilizer.potassium': '§d(K) Potassium: §r%s%%',
    'tfc.tooltip.seal_barrel': 'Seal',
    'tfc.tooltip.unseal_barrel': 'Unseal',
    'tfc.tooltip.while_sealed': 'While sealed',
    'tfc.tooltip.while_sealed_description': 'While the barrel is sealed and the required fluid is present',
    'tfc.tooltip.windmill_not_enough_space': 'There is not enough space to place a windmill here!',
    'tfc.tooltip.anvil_is_too_low_tier_to_weld': 'The Anvil is not a high enough tier to weld that!',
    'tfc.tooltip.anvil_is_too_low_tier_to_work': 'The Anvil is not a high enough tier to work that!',
    'tfc.tooltip.not_hot_enough_to_weld': 'Not hot enough to weld!',
    'tfc.tooltip.not_hot_enough_to_work': 'Not hot enough to work!',
    'tfc.tooltip.no_flux_to_weld': 'There is no flux in the anvil!',
    'tfc.tooltip.hammer_required_to_work': 'A hammer is required to work in the anvil!',
    'tfc.tooltip.anvil_has_been_worked': 'Worked',
    'tfc.tooltip.blast_furnace_ore': 'Input: %d / %d',
    'tfc.tooltip.blast_furnace_fuel': 'Fuel: %d / %d',
    'tfc.tooltip.crucible_content_line': '  %s (§2%s%%§r)',
    'tfc.tooltip.fertilized': '§6Fertilized',
    'tfc.tooltip.egg_hatch': 'Will hatch in %s days',
    'tfc.tooltip.egg_hatch_today': 'Will hatch today!',
    'tfc.tooltip.fishing.bait': '§6Bait: ',
    'tfc.tooltip.animal.pregnant': 'This %s is pregnant!',
    'tfc.tooltip.animal.male_milk': 'This %s is a male.',
    'tfc.tooltip.animal.old': 'This %s is too old to produce.',
    'tfc.tooltip.animal.young': 'This %s is too young to produce.',
    'tfc.tooltip.animal.low_familiarity': 'This %s is not familiar enough to produce.',
    'tfc.tooltip.animal.no_milk': 'This %s has no milk.',
    'tfc.tooltip.animal.no_wool': 'This %s has no wool.',
    'tfc.tooltip.animal.horse_angry_overburdened': 'The horse kicked you off for putting too much weight on it!',
    'tfc.tooltip.animal.cannot_pluck': 'This animal cannot be plucked for %s',
    'tfc.tooltip.animal.cannot_pluck_old_or_sick': 'This animal is too worn out to be plucked.',
    'tfc.tooltip.scribing_table.missing_ink': 'Ink is missing!',
    'tfc.tooltip.scribing_table.invalid_ink': 'Item isn\'t ink!',
    'tfc.tooltip.deals_damage.slashing': '§7Deals §fSlashing§7 Damage',
    'tfc.tooltip.deals_damage.piercing': '§7Deals §fPiercing§7 Damage',
    'tfc.tooltip.deals_damage.crushing': '§7Deals §fCrushing§7 Damage',
    'tfc.tooltip.resists_damage': '§7Resistances: §fSlashing§r %s, §fPiercing§r %s, §fCrushing§r %s',
    'tfc.tooltip.immune_to_damage': 'Immune',
    'tfc.tooltip.pot_boiling': 'Boiling!',
    'tfc.tooltip.pot_finished': 'Finished',
    'tfc.tooltip.pot_ready': 'Ready',
    'tfc.tooltip.infestation': 'This container has a foul smell.',
    'tfc.tooltip.usable_in_pan': 'Can be processed with a pan',
    'tfc.tooltip.usable_in_sluice': 'Can be processed in a sluice',
    'tfc.tooltip.usable_in_sluice_and_pan': 'Can be processed with a sluice or pan',
    'tfc.tooltip.powderkeg.disabled': 'Powderkegs are disabled on this server!',
    'tfc.tooltip.glass.title': 'Glass Operations:',
    'tfc.tooltip.glass.not_hot_enough': 'The glass is not hot enough to manipulate.',
    'tfc.tooltip.glass.tool_description': '§7Performs §f%s',
    'tfc.tooltip.glass.silica': 'Silica Glass',
    'tfc.tooltip.glass.hematitic': 'Hematitic Glass',
    'tfc.tooltip.glass.olivine': 'Olivine Glass',
    'tfc.tooltip.glass.volcanic': 'Volcanic Glass',
    'tfc.tooltip.glass.flatten_me': 'Right click with a paddle to flatten',
    'tfc.tooltip.sealed': 'Sealed',
    'tfc.tooltip.unsealed': 'Unsealed',
    'tfc.tooltip.switch_sides': 'Switch Sides',
    'tfc.tooltip.legend': 'Legend',
    'tfc.tooltip.chance': '%s%% chance',
    'tfc.tooltip.wind_speed': '%s km/h, %s%% %s, %s%% %s',
    'tfc.tooltip.javelin.thrown_damage': '%s Thrown Damage',
    'tfc.tooltip.rotation.angular_velocity': 'Rotating at \u03c9=%s rad/s',
    'tfc.tooltip.sewing.dark_cloth': 'Dark Cloth',
    'tfc.tooltip.sewing.light_cloth': 'Light Cloth',
    'tfc.tooltip.sewing.stitch': 'Stitch',
    'tfc.tooltip.sewing.remove_stitch': 'Remove Stitch',
    'tfc.tooltip.sewing.select_recipe': 'Select Recipe',

    **dict(('trim_material.tfc.%s' % mat, lang('%s material', mat)) for mat in TRIM_MATERIALS),

    'tfc.jade.sealed_date': 'Sealed Date: %s',
    'tfc.jade.catalyst_stacks': '%sx Catalyst Stacks',
    'tfc.jade.input_stacks': '%sx Input Stacks',
    'tfc.jade.fuel_stacks': '%sx Fuel Stacks',
    'tfc.jade.straws': '%s Straw',
    'tfc.jade.logs': '%s Logs',
    'tfc.jade.creating': 'Creating %s',
    'tfc.jade.burn_rate': 'Burn Rate: %s ticks / mB',
    'tfc.jade.burn_forever': 'Will burn indefinitely',
    'tfc.jade.time_left': 'Time left: %s',
    'tfc.jade.ready_to_grow': 'Ready to Grow',
    'tfc.jade.animal_wear': 'Wear & Tear: %s',
    'tfc.jade.familiarity': 'Familiarity: %s',
    'tfc.jade.adulthood_progress': 'Becomes adult in %s',
    'tfc.jade.juvenile': 'Juvenile',
    'tfc.jade.animal_size': 'Size: %s',
    'tfc.jade.product.generic': 'Has Animal Product',
    'tfc.jade.product.eggs': 'Has Eggs',
    'tfc.jade.product.milk': 'Ready to Milk',
    'tfc.jade.product.wool': 'Ready to Shear',
    'tfc.jade.can_mate': 'Ready to Mate',
    'tfc.jade.old_animal': 'Old, cannot reproduce or provide useful products',
    'tfc.jade.gestation_time_left': 'Gestation Time Left: %s',
    'tfc.jade.may_ride_horse': 'May be ridden',
    'tfc.jade.explosion_strength': 'Explosion Strength: %s',
    'tfc.jade.yield': 'Yield Multiplier: %s%%',
    'tfc.jade.no_stick': 'Needs stick to reach max growth',
    'tfc.jade.variant_and_markings': '%s, %s',
    'tfc.jade.raining_mud_bricks': 'Raining, cannot start drying',
    'tfc.jade.dried_mud_bricks': 'Dried',
    'tfc.jade.mud_bricks_nearly_done': 'Almost dry',
    'tfc.jade.loom_progress': 'Weaving Progress: %s / %s making %s',
    'tfc.jade.squid_size': 'Size: %s',
    'tfc.jade.freshwater': 'Freshwater',
    'tfc.jade.saltwater': 'Saltwater',
    'tfc.jade.diurnal': 'Diurnal',
    'tfc.jade.nocturnal': 'Nocturnal',
    'tfc.jade.pack_respect': 'Pack Respect: %s',
    'tfc.jade.large_bait': 'Needs large fishing bait to catch',
    'tfc.jade.hooked': 'Hooked Entity: %s',
    'tfc.jade.bait': 'Attached Bait: %s',
    'tfc.jade.smoke_level': 'Smoke Level: %s / 4',
    **{'tfc.jade.bellows_%s' % i: 'W' + ('o' * (2 + i)) + 'sh' for i in range(1, 11)},

    'config.jade.plugin_tfc.barrel': 'Barrel',
    'config.jade.plugin_tfc.bellows': 'Bellows',
    'config.jade.plugin_tfc.sapling': 'Sapling',
    'config.jade.plugin_tfc.blast_furnace': 'Blast Furnace',
    'config.jade.plugin_tfc.bloomery': 'Bloomery',
    'config.jade.plugin_tfc.bloom': 'Bloom',
    'config.jade.plugin_tfc.charcoal_forge': 'Charcoal Forge',
    'config.jade.plugin_tfc.composter': 'Composter',
    'config.jade.plugin_tfc.crop': 'Crop',
    'config.jade.plugin_tfc.crucible': 'Crucible',
    'config.jade.plugin_tfc.firepit': 'Firepit',
    'config.jade.plugin_tfc.fruit_tree_sapling': 'Fruit Tree Sapling',
    'config.jade.plugin_tfc.hoe_overlay': 'Hoe Overlay',
    'config.jade.plugin_tfc.lamp': 'Lamp',
    'config.jade.plugin_tfc.nest_box': 'Nest Box',
    'config.jade.plugin_tfc.pit_kiln_internal': 'Pit Kiln',
    'config.jade.plugin_tfc.pit_kiln_above': 'Pit Kiln',
    'config.jade.plugin_tfc.powder_keg': 'Powder Keg',
    'config.jade.plugin_tfc.torch': 'Torch',
    'config.jade.plugin_tfc.wall_torch': 'Torch',
    'config.jade.plugin_tfc.candle': 'Candle',
    'config.jade.plugin_tfc.candle_cake': 'Candle Cake',
    'config.jade.plugin_tfc.jack_o_lantern': 'Jack O Lantern',
    'config.jade.plugin_tfc.mud_bricks': 'Mud Bricks',
    'config.jade.plugin_tfc.decaying': 'Decaying Block',
    'config.jade.plugin_tfc.loom': 'Loom',
    'config.jade.plugin_tfc.sheet_pile': 'Sheet Pile',
    'config.jade.plugin_tfc.ingot_pile': 'Ingot Pile',
    'config.jade.plugin_tfc.axle': 'Axle',
    'config.jade.plugin_tfc.encased_axle': 'Encased Axle',
    'config.jade.plugin_tfc.clutch': 'Clutch',
    'config.jade.plugin_tfc.hand_wheel': 'Hand Wheel',
    'config.jade.plugin_tfc.gearbox': 'Gearbox',
    'config.jade.plugin_tfc.crankshaft': 'Crankshaft',
    'config.jade.plugin_tfc.quern': 'Quern',
    'config.jade.plugin_tfc.water_wheel': 'Water Wheel',
    'config.jade.plugin_tfc.windmill': 'Windmill',
    'config.jade.plugin_tfc.hot_poured_glass': 'Hot Poured Glass',

    'config.jade.plugin_tfc.animal': 'Animal',
    'config.jade.plugin_tfc.frog': 'Frog',
    'config.jade.plugin_tfc.horse': 'Horse',
    'config.jade.plugin_tfc.chested_horse': 'Chested Horse',
    'config.jade.plugin_tfc.wild_animal': 'Wild Animal',
    'config.jade.plugin_tfc.squid': 'Squid',
    'config.jade.plugin_tfc.fish': 'Fish',
    'config.jade.plugin_tfc.predator': 'Predator',
    'config.jade.plugin_tfc.pack_predator': 'Pack Predator',
    'config.jade.plugin_tfc.ocelot': 'Ocelot',
    'config.jade.plugin_tfc.rabbit': 'Rabbit',
    'config.jade.plugin_tfc.fishing_hook': 'Fishing Hook',


    # Commands

    'tfc.commands.time.query.daytime': 'The day time is %s',
    'tfc.commands.time.query.game_time': 'The game time is %s',
    'tfc.commands.time.query.day': 'The day is %s',
    'tfc.commands.time.query.player_ticks': 'The player ticks is %s',
    'tfc.commands.time.query.calendar_ticks': 'The calendar ticks is %s',
    'tfc.commands.heat.set_heat': 'Held item heat set to %s',
    'tfc.commands.clear_world.starting': 'Clearing world. Prepare for lag...',
    'tfc.commands.clear_world.done': 'Cleared %d Block(s).',
    'tfc.commands.count_block.done': 'Found %d',
    'tfc.commands.player.query_hunger': 'Hunger is %s / 20',
    'tfc.commands.player.query_saturation': 'Saturation is %s / 20',
    'tfc.commands.player.query_water': 'Water is %s / 100',
    'tfc.commands.player.query_nutrition': 'Player nutrition:',
    'tfc.commands.player.fail_invalid_food_stats': 'Player does not have any TFC nutrition or hydration data',
    'tfc.commands.locate.unknown_vein': 'Unknown vein: %s',
    'tfc.commands.locate.vein_not_found': 'Unable to find vein %s within reasonable distance (16 chunks radius)',
    'tfc.commands.locate.invalid_biome_source': 'This world does not have a compatible biome source',
    'tfc.commands.locate.volcano_not_found': 'Could not find a volcano within reasonable distance',
    'tfc.commands.propick.found_blocks': 'The propick scan found %s %s',
    'tfc.commands.propick.cleared': 'Cleared %s blocks, Found %s prospectable blocks',
    'tfc.commands.particle.no_fluid': 'Unknown Fluid: %s',
    'tfc.commands.trim.not_applied': 'A trim cannot be applied to this item',
    'tfc.commands.trim.not_armor': 'The metal specified does not have armor items',
    'tfc.commands.trim.bad_material': 'Material item not recognized',
    'tfc.commands.trim.bad_template': 'Template item not recognized',

    # Create World Screen Options
    'tfc.settings.km': '%s km',
    'generator.tfc.overworld': 'TerraFirmaCraft',
    'tfc.tooltip.create_world.title': 'TerraFirmaCraft World Settings',
    'tfc.create_world.flat_bedrock': 'Flat Bedrock',
    'tfc.create_world.spawn_distance': 'Spawn Distance',
    'tfc.create_world.spawn_distance.tooltip': 'Radial distance from the spawn center that the world spawn point can be.',
    'tfc.create_world.spawn_center_x': 'Spawn Center X',
    'tfc.create_world.spawn_center_x.tooltip': 'The midpoint of x positions that the world spawn can be.',
    'tfc.create_world.spawn_center_z': 'Spawn Center Z',
    'tfc.create_world.spawn_center_z.tooltip': 'The midpoint of z positions that the world spawn can be.',
    'tfc.create_world.temperature_scale': 'Temperature Scale',
    'tfc.create_world.temperature_scale.tooltip': 'The distance between temperature peaks / poles / extremes.',
    'tfc.create_world.rainfall_scale': 'Rainfall Scale',
    'tfc.create_world.rainfall_scale.tooltip': 'The distance between rainfall peaks / poles / extremes.',
    'tfc.create_world.temperature_constant': 'Constant Temperature',
    'tfc.create_world.temperature_constant.tooltip': 'The relative constant temperature of a world.',
    'tfc.create_world.rainfall_constant': 'Constant Rainfall',
    'tfc.create_world.rainfall_constant.tooltip': 'The relative constant rainfall of a world.',
    'tfc.create_world.continentalness': 'Continentalness',
    'tfc.create_world.continentalness.tooltip': 'The proportion of the world that is made up of land rather than water',
    'tfc.create_world.grass_density': 'Grass Density',
    'tfc.create_world.grass_density.tooltip': 'Multiplier that applies to the amount of short and tall grass placed within a chunk.',

    # Entities
    **dict(('entity.tfc.%s' % fish, lang(fish)) for fish in SIMPLE_FRESHWATER_FISH),
    'entity.tfc.cod': 'Cod',
    'entity.tfc.pufferfish': 'Pufferfish',
    'entity.tfc.tropical_fish': 'Tropical Fish',
    'entity.tfc.jellyfish': 'Jellyfish',
    'entity.tfc.manatee': 'Manatee',
    'entity.tfc.orca': 'Orca',
    'entity.tfc.dolphin': 'Dolphin',
    'entity.tfc.isopod': 'Isopod',
    'entity.tfc.lobster': 'Lobster',
    'entity.tfc.crayfish': 'Crayfish',
    'entity.tfc.horseshoe_crab': 'Horseshoe Crab',
    'entity.tfc.penguin': 'Penguin',
    'entity.tfc.frog': 'Frog',
    'entity.tfc.turtle': 'Turtle',
    'entity.tfc.pig': 'Pig',
    'entity.tfc.pig.male': 'Pig',
    'entity.tfc.pig.female': 'Sow',
    'entity.tfc.cow': 'Cow',
    'entity.tfc.cow.female': 'Cow',
    'entity.tfc.cow.male': 'Bull',
    'entity.tfc.goat': 'Goat',
    'entity.tfc.goat.female': 'Nanny Goat',
    'entity.tfc.goat.male': 'Billy Goat',
    'entity.tfc.alpaca': 'Alpaca',
    'entity.tfc.alpaca.female': 'Female Alpaca',
    'entity.tfc.alpaca.male': 'Male Alpaca',
    'entity.tfc.sheep': 'Sheep',
    'entity.tfc.sheep.female': 'Ewe',
    'entity.tfc.sheep.male': 'Ram',
    'entity.tfc.musk_ox': 'Musk Ox',
    'entity.tfc.musk_ox.female': 'Musk Ox Cow',
    'entity.tfc.musk_ox.male': 'Musk Ox Bull',
    'entity.tfc.yak': 'Yak',
    'entity.tfc.yak.female': 'Female Yak',
    'entity.tfc.yak.male': 'Male Yak',
    'entity.tfc.polar_bear': 'Polar Bear',
    'entity.tfc.grizzly_bear': 'Grizzly Bear',
    'entity.tfc.black_bear': 'Black Bear',
    'entity.tfc.cougar': 'Cougar',
    'entity.tfc.panther': 'Panther',
    'entity.tfc.lion': 'Lion',
    'entity.tfc.sabertooth': 'Sabertooth',
    'entity.tfc.tiger': 'Tiger',
    'entity.tfc.crocodile': 'Crocodile',
    'entity.tfc.falling_block': 'Falling Block',
    'entity.tfc.fishing_bobber': 'Fishing Bobber',
    'entity.tfc.chest_minecart': 'Chest Minecart',
    'entity.tfc.holding_minecart': 'Holding Minecart',
    'entity.tfc.squid': 'Squid',
    'entity.tfc.octopoteuthis': 'Octopoteuthis',
    'entity.tfc.glow_arrow': 'Glowing Arrow',
    'entity.tfc.thrown_javelin': 'Javelin',
    'entity.tfc.seat': 'Seat',
    'entity.tfc.chicken': 'Chicken',
    'entity.tfc.chicken.male': 'Rooster',
    'entity.tfc.chicken.female': 'Chicken',
    'entity.tfc.duck': 'Duck',
    'entity.tfc.duck.male': 'Drake',
    'entity.tfc.duck.female': 'Duck',
    'entity.tfc.quail': 'Quail',
    'entity.tfc.quail.male': 'Male Quail',
    'entity.tfc.quail.female': 'Female Quail',
    'entity.tfc.rabbit': 'Rabbit',
    'entity.tfc.fox': 'Fox',
    'entity.tfc.panda': 'Panda',
    'entity.tfc.boar': 'Boar',
    'entity.tfc.wildebeest': 'Wildebeest',
    'entity.tfc.ocelot': 'Ocelot',
    'entity.tfc.bongo': 'Bongo',
    'entity.tfc.caribou': 'Caribou',
    'entity.tfc.deer': 'Deer',
    'entity.tfc.gazelle': 'Gazelle',
    'entity.tfc.moose': 'Moose',
    'entity.tfc.grouse': 'Grouse',
    'entity.tfc.pheasant': 'Pheasant',
    'entity.tfc.turkey': 'Turkey',
    'entity.tfc.peafowl': 'Peafowl',
    'entity.tfc.peafowl.male': 'Peacock',
    'entity.tfc.peafowl.female': 'Peahen',
    'entity.tfc.rat': 'Rat',
    'entity.tfc.cat': 'Cat',
    'entity.tfc.cat.female': 'Female Cat',
    'entity.tfc.cat.male': 'Male Cat',
    'entity.tfc.dog': 'Dog',
    'entity.tfc.dog.male': 'Male Dog',
    'entity.tfc.dog.female': 'Female Dog',
    'entity.tfc.wolf': 'Wolf',
    'entity.tfc.hyena': 'Hyena',
    'entity.tfc.direwolf': 'Direwolf',
    'entity.tfc.mule': 'Mule',
    'entity.tfc.mule.male': 'Mule',
    'entity.tfc.mule.female': 'Mule',
    'entity.tfc.donkey': 'Donkey',
    'entity.tfc.donkey.male': 'Jack Donkey',
    'entity.tfc.donkey.female': 'Jenny Donkey',
    'entity.tfc.horse': 'Horse',
    'entity.tfc.horse.male': 'Stallion',
    'entity.tfc.horse.female': 'Mare',
    **{'entity.tfc.boat.%s' % wood: lang('%s boat', wood) for wood in WOODS.keys()},
    **{'entity.tfc.chest_boat.%s' % wood: lang('%s boat with chest', wood) for wood in WOODS.keys()},

    # Enums

    **dict(('tfc.enum.tier.tier_%s' % tier, 'Tier %s' % tier.upper()) for tier in ('0', 'i', 'ii', 'iii', 'iv', 'v', 'vi')),
    **lang_enum('heat', ('warming', 'hot', 'very_hot', 'faint_red', 'dark_red', 'bright_red', 'orange', 'yellow', 'yellow_white', 'white', 'brilliant_white')),
    **lang_enum('month', ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')),
    **lang_enum('day', ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')),
    **lang_enum('foresttype', ('sparse', 'old_growth', 'normal', 'edge', 'none')),
    **lang_enum('koppenclimateclassification', ('arctic', 'tundra', 'humid_subarctic', 'subarctic', 'cold_desert', 'hot_desert', 'temperate', 'subtropical', 'humid_subtropical', 'humid_oceanic', 'humid_subtropical', 'tropical_savanna', 'tropical_rainforest')),
    **lang_enum('direction', ('north', 'south', 'east', 'west', 'down', 'up')),
    'tfc.enum.season.january': 'Winter',
    'tfc.enum.season.february': 'Late Winter',
    'tfc.enum.season.march': 'Early Spring',
    'tfc.enum.season.april': 'Spring',
    'tfc.enum.season.may': 'Late Spring',
    'tfc.enum.season.june': 'Early Summer',
    'tfc.enum.season.july': 'Summer',
    'tfc.enum.season.august': 'Late Summer',
    'tfc.enum.season.september': 'Early Autumn',
    'tfc.enum.season.october': 'Autumn',
    'tfc.enum.season.november': 'Late Autumn',
    'tfc.enum.season.december': 'Early Winter',
    'tfc.enum.gender.male': 'Male',
    'tfc.enum.gender.female': 'Female',
    'tfc.enum.horse_variant.white': 'White Variant',
    'tfc.enum.horse_variant.creamy': 'Creamy Variant',
    'tfc.enum.horse_variant.chestnut': 'Chestnut Variant',
    'tfc.enum.horse_variant.brown': 'Brown Variant',
    'tfc.enum.horse_variant.black': 'Black Variant',
    'tfc.enum.horse_variant.gray': 'Gray Variant',
    'tfc.enum.horse_variant.dark_brown': 'Dark Brown',
    'tfc.enum.markings.none': 'No Markings',
    'tfc.enum.markings.white': 'White Markings',
    'tfc.enum.markings.white_field': 'White Field Markings',
    'tfc.enum.markings.white_dots': 'White Dot Markings',
    'tfc.enum.markings.black_dots': 'Black Dot Markings',
    'tfc.enum.size.tiny': 'Tiny',
    'tfc.enum.size.very_small': 'Very Small',
    'tfc.enum.size.small': 'Small',
    'tfc.enum.size.normal': 'Normal',
    'tfc.enum.size.large': 'Large',
    'tfc.enum.size.very_large': 'Very Large',
    'tfc.enum.size.huge': 'Huge',
    'tfc.enum.weight.very_light': 'Very Light',
    'tfc.enum.weight.light': 'Light',
    'tfc.enum.weight.medium': 'Medium',
    'tfc.enum.weight.heavy': 'Heavy',
    'tfc.enum.weight.very_heavy': 'Very Heavy',
    'tfc.enum.nutrient.grain': 'Grain',
    'tfc.enum.nutrient.fruit': 'Fruit',
    'tfc.enum.nutrient.vegetables': 'Vegetables',
    'tfc.enum.nutrient.protein': 'Protein',
    'tfc.enum.nutrient.dairy': 'Dairy',
    'tfc.enum.forgingbonus.none': 'No Forging Bonus',
    'tfc.enum.forgingbonus.modestly_forged': 'Modestly Forged',
    'tfc.enum.forgingbonus.well_forged': 'Well Forged',
    'tfc.enum.forgingbonus.expertly_forged': 'Expertly Forged',
    'tfc.enum.forgingbonus.perfectly_forged': 'Perfectly Forged!',
    'tfc.enum.forgestep.hit': 'Hit',
    'tfc.enum.forgestep.hit_light': 'Light Hit',
    'tfc.enum.forgestep.hit_medium': 'Medium Hit',
    'tfc.enum.forgestep.hit_hard': 'Hard Hit',
    'tfc.enum.forgestep.draw': 'Draw',
    'tfc.enum.forgestep.punch': 'Punch',
    'tfc.enum.forgestep.bend': 'Bend',
    'tfc.enum.forgestep.upset': 'Upset',
    'tfc.enum.forgestep.shrink': 'Shrink',
    'tfc.enum.order.any': 'Any',
    'tfc.enum.order.last': 'Last',
    'tfc.enum.order.not_last': 'Not Last',
    'tfc.enum.order.second_last': 'Second Last',
    'tfc.enum.order.third_last': 'Third Last',
    'tfc.enum.glassoperation.blow': 'Blow',
    'tfc.enum.glassoperation.roll': 'Roll',
    'tfc.enum.glassoperation.stretch': 'Stretch',
    'tfc.enum.glassoperation.pinch': 'Pinch',
    'tfc.enum.glassoperation.flatten': 'Flatten',
    'tfc.enum.glassoperation.saw': 'Saw',
    'tfc.enum.glassoperation.amethyst': 'Amethyst Powder',
    'tfc.enum.glassoperation.soda_ash': 'Soda Ash',
    'tfc.enum.glassoperation.sulfur': 'Sulfur',
    'tfc.enum.glassoperation.iron': 'Iron Powder',
    'tfc.enum.glassoperation.ruby': 'Ruby Powder',
    'tfc.enum.glassoperation.lapis_lazuli': 'Lapis Powder',
    'tfc.enum.glassoperation.pyrite': 'Pyrite Powder',
    'tfc.enum.glassoperation.sapphire': 'Sapphire Powder',
    'tfc.enum.glassoperation.gold': 'Gold Powder',
    'tfc.enum.glassoperation.graphite': 'Graphite Powder',
    'tfc.enum.glassoperation.copper': 'Copper Powder',
    'tfc.enum.glassoperation.nickel': 'Nickel Powder',
    'tfc.enum.glassoperation.tin': 'Tin Powder',
    'tfc.enum.glassoperation.silver': 'Silver Powder',
    'tfc.enum.glassoperation.table_pour': 'Table Pour',
    'tfc.enum.glassoperation.basin_pour': 'Basin Pour',
    'tfc.enum.command.relax': 'Relax',
    'tfc.enum.command.home': 'We\'re Home',
    'tfc.enum.command.sit': 'Sit',
    'tfc.enum.command.follow': 'Follow Me',
    'tfc.enum.command.hunt': 'Hunt With Me',
    'tfc.enum.command.relax.tooltip': 'The animal will wander around its home.',
    'tfc.enum.command.home.tooltip': 'Tells the animal to recognize this location as home.',
    'tfc.enum.command.sit.tooltip': 'The animal will sit for a while, but not forever.',
    'tfc.enum.command.follow.tooltip': 'The animal will follow you, but not try to aid in combat.',
    'tfc.enum.command.hunt.tooltip': 'The animal will follow you and engage in combat.',
    'tfc.pet.not_owner': 'You are not its owner, this pet will not obey your commands!',
    'tfc.pet.will_not_listen': 'It ignores your command.',
    'tfc.enum.rabbit_variant.brown': 'Brown Fur',
    'tfc.enum.rabbit_variant.white': 'White Fur',
    'tfc.enum.rabbit_variant.black': 'Black Fur',
    'tfc.enum.rabbit_variant.white_splotched': 'White Splotched Fur',
    'tfc.enum.rabbit_variant.gold': 'Golden Fur',
    'tfc.enum.rabbit_variant.salt': 'Salty Fur',
    'tfc.enum.rabbit_variant.evil': '§cEvil',
    'tfc.enum.rockcategory.igneous_intrusive': 'Igneous Intrusive',
    'tfc.enum.rockcategory.igneous_extrusive': 'Igneous Extrusive',
    'tfc.enum.rockcategory.sedimentary': 'Sedimentary',
    'tfc.enum.rockcategory.metamorphic': 'Metamorphic',
    'tfc.enum.rockdisplaycategory.mafic_igneous_intrusive': 'Mafic Igneous Intrusive',
    'tfc.enum.rockdisplaycategory.intermediate_igneous_intrusive': 'Igneous Intrusive',
    'tfc.enum.rockdisplaycategory.felsic_igneous_intrusive': 'Felsic Igneous Intrusive',
    'tfc.enum.rockdisplaycategory.mafic_igneous_extrusive': 'Igneous Extrusive',
    'tfc.enum.rockdisplaycategory.intermediate_igneous_extrusive': 'Igneous Extrusive',
    'tfc.enum.rockdisplaycategory.felsic_igneous_extrusive': 'Igneous Extrusive',
    'tfc.enum.rockdisplaycategory.sedimentary': 'Sedimentary',
    'tfc.enum.rockdisplaycategory.metamorphic': 'Metamorphic',

    'tfc.thatch_bed.use_no_sleep_no_spawn': 'This bed is too uncomfortable to sleep in.',
    'tfc.thatch_bed.use_sleep_no_spawn': 'This bed does not allow you to set your spawn.',
    'tfc.thatch_bed.use_no_sleep_spawn': 'This bed is too uncomfortable to sleep in, but your spawn point was set.',
    'tfc.thatch_bed.use_sleep_spawn': 'Spawn point set.',
    'tfc.thatch_bed.thundering': 'You are too scared to sleep.',
    'tfc.composter.rotten': 'This composter is smelly and might attract animals. You should empty it.',
    'tfc.composter.too_many_greens': 'This composter has enough green items',
    'tfc.composter.too_many_browns': 'This composter has enough brown items',
    'tfc.composter.green_items': '%s Green Items',
    'tfc.composter.brown_items': '%s Brown Items',
    'tfc.chisel.cannot_place': 'The chiseled version of this block cannot exist here',
    'tfc.chisel.no_recipe': 'This block cannot be chiseled',
    'tfc.chisel.bad_fluid': 'The chiseled version of this block cannot contain the fluid here',
    'tfc.fishing.no_bait': 'This fishing rod needs bait!',
    'tfc.fishing.pulled_too_hard': 'You pulled too hard, and the fish got away with the bait.',
    'painting.tfc.golden_field.title': 'Golden Field',
    'painting.tfc.golden_field.author': 'EERussianguy',
    'painting.tfc.hot_spring.title': 'Spring Dream',
    'painting.tfc.hot_spring.author': 'EERussianguy',
    'painting.tfc.volcano.title': 'Magma Rising',
    'painting.tfc.volcano.author': 'EERussianguy',
    'painting.tfc.supports.title': 'Endless Mineshaft',
    'painting.tfc.supports.author': 'Facu',
    'painting.tfc.lake.title': 'Lake',
    'painting.tfc.lake.author': 'Pxlsamosa',
    **dict(('metal.tfc.%s' % metal, lang(metal)) for metal in METALS.keys()),

    'tfc.jei.heating': 'Heating Recipe',
    'tfc.jei.quern': 'Quern Recipe',
    'tfc.jei.scraping': 'Scraping Recipe',
    'tfc.jei.clay_knapping': 'Clay Knapping Recipe',
    'tfc.jei.fire_clay_knapping': 'Fire Clay Knapping Recipe',
    'tfc.jei.leather_knapping': 'Leather Knapping Recipe',
    'tfc.jei.rock_knapping': 'Rock Knapping Recipe',
    'tfc.jei.goat_horn_knapping': 'Goat Horn Knapping Recipe',
    'tfc.jei.soup_pot': 'Soup Pot',
    'tfc.jei.simple_pot': 'Pot',
    'tfc.jei.jam_pot': 'Jam Pot',
    'tfc.jei.casting': 'Casting',
    'tfc.jei.alloying': 'Alloying',
    'tfc.jei.loom': 'Loom',
    'tfc.jei.glassworking': 'Glassworking',
    'tfc.jei.blast_furnace': 'Blast Furnace',
    'tfc.jei.instant_barrel': 'Instant Barrel Recipe',
    'tfc.jei.instant_fluid_barrel': 'Instant Fluid Barrel Recipe',
    'tfc.jei.sealed_barrel': 'Sealed Barrel Recipe',
    'tfc.jei.bloomery': 'Bloomery',
    'tfc.jei.welding': 'Welding',
    'tfc.jei.anvil': 'Anvil',
    'tfc.jei.chisel': 'Chisel',
    'tfc.jei.sewing': 'Sewing',

    'tfc.field_guide.book_name': 'TerraFirmaCraft',
    'tfc.field_guide.book_landing_text': 'Welcome traveller! This book will be the source of all you need to know as you explore the world of TerraFirmaCraft (TFC).'
}

# Automatically Generated by generate_trees.py
TREE_SAPLING_DROP_CHANCES = {
    'acacia': 0.0292,
    'ash': 0.0428,
    'aspen': 0.0428,
    'birch': 0.0311,
    'blackwood': 0.0780,
    'chestnut': 0.0112,
    'douglas_fir': 0.0132,
    'hickory': 0.0140,
    'kapok': 0.0115,
    'mangrove': 0.0447,
    'maple': 0.0201,
    'oak': 0.0130,
    'palm': 0.0911,
    'pine': 0.0248,
    'rosewood': 0.0193,
    'sequoia': 0.0238,
    'spruce': 0.0318,
    'sycamore': 0.0175,
    'white_cedar': 0.0318,
    'willow': 0.0143,
}

def entity_damage_resistance(rm: ResourceManager, name_parts: ResourceIdentifier, entity_tag: str, piercing: int = 0, slashing: int = 0, crushing: int = 0):
    rm.data(('tfc', 'entity_damage_resistances', name_parts), {
        'entity': entity_tag,
        'piercing': piercing,
        'slashing': slashing,
        'crushing': crushing
    })

def item_damage_resistance(rm: ResourceManager, name_parts: ResourceIdentifier, item: utils.Json, piercing: int = 0, slashing: int = 0, crushing: int = 0):
    rm.data(('tfc', 'item_damage_resistances', name_parts), {
        'ingredient': utils.ingredient(item),
        'piercing': piercing,
        'slashing': slashing,
        'crushing': crushing
    })

def mob_loot(rm: ResourceManager, name: str, drop: str, min_amount: int = 1, max_amount: int = None, hide_size: str = None, hide_chance: float = 1, bones: int = 0, extra_pool: Dict[str, Any] = None, livestock: bool = False, not_predated: bool = False, killed_by_player: bool = False):
    func = None if max_amount is None else loot_tables.set_count(min_amount, max_amount)
    if not_predated:
        conditions = [{'condition': 'tfc:not_predated'}]
    elif killed_by_player:
        conditions = [{'condition': 'minecraft:killed_by_player'}]
    else:
        conditions = None
    pools = [{'name': drop, 'functions': func, 'conditions': conditions}]
    if livestock:
        pools = [{'name': drop, 'functions': animal_yield(min_amount, (max(1, max_amount - 3), max_amount + 3))}]
    if hide_size is not None:
        func = None if hide_chance == 1 else loot_tables.random_chance(hide_chance)
        pools.append({'name': 'tfc:%s_raw_hide' % hide_size, 'conditions': func})
    if bones != 0:
        pools.append({'name': 'minecraft:bone', 'functions': loot_tables.set_count(1, bones)})
    if extra_pool is not None:
        pools.append(extra_pool)
    rm.entity_loot(name, *pools)

def animal_yield(lo: int, hi: Tuple[int, int]) -> utils.Json:
    return {
        'function': 'minecraft:set_count',
        'count': {
            'type': 'tfc:animal_yield',
            'min': lo,
            'max': {
                'type': 'minecraft:uniform',
                'min': hi[0],
                'max': hi[1]
            }
        }
    }

def lamp_fuel(rm: ResourceManager, name: str, fluid: str, burn_rate: int, valid_lamps: str = '#tfc:lamps'):
    rm.data(('tfc', 'lamp_fuels', name), {
        'fluid': fluid,
        'burn_rate': burn_rate,
        # This is a block ingredient, not an ingredient
        'valid_lamps': {'type': 'tfc:tag', 'tag': valid_lamps.replace('#', '')} if '#' in valid_lamps else valid_lamps
    })

def fertilizer(rm: ResourceManager, name: str, ingredient: str, n: float = None, p: float = None, k: float = None):
    rm.data(('tfc', 'fertilizers', name), {
        'ingredient': utils.ingredient(ingredient),
        'nitrogen': n,
        'potassium': k,
        'phosphorus': p
    })


def climate_config(min_temp: Optional[float] = None, max_temp: Optional[float] = None, min_rain: Optional[float] = None, max_rain: Optional[float] = None, needs_forest: Optional[bool] = False, fuzzy: Optional[bool] = None, min_forest: Optional[str] = None, max_forest: Optional[str] = None) -> Dict[str, Any]:
    return {
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'min_rainfall': min_rain,
        'max_rainfall': max_rain,
        'min_forest': 'normal' if needs_forest else min_forest,
        'max_forest': max_forest,
        'fuzzy': fuzzy
    }


def fauna(chance: int = None, distance_below_sea_level: int = None, climate: Dict[str, Any] = None, solid_ground: bool = None, max_brightness: int = None) -> Dict[str, Any]:
    return {
        'chance': chance,
        'distance_below_sea_level': distance_below_sea_level,
        'climate': climate,
        'solid_ground': solid_ground,
        'max_brightness': max_brightness
    }


def food_item(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, category: Category, hunger: int, saturation: float, water: int, decay: float, fruit: Optional[float] = None, veg: Optional[float] = None, protein: Optional[float] = None, grain: Optional[float] = None, dairy: Optional[float] = None):
    rm.item_tag('tfc:foods', ingredient)
    rm.data(('tfc', 'food_items', name_parts), {
        'ingredient': utils.ingredient(ingredient),
        'hunger': hunger,
        'saturation': saturation,
        'water': water if water != 0 else None,
        'decay_modifier': decay,
        'fruit': fruit,
        'vegetables': veg,
        'protein': protein,
        'grain': grain,
        'dairy': dairy
    })
    rm.item_tag('foods', ingredient)
    if category in (Category.fruit, Category.vegetable):
        rm.item_tag('foods/%ss' % category.name.lower(), ingredient)
    if category in (Category.meat, Category.cooked_meat):
        rm.item_tag('foods/meats', ingredient)
        if category == Category.cooked_meat:
            rm.item_tag('foods/cooked_meats', ingredient)
        else:
            rm.item_tag('foods/raw_meats', ingredient)
    if category == Category.dairy:
        rm.item_tag('foods/dairy', ingredient)

def dynamic_food_item(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, handler_type: str):
    rm.item_tag('foods', ingredient)
    rm.data(('tfc', 'food_items', name_parts), {
        'ingredient': utils.ingredient(ingredient),
        'type': handler_type
    })

def drinkable(rm: ResourceManager, name_parts: utils.ResourceIdentifier, fluid: utils.Json, thirst: Optional[int] = None, intoxication: Optional[int] = None, effects: Optional[utils.Json] = None, food: Optional[utils.Json] = None, allow_full: bool = None):
    rm.data(('tfc', 'drinkables', name_parts), {
        'ingredient': fluid_ingredient(fluid),
        'thirst': thirst,
        'intoxication': intoxication,
        'effects': effects,
        'food': food,
        'may_drink_when_full': allow_full,
    })

def damage_type(rm: ResourceManager, name_parts: utils.ResourceIdentifier, message_id: str = None, exhaustion: float = 0.0, scaling: str = 'when_caused_by_living_non_player', effects: str = None, message_type: str = None):
    rm.data(('damage_type', name_parts), {
        'message_id': message_id if message_id is not None else 'tfc.' + name_parts,
        'exhaustion': exhaustion,
        'scaling': scaling,
        'effects': effects,
        'death_message_type': message_type
    })

def item_size(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, size: Size, weight: Weight):
    rm.data(('tfc', 'item_sizes', name_parts), {
        'ingredient': utils.ingredient(ingredient),
        'size': size.name,
        'weight': weight.name
    })


def item_heat(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, heat_capacity: float, melt_temperature: Optional[float] = None, mb: Optional[int] = None):
    if melt_temperature is not None:
        forging_temperature = round(melt_temperature * 0.6)
        welding_temperature = round(melt_temperature * 0.8)
    else:
        forging_temperature = welding_temperature = None
    if mb is not None:
        # Interpret heat capacity as a specific heat capacity - so we need to scale by the mB present. Baseline is 100 mB (an ingot)
        # Higher mB = higher heat capacity = heats and cools slower = consumes proportionally more fuel
        heat_capacity = round(10 * heat_capacity * mb) / 1000
    rm.data(('tfc', 'item_heats', name_parts), {
        'ingredient': utils.ingredient(ingredient),
        'heat_capacity': heat_capacity,
        'forging_temperature': forging_temperature,
        'welding_temperature': welding_temperature
    })


def fuel_item(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, duration: int, temperature: float, purity: float = None):
    rm.data(('tfc', 'fuels', name_parts), {
        'ingredient': utils.ingredient(ingredient),
        'duration': duration,
        'temperature': temperature,
        'purity': purity,
    })


def panning(rm: ResourceManager, name_parts: utils.ResourceIdentifier, block: utils.Json, models: List[str], loot_table: str):
    rm.data(('tfc', 'panning', name_parts), {
        'ingredient': block,
        'model_stages': models,
        'loot_table': loot_table
    })


def sluicing(rm: ResourceManager, name_parts: utils.ResourceIdentifier, block: utils.Json, loot_table: str):
    rm.data(('tfc', 'sluicing', name_parts), {
        'ingredient': utils.ingredient(block),
        'loot_table': loot_table
    })


def trim_material(rm: ResourceManager, name: str, color: str, ingredient: str, item_model_index: float):
    rm.data(('trim_material', name), {
        'asset_name': name + '_' + rm.domain,  # this field is not properly namespaced, so we have to do that ourselves
        'description': {
            'color': color,
            'translate': 'trim_material.%s.%s' % (rm.domain, name)
        },
        'ingredient': ingredient,
        'item_model_index': item_model_index
    })
    rm.item_tag('tfc:trim_materials', ingredient)

def climate_range(rm: ResourceManager, name_parts: utils.ResourceIdentifier, hydration: Tuple[int, int, int] = None, temperature: Tuple[float, float, float] = None):
    data = {}
    if hydration is not None:
        data.update({'min_hydration': hydration[0], 'max_hydration': hydration[1], 'hydration_wiggle_range': hydration[2]})
    if temperature is not None:
        data.update({'min_temperature': temperature[0], 'max_temperature': temperature[1], 'temperature_wiggle_range': temperature[2]})
    rm.data(('tfc', 'climate_ranges', name_parts), data)


def hydration_from_rainfall(rainfall: float) -> int:
    return int(rainfall) * 60 // 500


def block_and_item_tag(rm: ResourceManager, name_parts: utils.ResourceIdentifier, *values: utils.ResourceIdentifier, replace: bool = False):
    rm.block_tag(name_parts, *values, replace=replace)
    rm.item_tag(name_parts, *values, replace=replace)
    
def simple_pot_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredients: Json, fluid: str, output_fluid: str = None, output_items: Json = None, duration: int = 2000, temp: int = 300):
    rm.recipe(('pot', name_parts), 'tfc:pot', {
        'ingredients': ingredients,
        'fluid_ingredient': fluid_stack_ingredient(fluid),
        'duration': duration,
        'temperature': temp,
        'fluid_output': fluid_stack(output_fluid) if output_fluid is not None else None,
        'item_output': [utils.item_stack(item) for item in output_items] if output_items is not None else None
    })


def disable_recipe(rm: ResourceManager, name_parts: ResourceIdentifier):
    # noinspection PyTypeChecker
    rm.recipe(name_parts, None, {}, conditions='forge:false')


def collapse_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient, result: Optional[utils.Json] = None, copy_input: Optional[bool] = None):
    assert result is not None or copy_input
    rm.recipe(('collapse', name_parts), 'tfc:collapse', {
        'ingredient': ingredient,
        'result': result,
        'copy_input': copy_input
    })


def landslide_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, result: utils.Json):
    rm.recipe(('landslide', name_parts), 'tfc:landslide', {
        'ingredient': ingredient,
        'result': result
    })

def chisel_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: utils.Json, result: str, mode: str):
    rm.recipe(('chisel', mode, name_parts), 'tfc:chisel', {
        'ingredient': ingredient,
        'result': result,
        'mode': mode,
        'extra_drop': item_stack_provider(result) if mode == 'slab' else None
    })

def stone_cutting(rm: ResourceManager, name_parts: utils.ResourceIdentifier, item: str, result: str, count: int = 1) -> RecipeContext:
    return rm.recipe(('stonecutting', name_parts), 'minecraft:stonecutting', {
        'ingredient': utils.ingredient(item),
        'result': result,
        'count': count
    })

def no_remainder_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: Json, group: str = None, conditions: utils.Json = None) -> RecipeContext:
    return delegate_recipe(rm, name_parts, 'tfc:no_remainder_shapeless_crafting', {
        'type': 'minecraft:crafting_shapeless',
        'group': group,
        'ingredients': utils.item_stack_list(ingredients),
        'result': utils.item_stack(result),
        'conditions': utils.recipe_condition(conditions)
    })

def no_remainder_shaped(rm: ResourceManager, name_parts: utils.ResourceIdentifier, pattern: Sequence[str], ingredients: Json, result: Json, group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    return delegate_recipe(rm, name_parts, 'tfc:no_remainder_shaped_crafting', {
        'type': 'minecraft:crafting_shaped',
        'group': group,
        'pattern': pattern,
        'key': utils.item_stack_dict(ingredients, ''.join(pattern)[0]),
        'result': utils.item_stack(result),
        'conditions': utils.recipe_condition(conditions)
    })

def damage_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: Json, group: str = None, conditions: utils.Json = None) -> RecipeContext:
    return delegate_recipe(rm, name_parts, 'tfc:damage_inputs_shapeless_crafting', {
        'type': 'minecraft:crafting_shapeless',
        'group': group,
        'ingredients': utils.item_stack_list(ingredients),
        'result': utils.item_stack(result),
        'conditions': utils.recipe_condition(conditions)
    })

def damage_shaped(rm: ResourceManager, name_parts: utils.ResourceIdentifier, pattern: Sequence[str], ingredients: Json, result: Json, group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    return delegate_recipe(rm, name_parts, 'tfc:damage_inputs_shaped_crafting', {
            'type': 'minecraft:crafting_shaped',
            'group': group,
            'pattern': pattern,
            'key': utils.item_stack_dict(ingredients, ''.join(pattern)[0]),
            'result': utils.item_stack(result),
            'conditions': utils.recipe_condition(conditions)
        }
    )

def extra_products_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: str, extra_result: str) -> RecipeContext:
    return delegate_recipe(rm, name_parts, 'tfc:extra_products_shapeless_crafting', {
        'type': 'minecraft:crafting_shapeless',
        'ingredients': utils.ingredient_list(ingredients),
        'result': utils.item_stack(result)
    }, {
        'extra_products': utils.item_stack_list(extra_result)
    })

def write_crafting_recipe(rm: ResourceManager, name_parts: ResourceIdentifier, data: Json) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), data)
    return RecipeContext(rm, res)

def delegate_recipe(rm: ResourceManager, name_parts: ResourceIdentifier, recipe_type: str, delegate: Json, data: Json = {}) -> RecipeContext:
    return write_crafting_recipe(rm, name_parts, {
        'type': recipe_type,
        **data,
        'recipe': delegate,
    })

def advanced_shaped(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: Sequence[str], ingredients: Json, result: Json, input_xy: Tuple[int, int], group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'tfc:advanced_shaped_crafting',
        'group': group,
        'pattern': pattern,
        'key': utils.item_stack_dict(ingredients, ''.join(pattern)[0]),
        'result': item_stack_provider(result),
        'input_row': input_xy[1],
        'input_column': input_xy[0],
        'conditions': utils.recipe_condition(conditions)
    })
    return RecipeContext(rm, res)

def advanced_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: Json, primary_ingredient: Json = None, group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'tfc:advanced_shapeless_crafting',
        'group': group,
        'ingredients': utils.item_stack_list(ingredients),
        'result': result,
        'primary_ingredient': None if primary_ingredient is None else utils.ingredient(primary_ingredient),
        'conditions': utils.recipe_condition(conditions)
    })
    return RecipeContext(rm, res)

def quern_recipe(rm: ResourceManager, name: ResourceIdentifier, item: str, result: str, count: int = 1) -> RecipeContext:
    result = result if not isinstance(result, str) else utils.item_stack((count, result))
    return rm.recipe(('quern', name), 'tfc:quern', {
        'ingredient': utils.ingredient(item),
        'result': result
    })


def scraping_recipe(rm: ResourceManager, name: ResourceIdentifier, item: str, result: str, count: int = 1, input_texture=None, output_texture=None, extra_drop: str=None) -> RecipeContext:
    return rm.recipe(('scraping', name), 'tfc:scraping', {
        'ingredient': utils.ingredient(item),
        'result': utils.item_stack((count, result)),
        'input_texture': input_texture,
        'output_texture': output_texture,
        'extra_drop': utils.item_stack(extra_drop) if extra_drop else None
    })


def clay_knapping(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: List[str], result: Json, outside_slot_required: bool = None):
    stack = utils.item_stack(result)
    if ('count' in stack and stack['count'] == 1) or 'count' not in stack:
        rm.item_tag('clay_recycle_5', stack['item'])
    else:
        rm.item_tag('clay_recycle_1', stack['item'])
    knapping_recipe(rm, name_parts, 'tfc:clay', pattern, result, None, outside_slot_required)


def fire_clay_knapping(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: List[str], result: Json, outside_slot_required: bool = None):
    stack = utils.item_stack(result)
    if ('count' in stack and stack['count'] == 1) or 'count' not in stack:
        rm.item_tag('fire_clay_recycle_5', stack['item'])
    else:
        rm.item_tag('fire_clay_recycle_1', stack['item'])
    knapping_recipe(rm, name_parts, 'tfc:fire_clay', pattern, result, None, outside_slot_required)


def leather_knapping(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: List[str], result: Json, outside_slot_required: bool = None):
    knapping_recipe(rm, name_parts, 'tfc:leather', pattern, result, None, outside_slot_required)


def rock_knapping(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: List[str], result: ResourceIdentifier, ingredient: str = None, outside_slot_required: bool = False):
    knapping_recipe(rm, name_parts, 'tfc:rock', pattern, result, ingredient, outside_slot_required)


def horn_knapping(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: List[str], result: ResourceIdentifier, ingredient: str = None, outside_slot_required: bool = False):
    knapping_recipe(rm, name_parts, 'tfc:goat_horn', pattern, {'item': 'minecraft:goat_horn', 'nbt': '{"instrument": "%s"}' % result}, ingredient, outside_slot_required)


def knapping_recipe(rm: ResourceManager, name_parts: ResourceIdentifier, knap_type: str, pattern: List[str], result: Json, ingredient: Json, outside_slot_required: bool):
    for part in pattern:
        assert 0 < len(part) < 6, 'Incorrect length: %s' % part
    rm.recipe((knap_type.split(':')[1] + '_knapping', name_parts), 'tfc:knapping', {
        'knapping_type': knap_type,
        'outside_slot_required': outside_slot_required,
        'pattern': pattern,
        'ingredient': None if ingredient is None else utils.ingredient(ingredient),
        'result': utils.item_stack(result)
    })


def knapping_type(rm: ResourceManager, name_parts: ResourceIdentifier, item_input: Json, amount_to_consume: Optional[int], click_sound: str, consume_after_complete: bool, use_disabled_texture: bool, spawns_particles: bool, jei_icon_item: Json):
    rm.data(('tfc', 'knapping_types', name_parts), {
        'input': item_stack_ingredient(item_input),
        'amount_to_consume': amount_to_consume,
        'click_sound': click_sound,
        'consume_after_complete': consume_after_complete,
        'use_disabled_texture': use_disabled_texture,
        'spawns_particles': spawns_particles,
        'jei_icon_item': utils.item_stack(jei_icon_item)
    })


def heat_recipe(rm: ResourceManager, name_parts: ResourceIdentifier, ingredient: Json, temperature: float, result_item: Optional[Union[str, Json]] = None, result_fluid: Optional[str] = None, use_durability: Optional[bool] = None, chance: Optional[float] = None) -> RecipeContext:
    result_item = item_stack_provider(result_item) if isinstance(result_item, str) else result_item
    result_fluid = None if result_fluid is None else fluid_stack(result_fluid)
    return rm.recipe(('heating', name_parts), 'tfc:heating', {
        'ingredient': utils.ingredient(ingredient),
        'result_item': result_item,
        'result_fluid': result_fluid,
        'temperature': temperature,
        'use_durability': use_durability if use_durability else None,
        'chance': chance,
    })


def casting_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, mold: str, metal: str, amount: int, break_chance: float, result_item: str = None):
    rm.recipe(('casting', name_parts), 'tfc:casting', {
        'mold': {'item': 'tfc:ceramic/%s_mold' % mold},
        'fluid': fluid_stack_ingredient('%d tfc:metal/%s' % (amount, metal)),
        'result': utils.item_stack('tfc:metal/%s/%s' % (mold, metal)) if result_item is None else utils.item_stack(result_item),
        'break_chance': break_chance
    })


def alloy_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, metal: str, *parts: Tuple[str, float, float]):
    rm.recipe(('alloy', name_parts), 'tfc:alloy', {
        'result': 'tfc:%s' % metal,
        'contents': [{
            'metal': 'tfc:%s' % p[0],
            'min': p[1],
            'max': p[2]
        } for p in parts]
    })


def bloomery_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, result: Json, metal: Json, catalyst: Json, time: int):
    rm.recipe(('bloomery', name_parts), 'tfc:bloomery', {
        'result': item_stack_provider(result),
        'fluid': fluid_stack_ingredient(metal),
        'catalyst': item_stack_ingredient(catalyst),
        'duration': time
    })


def blast_furnace_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, metal_in: Json, metal_out: Json, catalyst: Json):
    rm.recipe(('blast_furnace', name_parts), 'tfc:blast_furnace', {
        'fluid': fluid_stack_ingredient(metal_in),
        'result': fluid_stack(metal_out),
        'catalyst': utils.ingredient(catalyst)
    })


def barrel_sealed_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, translation: str, duration: int, input_item: Optional[Json] = None, input_fluid: Optional[Json] = None, output_item: Optional[Json] = None, output_fluid: Optional[Json] = None, on_seal: Optional[Json] = None, on_unseal: Optional[Json] = None, sound: Optional[str] = None):
    rm.recipe(('barrel', name_parts), 'tfc:barrel_sealed', {
        'input_item': item_stack_ingredient(input_item) if input_item is not None else None,
        'input_fluid': fluid_stack_ingredient(input_fluid) if input_fluid is not None else None,
        'output_item': item_stack_provider(output_item) if isinstance(output_item, str) else output_item,
        'output_fluid': fluid_stack(output_fluid) if output_fluid is not None else None,
        'duration': duration,
        'on_seal': on_seal,
        'on_unseal': on_unseal,
        'sound': sound
    })
    res = utils.resource_location('artisanal', name_parts)
    rm.lang('tfc.recipe.barrel.' + res.domain + '.barrel.' + res.path.replace('/', '.'), lang(translation))


def barrel_instant_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, input_item: Optional[Json] = None, input_fluid: Optional[Json] = None, output_item: Optional[Json] = None, output_fluid: Optional[Json] = None, sound: Optional[str] = None):
    rm.recipe(('barrel', name_parts), 'tfc:barrel_instant', {
        'input_item': item_stack_ingredient(input_item) if input_item is not None else None,
        'input_fluid': fluid_stack_ingredient(input_fluid) if input_fluid is not None else None,
        'output_item': item_stack_provider(output_item) if output_item is not None else None,
        'output_fluid': fluid_stack(output_fluid) if output_fluid is not None else None,
        'sound': sound
    })


def barrel_instant_fluid_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, primary_fluid: Optional[Json] = None, added_fluid: Optional[Json] = None, output_fluid: Optional[Json] = None, sound: Optional[str] = None):
    rm.recipe(('barrel', name_parts), 'tfc:barrel_instant_fluid', {
        'primary_fluid': fluid_stack_ingredient(primary_fluid) if primary_fluid is not None else None,
        'added_fluid': fluid_stack_ingredient(added_fluid) if added_fluid is not None else None,
        'output_fluid': fluid_stack(output_fluid) if output_fluid is not None else None,
        'sound': sound
    })


def loom_recipe(rm: ResourceManager, name: utils.ResourceIdentifier, ingredient: Json, result: Json, steps: int, in_progress_texture: str):
    return rm.recipe(('loom', name), 'tfc:loom', {
        'ingredient': item_stack_ingredient(ingredient),
        'result': utils.item_stack(result),
        'steps_required': steps,
        'in_progress_texture': in_progress_texture
    })


def anvil_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, ingredient: Json, result: Json, tier: int, *rules: Rules, bonus: bool = None):
    rm.recipe(('anvil', name_parts), 'tfc:anvil', {
        'input': utils.ingredient(ingredient),
        'result': item_stack_provider(result),
        'tier': tier,
        'rules': [r.name for r in rules],
        'apply_forging_bonus': bonus
    })


def welding_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, first_input: Json, second_input: Json, result: Json, tier: int, combine_forging: bool = None):
    rm.recipe(('welding', name_parts), 'tfc:welding', {
        'first_input': utils.ingredient(first_input),
        'second_input': utils.ingredient(second_input),
        'tier': tier,
        'result': item_stack_provider(result),
        'combine_forging_bonus': combine_forging
    })

def glass_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, steps: List[str], batch: str, result: str):
    rm.recipe(('glassworking', name_parts), 'tfc:glassworking', {
        'operations': steps,
        'batch': utils.ingredient(batch),
        'result': utils.item_stack(result)
    })

def sewing_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, stitches: List[int], squares: List[int], result: str):
    rm.recipe(('sewing', name_parts), 'tfc:sewing', {
        'stitches': stitches,
        'squares': squares,
        'result': utils.item_stack(result)
    })

def fluid_stack(data_in: Json) -> Json:
    if isinstance(data_in, dict):
        return data_in
    fluid, tag, amount, _ = utils.parse_item_stack(data_in, False)
    assert not tag, 'fluid_stack() cannot be a tag'
    return {
        'fluid': fluid,
        'amount': amount
    }


def fluid_stack_ingredient(data_in: Json) -> Json:
    if isinstance(data_in, dict):
        return {
            'ingredient': fluid_ingredient(data_in['ingredient']),
            'amount': data_in['amount']
        }
    if pair := utils.maybe_unordered_pair(data_in, int, object):
        amount, fluid = pair
        return {'ingredient': fluid_ingredient(fluid), 'amount': amount}
    fluid, tag, amount, _ = utils.parse_item_stack(data_in, False)
    if tag:
        return {'ingredient': {'tag': fluid}, 'amount': amount}
    else:
        return {'ingredient': fluid, 'amount': amount}


def fluid_ingredient(data_in: Json) -> Json:
    if isinstance(data_in, dict):
        return data_in
    elif isinstance(data_in, List):
        return [*utils.flatten_list([fluid_ingredient(e) for e in data_in])]
    else:
        fluid, tag, amount, _ = utils.parse_item_stack(data_in, False)
        if tag:
            return {'tag': fluid}
        else:
            return fluid


def item_stack_ingredient(data_in: Json):
    if isinstance(data_in, dict):
        if 'type' in data_in:
            return item_stack_ingredient({'ingredient': data_in})
        return {
            'ingredient': utils.ingredient(data_in['ingredient']),
            'count': data_in['count'] if data_in.get('count') is not None else None
        }
    if pair := utils.maybe_unordered_pair(data_in, int, object):
        count, item = pair
        return {'ingredient': fluid_ingredient(item), 'count': count}
    item, tag, count, _ = utils.parse_item_stack(data_in, False)
    if tag:
        return {'ingredient': {'tag': item}, 'count': count}
    else:
        return {'ingredient': {'item': item}, 'count': count}

def fluid_item_ingredient(fluid: Json, delegate: Json = None):
    return {
        'type': 'tfc:fluid_item',
        'ingredient': delegate,
        'fluid_ingredient': fluid_stack_ingredient(fluid)
    }


def item_stack_provider(
    data_in: Json = None,
    # Possible Modifiers
    copy_input: bool = False,
    copy_heat: bool = False,
    copy_food: bool = False,  # copies both decay and traits
    copy_oldest_food: bool = False,  # copies only decay, from all inputs (uses crafting container)
    reset_food: bool = False,  # rest_food modifier - used for newly created food from non-food
    add_glass: bool = False,  # glassworking specific
    add_powder: bool = False,  # glassworking specific
    add_heat: float = None,
    add_trait: str = None,  # applies a food trait and adjusts decay accordingly
    remove_trait: str = None,  # removes a food trait and adjusts decay accordingly
    empty_bowl: bool = False,  # replaces a soup with its bowl
    copy_forging: bool = False,
    add_bait_to_rod: bool = False,  # adds bait to the rod, uses crafting container
    dye_color: str = None,  # applies a dye color to leather dye-able armor
    meal: Json = None  # makes a meal from input specified in json
) -> Json:
    if isinstance(data_in, dict):
        return data_in
    stack = utils.item_stack(data_in) if data_in is not None else None
    modifiers = [k for k, v in (
        # Ordering is important here
        # First, modifiers that replace the entire stack (copy input style)
        # Then, modifiers that only mutate an existing stack
        ('tfc:empty_bowl', empty_bowl),
        ('tfc:copy_input', copy_input),
        ('tfc:copy_heat', copy_heat),
        ('tfc:copy_food', copy_food),
        ('tfc:copy_oldest_food', copy_oldest_food),
        ('tfc:reset_food', reset_food),
        ('tfc:copy_forging_bonus', copy_forging),
        ('tfc:add_bait_to_rod', add_bait_to_rod),
        ('tfc:add_glass', add_glass),
        ('tfc:add_powder', add_powder),
        ({'type': 'tfc:add_heat', 'temperature': add_heat}, add_heat is not None),
        ({'type': 'tfc:add_trait', 'trait': add_trait}, add_trait is not None),
        ({'type': 'tfc:remove_trait', 'trait': remove_trait}, remove_trait is not None),
        ({'type': 'tfc:dye_leather', 'color': dye_color}, dye_color is not None),
        ({'type': 'tfc:meal', **(meal if meal is not None else {})}, meal is not None),
    ) if v]
    if modifiers:
        return {
            'stack': stack,
            'modifiers': modifiers
        }
    return stack

def not_rotten(ingredient: Json) -> Json:
    return {
        'type': 'tfc:not_rotten',
        'ingredient': utils.ingredient(ingredient)
    }

def has_trait(ingredient: Json, trait: str, invert: bool = False) -> Json:
    return {
        'type': 'tfc:lacks_trait' if invert else 'tfc:has_trait',
        'trait': trait,
        'ingredient': utils.ingredient(ingredient)
    }

def lacks_trait(ingredient: Json, trait: str) -> Json:
    return has_trait(ingredient, trait, True)

def flower_pot_cross(rm: ResourceManager, simple_name: str, name: str, model: str, texture: str, loot: str):
    rm.blockstate(name, model='tfc:block/%s' % model).with_lang(lang('potted %s', simple_name)).with_tag('minecraft:flower_pots').with_block_loot(loot, 'minecraft:flower_pot')
    rm.block_model(model, parent='minecraft:block/flower_pot_cross', textures={'plant': texture, 'dirt': 'tfc:block/dirt/loam'})


def item_model_property(rm: ResourceManager, name_parts: utils.ResourceIdentifier, overrides: utils.Json, data: Dict[str, Any]) -> ItemContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'assets', res.domain, 'models', 'item', res.path), {
        **data,
        'overrides': overrides
    })
    return ItemContext(rm, res)


def water_based_fluid(rm: ResourceManager, name: str):
    rm.blockstate(('fluid', name)).with_block_model({'particle': 'minecraft:block/water_still'}, parent=None).with_lang(lang(name)).with_tag('all_fluids')
    rm.fluid_tag(name, 'artisanal:%s' % name, 'artisanal:flowing_%s' % name)

    item = rm.custom_item_model(('bucket', name), 'forge:fluid_container', {
        'parent': 'forge:item/bucket',
        'fluid': 'artisanal:%s' % name
    })
    item.with_lang(lang('%s bucket', name))
    rm.lang('fluid.artisanal.%s' % name, lang(name))


def cauldron(rm: ResourceManager, name: str, fluid: str, water: bool = True):
    block = rm.blockstate(('cauldron', fluid))
    block.with_block_model({
        'content': 'block/water_still' if water else 'tfc:block/molten_still',
        'inside': 'block/cauldron_inner',
        'particle': 'block/cauldron_side',
        'top': 'block/cauldron_top',
        'bottom': 'block/cauldron_bottom',
        'side': 'block/cauldron_side'
    }, parent='minecraft:block/template_cauldron_full')
    block.with_block_loot('minecraft:cauldron')
    block.with_lang(lang('%s cauldron', name))
    block.with_tag('minecraft:mineable/pickaxe')


def corals(rm: ResourceManager, color: str, dead: bool):
    # vanilla and tfc have a different convention for dead/color order
    left = 'dead_' + color if dead else color
    right = color + '_dead' if dead else color

    rm.blockstate('coral/%s_coral' % right, 'minecraft:block/%s_coral' % left).with_block_loot('tfc:coral/%s_coral' % right)
    rm.blockstate('coral/%s_coral_fan' % right, 'minecraft:block/%s_coral_fan' % left).with_block_loot('tfc:coral/%s_coral_fan' % right)
    rm.blockstate('coral/%s_coral_wall_fan' % right, variants=dict(
        ('facing=%s' % d, {'model': 'minecraft:block/%s_coral_wall_fan' % left, 'y': r})
        for d, r in (('north', None), ('east', 90), ('south', 180), ('west', 270))
    )).with_block_loot('tfc:coral/%s_coral_fan' % right)

    for variant in ('coral', 'coral_fan', 'coral_wall_fan'):
        rm.item_model('coral/%s_%s' % (right, variant), 'minecraft:block/%s_%s' % (left, variant))
        rm.lang('block.tfc.coral.%s_%s' % (right, variant), lang('%s %s', left, variant))

    if not dead:
        # Tag contents are used for selecting a random coral to place by features
        rm.block_tag('wall_corals', 'coral/%s_coral_wall_fan' % color)
        rm.block_tag('corals', 'coral/%s_coral' % color, 'coral/%s_coral_fan' % color)


def four_ways(model: str) -> List[Dict[str, Any]]:
    return [
        {'model': model, 'y': 90},
        {'model': model},
        {'model': model, 'y': 180},
        {'model': model, 'y': 270}
    ]


def four_rotations(model: str, rots: Tuple[Any, Any, Any, Any], suffix: str = '', prefix: str = '') -> Dict[str, Dict[str, Any]]:
    return {
        '%sfacing=east%s' % (prefix, suffix): {'model': model, 'y': rots[0]},
        '%sfacing=north%s' % (prefix, suffix): {'model': model, 'y': rots[1]},
        '%sfacing=south%s' % (prefix, suffix): {'model': model, 'y': rots[2]},
        '%sfacing=west%s' % (prefix, suffix): {'model': model, 'y': rots[3]}
    }

def crop_yield(lo: int, hi: Tuple[int, int]) -> utils.Json:
    return {
        'function': 'minecraft:set_count',
        'count': {
            'type': 'tfc:crop_yield_uniform',
            'min': lo,
            'max': {
                'type': 'minecraft:uniform',
                'min': hi[0],
                'max': hi[1]
            }
        }
    }


def make_javelin(rm: ResourceManager, name_parts: str, texture: str) -> 'ItemContext':
    rm.item_model(name_parts + '_throwing_base', {'particle': texture}, parent='minecraft:item/trident_throwing')
    rm.item_model(name_parts + '_in_hand', {'particle': texture}, parent='minecraft:item/trident_in_hand')
    rm.item_model(name_parts + '_gui', texture)
    model = rm.domain + ':item/' + name_parts
    correct_perspectives = {
        'none': {'parent': model + '_gui'},
        'fixed': {'parent': model + '_gui'},
        'ground': {'parent': model + '_gui'},
        'gui': {'parent': model + '_gui'}
    }
    rm.custom_item_model(name_parts + '_throwing', 'forge:separate_transforms', {
        'gui_light': 'front',
        'base': {'parent': model + '_throwing_base'},
        'perspectives': correct_perspectives
    })

    return rm.custom_item_model(name_parts, 'forge:separate_transforms', {
        'gui_light': 'front',
        'overrides': [{'predicate': {'tfc:throwing': 1}, 'model': model + '_throwing'}],
        'base': {'parent': model + '_in_hand'},
        'perspectives': correct_perspectives
    })


def contained_fluid(rm: ResourceManager, name_parts: utils.ResourceIdentifier, base: str, overlay: str) -> 'ItemContext':
    return rm.custom_item_model(name_parts, 'tfc:contained_fluid', {
        'parent': 'forge:item/default',
        'textures': {
            'base': base,
            'fluid': overlay
        }
    })

def trim_model(rm: ResourceManager, name_parts: utils.ResourceIdentifier, base: str, trim: str, overlay: str = None) -> 'ItemContext':
    return rm.custom_item_model(name_parts, 'tfc:trim', {
        'parent': 'forge:item/default',
        'textures': {
            'armor': base,
            'trim': trim,
            'overlay': overlay
        }
    })

def slab_loot(rm: ResourceManager, loot: str):
    return rm.block_loot(loot, {
        'name': loot,
        'functions': [{
            'function': 'minecraft:set_count',
            'conditions': [loot_tables.block_state_property(loot + '[type=double]')],
            'count': 2,
            'add': False
        }]
    })

def make_door(block_context: BlockContext, door_suffix: str = '_door', top_texture: Optional[str] = None, bottom_texture: Optional[str] = None) -> 'BlockContext':
    """
    Generates all blockstates and models required for a standard door
    """
    door = block_context.res.join() + door_suffix
    block = block_context.res.join('block/') + door_suffix
    bottom = block + '_bottom'
    top = block + '_top'

    if top_texture is None:
        top_texture = top
    if bottom_texture is None:
        bottom_texture = bottom

    block_context.rm.blockstate(door, variants=door_blockstate(block))
    for model in ('bottom_left', 'bottom_left_open', 'bottom_right', 'bottom_right_open', 'top_left', 'top_left_open', 'top_right', 'top_right_open'):
        block_context.rm.block_model(door + '_' + model, {'top': top_texture, 'bottom': bottom_texture}, parent='block/door_%s' % model)
    block_context.rm.item_model(door)
    return block_context

def door_blockstate(base: str) -> JsonObject:
    left = base + '_bottom_left'
    left_open = base + '_bottom_left_open'
    right = base + '_bottom_right'
    right_open = base + '_bottom_right_open'
    top_left = base + '_top_left'
    top_left_open = base + '_top_left_open'
    top_right = base + '_top_right'
    top_right_open = base + '_top_right_open'
    return {
        'facing=east,half=lower,hinge=left,open=false': {'model': left},
        'facing=east,half=lower,hinge=left,open=true': {'model': left_open, 'y': 90},
        'facing=east,half=lower,hinge=right,open=false': {'model': right},
        'facing=east,half=lower,hinge=right,open=true': {'model': right_open, 'y': 270},
        'facing=east,half=upper,hinge=left,open=false': {'model': top_left},
        'facing=east,half=upper,hinge=left,open=true': {'model': top_left_open, 'y': 90},
        'facing=east,half=upper,hinge=right,open=false': {'model': top_right},
        'facing=east,half=upper,hinge=right,open=true': {'model': top_right_open, 'y': 270},
        'facing=north,half=lower,hinge=left,open=false': {'model': left, 'y': 270},
        'facing=north,half=lower,hinge=left,open=true': {'model': left_open},
        'facing=north,half=lower,hinge=right,open=false': {'model': right, 'y': 270},
        'facing=north,half=lower,hinge=right,open=true': {'model': right_open, 'y': 180},
        'facing=north,half=upper,hinge=left,open=false': {'model': top_left, 'y': 270},
        'facing=north,half=upper,hinge=left,open=true': {'model': top_left_open},
        'facing=north,half=upper,hinge=right,open=false': {'model': top_right, 'y': 270},
        'facing=north,half=upper,hinge=right,open=true': {'model': top_right_open, 'y': 180},
        'facing=south,half=lower,hinge=left,open=false': {'model': left, 'y': 90},
        'facing=south,half=lower,hinge=left,open=true': {'model': left_open, 'y': 180},
        'facing=south,half=lower,hinge=right,open=false': {'model': right, 'y': 90},
        'facing=south,half=lower,hinge=right,open=true': {'model': right_open},
        'facing=south,half=upper,hinge=left,open=false': {'model': top_left, 'y': 90},
        'facing=south,half=upper,hinge=left,open=true': {'model': top_left_open, 'y': 180},
        'facing=south,half=upper,hinge=right,open=false': {'model': top_right, 'y': 90},
        'facing=south,half=upper,hinge=right,open=true': {'model': top_right_open},
        'facing=west,half=lower,hinge=left,open=false': {'model': left, 'y': 180},
        'facing=west,half=lower,hinge=left,open=true': {'model': left_open, 'y': 270},
        'facing=west,half=lower,hinge=right,open=false': {'model': right, 'y': 180},
        'facing=west,half=lower,hinge=right,open=true': {'model': right_open, 'y': 90},
        'facing=west,half=upper,hinge=left,open=false': {'model': top_left, 'y': 180},
        'facing=west,half=upper,hinge=left,open=true': {'model': top_left_open, 'y': 270},
        'facing=west,half=upper,hinge=right,open=false': {'model': top_right, 'y': 180},
        'facing=west,half=upper,hinge=right,open=true': {'model': top_right_open, 'y': 90}
    }

def configured_placed_feature(rm: ResourceManager, name_parts: ResourceIdentifier, feature: Optional[ResourceIdentifier] = None, config: JsonObject = None, *placements: Json):
    res = utils.resource_location(rm.domain, name_parts)
    if feature is None:
        feature = res
    rm.configured_feature(res, feature, config)
    rm.placed_feature(res, res, *placements)


def tall_plant_config(state1: str, state2: str, tries: int, radius: int, min_height: int, max_height: int) -> Json:
    return {
        'body': state1,
        'head': state2,
        'tries': tries,
        'radius': radius,
        'min_height': min_height,
        'max_height': max_height
    }


def vine_config(state: str, tries: int, radius: int, min_height: int, max_height: int) -> Json:
    return {
        'state': state,
        'tries': tries,
        'radius': radius,
        'min_height': min_height,
        'max_height': max_height
    }


class PlantConfig(NamedTuple):
    block: str
    y_spread: int
    xz_spread: int
    tries: int
    requires_clay: bool
    water_plant: bool
    emergent_plant: bool
    tall_plant: bool
    epiphyte_plant: bool
    limit_density: bool
    no_solid_neighbors: bool
    tall_water_plant: bool


def plant_config(block: str, y_spread: int, xz_spread: int, tries: int = None, requires_clay: bool = False, water_plant: bool = False, emergent_plant: bool = False, tall_plant: bool = False, epiphyte_plant: bool = False, limit_density: bool = False, no_solid_neighbors: bool = False, tall_water_plant: bool = False) -> PlantConfig:
    return PlantConfig(block, y_spread, xz_spread, tries, requires_clay, water_plant, emergent_plant, tall_plant, epiphyte_plant, limit_density, no_solid_neighbors, tall_water_plant)


def configured_plant_patch_feature(rm: ResourceManager, name_parts: ResourceIdentifier, config: PlantConfig, *patch_decorators: Json):
    state_provider = {
        'type': 'tfc:random_property',
        'state': utils.block_state(config.block), 'property': 'age'
    }
    feature = 'simple_block', {'to_place': state_provider}
    heightmap: Heightmap = 'world_surface_wg'
    would_survive = decorate_would_survive(config.block)

    if config.water_plant or config.emergent_plant or config.tall_water_plant:
        heightmap = 'ocean_floor_wg'
        would_survive = decorate_would_survive_with_fluid(config.block)

    if config.water_plant:
        feature = 'tfc:block_with_fluid', feature[1]
    if config.emergent_plant:
        feature = 'tfc:emergent_plant', {'block': utils.block_state(config.block)['Name']}
    if config.tall_plant:
        feature = 'tfc:tall_plant', {'block': utils.block_state(config.block)['Name']}
    if config.epiphyte_plant:
        feature = 'tfc:epiphyte_plant', {'block': utils.block_state(config.block)['Name']}
    if config.tall_water_plant:
        feature = 'tfc:submerged_tall_plant', {'block': utils.block_state(config.block)['Name']}

    res = utils.resource_location(rm.domain, name_parts)
    patch_feature = res.join() + '_patch'
    singular_feature = utils.resource_location(rm.domain, name_parts)
    predicate = decorate_air_or_empty_fluid() if not config.requires_clay else decorate_replaceable()

    rm.configured_feature(patch_feature, 'minecraft:random_patch' if not config.limit_density else 'tfc:dynamic_random_patch', {
        'tries': config.tries,
        'xz_spread': config.xz_spread,
        'y_spread': config.y_spread,
        'feature': singular_feature.join()
    })
    rm.configured_feature(singular_feature, *feature)
    rm.placed_feature(patch_feature, patch_feature, *patch_decorators)
    if config.no_solid_neighbors:
        rm.placed_feature(singular_feature, singular_feature, decorate_heightmap(heightmap), predicate, would_survive, decorate_no_solid_neighbors())
    else:
        rm.placed_feature(singular_feature, singular_feature, decorate_heightmap(heightmap), predicate, would_survive)

class PatchConfig(NamedTuple):
    block: str
    y_spread: int
    xz_spread: int
    tries: int
    any_water: bool
    salt_water: bool
    fresh_water: bool
    custom_feature: str
    custom_config: Json


def patch_config(block: str, y_spread: int, xz_spread: int, tries: int = 64, water: Union[bool, Literal['salt'], Literal['fresh']] = False, custom_feature: Optional[str] = None, custom_config: Json = None) -> PatchConfig:
    return PatchConfig(block, y_spread, xz_spread, tries, (isinstance(water, bool) and water) or isinstance(water, str), water == 'salt', water == 'fresh', custom_feature, custom_config)

def configured_patch_feature(rm: ResourceManager, name_parts: ResourceIdentifier, patch: PatchConfig, *patch_decorators: Json, extra_singular_decorators: Optional[List[Json]] = None, biome_check: bool = True):
    feature = 'minecraft:simple_block'
    config = {'to_place': {'type': 'minecraft:simple_state_provider', 'state': utils.block_state(patch.block)}}
    singular_decorators = []

    if patch.any_water:
        feature = 'tfc:block_with_fluid'
        if patch.salt_water:
            singular_decorators.append(decorate_matching_blocks('tfc:fluid/salt_water'))
        elif patch.fresh_water:
            singular_decorators.append(decorate_matching_blocks('minecraft:water'))
        else:
            singular_decorators.append(decorate_air_or_empty_fluid())
    else:
        singular_decorators.append(decorate_replaceable())

    if patch.custom_feature is not None:
        assert patch.custom_config
        feature = patch.custom_feature
        config = patch.custom_config

    heightmap: Heightmap = 'world_surface_wg'
    if patch.any_water:
        heightmap = 'ocean_floor_wg'
        singular_decorators.append(decorate_would_survive_with_fluid(patch.block))
    else:
        singular_decorators.append(decorate_would_survive(patch.block))

    if extra_singular_decorators is not None:
        singular_decorators += extra_singular_decorators
    if biome_check:
        patch_decorators = [*patch_decorators, decorate_biome()]

    res = utils.resource_location(rm.domain, name_parts)
    patch_feature = res.join() + '_patch'
    singular_feature = utils.resource_location(rm.domain, name_parts)

    rm.configured_feature(patch_feature, 'minecraft:random_patch', {
        'tries': patch.tries,
        'xz_spread': patch.xz_spread,
        'y_spread': patch.y_spread,
        'feature': singular_feature.join()
    })
    rm.configured_feature(singular_feature, feature, config)
    rm.placed_feature(patch_feature, patch_feature, *patch_decorators)
    rm.placed_feature(singular_feature, singular_feature, decorate_heightmap(heightmap), *singular_decorators)


def configured_noise_plant_feature(rm: ResourceManager, name_parts: ResourceIdentifier, config: PlantConfig, *patch_decorators: Json, water: bool = True, water_depth: int = 5, min_water_depth: int = None):
    res = utils.resource_location(rm.domain, name_parts)
    patch_feature = res.join() + '_patch'
    singular_feature = utils.resource_location(rm.domain, name_parts)
    placed_decorators = [decorate_heightmap('world_surface_wg'), decorate_air_or_empty_fluid(), decorate_would_survive(config.block)]
    if water:
        placed_decorators.append(decorate_shallow(water_depth, min_water_depth))

    rm.configured_feature(singular_feature, 'minecraft:simple_block', {
        'to_place': {
            'seed': 2345,
            'noise': normal_noise(-3, 1.0),
            'scale': 1.0,
            'states': [utils.block_state(config.block)],
            'variety': [1, 1],
            'slow_noise': normal_noise(-10, 1.0),
            'slow_scale': 1.0,
            'type': 'minecraft:dual_noise_provider'
        }
    })
    rm.configured_feature(patch_feature, 'minecraft:random_patch', {
        'tries': config.tries,
        'xz_spread': config.xz_spread,
        'y_spread': config.y_spread,
        'feature': singular_feature.join()
    })
    rm.placed_feature(patch_feature, patch_feature, *patch_decorators)
    rm.placed_feature(singular_feature, singular_feature, *placed_decorators)


def normal_noise(first_octave: int, amplitude: float):
    return {'firstOctave': first_octave, 'amplitudes': [amplitude]}


def simple_state_provider(name: str) -> Dict[str, Any]:
    return {'type': 'minecraft:simple_state_provider', 'state': utils.block_state(name)}


# Vein Helper Functions

def vein_ore_blocks(vein: Vein, rock: str) -> List[Dict[str, Any]]:
    poor, normal, rich = vein.grade
    ore_blocks = [{
        'weight': poor,
        'block': 'tfc:ore/poor_%s/%s' % (vein.ore, rock)
    }, {
        'weight': normal,
        'block': 'tfc:ore/normal_%s/%s' % (vein.ore, rock)
    }, {
        'weight': rich,
        'block': 'tfc:ore/rich_%s/%s' % (vein.ore, rock)
    }]
    if False:  # todo: spoiler stuff?
        if vein.spoiler_ore is not None and rock in vein.spoiler_rocks:
            p = vein.spoiler_rarity * 0.01  # as a percentage of the overall vein
            ore_blocks.append({
                'weight': int(100 * p / (1 - p)),
                'block': 'tfc:ore/%s/%s' % (vein.spoiler_ore, rock)
            })
    if vein.deposits:
        ore_blocks.append({
            'weight': 10,
            'block': 'tfc:deposit/%s/%s' % (vein.ore, rock)
        })
    return ore_blocks


def mineral_ore_blocks(vein: Vein, rock: str) -> List[Dict[str, Any]]:
    if False:
        if vein.spoiler_ore is not None and rock in vein.spoiler_rocks:
            ore_blocks = [{'weight': 100, 'block': 'tfc:ore/%s/%s' % (vein.ore, rock)}]
            p = vein.spoiler_rarity * 0.01  # as a percentage of the overall vein
            ore_blocks.append({
                'weight': int(100 * p / (1 - p)),
                'block': 'tfc:ore/%s/%s' % (vein.spoiler_ore, rock)
            })
    ore_blocks = [{'block': 'tfc:ore/%s/%s' % (vein.ore, rock)}]
    return ore_blocks


def vein_density(density: int) -> float:
    assert 0 <= density <= 100, 'Invalid density: %s' % str(density)
    return round(density * 0.01, 2)


# Tree Helper Functions

def forest_config(rm: ResourceManager, min_rain: float, max_rain: float, min_temp: float, max_temp: float, tree: str, old_growth: bool, old_growth_chance: int = None, spoiler_chance: int = None, krum: bool = False, floating: bool = None):
    cfg = {
        'climate': {
            'min_temperature': min_temp,
            'max_temperature': max_temp,
            'min_rainfall': min_rain,
            'max_rainfall': max_rain
        },
        'groundcover': [{'block': 'tfc:wood/twig/%s' % tree}],
        'normal_tree': 'tfc:tree/%s' % tree,
        'dead_tree': 'tfc:tree/%s_dead' % tree,
        'krummholz': None if not krum else 'tfc:tree/%s_krummholz' % tree,
        'old_growth_chance': old_growth_chance,
        'spoiler_old_growth_chance': spoiler_chance,
        'floating': floating,
    }
    if tree != 'palm':
        cfg['groundcover'] += [{'block': 'tfc:wood/fallen_leaves/%s' % tree}]
    if tree == 'pine':
        cfg['groundcover'] += [{'block': 'tfc:groundcover/pinecone'}]
    if tree not in ('acacia', 'willow'):
        cfg['fallen_log'] = 'tfc:wood/log/%s' % tree
        cfg['fallen_leaves'] = 'tfc:wood/fallen_leaves/%s' % tree
    else:
        cfg['fallen_tree_chance'] = 0
    if tree not in ('palm', 'rosewood', 'sycamore'):
        cfg['bush_log'] = utils.block_state('tfc:wood/wood/%s[branch_direction=down,axis=y]' % tree)
        cfg['bush_leaves'] = 'tfc:wood/leaves/%s' % tree
    if old_growth:
        cfg['old_growth_tree'] = 'tfc:tree/%s_large' % tree
    rm.configured_feature('tree/%s_entry' % tree, 'tfc:forest_entry', cfg)
    cfg['dead_chance'] = 1
    cfg['fallen_tree_chance'] = 8
    cfg['floating'] = None
    rm.configured_feature('tree/dead_%s_entry' % tree, 'tfc:forest_entry', cfg)


def overlay_config(tree: str, min_height: int, max_height: int, width: int = 1, radius: int = 1, suffix: str = '', place=None, roots=None):
    block = 'tfc:wood/log/%s[axis=y,branch_direction=none]' % tree
    tree += suffix
    return {
        'base': 'tfc:%s/base' % tree,
        'overlay': 'tfc:%s/overlay' % tree,
        'trunk': trunk_config(block, min_height, max_height, width),
        'radius': radius,
        'placement': place,
        'root_system': roots
    }


def random_config(tree: str, structure_count: int, radius: int = 1, suffix: str = '', trunk: List = None, place=None, roots=None):
    block = 'tfc:wood/log/%s[axis=y,branch_direction=none]' % tree
    tree += suffix
    cfg = {
        'structures': ['tfc:%s/%d' % (tree, i) for i in range(1, 1 + structure_count)],
        'radius': radius,
        'placement': place,
        'root_system': roots
    }
    if trunk is not None:
        cfg['trunk'] = trunk_config(block, *trunk)
    return cfg


def stacked_config(tree: str, min_height: int, max_height: int, width: int, layers: List[Tuple[int, int, int]], radius: int = 1, suffix: str = '', place: Json = None, roots=None) -> JsonObject:
    # layers consists of each layer, which is a (min_count, max_count, total_templates)
    block = 'tfc:wood/log/%s[axis=y,branch_direction=none]' % tree
    tree += suffix
    return {
        'trunk': trunk_config(block, min_height, max_height, width),
        'layers': [{
            'templates': ['tfc:%s/layer%d_%d' % (tree, 1 + i, j) for j in range(1, 1 + layer[2])],
            'min_count': layer[0],
            'max_count': layer[1]
        } for i, layer in enumerate(layers)],
        'radius': radius,
        'placement': place,
        'root_system': roots
    }


def trunk_config(block: str, min_height: int, max_height: int, width: int) -> JsonObject:
    assert width == 1 or width == 2
    return {
        'state': utils.block_state(block),
        'min_height': min_height,
        'max_height': max_height,
        'wide': width == 2,
    }

def root_config(width: int, height: int, tries: int, mangrove: bool = False) -> JsonObject:
    blocks = [{
        'replace': ['tfc:%s/%s' % (variant, soil)],
        'with': [{'block': 'tfc:rooted_dirt/%s' % soil}]
    } for soil in SOIL_BLOCK_VARIANTS for variant in ('grass', 'dirt')]
    blocks += [{
        'replace': ['tfc:mud/%s' % soil],
        'with': [{'block': 'tfc:muddy_roots/%s' % soil}]
    } for soil in SOIL_BLOCK_VARIANTS]
    cfg = {
        'blocks': blocks,
        'width': width,
        'height': height,
        'tries': tries
    }
    if mangrove:
        cfg['special_placer'] = {
            'skew_chance': 0.2
        }
        cfg['required'] = True
    return cfg


def tree_placement_config(width: int, height: int, ground_type: str = None) -> JsonObject:
    return {
        'width': width,
        'height': height,
        'ground_type': ground_type
    }


Heightmap = Literal['motion_blocking', 'motion_blocking_no_leaves', 'ocean_floor', 'ocean_floor_wg', 'world_surface', 'world_surface_wg']
HeightProviderType = Literal['constant', 'uniform', 'biased_to_bottom', 'very_biased_to_bottom', 'trapezoid', 'weighted_list']


# Decorators / Placements

def decorate_square() -> Json:
    return 'minecraft:in_square'


def decorate_biome() -> Json:
    return 'tfc:biome'


def decorate_chance(rarity_or_probability: Union[int, float]) -> Json:
    return {'type': 'minecraft:rarity_filter', 'chance': round(1 / rarity_or_probability) if isinstance(rarity_or_probability, float) else rarity_or_probability}


def decorate_count(count: int) -> Json:
    return {'type': 'minecraft:count', 'count': count}


def decorate_shallow(max_depth: int = 5, min_depth: int = None) -> Json:
    return {'type': 'tfc:shallow_water', 'max_depth': max_depth, 'min_depth': min_depth}

def decorate_flat_enough(flatness: float = None, radius: int = None, max_depth: int = None):
    return {'type': 'tfc:flat_enough', 'flatness': flatness, 'radius': radius, 'max_depth': max_depth}

def decorate_underground() -> Json:
    return 'tfc:underground'

def decorate_heightmap(heightmap: Heightmap) -> Json:
    assert heightmap in get_args(Heightmap)
    return 'minecraft:heightmap', {'heightmap': heightmap.upper()}


def decorate_range(min_y: VerticalAnchor, max_y: VerticalAnchor, bias: HeightProviderType = 'uniform') -> Json:
    return {
        'type': 'minecraft:height_range',
        'height': height_provider(min_y, max_y, bias)
    }


def decorate_carving_mask(min_y: Optional[VerticalAnchor] = None, max_y: Optional[VerticalAnchor] = None) -> Json:
    return {
        'type': 'tfc:carving_mask',
        'step': 'air',
        'min_y': utils.as_vertical_anchor(min_y) if min_y is not None else None,
        'max_y': utils.as_vertical_anchor(max_y) if max_y is not None else None
    }


def decorate_climate(min_temp: Optional[float] = None, max_temp: Optional[float] = None, min_rain: Optional[float] = None, max_rain: Optional[float] = None, needs_forest: Optional[bool] = False, fuzzy: Optional[bool] = None, min_forest: Optional[str] = None, max_forest: Optional[str] = None) -> Json:
    return {
        'type': 'tfc:climate',
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'min_rainfall': min_rain,
        'max_rainfall': max_rain,
        'min_forest': 'normal' if needs_forest else min_forest,
        'max_forest': max_forest,
        'fuzzy': fuzzy
    }

def decorate_no_solid_neighbors() -> Json:
    return 'tfc:no_solid_neighbors'

def decorate_scanner(direction: str, max_steps: int) -> Json:
    return {
        'type': 'minecraft:environment_scan',
        'max_steps': max_steps,
        'direction_of_search': direction,
        'target_condition': {'type': 'minecraft:solid'},
        'allowed_search_condition': {'type': 'minecraft:matching_blocks', 'blocks': ['minecraft:air']}
    }

def decorate_on_top_of(tag: str) -> Json:
    return {
        'type': 'tfc:on_top',
        'predicate': {
            'type': 'minecraft:matching_block_tag',
            'tag': tag
        }
    }

def decorate_near_water(radius: int = None, salt_water: bool = False, fresh_water: bool = False) -> Json:
    fluids = ['tfc:salt_water', 'minecraft:water', 'tfc:spring_water']
    if salt_water:
        fluids = ['tfc:salt_water']
    if fresh_water:
        fluids = ['minecraft:water']
    return {
        'type': 'tfc:near_fluid',
        'fluids': fluids,
        'radius': radius
    }

def decorate_random_offset(xz: int, y: int) -> Json:
    return {'xz_spread': xz, 'y_spread': y, 'type': 'minecraft:random_offset'}


def decorate_matching_blocks(*blocks: str) -> Json:
    return decorate_block_predicate({
        'type': 'matching_blocks',
        'blocks': list(blocks)
    })


def decorate_would_survive(block: str) -> Json:
    return decorate_block_predicate({
        'type': 'would_survive',
        'state': utils.block_state(block)
    })


def decorate_would_survive_with_fluid(block: str) -> Json:
    return decorate_block_predicate({
        'type': 'tfc:would_survive_with_fluid',
        'state': utils.block_state(block)
    })

def decorate_replaceable() -> Json:
    return decorate_block_predicate({'type': 'tfc:replaceable'})

def decorate_dry_replaceable() -> Json:
    return decorate_block_predicate({'type': 'tfc:dry_replaceable'})

def decorate_air_or_empty_fluid() -> Json:
    return decorate_block_predicate({'type': 'tfc:air_or_empty_fluid'})


def decorate_block_predicate(predicate: Json) -> Json:
    return {
        'type': 'block_predicate_filter',
        'predicate': predicate
    }


# Value Providers

def uniform_float(min_inclusive: float, max_exclusive: float) -> Dict[str, Any]:
    return {
        'type': 'uniform',
        'value': {
            'min_inclusive': min_inclusive,
            'max_exclusive': max_exclusive
        }
    }


def uniform_int(min_inclusive: int, max_inclusive: int) -> Dict[str, Any]:
    return {
        'type': 'uniform',
        'value': {
            'min_inclusive': min_inclusive,
            'max_inclusive': max_inclusive
        }
    }


def trapezoid_float(min_value: float, max_value: float, plateau: float) -> Dict[str, Any]:
    return {
        'type': 'trapezoid',
        'value': {
            'min': min_value,
            'max': max_value,
            'plateau': plateau
        }
    }


def height_provider(min_y: VerticalAnchor, max_y: VerticalAnchor, height_type: HeightProviderType = 'uniform') -> Dict[str, Any]:
    assert height_type in get_args(HeightProviderType)
    return {
        'type': height_type,
        'min_inclusive': utils.as_vertical_anchor(min_y),
        'max_inclusive': utils.as_vertical_anchor(max_y)
    }


def biome(rm: ResourceManager, name: str, category: str, boulders: bool = False, spawnable: bool = True, ocean_features: Union[bool, Literal['both']] = False, lake_features: Union[bool, Literal['default']] = 'default', volcano_features: bool = False, reef_features: bool = False, hot_spring_features: Union[bool, Literal['empty']] = False):
    spawners = {}
    soil_discs = []
    large_features = []
    surface_decorations = []
    costs = {}

    if ocean_features == 'both':  # Both applies both ocean + land features. True or false applies only one
        land_features = True
        ocean_features = True
    else:
        land_features = not ocean_features
    if lake_features == 'default':  # Default = Lakes are on all non-ocean biomes. True/False to force either way
        lake_features = not ocean_features

    if boulders:
        large_features.append('#tfc:feature/boulders')

    # Oceans
    if ocean_features:
        large_features.append('#tfc:feature/icebergs')
        if name != 'tidal_flats':
            surface_decorations.append('#tfc:feature/ocean_plants')
        if name == 'shore':
            surface_decorations.append('tfc:plant/beachgrass_patch')
            surface_decorations.append('tfc:plant/sea_palm_patch')

        if category == 'beach':
            surface_decorations.append('#tfc:feature/shore_decorations')
            spawners['creature'] = [entity for entity in SHORE_CREATURES.values()]
        else:
            surface_decorations.append('#tfc:feature/ocean_decorations')

        spawners['water_ambient'] = [entity for entity in OCEAN_AMBIENT.values()]
        spawners['water_creature'] = [entity for entity in OCEAN_CREATURES.values()]
        spawners['underground_water_creature'] = [entity for entity in UNDERGROUND_WATER_CREATURES.values()]
        costs['tfc:octopoteuthis'] = {'energy_budget': 0.12, 'charge': 1.0}

    if category in ('river', 'lake'):
        soil_discs.append('#tfc:feature/ore_deposits')
    if category in ('lake', 'swamp', 'river'):
        surface_decorations.append('tfc:plant/dry_phragmite')
    if category == 'river':
        spawners['water_ambient'] = [entity for entity in RIVER_AMBIENT.values()]

    if name == 'deep_ocean_trench':
        large_features.append('tfc:lava_hot_spring')

    if 'lake' in name:
        spawners['water_ambient'] = [entity for entity in LAKE_AMBIENT.values()]
        spawners['water_creature'] = [entity for entity in LAKE_CREATURES.values()]
    if 'swamp' == category:
        spawners['water_ambient'] = [entity for entity in LAKE_AMBIENT.values()]
    if 'salt_marsh' == name:
        spawners['water_ambient'] = [entity for entity in SALT_MARSH_AMBIENT.values()]
    spawners['monster'] = [entity for entity in VANILLA_MONSTERS.values()]

    if reef_features:
        large_features.append('tfc:coral_reef')

    # Continental / Land Features
    if land_features:
        soil_discs.append('#tfc:feature/soil_discs')
        if 'salt_marsh' not in name:
            large_features += ['tfc:forest']
        else:
            large_features += ['tfc:mangrove_forest']
            surface_decorations += ['tfc:plant/marsh_jungle_vines']
        if 'lowlands' in name:
            large_features += ['tfc:dead_forest']
        large_features += ['tfc:rare_bamboo', 'tfc:bamboo', 'tfc:cave_vegetation']
        surface_decorations.append('#tfc:feature/land_plants')
        spawners['creature'] = [entity for entity in LAND_CREATURES.values()]

    if volcano_features:
        large_features.append('#tfc:feature/volcanoes')

    if hot_spring_features:  # can be True, 'empty'
        if hot_spring_features == 'empty':
            large_features.append('tfc:random_empty_hot_spring')
        else:
            large_features.append('tfc:random_active_hot_spring')

    # Feature Tags
    # We don't directly use vanilla's generation step, but we line this up *approximately* with it, so that mods that add features add them in roughly the right location
    feature_tags = [
        '#tfc:in_biome/erosion',  # Raw Generation
        '#tfc:in_biome/all_lakes' if lake_features else '#tfc:in_biome/underground_lakes',  # Lakes
        '#tfc:in_biome/soil_discs/%s' % name,  # Local Modifications
        '#tfc:in_biome/underground_structures',  # Underground Structures
        '#tfc:in_biome/surface_structures',  # Surface Structures
        '#tfc:in_biome/strongholds',  # Strongholds
        '#tfc:in_biome/veins',  # Underground Ores
        '#tfc:in_biome/underground_decoration',  # Underground Decoration
        '#tfc:in_biome/large_features/%s' % name,  # Fluid Springs (we co-opt this as they likely won't interfere and it's in the right order)
        '#tfc:in_biome/surface_decoration/%s' % name,  # Vegetal Decoration
        '#tfc:in_biome/top_layer_modification'  # Top Layer Modification
    ]

    rm.placed_feature_tag(('in_biome/soil_discs', name), *soil_discs)
    rm.placed_feature_tag(('in_biome/large_features', name), *large_features)
    rm.placed_feature_tag(('in_biome/surface_decoration', name), *surface_decorations)

    if volcano_features:
        rm.biome_tag('is_volcanic', name)
    if 'lake' in name:
        rm.biome_tag('is_lake', name)
    if 'river' in name:
        rm.biome_tag('is_river', name)
    if 'ocean' in name and 'mountain' not in name:
        rm.biome_tag('is_ocean', name)

    rm.lang('biome.tfc.%s' % name, lang(name))
    mcresources_biome(rm,
        name_parts=name,
        has_precipitation=True,
        category=category,
        temperature=0.5,
        downfall=0.5,
        effects={
            'fog_color': 0xC0D8FF,
            'sky_color': 0x84E6FF,
            'water_color': 0x3F76E4,
            'water_fog_color': 0x050533
        },
        spawners=spawners,
        air_carvers=['tfc:cave', 'tfc:canyon'],
        water_carvers=[],
        features=feature_tags,
        player_spawn_friendly=spawnable,
        creature_spawn_probability=0.08,
        spawn_costs=costs
    )


def expand_rocks(rocks: list[str]) -> list[str]:
    assert all(r in ROCKS or r in ROCK_CATEGORIES for r in rocks)
    return [
        rock
        for spec in rocks
        for rock in ([spec] if spec in ROCKS else [r for r, d in ROCKS.items() if d.category == spec])
    ]


def join_not_empty(c: str, *elements: str) -> str:
    return c.join((item for item in elements if item != ''))


def count_weighted_list(*pairs: Tuple[Any, int]) -> List[Any]:
    return [item for item, count in pairs for _ in range(count)]


def mcresources_biome(self, name_parts: ResourceIdentifier, has_precipitation: bool, category: str = 'none', temperature: float = 0, temperature_modifier: str = 'none', downfall: float = 0.5, effects: Optional[Json] = None, air_carvers: Optional[Sequence[str]] = None, water_carvers: Optional[Sequence[str]] = None, features: Sequence[Sequence[str]] = None, structures: Sequence[str] = None, spawners: Optional[Json] = None, player_spawn_friendly: bool = True, creature_spawn_probability: float = 0.5, parent: Optional[str] = None, spawn_costs: Optional[Json] = None):
    """ Creates a biome, with all possible optional parameters filled in to the minimum required state. Parameters are exactly as they appear in the final biome. """
    if effects is None:
        effects = {}
    for required_effect in ('fog_color', 'sky_color', 'water_color', 'water_fog_color'):
        if required_effect not in effects:
            effects[required_effect] = 0

    if features is None:
        features = []
    if structures is None:
        structures = []
    if spawners is None:
        spawners = {}
    if spawn_costs is None:
        spawn_costs = {}
    res = utils.resource_location(self.domain, name_parts)
    self.write((*self.resource_dir, 'data', res.domain, 'worldgen', 'biome', res.path), {
        'has_precipitation': has_precipitation,
        'category': category,
        'temperature': temperature,
        'temperature_modifier': temperature_modifier,
        'downfall': downfall,
        'effects': effects,
        'carvers': {
            'air': air_carvers,
            'liquid': water_carvers
        },
        'features': features,
        'starts': structures,
        'spawners': spawners,
        'player_spawn_friendly': player_spawn_friendly,
        'creature_spawn_probability': creature_spawn_probability,
        'parent': parent,
        'spawn_costs': spawn_costs
    })


def rock_layers():
    def make(name: str, **kwargs):
        return {'id': name, 'layers': kwargs}

    return {
        'rocks': {rock: 'tfc:%s' % rock for rock in ROCKS},
        'bottom': ['gneiss', 'schist', 'diorite', 'granite', 'gabbro'],
        'layers': [
            make('felsic', granite='bottom'),
            make('intermediate', diorite='bottom'),
            make('mafic', gabbro='bottom'),
            make('igneous_extrusive', rhyolite='felsic', andesite='intermediate', dacite='intermediate', basalt='mafic'),
            make('igneous_extrusive_x2', rhyolite='igneous_extrusive', andesite='igneous_extrusive', dacite='igneous_extrusive', basalt='igneous_extrusive'),
            make('phyllite', phyllite='bottom', gneiss='bottom', schist='bottom'),
            make('slate', slate='bottom', phyllite='phyllite'),
            make('marble', marble='bottom'),
            make('quartzite', quartzite='bottom'),
            make('sedimentary', shale='slate', claystone='slate', conglomerate='slate', limestone='marble', dolomite='marble', chalk='marble', chert='quartzite'),
            make('uplift',
                 slate='phyllite', marble='bottom', quartzite='bottom',  # Metamorphic that was exposed, so it proceeds normally
                 diorite='sedimentary', granite='sedimentary', gabbro='sedimentary'  # Uplift / cap, so igneous intrusive on top of sedimentary
                 ),
        ],
        'ocean_floor': ['igneous_extrusive'],
        'volcanic': ['igneous_extrusive', 'igneous_extrusive_x2'],
        'land': ['igneous_extrusive', 'sedimentary'],
        'uplift': ['sedimentary', 'uplift']
    }

def kill_mob(mob: str, other: Dict = None) -> Json:
    return generic('minecraft:player_killed_entity', {'entity': [entity_predicate(mob, other)]})

# if the predicate is (and usually it will be) an EntityPredicate.Composite, this should be inside an array.
# EntityPredicate.Composite wraps a vanilla loot event in a trigger event
def entity_predicate(mob: str, other: Dict = None) -> Json:
    dic = {
        'condition': 'minecraft:entity_properties',
        'predicate': {'type': mob},  # can be a hashtag to refer to entity tags
        'entity': 'this',
    }
    if other is not None:
        dic.update(other)
    return dic


def consume_item(item: str, name: str = 'item_consumed') -> Json:
    if isinstance(item, str) and name == 'item_consumed':
        name = item.split(':')[1]
    return generic('minecraft:consume_item', {'item': utils.item_predicate(item)}, name=name)

def icon(name: str) -> Json:
    return {'item': name}

def biome(biome_name: str) -> Json:
    return location({'biome': 'tfc:%s' % biome_name}, biome_name)

def location(location_predicate: Json, name: str):
    return generic('minecraft:location', {
        'player': [
            {
                'condition': 'minecraft:entity_properties',
                'entity': 'this',
                'predicate': {
                    'location': location_predicate
                }
            }
        ]}, name=name)

def multiple(*conditions: Json) -> Json:
    merged = {}
    for c in conditions:
        merged.update(c)
    return merged

def generic(trigger_type: str, conditions: Json, name: str = 'special_condition') -> Json:
    return {name: {'trigger': trigger_type, 'conditions': conditions}}

def inventory_changed(item: str | Json, name: str = 'item_obtained') -> Json:
    if isinstance(item, str) and name == 'item_obtained':
        name = item.split(':')[1]
    return {name: advancements.inventory_changed(item)}

def item_use_on_block(block: str, item: str, name: str = 'item_use_on_block_condition'):
    block_json = {'tag': block[1:]} if block[0] == '#' else {'blocks': [block]}
    return {name: {'trigger': 'minecraft:item_used_on_block', 'conditions': {
        'location': {'block': block_json},
        'item': {'items': [item]}
    }}}

def root_trigger() -> Json:
    return {'in_game_condition': {'trigger': 'minecraft:tick'}}