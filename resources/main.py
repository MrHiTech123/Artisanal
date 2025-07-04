import json

import forge_condition
from alcs_n_russians_funcs import *
from mcresources import ResourceManager


SIMPLE_FLUIDS = ('lard', 'schmaltz', 'soapy_water', 'soap', 'sugarcane_juice', 'filtered_sugarcane_juice', 'alkalized_sugarcane_juice', 'clarified_sugarcane_juice', 'molasses', 'condensed_milk', 'condensed_goat_milk', 'condensed_yak_milk', 'petroleum', 'apple_juice', 'carrot_juice', 'lemon_juice', 'diluted_lemon_juice', 'orange_juice', 'peach_juice', 'pineapple_juice', 'tomato_juice', 'screwdriver', 'sulfuric_acid')
AFC_WOODS = ('eucalyptus', 'mahogany', 'baobab', 'hevea', 'tualang', 'teak', 'cypress', 'fig', 'ironwood', 'ipe')
MAGNIFYING_GLASS_METALS = ('bismuth', 'brass', 'gold', 'rose_gold', 'silver', 'sterling_silver', 'tin')
CANNABLE_FOOD_TAGS = ('breads', 'dairy', 'flour', 'fruits', 'grains', 'meats', 'vegetables')
POTTABLE_FOOD_TAGS = ('meats', 'vegetables')
CAN_STATUSES = ('sterilized', 'sealed')
DRUM_METALS = ['bismuth_bronze', 'black_bronze', 'bronze', 'steel', 'red_steel', 'blue_steel']
CAN_METALS = {'tin', 'stainless_steel'}
CANS_MB_AMOUNTS = {
    'tin': 150,
    'stainless_steel': 50
}

BLOOMERY_SHEETS = ['bismuth_bronze', 'black_bronze', 'bronze', 'wrought_iron', 'steel', 'black_steel', 'blue_steel', 'red_steel']
STEELS = {metal: METALS[metal] for metal in ('steel', 'black_steel', 'blue_steel', 'red_steel')}
SULFUR_BURN = 175


class CleaningRecipe(NamedTuple):
    item_name: str
    input_item: str
    output_item: str

CLEANABLES = (
    CleaningRecipe('jute_net', 'tfc:dirty_jute_net', 'tfc:jute_net'),
    CleaningRecipe('soup_bowl', '#tfc:dynamic_bowl_items', item_stack_provider(empty_bowl=True)),
    CleaningRecipe('filled_jar', '#tfc:foods/preserves', 'tfc:empty_jar'),
    CleaningRecipe('sealed_jar', '#tfc:foods/sealed_preserves', 'tfc:empty_jar'),
    CleaningRecipe('empty_jar', 'artisanal:dirty_jar', 'tfc:empty_jar'),
    CleaningRecipe('sugarcane', not_rotten('tfc:food/sugarcane'), item_stack_provider('artisanal:food/cleaned_sugarcane', copy_food=True)),
    CleaningRecipe('hematitic_wine_bottle', 'firmalife:hematitic_wine_bottle', 'firmalife:empty_hematitic_wine_bottle'),
    CleaningRecipe('olivine_wine_bottle', 'firmalife:olivine_wine_bottle', 'firmalife:empty_olivine_wine_bottle'),
    CleaningRecipe('volcanic_wine_bottle', 'firmalife:volcanic_wine_bottle', 'firmalife:empty_volcanic_wine_bottle'),
    CleaningRecipe('any_bowl', '#firmalife:foods/washable', item_stack_provider(other_modifier='firmalife:empty_pan')),
    *[
        x for metal in CAN_METALS for x in
        (
            CleaningRecipe(f'{metal}_can', f'artisanal:metal/can/{metal}_dirty', f'artisanal:metal/can/{metal}'),
            CleaningRecipe(f'dented_{metal}_can', f'artisanal:metal/can/{metal}_dirty_dented', f'artisanal:metal/can/{metal}_dented')
        )
    ],
    CleaningRecipe('small_pot', 'artisanal:ceramic/dirty_small_pot', 'artisanal:ceramic/small_pot'),
    CleaningRecipe('burlap_cloth', 'artisanal:dirty_burlap_cloth', 'tfc:burlap_cloth'),
    CleaningRecipe('silk_cloth', 'artisanal:dirty_silk_cloth', 'tfc:silk_cloth'),
    CleaningRecipe('wool_cloth', 'artisanal:dirty_wool_cloth', 'tfc:wool_cloth')
)

def disable_data(rm: ResourceManager, name_parts: ResourceIdentifier):
    # noinspection PyTypeChecker
    rm.data(name_parts, {
            'group': None,
            **{},
            'conditions': utils.recipe_condition('forge:false')})

def juicing_recipe(rm: ResourceManager, name: ResourceIdentifier, item: str, result: str) -> RecipeContext:
    result = result if not isinstance(result, str) else fluid_stack(result)
    return rm.recipe(('juicing', name), 'artisanal:juicing', {
        'ingredient': utils.ingredient(item),
        'result': result
    })
    

def melt_metal(name: str, mb: int):
    metal = METALS[name]
    if metal.melt_metal is not None:
        name = metal.melt_metal
    return f'{mb} {metal.namespace}:metal/{name}'


def optional_tag(id: str) -> dict[str, Any]:
    return {
        "id": id,
        "required": False
    }

def only_if_flux_makes_limewater_instant_barrel_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, input_item: Optional[Json] = None, input_fluid: Optional[Json] = None, output_item: Optional[Json] = None, output_fluid: Optional[Json] = None, sound: Optional[str] = None, conditions=None):
    rm.recipe(('barrel', name_parts), 'artisanal:only_if_flux_makes_limewater_instant_barrel', {
        'input_item': item_stack_ingredient(input_item) if input_item is not None else None,
        'input_fluid': fluid_stack_ingredient(input_fluid) if input_fluid is not None else None,
        'output_item': item_stack_provider(output_item) if output_item is not None else None,
        'output_fluid': fluid_stack(output_fluid) if output_fluid is not None else None,
        'sound': sound
    }, conditions=conditions)


rm = ResourceManager('artisanal')

forge_rm = ResourceManager('forge')

canning_modifier = {
    'food': {
        'decay_modifier': 4.5
    },
    'portions': [{
        'ingredient': utils.ingredient('#artisanal:foods/can_be_canned'),
        'nutrient_modifier': 0,
        'water_modifier': 0,
        'saturation_modifier': 0,
    }]
}

def advancement(rm: ResourceManager, name_parts: tuple, icon: dict[str, Any] | Sequence | str | int | bool | None, title: str, description: str, parent: str, criteria: dict[str, Any] | Sequence | str | int | bool | None, requirements: Sequence[Sequence[str]] | None = None, rewards: dict[str, Any] | Sequence | str | int | bool | None = None, hidden: bool=False):
    if (isinstance(name_parts, str)):
        name_parts = (name_parts, )
    
    key = f'{rm.domain}.advancements.{".".join(name_parts)}'
    
    rm.advancement(name_parts, {
        'icon': utils.item_stack(icon),
        'title': {'translate': key + '.title'},
        'description': {'translate': key + '.description'},
        'frame': 'task',
        'show_toast': True,
        'announce_to_chat': True,
        'hidden': hidden,
    }, parent, criteria, requirements)
    
    rm.lang(key + '.title', title)
    rm.lang(key + '.description', description)
    
def catalyst_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: Json, group: str = None, conditions: utils.Json = None) -> RecipeContext:
    return delegate_recipe(rm, name_parts, 'artisanal:damage_and_catalyst_shapeless_crafting', {
        'type': 'minecraft:crafting_shapeless',
        'group': group,
        'ingredients': utils.item_stack_list(ingredients),
        'result': utils.item_stack(result),
        'conditions': utils.recipe_condition(conditions)
    })

def heatable_ingredient(ingredient: str, min_temp: int):
    return {'type': 'tfc:heatable', 'min_temp': min_temp, 'ingredient': utils.ingredient(ingredient)}

def loot_modifier_add_itemstack_min_max(rm: ResourceManager, loot_modifiers: list, name_parts, entity_tag, item, little, big):
    data = {
      "type": "artisanal:add_itemstack_min_max",
      "conditions": [
        {
          "condition": "minecraft:entity_properties",
          "predicate": {
              "type": entity_tag
          },
          "entity": "this"
        }
      ],
      "item": item,
      "min": little,
      "max": big
    }
    
    loot_modifier(rm, loot_modifiers, name_parts, data)

def loot_modifier_add_fat(rm: ResourceManager, loot_modifiers: list, name_parts, entity_tag, item, little, big):
    data = {
      "type": "artisanal:add_fat",
      "conditions": [
        {
          "condition": "minecraft:entity_properties",
          "predicate": {
              "type": entity_tag
          },
          "entity": "this"
        }
      ],
      "item": item,
      "min": little,
      "max": big
    }
    
    loot_modifier(rm, loot_modifiers, name_parts, data)
    
def loot_modifier(rm: ResourceManager, loot_modifiers: list, name_parts, data):

    if isinstance(name_parts, str):
        name_parts = [name_parts]
    
    rm.data(['loot_modifiers'] + name_parts, data)
    
    loot_modifiers.append(f'artisanal:{"/".join(name_parts)}')

def remove_many_traits(stack: dict, *traits: str):
    if 'modifiers' not in stack:
        stack = {
            'stack': stack,
            'modifiers': []
        }
    for trait in traits:
        stack['modifiers'].append({
            'type': 'tfc:remove_trait',
            'trait': trait
        })
    return stack

def scalable_pot_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, fluid: str, output_fluid: str = None, output_items: Json = None, duration: int = 2000, temp: int = 300, conditions=None):
    rm.recipe(('pot', name_parts), 'artisanal:scalable_pot', {
        'ingredients': [],
        'fluid_ingredient': fluid_stack_ingredient(fluid),
        'duration': duration,
        'temperature': temp,
        'fluid_output': fluid_stack(output_fluid) if output_fluid is not None else None,
        'item_output': [utils.item_stack(item) for item in output_items] if output_items is not None else None
    }, conditions=conditions)

def specific_no_remainder_damage_shaped(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: Sequence[str], ingredients: Json, result: Json, input_xy: Tuple[int, int], group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'artisanal:specific_no_remainder_damage_shaped',
        'group': group,
        'pattern': pattern,
        'key': utils.item_stack_dict(ingredients, ''.join(pattern)[0]),
        'result': item_stack_provider(result),
        'input_row': input_xy[1],
        'input_column': input_xy[0],
        'conditions': utils.recipe_condition(conditions)
    })
    return RecipeContext(rm, res)

def specific_no_remainder_shaped(rm: ResourceManager, name_parts: ResourceIdentifier, pattern: Sequence[str], ingredients: Json, result: Json, input_xy: Tuple[int, int], group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'artisanal:specific_no_remainder_shaped',
        'group': group,
        'pattern': pattern,
        'key': utils.item_stack_dict(ingredients, ''.join(pattern)[0]),
        'result': item_stack_provider(result),
        'input_row': input_xy[1],
        'input_column': input_xy[0],
        'conditions': utils.recipe_condition(conditions)
    })
    return RecipeContext(rm, res)

def specific_no_remainder_shapeless(rm: ResourceManager, name_parts: ResourceIdentifier, ingredients: Json, result: Json, primary_ingredient: Json = None, group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
    res = utils.resource_location(rm.domain, name_parts)
    item_stack_provider()
    rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
        'type': 'artisanal:specific_no_remainder_shapeless',
        'group': group,
        'ingredients': utils.item_stack_list(ingredients),
        'result': result,
        'primary_ingredient': None if primary_ingredient is None else utils.ingredient(primary_ingredient),
        'conditions': utils.recipe_condition(conditions)
    })
    return RecipeContext(rm, res)

def universal_ingredient() -> Json:
    return {'type': 'artisanal:universal_ingredient'}
    

def generate_advancements():
    print('Generating advancements...')
    advancement(rm, ('story', 'magnifying_glass'), 'artisanal:metal/magnifying_glass/brass', 'Inspector Detector', 'Craft a Magnifying Glass', 'tfc:story/lens', inventory_changed('#artisanal:magnifying_glasses'))
    advancement(rm, ('story', 'perishable_sugar'), 'artisanal:perishable_sugar', 'Sweet Tooth', 'Create Perishable Sugar', 'artisanal:story/juicing', inventory_changed('artisanal:perishable_sugar'))
    advancement(rm, ('story', 'non_perishable_sugar'), 'artisanal:non_perishable_sugar', 'Everlasting Sweet Tooth', 'Create Non-Perishable Sugar', 'artisanal:story/perishable_sugar', inventory_changed('artisanal:non_perishable_sugar'))
    advancement(rm, ('story', 'sugar'), 'minecraft:sugar', 'Swhite Tooth', 'Create White Sugar', 'artisanal:story/non_perishable_sugar', inventory_changed('minecraft:sugar'))
    advancement(rm, ('story', 'powdered_milk'), 'artisanal:powdered_milk', 'Just Add Water', 'Create Powdered Milk', 'tfc:story/quern', inventory_changed('#artisanal:powdered_milks'))
    advancement(rm, ('story', 'quill'), 'artisanal:quill', 'Not Quite Ballpoint', 'Create a Quill', 'tfc:story/barrel', inventory_changed('artisanal:quill'))
    advancement(rm, ('story', 'writable_book'), 'minecraft:writable_book', 'Bookkeeper', 'Create a Book and Quill', 'artisanal:story/quill', inventory_changed('minecraft:writable_book'))
    advancement(rm, ('story', 'soap'), 'artisanal:soap', 'Clean as a Whistle', 'Create Soap', 'tfc:story/barrel', inventory_changed('artisanal:soap'))
    advancement(rm, ('story', 'drum'), 'artisanal:metal/drum/bronze', 'Drumroll, Please!', 'Make a Drum from Metal Sheets', 'tfc:story/barrel', inventory_changed('#artisanal:metal/drums'))
    advancement(rm, ('story', 'lava_drum'), 'artisanal:metal/drum/blue_steel', 'Lava Holder', 'Make a Drum that can hold Lava', 'artisanal:story/drum', inventory_changed('artisanal:metal/drum/blue_steel'))
    advancement(rm, ('story', 'play_drum'), 'artisanal:metal/drum/steel', 'This One\'s a Banger!', 'Play a Drum like a...well...like a Drum.', 'artisanal:story/drum', generic('artisanal:play_drum', None), hidden=True)
    advancement(rm, ('story', 'juicing'), {'item': 'tfc:silica_glass_bottle', 'nbt': "{\"fluid\":{\"Amount\": 500, \"FluidName\": \"artisanal:orange_juice\"}}"}, 'Juicer', 'Collect some Juice in a Barrel placed underneath your Quern', 'tfc:story/quern', generic('artisanal:juicing', None))
    advancement(rm, ('story', 'flint_and_pyrite'), 'artisanal:stone/flint_and/pyrite', 'Pyrestarter', 'Make a Flint and Pyrite', 'tfc:story/firestarter', inventory_changed('artisanal:stone/flint_and/pyrite'))
    advancement(rm, ('story', 'flint_and_cut_pyrite'), 'artisanal:stone/flint_and/cut_pyrite', 'Pretty Pyrestarter', 'Make a Flint and Cut Pyrite', 'artisanal:story/flint_and_pyrite', inventory_changed('artisanal:stone/flint_and/cut_pyrite'))
    advancement(rm, ('story', 'flint_and_colored_steel'), 'artisanal:metal/flint_and/red_steel', 'Ocean of Flame', 'Craft a Flint and Steel using Red or Blue Steel', 'tfc:story/flint_and_steel', inventory_changed('#artisanal:metal/flint_and/colored_steel'))
    advancement(rm, ('story', 'sterilized_tin_can'), 'artisanal:metal/can/tin_sterilized', 'Local Cannery', 'Seal some food in a Can and sterilize it', 'tfc:story/sheet', inventory_changed('#artisanal:metal/sterilized_cans'))
    
    
    
    
def generate_drinkables():
    print('\tGenerating drinkables...')
    drinkable(rm, ('molasses'), 'artisanal:molasses', thirst=-1, food={'hunger': 4, 'saturation': 0, 'vegetables': 2, 'fruit': 2})
    drinkable(rm, ('apple_juice'), 'artisanal:apple_juice', thirst=10, food={'hunger': 0, 'saturation': 0, 'fruit': 0.7})
    drinkable(rm, ('carrot_juice'), 'artisanal:carrot_juice', thirst=10, food={'hunger': 0, 'saturation': 0, 'vegetables': 0.7})
    drinkable(rm, ('diluted_lemon_juice'), 'artisanal:diluted_lemon_juice', thirst=10, food={'hunger': 0, 'saturation': 0, 'fruit': 0.7})
    drinkable(rm, ('orange_juice'), 'artisanal:orange_juice', thirst=10, food={'hunger': 0, 'saturation': 0, 'fruit': 0.7})
    drinkable(rm, ('peach_juice'), 'artisanal:peach_juice', thirst=10, food={'hunger': 0, 'saturation': 0, 'fruit': 0.7})
    drinkable(rm, ('pineapple_juice'), 'artisanal:pineapple_juice', thirst=10, food={'hunger': 0, 'saturation': 0, 'fruit': 0.7})
    drinkable(rm, ('tomato_juice'), 'artisanal:tomato_juice', thirst=10, food={'hunger': 0, 'saturation': 0, 'vegetables': 0.7})
    drinkable(rm, ('screwdriver'), 'artisanal:screwdriver', thirst=10, food={'fruit': 0.5, 'vegetables': 0.5}, intoxication=2000, allow_full=True)
    
    
    disable_data(rm, 'tfc:tfc/drinkables/alcohol')
    drinkable(rm, ('alcohol/fruit'), '#artisanal:alcohols/fruit', thirst=10, intoxication=4000, allow_full=True, food={'fruit': 0.7})
    drinkable(rm, ('alcohol/grain'), '#artisanal:alcohols/grain', thirst=10, intoxication=4000, allow_full=True, food={'grain': 0.7})
    drinkable(rm, ('alcohol/vegetable'), '#artisanal:alcohols/vegetable', thirst=10, intoxication=4000, allow_full=True, food={'vegetables': 0.7})
    drinkable(rm, ('alcohol/fruit_and_veg'), '#artisanal:alcohols/fruit_and_veg', thirst=10, intoxication=4000, allow_full=True, food={'fruit': 0.7, 'vegetables': 0.7})
    drinkable(rm, ('alcohol/no_nutrition'), '#artisanal:alcohols/no_nutrition', thirst=10, intoxication=4000, allow_full=True)
    
    
def generate_lamp_fuels():
    print('\tGenerating lamp fuels...')
    lamp_fuel(rm, 'lard', 'artisanal:lard', 1800)
    lamp_fuel(rm, 'schmaltz', 'artisanal:schmaltz', 1800)

def generate_fuels():
    print('\tGenerating fuels...')
    generate_lamp_fuels()
    fuel_item(rm, ('bagasse'), 'artisanal:bagasse', 750, 350)
    
    
    
def generate_item_foods():
    print('\tGenerating item foods...')
    food_item(rm, ('cleaned_sugarcane'), 'artisanal:food/cleaned_sugarcane', Category.other, 4, 0, 0, 0.5)
    food_item(rm, ('fruit_mash'), 'artisanal:food/fruit_mash', Category.fruit, 4, 0, 0, 3, fruit=0.5)
    food_item(rm, ('carrot_mash'), 'artisanal:food/carrot_mash', Category.vegetable, 4, 0, 0, 3, veg=0.5)
    food_item(rm, ('tomato_mash'), 'artisanal:food/tomato_mash', Category.vegetable, 4, 0, 0, 3, veg=0.5)
    food_item(rm, ('perishable_sugar'), 'artisanal:perishable_sugar', Category.other, 0, 0, 0, 3)
    food_item(rm, ('non_perishable_sugar'), 'artisanal:non_perishable_sugar', Category.other, 0, 0, 0, 0, tag_as_food=False)
    food_item(rm, ('sugar'), 'minecraft:sugar', Category.other, 0, 0, 0, 0, tag_as_food=False)
    food_item(rm, ('maple_sugar'), 'afc:maple_sugar', Category.other, 0, 0, 0, 0, tag_as_food=False)
    food_item(rm, ('birch_sugar'), 'afc:birch_sugar', Category.other, 0, 0, 0, 0, tag_as_food=False)
    food_item(rm, ('honey'), 'firmalife:raw_honey', Category.other, 0, 0, 0, 0, tag_as_food=False)
    
    for metal in CAN_METALS:
        dynamic_food_item(rm, ('metal', 'can', f'{metal}_sealed'), f'artisanal:metal/can/{metal}_sealed', 'dynamic')
        dynamic_food_item(rm, ('metal', 'can', f'{metal}_sterilized'), f'artisanal:metal/can/{metal}_sterilized', 'dynamic')
    dynamic_food_item(rm, ('closed_small_pot'), 'artisanal:ceramic/closed_small_pot', 'dynamic')
    dynamic_food_item(rm, ('dirty_bowl'), 'artisanal:dirty_bowl', 'dynamic_bowl')
    
def generate_item_heats():
    print('\tGenerating item heats...')
    item_heat(rm, ('sand'), '#forge:sand', 0.8, None, None)
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        item_heat(rm, ('metal', 'magnifying_glass', metal), f'artisanal:metal/magnifying_glass/{metal}', metal_data.ingot_heat_capacity(), metal_data.melt_temperature, 50)
        item_heat(rm, ('metal', 'magnifying_glass_frame', metal), f'artisanal:metal/magnifying_glass_frame/{metal}', metal_data.ingot_heat_capacity(), metal_data.melt_temperature, 50)
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            item_heat(rm, ('metal', 'circle_blade', metal), f'artisanal:metal/circle_blade/{metal}', metal_data.ingot_heat_capacity(), metal_data.melt_temperature, 50)
            item_heat(rm, ('metal', 'brick_mold', metal), f'artisanal:metal/brick_mold/{metal}', metal_data.ingot_heat_capacity(), metal_data.melt_temperature, 50)
    
    item_heat(rm, ('metal', 'tinplate'), 'artisanal:metal/tinplate', METALS['tin'].ingot_heat_capacity(), METALS['tin'].melt_temperature, CANS_MB_AMOUNTS['tin'])
    item_heat(rm, ('metal', 'stainless_steelplate'), 'artisanal:metal/stainless_steelplate', METALS['stainless_steel'].ingot_heat_capacity(), METALS['stainless_steel'].melt_temperature, CANS_MB_AMOUNTS['stainless_steel'])
    
    for metal in CAN_METALS:
        item_heat(rm, ('metal', 'can', f'{metal}'), f'artisanal:metal/can/{metal}', METALS[metal].ingot_heat_capacity(), METALS[metal].melt_temperature, CANS_MB_AMOUNTS[metal] + 100)
        item_heat(rm, ('metal', 'can', f'{metal}_sealed'), f'artisanal:metal/can/{metal}_sealed', METALS[metal].ingot_heat_capacity(), METALS[metal].melt_temperature, CANS_MB_AMOUNTS[metal] + 100)
        item_heat(rm, ('metal', 'can', f'{metal}_dented'), f'artisanal:metal/can/{metal}_dented', METALS[metal].ingot_heat_capacity(), METALS[metal].melt_temperature, CANS_MB_AMOUNTS[metal] + 100)
    
    for metal, metal_data in STEELS.items():
        item_heat(rm, ('metal', 'striker', metal), f'artisanal:metal/striker/{metal}', metal_data.ingot_heat_capacity(), metal_data.melt_temperature, 50)
    
    item_heat(rm, ('ceramic', 'unfired_small_pot'), 'artisanal:ceramic/unfired_small_pot', POTTERY_HEAT_CAPACITY)
    
    item_heat(rm, ('metal', 'pickled_double_sheet', 'wrought_iron'), 'artisanal:metal/pickled_double_sheet/wrought_iron', METALS['wrought_iron'].ingot_heat_capacity(), METALS['wrought_iron'].melt_temperature, 400)
    item_heat(rm, ('metal', 'pickled_double_sheet', 'steel'), 'artisanal:metal/pickled_double_sheet/steel', METALS['steel'].ingot_heat_capacity(), METALS['steel'].melt_temperature, 400)
    
    item_heat(rm, ('powder', 'sulfur'), 'tfc:powder/sulfur', 0.8, None, None)
    
    for metal in DRUM_METALS:
        metal_data = METALS[metal]
        item_heat(rm, ('metal', 'drum', metal), f'artisanal:metal/drum/{metal}', metal_data.ingot_heat_capacity(), metal_data.melt_temperature, 1400)

def generate_item_size_weights():
    print('\tGenerating item size weights...')
    
    for metal in CAN_METALS:
        item_size(rm, ('metal', 'can', f'{metal}'), f'artisanal:metal/can/{metal}', Size.small, Weight.light)
        item_size(rm, ('metal', 'can', f'{metal}_sealed'), f'artisanal:metal/can/{metal}_sealed', Size.small, Weight.light)
        item_size(rm, ('metal', 'can', f'{metal}_sterilized'), f'artisanal:metal/can/{metal}_sterilized', Size.small, Weight.light)
        item_size(rm, ('metal', 'can', f'{metal}_dirty'), f'artisanal:metal/can/{metal}_dirty', Size.small, Weight.light)
        item_size(rm, ('metal', 'can', f'{metal}_dented'), f'artisanal:metal/can/{metal}_dented', Size.small, Weight.light)
        item_size(rm, ('metal', 'can', f'{metal}_dirty_dented'), f'artisanal:metal/can/{metal}_dirty_dented', Size.small, Weight.light)
    
    item_size(rm, ('ceramic', 'small_pot'), 'artisanal:ceramic/small_pot', Size.small, Weight.light)
    item_size(rm, ('ceramic', 'dirty_small_pot'), 'artisanal:ceramic/dirty_small_pot', Size.small, Weight.light)
    item_size(rm, ('ceramic', 'closed_small_pot'), 'artisanal:ceramic/closed_small_pot', Size.small, Weight.light)
    item_size(rm, ('ceramic', 'unfired_small_pot'), 'artisanal:ceramic/unfired_small_pot', Size.small, Weight.light)
    
    
    for metal, metal_data in METALS.items():
        item_size(rm, ('metal', 'brick_mold', metal), f'artisanal:metal/brick_mold/{metal}', Size.large, Weight.light)
    
    item_size(rm, ('metal', 'pickled_double_sheet', 'wrought_iron'), 'artisanal:metal/pickled_double_sheet/wrought_iron', Size.large, Weight.heavy)
    item_size(rm, ('metal', 'pickled_double_sheet', 'steel'), 'artisanal:metal/pickled_double_sheet/steel', Size.large, Weight.heavy)
    
    item_size(rm, 'dirty_jar', 'artisanal:dirty_jar', Size.tiny, Weight.medium)
    item_size(rm, 'dirty_bowl', 'artisanal:dirty_bowl', Size.small, Weight.light)
    
    item_size(rm, 'dirty_burlap_cloth', 'artisanal:dirty_burlap_cloth', Size.small, Weight.very_light)
    item_size(rm, 'dirty_silk_cloth', 'artisanal:dirty_silk_cloth', Size.small, Weight.light)
    item_size(rm, 'dirty_wool_cloth', 'artisanal:dirty_wool_cloth', Size.small, Weight.light)
    
    

def generate_data():
    print('Generating data...')
    generate_drinkables()
    generate_fuels()
    generate_item_foods()
    generate_item_heats()
    generate_item_size_weights()

def generate_loot_modifiers():
    print('Creating loot modifiers...')
    
    loot_modifiers = []
    loot_modifier_add_fat(rm, loot_modifiers, 'animals_drop_suet', '#artisanal:drops_suet', 'artisanal:suet', 1, 3)
    loot_modifier_add_fat(rm, loot_modifiers, 'animals_drop_pork_fat', '#artisanal:drops_pork_fat', 'artisanal:pork_fat', 1, 3)
    loot_modifier_add_fat(rm, loot_modifiers, 'animals_drop_bear_fat', '#artisanal:drops_bear_fat', 'artisanal:bear_fat', 1, 3)
    loot_modifier_add_fat(rm, loot_modifiers, 'animals_drop_poultry_fat', '#artisanal:drops_poultry_fat', 'artisanal:poultry_fat', 1, 1)
    
    forge_rm.data(('loot_modifiers', 'global_loot_modifiers'), {'replace': False, 'entries': loot_modifiers})

def generate_misc_lang():
    print('Generating misc lang...')
    rm.lang('tfc.jei.scalable_pot', 'Scalable Pot Recipe')
    rm.lang("block.tfc.fluid.limewater", "Slaked Lime")
    rm.lang("item.tfc.bucket.limewater", "Slaked Lime Bucket")
    rm.lang("fluid.tfc.limewater", "Slaked Lime")
    rm.lang("block.tfc.cauldron.limewater", "Slaked Lime Cauldron")
    rm.lang("item.minecraft.cooked_beef", "Whatever Food Was Inside the Can")
    rm.lang('tfc.jei.juicing', 'Juicing Recipe')
    rm.lang('item.minecraft.sugar', 'White Sugar')

def generate_block_models():
    print('\tGenerating block models...')
    for metal in DRUM_METALS:
        texture = f'tfc:block/metal/block/{metal}'
        textures = {'particle': texture, 'planks': texture, 'sheet': f'tfc:block/metal/smooth/{metal}', 'hoop': texture}
        
        faces = (('up', 0), ('east', 0), ('west', 180), ('south', 90), ('north', 270))
        seals = (('true', 'drum_sealed'), ('false', 'drum'))
        racks = (('true', '_rack'), ('false', ''))
        block = rm.blockstate(('metal', 'drum', metal), variants=dict((
            'facing=%s,rack=%s,sealed=%s' % (face, rack, is_seal), {'model': 'artisanal:block/metal/%s/%s%s%s' % (seal_type, metal, '_side' if face != 'up' else '', suffix if face != 'up' else ''), 'y': yrot if yrot != 0 else None}
        ) for face, yrot in faces for rack, suffix in racks for is_seal, seal_type in seals))

        item_model_property(rm, ('metal', 'drum', metal), [{'predicate': {'tfc:sealed': 1.0}, 'model': f'artisanal:block/metal/drum_sealed/{metal}'}], {'parent': f'artisanal:block/metal/drum/{metal}'})
        block.with_block_model(textures, 'tfc:block/barrel')
        rm.block_model(('metal', 'drum', metal + '_side'), textures, 'tfc:block/barrel_side')
        rm.block_model(('metal', 'drum', metal + '_side_rack'), textures, 'tfc:block/barrel_side_rack')
        rm.block_model(('metal', 'drum_sealed', metal + '_side_rack'), textures, 'tfc:block/barrel_side_sealed_rack')
        rm.block_model(('metal', 'drum_sealed', metal), textures, 'tfc:block/barrel_sealed')
        rm.block_model(('metal', 'drum_sealed', metal + '_side'), textures, 'tfc:block/barrel_side_sealed')
        block.with_lang(lang(f'{metal} drum'))
        block.with_block_loot(({
            'name': f'artisanal:metal/drum/{metal}',
            'functions': [loot_tables.copy_block_entity_name(), loot_tables.copy_block_entity_nbt()],
            'conditions': [loot_tables.block_state_property(f'artisanal:metal/drum/{metal}[sealed=true]')]
        }, f'artisanal:metal/drum/{metal}'))

def generate_item_models():
    print('\tGenerating item models...')
    for fluid in SIMPLE_FLUIDS:
        water_based_fluid(rm, fluid)
    
    rm.item_model('suet', 'artisanal:item/suet').with_lang(lang('suet'))
    rm.item_model('pork_fat', 'artisanal:item/pork_fat').with_lang(lang('pork_fat'))
    rm.item_model('bear_fat', 'artisanal:item/bear_fat').with_lang(lang('bear_fat'))
    rm.item_model('poultry_fat', 'artisanal:item/poultry_fat').with_lang(lang('poultry_fat'))
    rm.item_model('animal_fat', 'artisanal:item/animal_fat').with_lang(lang('animal_fat'))
    rm.item_model('soap', 'artisanal:item/soap').with_lang('Soap')
    
    rm.item_model('trimmed_feather', 'artisanal:item/trimmed_feather').with_lang(lang('trimmed_feather'))
    rm.item_model('soaked_feather', 'artisanal:item/soaked_feather').with_lang(lang('soaked_feather'))
    rm.item_model('tempered_feather', 'artisanal:item/tempered_feather').with_lang(lang('tempered_feather'))
    rm.item_model('quill', 'artisanal:item/quill').with_lang(lang('quill'))
    
    rm.item_model(('food', 'cleaned_sugarcane'), 'artisanal:item/food/cleaned_sugarcane').with_lang(lang('cleaned_sugarcane'))
    rm.item_model('bagasse', 'artisanal:item/bagasse').with_lang(lang('bagasse'))
    rm.item_model('perishable_sugar', 'artisanal:item/perishable_sugar').with_lang(lang('perishable_sugar'))
    rm.item_model('non_perishable_sugar', 'artisanal:item/non_perishable_sugar').with_lang('Non-Perishable Sugar')
    
    rm.item_model('milk_flakes', 'artisanal:item/milk_flakes').with_lang(lang('milk_flakes'))
    rm.item_model('goat_milk_flakes', 'artisanal:item/goat_milk_flakes').with_lang(lang('goat_milk_flakes'))
    rm.item_model('yak_milk_flakes', 'artisanal:item/yak_milk_flakes').with_lang(lang('yak_milk_flakes'))
    
    rm.item_model('powdered_milk', 'artisanal:item/powdered_milk').with_lang(lang('powdered_milk'))
    rm.item_model('powdered_goat_milk', 'artisanal:item/powdered_goat_milk').with_lang(lang('powdered_goat_milk'))
    rm.item_model('powdered_yak_milk', 'artisanal:item/powdered_yak_milk').with_lang(lang('powdered_yak_milk'))
    
    for metal in MAGNIFYING_GLASS_METALS:
        rm.item_model(('metal', 'magnifying_glass', f'{metal}'), f'artisanal:item/metal/magnifying_glass/{metal}').with_lang(lang(f'{metal}_magnifying_glass'))
        rm.item_model(('metal', 'magnifying_glass_frame', f'{metal}'), f'artisanal:item/metal/magnifying_glass_frame/{metal}').with_lang(lang(f'{metal}_magnifying_glass_frame'))
    
    rm.item_model(('metal', 'tinplate'), 'artisanal:item/metal/tinplate').with_lang(lang('tinplate'))
    rm.item_model(('metal', 'stainless_steelplate'), 'artisanal:item/metal/stainless_steelplate').with_lang(lang('stainless_steelplate'))
    
    for metal in CAN_METALS:
        rm.item_model(('metal', 'can', f'{metal}'), f'artisanal:item/metal/can/{metal}').with_lang(lang(f'{metal}_can'))
        rm.item_model(('metal', 'can', f'{metal}_sealed'), f'artisanal:item/metal/can/{metal}_sealed').with_lang(lang(f'sealed_{metal}_can'))
        rm.item_model(('metal', 'can', f'{metal}_sterilized'), f'artisanal:item/metal/can/{metal}_sterilized').with_lang(lang(f'sterilized_{metal}_can'))
        rm.item_model(('metal', 'can', f'{metal}_dirty'), f'artisanal:item/metal/can/{metal}_dirty').with_lang(lang(f'dirty_{metal}_can'))
        rm.item_model(('metal', 'can', f'{metal}_dented'), f'artisanal:item/metal/can/{metal}_dented').with_lang(lang(f'dented_{metal}_can'))
        rm.item_model(('metal', 'can', f'{metal}_dirty_dented'), f'artisanal:item/metal/can/{metal}_dirty_dented').with_lang(lang(f'dirty_dented_{metal}_can'))
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            rm.item_model(('metal', 'can_opener', metal), f'artisanal:item/metal/can_opener/{metal}').with_lang(lang(f'{metal} can opener'))
            rm.item_model(('metal', 'circle_blade', metal), f'artisanal:item/metal/circle_blade/{metal}').with_lang(lang(f'{metal} circle blade'))
            rm.item_model(('metal', 'brick_mold', metal), f'artisanal:item/metal/brick_mold/{metal}').with_lang(lang(f'{metal}_brick_mold'))
    
    for metal in STEELS:
        rm.item_model(('metal', 'striker', metal), f'artisanal:item/metal/striker/{metal}').with_lang(lang(f'{metal}_striker'))
        if metal != 'steel':
            rm.item_model(('metal', 'flint_and', metal), f'artisanal:item/metal/flint_and/{metal}').with_lang(lang(f'flint_and_{metal}'))
    
    rm.item_model(('stone', 'flint_and', 'pyrite'), f'artisanal:item/stone/flint_and/pyrite').with_lang(lang('flint_and_pyrite'))
    rm.item_model(('stone', 'flint_and', 'cut_pyrite'), f'artisanal:item/stone/flint_and/cut_pyrite').with_lang(lang('flint_and_cut_pyrite'))
    
    rm.item_model('dirty_jar', 'artisanal:item/dirty_jar').with_lang('Dirty Jar')
    
    rm.item_model(('ceramic', 'dirty_small_pot'), 'artisanal:item/ceramic/dirty_small_pot').with_lang(lang('dirty_small_pot'))
    rm.item_model(('ceramic', 'small_pot'), 'artisanal:item/ceramic/small_pot').with_lang(lang('small_pot'))
    rm.item_model(('ceramic', 'unfired_small_pot'), 'artisanal:item/ceramic/unfired_small_pot').with_lang(lang('unfired_small_pot'))
    rm.item_model(('ceramic', 'closed_small_pot'), 'artisanal:item/ceramic/closed_small_pot').with_lang(lang('closed_small_pot'))
    
    rm.item_model(('dirty_bowl'), 'artisanal:item/dirty_bowl').with_lang(lang('dirty_bowl'))
    
    rm.item_model(('food', 'fruit_mash'), 'artisanal:item/food/fruit_mash').with_lang(lang('fruit_mash'))
    rm.item_model(('food', 'carrot_mash'), 'artisanal:item/food/carrot_mash').with_lang(lang('carrot_mash'))
    rm.item_model(('food', 'tomato_mash'), 'artisanal:item/food/tomato_mash').with_lang(lang('tomato_mash'))
    
    rm.item_model(('metal', 'pickled_double_sheet', 'wrought_iron'), 'artisanal:item/metal/pickled_double_sheet/wrought_iron').with_lang(lang('pickled_wrought_iron_double_sheet'))
    rm.item_model(('metal', 'pickled_double_sheet', 'steel'), 'artisanal:item/metal/pickled_double_sheet/steel').with_lang(lang('pickled_steel_double_sheet'))
    
    rm.item_model('dirty_burlap_cloth', 'artisanal:item/dirty_burlap_cloth').with_lang(lang('dirty_burlap_cloth'))
    rm.item_model('dirty_silk_cloth', 'artisanal:item/dirty_silk_cloth').with_lang(lang('dirty_silk_cloth'))
    rm.item_model('dirty_wool_cloth', 'artisanal:item/dirty_wool_cloth').with_lang(lang('dirty_wool_cloth'))
    
    
def generate_models():
    print('Generating models...')
    generate_block_models()
    generate_item_models()

def generate_anvil_recipes():
    print('\tGenerating anvil recipes...')
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        anvil_recipe(rm, ('metal', 'magnifying_glass_frame', metal), f'tfc:metal/rod/{metal}', f'artisanal:metal/magnifying_glass_frame/{metal}', metal_data.tier, Rules.bend_last, Rules.hit_any, Rules.bend_not_last)
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            anvil_recipe(rm, ('metal', 'circle_blade', metal), f'tfc:metal/ingot/{metal}', (2, f'artisanal:metal/circle_blade/{metal}'), metal_data.tier, Rules.shrink_third_last, Rules.hit_second_last, Rules.hit_last)
            anvil_recipe(rm, ('metal', 'brick_mold', metal), f'tfc:metal/rod/{metal}', f'artisanal:metal/brick_mold/{metal}', metal_data.tier, Rules.bend_not_last, Rules.draw_not_last, Rules.hit_last, bonus=True)
    
    for metal, metal_data in STEELS.items():
        anvil_recipe(rm, ('metal', 'striker', metal), f'tfc:metal/ingot/high_carbon_{metal}', f'artisanal:metal/striker/{metal}', metal_data.tier, Rules.bend_any, Rules.hit_any, Rules.punch_any, bonus=True)
    
    anvil_recipe(rm, ('metal', 'can', 'tin'), 'artisanal:metal/tinplate', 'artisanal:metal/can/tin', 1, Rules.bend_not_last, Rules.hit_not_last, Rules.hit_last)
    
    anvil_recipe(rm, ('metal', 'stainless_steelplate'), 'firmalife:metal/sheet/stainless_steel', (4, 'artisanal:metal/stainless_steelplate'), 1, Rules.hit_third_last, Rules.hit_second_last, Rules.hit_last)
    anvil_recipe(rm, ('metal', 'can', 'stainless_steel'), 'artisanal:metal/stainless_steelplate', 'artisanal:metal/can/stainless_steel', 1, Rules.bend_not_last, Rules.hit_not_last, Rules.hit_last)
    
    for metal in CAN_METALS:
        anvil_recipe(rm, ('metal', 'can', f'{metal}_repair'), f'artisanal:metal/can/{metal}_dented', f'artisanal:metal/can/{metal}', 1, Rules.hit_third_last, Rules.hit_second_last, Rules.hit_last)
    
    welding_recipe(rm, ('metal', 'tinplate_from_iron'), 'tfc:metal/double_sheet/wrought_iron', 'tfc:metal/sheet/tin', item_stack_provider((4, 'artisanal:metal/tinplate'), cap_heat=METALS['tin'].melt_temperature - 1), 0)
    welding_recipe(rm, ('metal', 'tinplate_from_pickled_iron'), 'artisanal:metal/pickled_double_sheet/wrought_iron', 'tfc:metal/sheet/tin', item_stack_provider((6, 'artisanal:metal/tinplate'), cap_heat=METALS['tin'].melt_temperature - 1), 0)
    welding_recipe(rm, ('metal', 'tinplate_from_steel'), 'tfc:metal/double_sheet/steel', 'tfc:metal/sheet/tin', item_stack_provider((8, 'artisanal:metal/tinplate'), cap_heat=METALS['tin'].melt_temperature - 1), 0)
    welding_recipe(rm, ('metal', 'tinplate_from_pickled_steel'), 'artisanal:metal/pickled_double_sheet/steel', 'tfc:metal/sheet/tin', item_stack_provider((12, 'artisanal:metal/tinplate'), cap_heat=METALS['tin'].melt_temperature - 1), 0)
    
    disable_recipe(rm, 'firmalife:anvil/stainless_steel_jar_lid')
    anvil_recipe(rm, 'stainless_steel_jar_lid', 'firmalife:metal/ingot/stainless_steel', (16, 'tfc:jar_lid'), 4, Rules.hit_last, Rules.hit_second_last, Rules.punch_third_last, conditions=[
        forge_condition.and_(
            forge_condition.mod_loaded('firmalife'),
            forge_condition.mod_not_loaded('lithicaddon')
        )
    ])
    
def generate_barrel_recipes():
    print('\tGenerating barrel recipes...')
    barrel_sealed_recipe(rm, ('soaked_feather'), 'Soaking Feather', 8000, 'artisanal:trimmed_feather', '200 minecraft:water', 'artisanal:soaked_feather', None)
    barrel_instant_fluid_recipe(rm, ('soap_fluid'), '9 #artisanal:rendered_fats', '1 tfc:lye', '10 artisanal:soap')
    barrel_instant_fluid_recipe(rm, ('soap_fluid_from_olive_oil'), '9 tfc:olive_oil', '1 tfc:lye', '10 artisanal:soap')
    barrel_sealed_recipe(rm, ('soap_solid'), 'Solidifying Soap', 8000, None, '125 artisanal:soap', 'artisanal:soap', None, None)
    
    barrel_instant_recipe(rm, ('soapy_water'), 'artisanal:soap', '1000 minecraft:water', None, '1000 artisanal:soapy_water')
    
    only_if_flux_makes_limewater_instant_barrel_recipe(rm, ('conditional_limewater_from_flux'), 'tfc:powder/flux', '500 minecraft:water', output_fluid='500 tfc:limewater')
    
    disable_recipe(rm, 'tfc:barrel/clean_jar')
    disable_recipe(rm, 'tfc:barrel/clean_jute_net')
    disable_recipe(rm, 'tfc:barrel/clean_sealed_jar')
    disable_recipe(rm, 'tfc:barrel/clean_soup_bowl')
    disable_recipe(rm, 'firmalife:barrel/clean_hematitic_wine_bottle')
    disable_recipe(rm, 'firmalife:barrel/clean_olivine_wine_bottle')
    disable_recipe(rm, 'firmalife:barrel/clean_volcanic_wine_bottle')
    disable_recipe(rm, 'firmalife:barrel/clean_any_bowl')
    disable_recipe(rm, 'tfc:barrel/sugar')
    
    
    for cleanable in CLEANABLES:
        barrel_sealed_recipe(rm, ('clean', cleanable.item_name, 'water'), f'Cleaning {lang(cleanable.item_name)}', 8000, cleanable.input_item, '100 minecraft:water', output_item=cleanable.output_item)
        barrel_instant_recipe(rm, ('clean', cleanable.item_name, 'soapy_water'), cleanable.input_item, '100 artisanal:soapy_water', output_item=cleanable.output_item)
    
    disable_recipe(rm, 'tfc:barrel/candle')
    barrel_sealed_recipe(rm, 'candle', 'Candle', 4000, '#forge:string', '40 #artisanal:rendered_fats', 'tfc:candle')
    
    disable_recipe(rm, 'firmaciv:barrel/large_waterproof_hide_tallow')
    barrel_sealed_recipe(rm, 'large_waterproof_hide_rendered_fat', 'Large Waterproof Hide', 8000, 'tfc:large_prepared_hide', '100 #artisanal:rendered_fats', 'firmaciv:large_waterproof_hide')
    
    barrel_instant_recipe(rm, ('olive_oil_water', 'burlap_cloth'), 'tfc:burlap_cloth', '500 tfc:olive_oil_water', 'artisanal:dirty_burlap_cloth', '100 tfc:olive_oil')
    barrel_instant_recipe(rm, ('olive_oil_water', 'silk_cloth'), 'tfc:silk_cloth', '500 tfc:olive_oil_water', 'artisanal:dirty_silk_cloth', '100 tfc:olive_oil')
    barrel_instant_recipe(rm, ('olive_oil_water', 'wool_cloth'), 'tfc:wool_cloth', '500 tfc:olive_oil_water', 'artisanal:dirty_wool_cloth', '100 tfc:olive_oil')
    
    barrel_instant_recipe(rm, ('sugarcane_juice', 'filtered', 'jute_net'), 'tfc:jute_net', '250 artisanal:sugarcane_juice', 'tfc:dirty_jute_net', '250 artisanal:filtered_sugarcane_juice')
    barrel_instant_recipe(rm, ('sugarcane_juice', 'filtered', 'burlap_cloth'), 'tfc:burlap_cloth', '500 artisanal:sugarcane_juice', 'artisanal:dirty_burlap_cloth', '500 artisanal:filtered_sugarcane_juice')
    barrel_instant_recipe(rm, ('sugarcane_juice', 'filtered', 'silk_cloth'), 'tfc:silk_cloth', '500 artisanal:sugarcane_juice', 'artisanal:dirty_silk_cloth', '500 artisanal:filtered_sugarcane_juice')
    barrel_instant_recipe(rm, ('sugarcane_juice', 'filtered', 'wool_cloth'), 'tfc:wool_cloth', '500 artisanal:sugarcane_juice', 'artisanal:dirty_wool_cloth', '500 artisanal:filtered_sugarcane_juice')
    
    barrel_instant_recipe(rm, ('sugarcane_juice', 'clarified', 'jute_net'), 'tfc:jute_net', '250 artisanal:alkalized_sugarcane_juice', 'tfc:dirty_jute_net', '250 artisanal:clarified_sugarcane_juice')
    barrel_instant_recipe(rm, ('sugarcane_juice', 'clarified', 'burlap_cloth'), 'tfc:burlap_cloth', '500 artisanal:alkalized_sugarcane_juice', 'artisanal:dirty_burlap_cloth', '500 artisanal:clarified_sugarcane_juice')
    barrel_instant_recipe(rm, ('sugarcane_juice', 'clarified', 'silk_cloth'), 'tfc:silk_cloth', '500 artisanal:alkalized_sugarcane_juice', 'artisanal:dirty_silk_cloth', '500 artisanal:clarified_sugarcane_juice')
    barrel_instant_recipe(rm, ('sugarcane_juice', 'clarified', 'wool_cloth'), 'tfc:wool_cloth', '500 artisanal:alkalized_sugarcane_juice', 'artisanal:dirty_wool_cloth', '500 artisanal:clarified_sugarcane_juice')
    
    barrel_sealed_recipe(rm, 'alkalized_sugarcane_juice', 'Alkalizing Sugarcane Juice', 8000, 'tfc:powder/lime', '500 artisanal:filtered_sugarcane_juice', None, '500 artisanal:alkalized_sugarcane_juice')
    
    barrel_sealed_recipe(rm, 'paper', 'Bleaching Paper', 1000, 'tfc:unrefined_paper', '25 tfc:lye', 'minecraft:paper')
    
    barrel_instant_recipe(rm, ('milk', 'cow'), 'artisanal:powdered_milk', '100 minecraft:water', None, '100 minecraft:milk')
    barrel_instant_recipe(rm, ('milk', 'goat'), 'artisanal:powdered_goat_milk', '100 minecraft:water', None, '100 firmalife:goat_milk', conditions=[forge_condition.mod_loaded('firmalife')])
    barrel_instant_recipe(rm, ('milk', 'yak'), 'artisanal:powdered_yak_milk', '100 minecraft:water', None, '100 firmalife:yak_milk', conditions=[forge_condition.mod_loaded('firmalife')])
    
    disable_recipe(rm, 'tfc:barrel/limewater')
    disable_recipe(rm, 'tfc:barrel/rum')
    disable_recipe(rm, 'tfc:barrel/cider')
    barrel_sealed_recipe(rm, ('rum'), 'Fermenting Rum', 72000, None, '1 artisanal:molasses', None, '1 tfc:rum')
    barrel_sealed_recipe(rm, ('cider'), 'Fermenting Cider', 72000, None, '1 artisanal:apple_juice', None, '1 tfc:cider')
    barrel_instant_fluid_recipe(rm, ('screwdriver'), '1 tfc:vodka', '1 artisanal:orange_juice', '2 artisanal:screwdriver')
    
    barrel_sealed_recipe(rm, ('metal', 'pickled_double_sheet', 'wrought_iron'), lang('Pickling Wrought Iron Double Sheet'), 1000, 'tfc:metal/double_sheet/wrought_iron', '100 #artisanal:acids', 'artisanal:metal/pickled_double_sheet/wrought_iron')
    barrel_sealed_recipe(rm, ('metal', 'pickled_double_sheet', 'steel'), lang('Pickling Steel Double Sheet'), 1000, 'tfc:metal/double_sheet/steel', '100 #artisanal:acids', 'artisanal:metal/pickled_double_sheet/steel')
    
    barrel_instant_fluid_recipe(rm, ('diluted_lemon_juice'), '1 artisanal:lemon_juice', '1 minecraft:water', '2 artisanal:diluted_lemon_juice')
    
    barrel_instant_recipe(rm, 'lava_garbage_disposal', universal_ingredient(), '1 minecraft:lava', None, None)
    
def generate_crafting_recipes():
    print('\tGenerating crafting recipes...')
    damage_shapeless(rm, ('crafting', 'trimmed_feather'), ('#tfc:knives', 'minecraft:feather'), 'artisanal:trimmed_feather')
    advanced_shapeless(rm, ('crafting', 'tempered_feather'), utils.ingredient_list(('artisanal:soaked_feather', heatable_ingredient('#forge:sand', 350))), {'item': 'artisanal:tempered_feather'})
    damage_shapeless(rm, ('crafting', 'quill'), ('#tfc:knives', 'artisanal:tempered_feather'), 'artisanal:quill')
    
    
    rm.crafting_shapeless(('crafting', 'writable_book'), ('minecraft:book', 'minecraft:black_dye', 'artisanal:quill'), 'minecraft:writable_book')
    rm.crafting_shapeless(('crafting', 'writable_book_from_dye'), ('minecraft:book', fluid_item_ingredient('100 tfc:black_dye'), 'artisanal:quill'), 'minecraft:writable_book')
    disable_recipe(rm, 'minecraft:writable_book')
    
    for wood in WOODS:
        rm.crafting_shaped(('crafting', 'wood', f'{wood}_scribing_table'), ['Q B', 'XXX', 'Y Y'], {'Q': 'artisanal:quill', 'B': 'minecraft:black_dye', 'X': f'tfc:wood/planks/{wood}_slab', 'Y': f'tfc:wood/planks/{wood}'}, f'tfc:wood/scribing_table/{wood}').with_advancement(f'tfc:wood/planks/{wood}')
        disable_recipe(rm, f'tfc:crafting/wood/{wood}_scribing_table')
    
    for wood in AFC_WOODS:
        rm.crafting_shaped(('crafting', 'wood', f'{wood}_scribing_table'), ['Q B', 'XXX', 'Y Y'], {'Q': 'artisanal:quill', 'B': 'minecraft:black_dye', 'X': f'afc:wood/planks/{wood}_slab', 'Y': f'afc:wood/planks/{wood}'}, f'afc:wood/scribing_table/{wood}')
        disable_recipe(rm, f'afc:crafting/wood/{wood}_scribing_table')
        
    
    damage_shapeless(rm, 'crafting/pumpkin_pie', (not_rotten('#tfc:foods/dough'), not_rotten('tfc:food/pumpkin_chunks'), '#tfc:knives', not_rotten('minecraft:egg'), not_rotten('#tfc:sweetener')), 'minecraft:pumpkin_pie', conditions=[forge_condition.mod_not_loaded('firmalife')]).with_advancement('tfc:pumpkin')
    rm.crafting_shaped('crafting/cake', ['AAA', 'BEB', 'CCC'], {'A': fluid_item_ingredient('100 #tfc:milks'), 'B': not_rotten('#tfc:sweetener'), 'E': not_rotten('minecraft:egg'), 'C': not_rotten('#tfc:foods/grains')}, 'tfc:cake').with_advancement('#tfc:foods/grains')
    disable_recipe(rm, 'tfc:crafting/cake')
    disable_recipe(rm, 'tfc:crafting/pumpkin_pie')
    
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        rm.crafting_shapeless(('crafting', 'metal', 'magnifying_glass', metal), (f'artisanal:metal/magnifying_glass_frame/{metal}', 'tfc:lens'), f'artisanal:metal/magnifying_glass/{metal}')
        extra_products_shapeless(rm, ('crafting', 'metal', 'magnifying_glass', f'{metal}_uncraft'), (f'artisanal:metal/magnifying_glass/{metal}'), f'artisanal:metal/magnifying_glass_frame/{metal}', 'tfc:lens')
    
    for grain in GRAINS:
        rm.crafting_shapeless(f'crafting/dough/{grain}', (not_rotten('tfc:food/%s_flour' % grain), fluid_item_ingredient('100 firmalife:yeast_starter'), not_rotten('#tfc:sweetener')), (4, 'firmalife:food/%s_dough' % grain)).with_advancement('tfc:food/%s_grain' % grain)
        disable_recipe(rm, f'firmalife:crafting/{grain}_dough')
    for gem in GEMS:
        catalyst_shapeless(rm, ('crafting', 'cut_gem', gem), ('tfc:ore/%s' % gem, 'tfc:sandpaper', '#artisanal:magnifying_glasses'), 'tfc:gem/%s' % gem).with_advancement('tfc:sandpaper')
        disable_recipe(rm, f'tfc:{gem}_cut')
    for i in range(1, 6 + 1):
        for metal in CAN_METALS:
            damage_shapeless(rm, ('crafting', 'metal', 'can', f'{metal}_{i}'), (heatable_ingredient(f'artisanal:metal/can/{metal}', 120), 'tfc:powder/flux', '#tfc:hammers', *([not_rotten('#artisanal:foods/can_be_canned')] * i)), item_stack_provider(f'artisanal:metal/can/{metal}_sealed', meal=canning_modifier, inherit_decay=1, copy_oldest_food=True, other_modifier='artisanal:homogenous_ingredients'), primary_ingredient='#artisanal:foods/can_be_canned')
        
        advanced_shapeless(rm, ('crafting', 'pot', f'{i}_rendered_fat'), ('artisanal:ceramic/small_pot', fluid_item_ingredient('100 #artisanal:rendered_fats'), 'tfc:powder/saltpeter', *([not_rotten('#artisanal:foods/can_be_potted')] * i)), item_stack_provider('artisanal:ceramic/closed_small_pot', meal=canning_modifier, inherit_decay=0.33, copy_oldest_food=True, other_modifier='artisanal:homogenous_ingredients'), primary_ingredient='#artisanal:foods/can_be_potted')
        advanced_shapeless(rm, ('crafting', 'pot', f'{i}_butter'), ('artisanal:ceramic/small_pot', 'firmalife:food/butter', 'tfc:powder/saltpeter', *([not_rotten('#artisanal:foods/can_be_potted')] * i)), item_stack_provider('artisanal:ceramic/closed_small_pot', meal=canning_modifier, remove_butter=True, inherit_decay=0.33, copy_oldest_food=True, other_modifier='artisanal:homogenous_ingredients'), primary_ingredient='#artisanal:foods/can_be_potted')
        
    for metal in CAN_METALS:
        for can_status in CAN_STATUSES:
            rm.recipe(('crafting', 'metal', 'open_can', f'{metal}_{can_status}_hammer'), 'tfc:extra_products_shapeless_crafting',
                {
                    "__comment__": "This file was automatically created by mcresources",
                    "recipe": {
                        "type": "tfc:damage_inputs_shapeless_crafting",
                        "recipe": {
                            "type": "tfc:advanced_shapeless_crafting",
                            "ingredients": [utils.ingredient(f'artisanal:metal/can/{metal}_{can_status}'), utils.ingredient("#tfc:hammers")],
                            "result": item_stack_provider(other_modifier="artisanal:extract_canned_food", copy_food=(can_status == 'sealed')),
                            "primary_ingredient": utils.ingredient(f"artisanal:metal/can/{metal}_{can_status}")
                        }
                    },
                    "extra_products": [
                        item_stack_provider(f"artisanal:metal/can/{metal}_dirty_dented")
                    ]
                }
            )
            rm.recipe(('crafting', 'metal', 'open_can', f'{metal}_{can_status}_can_opener'), 'tfc:extra_products_shapeless_crafting',
                {
                    "__comment__": "This file was automatically created by mcresources",
                    "recipe": {
                        "type": "tfc:damage_inputs_shapeless_crafting",
                        "recipe": {
                            "type": "tfc:advanced_shapeless_crafting",
                            "ingredients": [utils.ingredient(f'artisanal:metal/can/{metal}_{can_status}'), utils.ingredient("#artisanal:can_openers")],
                            "result": item_stack_provider(other_modifier="artisanal:extract_canned_food", copy_food=(can_status == 'sealed')),
                            "primary_ingredient": utils.ingredient(f"artisanal:metal/can/{metal}_{can_status}")
                        }
                    },
                    "extra_products": [
                        item_stack_provider(f"artisanal:metal/can/{metal}_dirty")
                    ]
                }
            )
        
    rm.recipe(('crafting', 'open_pot'), 'tfc:extra_products_shapeless_crafting',
        {
            "__comment__": "This file was automatically created by mcresources",
            "recipe": {
                "type": "tfc:damage_inputs_shapeless_crafting",
                "recipe": {
                    "type": "tfc:advanced_shapeless_crafting",
                    "ingredients": [utils.ingredient('artisanal:ceramic/closed_small_pot')],
                    "result": item_stack_provider(other_modifier="artisanal:extract_canned_food", copy_food=True),
                    "primary_ingredient": utils.ingredient("artisanal:ceramic/closed_small_pot")
                }
            },
            "extra_products": [
                item_stack_provider("artisanal:ceramic/dirty_small_pot")
            ]
        }
    )
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            rm.crafting_shaped(('crafting', 'metal', 'can_opener', metal), ['MBR', 'B  ', 'R  '], {'M': 'tfc:brass_mechanisms', 'B': f'artisanal:metal/circle_blade/{metal}', 'R': '#artisanal:rods/metal'}, f'artisanal:metal/can_opener/{metal}')
    
    for metal in CAN_METALS:
        advanced_shapeless(rm, ('crafting', 'metal', f'remove_{metal}_can_traits'), f'artisanal:metal/can/{metal}_sterilized', remove_many_traits(item_stack_provider(f'artisanal:metal/can/{metal}_sterilized', other_modifier='artisanal:copy_dynamic_food'), 'tfc:charcoal_grilled', 'tfc:wood_grilled', 'tfc:burnt_to_a_crisp'), primary_ingredient=f'artisanal:metal/can/{metal}_sterilized')
    
    
    for metal, metal_data in STEELS.items():
        if metal == 'steel':
            result = 'minecraft:flint_and_steel'
        else:
            result = f'artisanal:metal/flint_and/{metal}'
        
        advanced_shapeless(rm, ('crafting', 'metal', 'flint_and', metal), (f'artisanal:metal/striker/{metal}', 'minecraft:flint'), item_stack_provider(result, copy_forging=True), f'artisanal:metal/striker/{metal}')
        advanced_shapeless(rm, ('crafting', 'metal', 'ingot', f'high_carbon_{metal}'), (heatable_ingredient(f'tfc:metal/ingot/{metal}', metal_data.melt_temperature * 0.8), 'tfc:powder/charcoal'), item_stack_provider(f'tfc:metal/ingot/high_carbon_{metal}', copy_heat=True), f'tfc:metal/ingot/{metal}')
    
    disable_recipe(rm, 'tfc:crafting/vanilla/flint_and_steel')
    
    for cleanable in CLEANABLES:
        specific_no_remainder_shapeless(rm, ('crafting', 'clean', cleanable.item_name, 'water'), (fluid_item_ingredient('100 minecraft:water'), cleanable.input_item), utils.item_stack(cleanable.output_item), primary_ingredient=cleanable.input_item)
        specific_no_remainder_shapeless(rm, ('crafting', 'clean', cleanable.item_name, 'soapy_water'), (fluid_item_ingredient('100 artisanal:soapy_water'), cleanable.input_item), utils.item_stack(cleanable.output_item), primary_ingredient=cleanable.input_item)
    
    rm.crafting_shapeless(('crafting', 'aggregate'), ('#forge:gravel', '#forge:sand', '#forge:gravel', '#forge:sand', 'tfc:powder/lime', '#forge:sand', '#forge:gravel', '#forge:sand', '#forge:gravel'), (8, 'tfc:aggregate'))
    disable_recipe(rm, 'tfc:crafting/aggregate')
    
    for i in range(1, 8 + 1):
        max_amount = 100 * i
        min_amount = (100 * (i - 1)) + 1
        no_remainder_shapeless(rm, ('crafting', 'milk', f'cow_{i}'), (fluid_item_ingredient(f'{min_amount} minecraft:water'), *['artisanal:powdered_milk'] * i), item_stack_provider('tfc:ceramic/jug', modify_fluid=f'{max_amount} minecraft:milk'), primary_ingredient=fluid_item_ingredient(f'{min_amount} minecraft:water'))
        no_remainder_shapeless(rm, ('crafting', 'milk', f'goat_{i}'), (fluid_item_ingredient(f'{min_amount} minecraft:water'), *['artisanal:powdered_goat_milk'] * i), item_stack_provider('tfc:ceramic/jug', modify_fluid=f'{max_amount} firmalife:goat_milk'), primary_ingredient=fluid_item_ingredient(f'{min_amount} minecraft:water'), conditions=[forge_condition.mod_loaded('firmalife')])
        no_remainder_shapeless(rm, ('crafting', 'milk', f'yak_{i}'), (fluid_item_ingredient(f'{min_amount} minecraft:water'), *['artisanal:powdered_yak_milk'] * i), item_stack_provider('tfc:ceramic/jug', modify_fluid=f'{max_amount} firmalife:yak_milk'), primary_ingredient=fluid_item_ingredient(f'{min_amount} minecraft:water'), conditions=[forge_condition.mod_loaded('firmalife')])
    
    disable_recipe(rm, 'tfc:crafting/bloomery')
    rm.crafting_shaped(('crafting', 'bloomery'), ('XXX', 'X X', 'XXX'), {'X': '#artisanal:bloomery_sheets'}, 'tfc:bloomery')
    
    advanced_shapeless(rm, ('crafting', 'animal_fat'), ('#artisanal:fats',), item_stack_provider('artisanal:animal_fat', only_if_generic_animal_fat=True))
    
    rm.crafting_shapeless(('crafting', 'stone', 'flint_and', 'pyrite'), ('tfc:ore/pyrite', 'minecraft:flint'), 'artisanal:stone/flint_and/pyrite')
    rm.crafting_shapeless(('crafting', 'stone', 'flint_and', 'cut_pyrite'), ('tfc:gem/pyrite', 'minecraft:flint'), 'artisanal:stone/flint_and/cut_pyrite')
    
    damage_shaped(rm, ('crafting', 'sugar'), ['N', 'S', 'T'], {'N': 'artisanal:non_perishable_sugar', 'S': heatable_ingredient('tfc:powder/sulfur', SULFUR_BURN), 'T': '#tfc:tuyeres'}, 'minecraft:sugar')
    
    specific_no_remainder_damage_shaped(
        rm,
        ('crafting', 'sulfuric_acid'),
        ('W', 'S', 'T'),
        {
            'W': fluid_item_ingredient('100 minecraft:water', utils.ingredient('#tfc:glass_bottles')),
            'S': heatable_ingredient('tfc:powder/sulfur', SULFUR_BURN),
            'T': '#tfc:tuyeres'
        },
        item_stack_provider('tfc:ceramic/jug', modify_fluid=f'500 artisanal:sulfuric_acid'),
        (0, 0)
    )
    for metal in DRUM_METALS:
        rm.crafting_shaped(('crafting', 'metal', 'drum', metal), ('X X', 'X X', 'XXX'), {'X': f'tfc:metal/sheet/{metal}'}, f'artisanal:metal/drum/{metal}')
    
    damage_shapeless(rm, ('crafting', 'ceramic', 'unfired_brick'), ('#artisanal:brick_molds', 'minecraft:clay_ball', 'minecraft:clay_ball'), 'tfc:ceramic/unfired_brick')
    rm.crafting_shapeless(('crafting', 'powder', 'sulfur'), ('tfc:powder/pyrite'), 'tfc:powder/sulfur')
    
def generate_glassworking_recipes():
    print("\tGenerating glassworking recipes")
    
    glass_recipe(rm, ('orange_glass_block'), ['sulfur', 'basin_pour'], 'tfc:silica_glass_batch', 'minecraft:orange_stained_glass')
    glass_recipe(rm, ('orange_glass_pane'), ['sulfur', 'table_pour'], 'tfc:silica_glass_batch', 'tfc:orange_poured_glass')
    
    disable_recipe(rm, 'tfc:glassworking/orange_glass_block')
    disable_recipe(rm, 'tfc:glassworking/orange_glass_pane')
    
    
def generate_knapping_recipes():
    print("\tGenerating knapping recipes...")
    clay_knapping(rm, ('unfired_small_pot'), (' XX  ', 'XX   ', 'X X X', '  XXX', '  XXX'), 'artisanal:ceramic/unfired_small_pot', False)
    
    
def generate_heat_recipes():
    print("\tGenerating heat recipes...")
    
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        heat_recipe(rm, ('metal', 'magnifying_glass', metal), f'artisanal:metal/magnifying_glass/{metal}', metal_data.melt_temperature, 'tfc:lens', melt_metal(metal, 50))
        heat_recipe(rm, ('metal', 'magnifying_glass_frame', metal), f'artisanal:metal/magnifying_glass_frame/{metal}', metal_data.melt_temperature, None, melt_metal(metal, 50))
    
    for metal in CAN_METALS:
        heat_recipe(rm, ('metal', 'can', f'{metal}_sterilized'), not_rotten(f'artisanal:metal/can/{metal}_sealed'), 150, remove_many_traits(item_stack_provider(f'artisanal:metal/can/{metal}_sterilized', other_modifier='artisanal:copy_dynamic_food_never_expires'), 'tfc:charcoal_grilled', 'tfc:wood_grilled', 'tfc:burnt_to_a_crisp'))
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            heat_recipe(rm, ('metal', 'circle_blade', metal), f'artisanal:metal/circle_blade/{metal}', metal_data.melt_temperature, result_fluid=melt_metal(metal, 50))
            heat_recipe(rm, ('metal', 'brick_mold', metal), f'artisanal:metal/brick_mold/{metal}', metal_data.melt_temperature, result_fluid=melt_metal(metal, 50), use_durability=True)
    
    heat_recipe(rm, ('metal', 'striker', "steel"), f'artisanal:metal/striker/steel', METALS['steel'].melt_temperature, result_fluid='100 tfc:metal/pig_iron')
    heat_recipe(rm, ('metal', 'striker', "black_steel"), f'artisanal:metal/striker/black_steel', METALS['black_steel'].melt_temperature, result_fluid='100 tfc:metal/weak_steel')
    heat_recipe(rm, ('metal', 'striker', "blue_steel"), f'artisanal:metal/striker/blue_steel', METALS['blue_steel'].melt_temperature, result_fluid='100 tfc:metal/weak_blue_steel')
    heat_recipe(rm, ('metal', 'striker', "red_steel"), f'artisanal:metal/striker/red_steel', METALS['red_steel'].melt_temperature, result_fluid='100 tfc:metal/weak_red_steel')
    
    heat_recipe(rm, ('ceramic', 'unfired_small_pot'), 'artisanal:ceramic/unfired_small_pot', POTTERY_MELT, 'artisanal:ceramic/small_pot')
    
    heat_recipe(rm, ('metal', 'pickled_double_sheet', 'wrought_iron'), 'artisanal:metal/pickled_double_sheet/wrought_iron', METALS['wrought_iron'].melt_temperature, result_fluid=f'{melt_metal("wrought_iron", 400)}')
    heat_recipe(rm, ('metal', 'pickled_double_sheet', 'steel'), 'artisanal:metal/pickled_double_sheet/steel', METALS['steel'].melt_temperature, result_fluid=f'{melt_metal("steel", 400)}')
    
    disable_recipe(rm, 'tfc:heating/jar_lid')
    heat_recipe(rm, ('jar_lid'), 'tfc:jar_lid', METALS['tin'].melt_temperature, result_fluid='6 tfc:metal/tin', conditions=[
        forge_condition.or_(
            forge_condition.mod_loaded('lithicaddon'),
            forge_condition.mod_not_loaded('firmalife')
        )
    ])
    
    for metal in DRUM_METALS:
        metal_data = METALS[metal]
        heat_recipe(rm, ('metal', 'drum', metal), f'artisanal:metal/drum/{metal}', metal_data.melt_temperature, result_fluid=melt_metal(metal, 1400))
    
    heat_recipe(rm, ('metal', 'stainless_steelplate'), 'artisanal:metal/stainless_steelplate', METALS['stainless_steel'].melt_temperature, result_fluid=melt_metal('stainless_steel', CANS_MB_AMOUNTS['stainless_steel']))
    heat_recipe(rm, ('metal', 'can', 'stainless_steel'), 'artisanal:metal/can/stainless_steel', METALS['stainless_steel'].melt_temperature, result_fluid=melt_metal('stainless_steel', CANS_MB_AMOUNTS['stainless_steel']))
    
def generate_juicing_recipes():
    print('\tGenerating juicing recipes...')
    juicing_recipe(rm, ('apple_juice_from_red'), not_rotten('tfc:food/red_apple'), '200 artisanal:apple_juice')
    juicing_recipe(rm, ('apple_juice_from_green'), not_rotten('tfc:food/green_apple'), '200 artisanal:apple_juice')
    juicing_recipe(rm, ('lemon_juice'), not_rotten('tfc:food/lemon'), '100 artisanal:lemon_juice')
    juicing_recipe(rm, ('orange_juice'), not_rotten('tfc:food/orange'), '200 artisanal:orange_juice')
    juicing_recipe(rm, ('peach_juice'), not_rotten('tfc:food/peach'), '200 artisanal:peach_juice')
    juicing_recipe(rm, ('pineapple_juice'), not_rotten('firmalife:food/pineapple'), '200 artisanal:pineapple_juice')
    juicing_recipe(rm, ('carrot_juice'), not_rotten('tfc:food/carrot'), '100 artisanal:carrot_juice')
    juicing_recipe(rm, ('tomato_juice'), not_rotten('tfc:food/tomato'), '200 artisanal:tomato_juice')
    juicing_recipe(rm, ('sugarcane_juice'), not_rotten('artisanal:food/cleaned_sugarcane'), '200 artisanal:sugarcane_juice')
    
def generate_mixing_recipes():
    mixing_recipe(rm, 'pie_dough', ingredients=[not_rotten('firmalife:food/butter'), not_rotten('#tfc:foods/flour'), not_rotten('#tfc:sweetener')], fluid='1000 minecraft:water', output_item='firmalife:food/pie_dough')
    mixing_recipe(rm, 'pumpkin_pie_dough', ingredients=[utils.ingredient('#firmalife:foods/raw_eggs'), not_rotten('tfc:food/pumpkin_chunks'), not_rotten('tfc:food/pumpkin_chunks'), not_rotten('#tfc:foods/flour'), not_rotten('#tfc:sweetener')], fluid='1000 minecraft:water', output_item='firmalife:food/pumpkin_pie_dough')
    mixing_recipe(rm, 'dark_chocolate_blend', ingredients=[not_rotten(utils.ingredient('#tfc:sweetener')), not_rotten('firmalife:food/cocoa_powder'), not_rotten('firmalife:food/cocoa_powder')], fluid='1000 #tfc:milks', output_item='2 firmalife:food/dark_chocolate_blend')
    mixing_recipe(rm, 'white_chocolate_blend', ingredients=[not_rotten(utils.ingredient('#tfc:sweetener')), not_rotten('firmalife:food/cocoa_butter'), not_rotten('firmalife:food/cocoa_butter')], fluid='1000 #tfc:milks', output_item='2 firmalife:food/white_chocolate_blend')
    mixing_recipe(rm, 'milk_chocolate_blend', ingredients=[not_rotten(utils.ingredient('#tfc:sweetener')), not_rotten('firmalife:food/cocoa_butter'), not_rotten('firmalife:food/cocoa_powder')], fluid='1000 #tfc:milks', output_item='2 firmalife:food/milk_chocolate_blend')
    mixing_recipe(rm, 'vanilla_ice_cream', ingredients=[not_rotten(utils.ingredient('#tfc:sweetener')), utils.ingredient('firmalife:spice/vanilla'), utils.ingredient('firmalife:ice_shavings')], fluid='1000 firmalife:cream', output_item='2 firmalife:food/vanilla_ice_cream')
    mixing_recipe(rm, 'cookie_dough', ingredients=[not_rotten('#firmalife:foods/raw_eggs'), utils.ingredient('firmalife:spice/vanilla'), not_rotten('firmalife:food/butter'), not_rotten('#tfc:sweetener'), not_rotten('#tfc:foods/flour')], output_item='4 firmalife:food/cookie_dough')
    
    disable_recipe(rm, 'firmalife:mixing_bowl/pie_dough')
    disable_recipe(rm, 'firmalife:mixing_bowl/pumpkin_pie_dough')
    disable_recipe(rm, 'firmalife:mixing_bowl/dark_chocolate_blend')
    disable_recipe(rm, 'firmalife:mixing_bowl/white_chocolate_blend')
    disable_recipe(rm, 'firmalife:mixing_bowl/milk_chocolate_blend')
    disable_recipe(rm, 'firmalife:mixing_bowl/vanilla_ice_cream')
    disable_recipe(rm, 'firmalife:mixing_bowl/cookie_dough')
    
def generate_pot_recipes():
    print('\tGenerating pot recipes...')
    
    for i in range(1, 5 + 1):
        simple_pot_recipe(rm, ('render', 'tallow', f'{i}_suet'), [utils.ingredient('artisanal:suet')] * i, f'{100 * i} minecraft:water', f'{100 * i} tfc:tallow', None, 2000, 600)
        simple_pot_recipe(rm, ('render', 'lard', f'{i}_pork'), [utils.ingredient('artisanal:pork_fat')] * i, f'{100 * i} minecraft:water', f'{100 * i} artisanal:lard', None, 2000, 600)
        simple_pot_recipe(rm, ('render', 'lard', f'{i}_bear'), [utils.ingredient('artisanal:bear_fat')] * i, f'{100 * i} minecraft:water', f'{100 * i} artisanal:lard', None, 2000, 600)
        simple_pot_recipe(rm, ('render', 'schmaltz', f'{i}_poultry'), [utils.ingredient('artisanal:poultry_fat')] * i, f'{100 * i} minecraft:water', f'{100 * i} artisanal:schmaltz', None, 2000, 600)
        simple_pot_recipe(rm, ('render', 'tallow', f'{i}_animal'), [utils.ingredient('artisanal:animal_fat')] * i, f'{100 * i} minecraft:water', f'{100 * i} tfc:tallow', None, 2000, 600)
    
    scalable_pot_recipe(rm, ('milk', 'condensed', 'cow'), '2 minecraft:milk', '1 artisanal:condensed_milk', None, 3000, 100)
    scalable_pot_recipe(rm, ('milk', 'condensed', 'goat'), '2 firmalife:goat_milk', '1 artisanal:condensed_goat_milk', None, 3000, 100, conditions=[forge_condition.mod_loaded('firmalife')])
    scalable_pot_recipe(rm, ('milk', 'condensed', 'yak'), '2 firmalife:yak_milk', '1 artisanal:condensed_yak_milk', None, 3000, 100, conditions=[forge_condition.mod_loaded('firmalife')])
    scalable_pot_recipe(rm, ('milk', 'flakes', 'cow'), '100 artisanal:condensed_milk', None, [{'item': 'artisanal:milk_flakes'}], 3000, 100)
    scalable_pot_recipe(rm, ('milk', 'flakes', 'goat'), '100 artisanal:condensed_goat_milk', None, [{'item': 'artisanal:goat_milk_flakes'}], 3000, 100)
    scalable_pot_recipe(rm, ('milk', 'flakes', 'yak'), '100 artisanal:condensed_yak_milk', None, [{'item': 'artisanal:yak_milk_flakes'}], 3000, 100)
    
    scalable_pot_recipe(rm, ('salt'), '125 tfc:salt_water', None, [{'item': 'tfc:powder/salt'}], 2000, 300)
    scalable_pot_recipe(rm, ('perishable_sugar'), '200 artisanal:sugarcane_juice', '20 artisanal:molasses', [item_stack_provider('artisanal:perishable_sugar')], 2000, 107)
    scalable_pot_recipe(rm, ('perishable_sugar_from_filtered'), '200 artisanal:filtered_sugarcane_juice', '20 artisanal:molasses', [item_stack_provider('artisanal:perishable_sugar')], 2000, 107)
    scalable_pot_recipe(rm, ('non_perishable_sugar'), '200 artisanal:clarified_sugarcane_juice', '20 artisanal:molasses', [{'item': 'artisanal:non_perishable_sugar'}], 2000, 107)
    scalable_pot_recipe(rm, ('maple_sap_concentrate'), '10 afc:maple_sap', '1 afc:maple_sap_concentrate')
    scalable_pot_recipe(rm, ('maple_syrup'), '5 afc:maple_sap_concentrate', '1 afc:maple_syrup')
    scalable_pot_recipe(rm, ('birch_sap_concentrate'), '10 afc:birch_sap', '1 afc:birch_sap_concentrate')
    scalable_pot_recipe(rm, ('birch_syrup'), '5 afc:birch_sap_concentrate', '1 afc:birch_syrup')
    
    disable_recipe(rm, 'afc:pot/maple_concentrate')
    disable_recipe(rm, 'afc:pot/maple_syrup')
    disable_recipe(rm, 'afc:pot/maple_syrup_half_batch')
    disable_recipe(rm, 'afc:pot/birch_concentrate')
    disable_recipe(rm, 'afc:pot/birch_syrup')
    
    simple_pot_recipe(rm, 'chocolate', [not_rotten(utils.ingredient('#tfc:sweetener')), not_rotten('#firmalife:foods/chocolate')], '1000 #tfc:milks', output_fluid='1000 firmalife:chocolate')
    disable_recipe(rm, 'firmalife:pot/chocolate')
    
    for count in (2, 3, 4):
        for fruit in JAR_FRUITS:
            jam_food = not_rotten(utils.ingredient('tfc:food/%s' % fruit))
            rm.recipe(('pot', 'jam', f'{fruit}_{count}'), 'tfc:pot_jam', {
                'ingredients': [jam_food] * count + [not_rotten(utils.ingredient('#tfc:sweetener'))],
                'fluid_ingredient': fluid_stack_ingredient('100 minecraft:water'),
                'duration': 500,
                'temperature': 300,
                'result': utils.item_stack('%s tfc:jar/%s' % (count, fruit)),
                'texture': 'tfc:block/jar/%s' % fruit
            }, conditions=[forge_condition.mod_not_loaded('lithicaddon')])
            disable_recipe(rm, f'tfc:pot/jam_{fruit}_{count}')
            
            jam_food = not_rotten(utils.ingredient('tfc:food/%s' % fruit))
            rm.recipe(('pot', 'jam', 'lithic', f'{fruit}_{count}'), 'tfc:pot_jam', {
                'ingredients': [jam_food] * count + [not_rotten(utils.ingredient('#tfc:sweetener'))],
                'fluid_ingredient': fluid_stack_ingredient('100 minecraft:water'),
                'duration': 500,
                'temperature': 300,
                'result': utils.item_stack('%s tfc:jar/%s_unsealed' % (count, fruit)),
                'texture': 'tfc:block/jar/%s' % fruit
            }, conditions=[forge_condition.mod_loaded('lithicaddon')])
            
            disable_recipe(rm, f'tfc:crafting/unseal_{fruit}_jar')
            extra_products_shapeless(rm, ('crafting', 'unseal', fruit), (f'tfc:jar/{fruit}'), item_stack_provider(f'tfc:jar/{fruit}_unsealed', copy_food=True), ('tfc:jar_lid'), primary_ingredient=f'tfc:jar/{fruit}', conditions=forge_condition.mod_not_loaded('lithicaddon'))
            
        for fruit in FL_FRUITS:
            ingredient = not_rotten(has_trait('firmalife:food/%s' % fruit, 'firmalife:dried', True))
            rm.recipe(('pot', 'jam', f'{fruit}_{count}'), 'tfc:pot_jam', {
                'ingredients': [ingredient] * count + [not_rotten('#tfc:sweetener')],
                'fluid_ingredient': fluid_stack_ingredient('100 minecraft:water'),
                'duration': 500,
                'temperature': 300,
                'result': utils.item_stack('%s firmalife:jar/%s' % (count, fruit)),
                'texture': 'firmalife:block/jar/%s' % fruit
            }, conditions=[forge_condition.mod_not_loaded('lithicaddon')])
            disable_recipe(rm, f'firmalife:pot/jam_{fruit}_{count}')
            
            rm.recipe(('pot', 'jam', 'lithic', f'{fruit}_{count}'), 'tfc:pot_jam', {
                'ingredients': [ingredient] * count + [not_rotten('#tfc:sweetener')],
                'fluid_ingredient': fluid_stack_ingredient('100 minecraft:water'),
                'duration': 500,
                'temperature': 300,
                'result': utils.item_stack('%s firmalife:jar/%s_unsealed' % (count, fruit)),
                'texture': 'firmalife:block/jar/%s' % fruit
            }, conditions=[forge_condition.mod_loaded('lithicaddon')])
            
            disable_recipe(rm, f'firmalife:crafting/unseal_{fruit}_jar')
            extra_products_shapeless(
                rm, 
                ('crafting', 'unseal', fruit), 
                (f'firmalife:jar/{fruit}'), 
                item_stack_provider(f'firmalife:jar/{fruit}_unsealed', copy_food=True), 
                ('tfc:jar_lid'), 
                primary_ingredient=f'firmalife:jar/{fruit}', 
                conditions=[forge_condition.mod_not_loaded('lithicaddon')]
                
            )
            
    
def generate_quern_recipes():
    print('\tGenerating quern recipes...')
    quern_recipe(rm, ('food', 'cleaned_sugarcane'), not_rotten('artisanal:food/cleaned_sugarcane'), 'artisanal:bagasse')
    quern_recipe(rm, ('food', 'red_apple'), not_rotten('tfc:food/red_apple'), 'artisanal:food/fruit_mash')
    quern_recipe(rm, ('food', 'green_apple'), not_rotten('tfc:food/green_apple'), 'artisanal:food/fruit_mash')
    quern_recipe(rm, ('food', 'lemon'), not_rotten('tfc:food/lemon'), 'artisanal:food/fruit_mash')
    quern_recipe(rm, ('food', 'orange'), not_rotten('tfc:food/orange'), 'artisanal:food/fruit_mash')
    quern_recipe(rm, ('food', 'peach'), not_rotten('tfc:food/peach'), 'artisanal:food/fruit_mash')
    quern_recipe(rm, ('food', 'pineapple'), not_rotten('firmalife:food/pineapple'), 'artisanal:food/fruit_mash')
    quern_recipe(rm, ('food', 'carrot'), not_rotten('tfc:food/carrot'), 'artisanal:food/carrot_mash')
    quern_recipe(rm, ('food', 'tomato'), not_rotten('tfc:food/tomato'), 'artisanal:food/tomato_mash')
    quern_recipe(rm, ('powdered_milk'), 'artisanal:milk_flakes', 'artisanal:powdered_milk', 2)
    quern_recipe(rm, ('powdered_goat_milk'), 'artisanal:goat_milk_flakes', 'artisanal:powdered_goat_milk', 2)
    quern_recipe(rm, ('powdered_yak_milk'), 'artisanal:yak_milk_flakes', 'artisanal:powdered_yak_milk', 2)
    
    disable_recipe(rm, 'firmaciv:quern/pyrite')
    

def generate_vat_recipes():
    print('\tGenerating vat recipes...')
    vat_recipe(rm, 'sugar_water', not_rotten('#tfc:sweetener'), '1000 minecraft:water', output_fluid='500 firmalife:sugar_water')
    vat_recipe(rm, 'perishable_sugar', None, '200 artisanal:sugarcane_juice', 'artisanal:perishable_sugar', '20 artisanal:molasses', temp=107)
    vat_recipe(rm, 'perishable_sugar_from_filtered', None, '200 artisanal:filtered_sugarcane_juice', 'artisanal:perishable_sugar', '20 artisanal:molasses', temp=107)
    vat_recipe(rm, 'non_perishable_sugar', None, '200 artisanal:clarified_sugarcane_juice', 'artisanal:non_perishable_sugar', '20 artisanal:molasses', temp=107)
    
    vat_recipe(rm, ('render', 'tallow'), 'artisanal:suet', '100 minecraft:water', output_fluid='100 tfc:tallow')
    vat_recipe(rm, ('render', 'lard'), 'artisanal:pork_fat', '100 minecraft:water', output_fluid='100 artisanal:lard')
    vat_recipe(rm, ('render', 'lard_from_bear'), 'artisanal:bear_fat', '100 minecraft:water', output_fluid='100 artisanal:lard')
    vat_recipe(rm, ('render', 'schmaltz'), 'artisanal:poultry_fat', '100 minecraft:water', output_fluid='100 artisanal:schmaltz')
    vat_recipe(rm, ('render', 'tallow_from_animal'), 'artisanal:animal_fat', '100 minecraft:water', output_fluid='100 tfc:tallow')
    
    vat_recipe(rm, ('milk', 'condensed', 'cow'), None, '2 minecraft:milk', None, '1 artisanal:condensed_milk', length=3000, temp=100)
    vat_recipe(rm, ('milk', 'condensed', 'goat'), None, '2 firmalife:goat_milk', None, '1 artisanal:condensed_goat_milk', length=3000, temp=100)
    vat_recipe(rm, ('milk', 'condensed', 'yak'), None, '2 firmalife:yak_milk', None, '1 artisanal:condensed_yak_milk', length=3000, temp=100)
    vat_recipe(rm, ('milk', 'flakes', 'cow'), None, '100 artisanal:condensed_milk', 'artisanal:milk_flakes', length=3000, temp=100)
    vat_recipe(rm, ('milk', 'flakes', 'goat'), None, '100 artisanal:condensed_goat_milk', 'artisanal:goat_milk_flakes', length=3000, temp=100)
    vat_recipe(rm, ('milk', 'flakes', 'yak'), None, '100 artisanal:condensed_yak_milk', 'artisanal:yak_milk_flakes', length=3000, temp=100)
    
    vat_recipe(rm, 'salt', input_item=None, input_fluid='125 tfc:salt_water', output_item='tfc:powder/salt')
    
    disable_recipe(rm, 'firmalife:vat/sugar_water')
    
def generate_recipes():
    print('Generating recipes...')
    generate_anvil_recipes()
    generate_barrel_recipes()
    generate_crafting_recipes()
    generate_glassworking_recipes()
    generate_knapping_recipes()
    generate_heat_recipes()
    generate_juicing_recipes()
    generate_mixing_recipes()
    generate_pot_recipes()
    generate_quern_recipes()
    generate_vat_recipes()

def generate_block_tags():
    print('\tGenerating block tags...')
    block_and_item_tag(rm, 'metal/drums', *[f'artisanal:metal/drum/{metal}' for metal in DRUM_METALS])
    block_and_item_tag(rm, 'tfc:barrels', '#artisanal:metal/drums')
    block_and_item_tag(rm, 'minecraft:mineable/pickaxe', "#artisanal:metal/drums")

def generate_entity_tags():
    print('\tGenerating entity tags...')
    rm.entity_tag('drops_suet', 'tfc:cow', 'tfc:goat', 'tfc:yak', 'tfc:alpaca', 'tfc:sheep', 'tfc:musk_ox', 'tfc:deer', 'tfc:caribou', 'tfc:bongo', 'tfc:gazelle', 'tfc:moose', 'tfc:wildebeest')
    rm.entity_tag('drops_pork_fat', 'tfc:pig', 'tfc:boar')
    rm.entity_tag('drops_bear_fat', '#tfc:bears', 'tfc:panda')
    rm.entity_tag('drops_poultry_fat', 'tfc:chicken', 'tfc:duck', 'tfc:quail', 'tfc:grouse', 'tfc:pheasant', 'tfc:turkey', 'tfc:peafowl')

def generate_fluid_tags():
    print('\tGenerating fluid tags...')
    rm.fluid_tag('rendered_fats', 'tfc:tallow', 'artisanal:lard', 'artisanal:schmaltz')
    rm.fluid_tag('acids', 'artisanal:sulfuric_acid', 'artisanal:lemon_juice')
    rm.fluid_tag('usable_in_drum', '#tfc:usable_in_barrel', '#artisanal:acids', 'tfc:metal/gold')
    rm.fluid_tag('usable_in_lava_drum', '#artisanal:usable_in_drum', 'minecraft:lava')
    rm.fluid_tag('tfc:ingredients', '#artisanal:rendered_fats', 'artisanal:soap', 'artisanal:soapy_water', 'artisanal:sugarcane_juice', 'artisanal:filtered_sugarcane_juice', 'artisanal:alkalized_sugarcane_juice', 'artisanal:clarified_sugarcane_juice', 'artisanal:molasses', 'artisanal:petroleum', 'artisanal:condensed_milk', 'artisanal:condensed_goat_milk', 'artisanal:condensed_yak_milk')
    rm.fluid_tag('tfc:drinkables', 'artisanal:sugarcane_juice', 'artisanal:molasses', 'artisanal:apple_juice', 'artisanal:carrot_juice', 'artisanal:diluted_lemon_juice', 'artisanal:orange_juice', 'artisanal:peach_juice', 'artisanal:pineapple_juice', 'artisanal:tomato_juice', 'artisanal:screwdriver')
    rm.fluid_tag('tfc:usable_in_jug', '#tfc:ingredients', '#artisanal:acids')
    
    rm.fluid_tag('alcohols/fruit', 'tfc:cider', optional_tag('#firmalife:wine'))
    rm.fluid_tag('alcohols/grain', 'tfc:beer', 'tfc:corn_whiskey', 'tfc:rye_whiskey', 'tfc:sake', 'tfc:whiskey')
    rm.fluid_tag('alcohols/vegetable', 'tfc:vodka')
    rm.fluid_tag('alcohols/fruit_and_veg', 'tfc:rum')
    rm.fluid_tag('alcohols/no_nutrition')
    


def generate_item_tags():
    print('\tGenerating item tags...')
    rm.item_tag('bloomery_sheets', *[f'tfc:metal/double_sheet/{metal}' for metal in BLOOMERY_SHEETS])
    rm.item_tag('firmalife:sweetener', 'artisanal:perishable_sugar', 'artisanal:non_perishable_sugar')
    rm.item_tag('fats', 'artisanal:bear_fat', 'artisanal:pork_fat', 'artisanal:poultry_fat', 'artisanal:suet', 'artisanal:animal_fat')
    rm.item_tag('magnifying_glasses', *[f'artisanal:metal/magnifying_glass/{metal}' for metal in MAGNIFYING_GLASS_METALS])
    rm.item_tag('crafting_catalysts', '#artisanal:magnifying_glasses')
    rm.item_tag('foods/can_be_canned', *[f'#tfc:foods/{tag}' for tag in CANNABLE_FOOD_TAGS], '#firmalife:foods/flatbreads', '#firmalife:foods/slices')
    rm.item_tag('foods/can_be_potted', *[f'#tfc:foods/{tag}' for tag in POTTABLE_FOOD_TAGS])
    rm.item_tag('brick_molds', *[f'artisanal:metal/brick_mold/{metal}' for metal in METALS if 'tool' in METALS[metal].types])
    rm.item_tag('can_openers', *[f'artisanal:metal/can_opener/{metal}' for metal in METALS if 'tool' in METALS[metal].types])
    rm.item_tag('rods/metal', *[f'tfc:metal/rod/{metal}' for metal in METALS if 'utility' in METALS[metal].types])
    rm.item_tag('metal/flint_and/colored_steel', 'artisanal:metal/flint_and/blue_steel', 'artisanal:metal/flint_and/red_steel')
    rm.item_tag('metal/sterilized_cans', *[f'artisanal:metal/can/{metal}_sterilized' for metal in CAN_METALS])
    
    
    rm.item_tag('tfc:firepit_kindling', 'artisanal:bagasse')
    rm.item_tag('tfc:starts_fires_with_durability', *[f'artisanal:metal/flint_and/{metal}' for metal in STEELS if metal != 'steel'], 'artisanal:stone/flint_and/pyrite', 'artisanal:stone/flint_and/cut_pyrite')
    rm.item_tag('tfc:compost_browns_high', 'artisanal:bagasse')
    rm.item_tag('tfc:dynamic_bowl_items', 'artisanal:dirty_bowl')
    rm.item_tag('tfc:firepit_fuel', 'artisanal:bagasse')
    rm.item_tag('tfc:foods', '#tfc:sweetener')
    rm.item_tag('tfc:foods/fruits', 'artisanal:food/fruit_mash')
    rm.item_tag('tfc:foods/vegetables', 'artisanal:food/carrot_mash', 'artisanal:food/tomato_mash')
    rm.item_tag('tfc:sweetener', 'artisanal:perishable_sugar', 'artisanal:non_perishable_sugar')
    rm.item_tag('tfc:usable_on_tool_rack', '#artisanal:magnifying_glasses')

def generate_tags():
    print('Generating tags...')
    generate_block_tags()
    generate_entity_tags()
    generate_fluid_tags()
    generate_item_tags()

def main():
    generate_advancements()
    generate_data()
    generate_loot_modifiers()
    generate_misc_lang()
    generate_models()
    generate_recipes()
    generate_tags()
    
    rm.flush()
    
    
    
main()