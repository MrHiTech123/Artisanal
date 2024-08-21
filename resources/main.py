import json

from alcs_n_russians_funcs import *
from mcresources import ResourceManager


SIMPLE_FLUIDS = ('lard', 'schmaltz', 'soapy_water', 'soap', 'sugarcane_juice', 'filtered_sugarcane_juice', 'alkalized_sugarcane_juice', 'clarified_sugarcane_juice', 'molasses', 'condensed_milk', 'petroleum')
AFC_WOODS = ('eucalyptus', 'mahogany', 'baobab', 'hevea', 'tualang', 'teak', 'cypress', 'fig', 'ironwood', 'ipe')
MAGNIFYING_GLASS_METALS = ('bismuth', 'brass', 'gold', 'rose_gold', 'silver', 'sterling_silver', 'tin')
CANNABLE_FOOD_TAGS = ('breads', 'dairy', 'flour', 'fruits', 'grains', 'meats', 'vegetables')
OPENABLE_CAN_ITEMS = ('sterilized_tin_can', 'sealed_tin_can')



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

def advancement(rm: ResourceManager, name_parts: tuple, icon: dict[str, Any] | Sequence | str | int | bool | None, title: str, description: str, parent: str, criteria: dict[str, Any] | Sequence | str | int | bool | None, requirements: Sequence[Sequence[str]] | None = None, rewards: dict[str, Any] | Sequence | str | int | bool | None = None):
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
        'hidden': False,
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
 
def scalable_pot_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, fluid: str, output_fluid: str = None, output_items: Json = None, duration: int = 2000, temp: int = 300):
    rm.recipe(('pot', name_parts), 'artisanal:scalable_pot', {
        'ingredients': [],
        'fluid_ingredient': fluid_stack_ingredient(fluid),
        'duration': duration,
        'temperature': temp,
        'fluid_output': fluid_stack(output_fluid) if output_fluid is not None else None,
        'item_output': [utils.item_stack(item) for item in output_items] if output_items is not None else None
    })



def generate_advancements():
    print('Generating advancements...')
    advancement(rm, ('story', 'magnifying_glass'), 'artisanal:metal/magnifying_glass/brass', 'Inspector Detector', 'Craft a Magnifying Glass', 'tfc:story/lens', inventory_changed('#artisanal:magnifying_glasses'))
    advancement(rm, ('story', 'perishable_sugar'), 'artisanal:perishable_sugar', 'Sweet Tooth', 'Create Perishable Sugar', 'tfc:story/barrel', inventory_changed('artisanal:perishable_sugar'))
    advancement(rm, ('story', 'non_perishable_sugar'), 'artisanal:non_perishable_sugar', 'Everlasting Sweet Tooth', 'Create Non-Perishable Sugar', 'artisanal:story/perishable_sugar', inventory_changed('artisanal:non_perishable_sugar'))
    advancement(rm, ('story', 'powdered_milk'), 'artisanal:powdered_milk', 'Just Add Water', 'Create Powdered Milk', 'tfc:story/quern', inventory_changed('artisanal:powdered_milk'))
    advancement(rm, ('story', 'quill'), 'artisanal:quill', 'Not Quite Ballpoint', 'Create a Quill', 'tfc:story/barrel', inventory_changed('artisanal:quill'))
    advancement(rm, ('story', 'writable_book'), 'minecraft:writable_book', 'Bookkeeper', 'Create a Book and Quill', 'artisanal:story/quill', inventory_changed('minecraft:writable_book'))
    advancement(rm, ('story', 'soap'), 'artisanal:soap', 'Clean as a Whistle', 'Create Soap', 'tfc:story/barrel', inventory_changed('artisanal:soap'))
    

def generate_drinkables():
    print('\tGenerating drinkables...')
    drinkable(rm, ('molasses'), 'artisanal:molasses', thirst=-1, food={'hunger': 4, 'saturation': 0, 'vegetables': 3, 'fruit': 3})
    
def generate_lamp_fuels():
    print('\tGenerating lamp fuels...')
    lamp_fuel(rm, 'lard', 'artisanal:lard', 1800)
    lamp_fuel(rm, 'schmaltz', 'artisanal:schmaltz', 1800)

def generate_fuels():
    print('\tGenerating fuels...')
    generate_lamp_fuels()
    fuel_item(rm, ('dry_bagasse'), 'artisanal:dry_bagasse', 750, 350)
    
    
    
def generate_item_foods():
    print('\tGenerating item foods...')
    food_item(rm, ('cleaned_sugarcane'), 'artisanal:food/cleaned_sugarcane', Category.other, 4, 0, 0, 0.5)
    food_item(rm, ('perishable_sugar'), 'artisanal:perishable_sugar', Category.other, 0, 0, 0, 3)
    food_item(rm, ('non_perishable_sugar'), 'artisanal:non_perishable_sugar', Category.other, 0, 0, 0, 0)
    food_item(rm, ('sugar'), 'minecraft:sugar', Category.other, 0, 0, 0, 0)
    food_item(rm, ('maple_sugar'), 'afc:maple_sugar', Category.other, 0, 0, 0, 0, tag_as_food=False)
    food_item(rm, ('birch_sugar'), 'afc:birch_sugar', Category.other, 0, 0, 0, 0, tag_as_food=False)
    food_item(rm, ('honey'), 'firmalife:raw_honey', Category.other, 0, 0, 0, 0, tag_as_food=False)
    dynamic_food_item(rm, ('sealed_tin_can'), 'artisanal:metal/sealed_tin_can', 'dynamic')
    dynamic_food_item(rm, ('sterilized_tin_can'), 'artisanal:metal/sterilized_tin_can', 'dynamic')
    
def generate_item_heats():
    print('\tGenerating item heats...')
    item_heat(rm, ('sand'), '#forge:sand', 0.8, None, None)
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        item_heat(rm, ('metal', 'magnifying_glass', metal), f'artisanal:metal/magnifying_glass/{metal}', metal_data.ingot_heat_capacity() / 2, metal_data.melt_temperature, 50)
        item_heat(rm, ('metal', 'magnifying_glass_frame', metal), f'artisanal:metal/magnifying_glass_frame/{metal}', metal_data.ingot_heat_capacity() / 2, metal_data.melt_temperature, 50)
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            item_heat(rm, ('metal', 'circle_blade', metal), f'artisanal:metal/circle_blade/{metal}', metal_data.ingot_heat_capacity() / 2, metal_data.melt_temperature, 50)
    
    
    
    
    item_heat(rm, ('metal', 'tinplate'), 'artisanal:metal/tinplate', METALS['tin'].ingot_heat_capacity() / 2, METALS['tin'].melt_temperature, 150)
    item_heat(rm, ('metal', 'tin_can'), 'artisanal:metal/tin_can', METALS['tin'].ingot_heat_capacity() / 2, METALS['tin'].melt_temperature, 150)
    item_heat(rm, ('metal', 'sealed_tin_can'), 'artisanal:metal/sealed_tin_can', METALS['tin'].ingot_heat_capacity() / 2, METALS['tin'].melt_temperature, 150)
    item_heat(rm, ('metal', 'dented_tin_can'), 'artisanal:metal/dented_tin_can', METALS['tin'].ingot_heat_capacity() / 2, METALS['tin'].melt_temperature, 150)
    
def generate_data():
    print('Generating data...')
    generate_drinkables()
    generate_fuels()
    generate_item_foods()
    generate_item_heats()

def generate_loot_modifiers():
    print('Creating loot modifiers...')
    
    loot_modifiers = []
    loot_modifier_add_itemstack_min_max(rm, loot_modifiers, 'animals_drop_suet', '#artisanal:drops_suet', 'artisanal:suet', 1, 3)
    loot_modifier_add_itemstack_min_max(rm, loot_modifiers, 'animals_drop_pork_fat', '#artisanal:drops_pork_fat', 'artisanal:pork_fat', 1, 3)
    loot_modifier_add_itemstack_min_max(rm, loot_modifiers, 'animals_drop_bear_fat', '#artisanal:drops_bear_fat', 'artisanal:bear_fat', 1, 3)
    loot_modifier_add_itemstack_min_max(rm, loot_modifiers, 'animals_drop_poultry_fat', '#artisanal:drops_poultry_fat', 'artisanal:poultry_fat', 1, 1)
    
    forge_rm.data(('loot_modifiers', 'global_loot_modifiers'), {'replace': False, 'entries': loot_modifiers})

def generate_misc_lang():
    print('Generating misc lang...')
    rm.lang('tfc.jei.scalable_pot', 'Scalable Pot Recipe')
    rm.lang("block.tfc.fluid.limewater", "Slaked Lime")
    rm.lang("item.tfc.bucket.limewater", "Slaked Lime Bucket")
    rm.lang("fluid.tfc.limewater", "Slaked Lime")
    rm.lang("block.tfc.cauldron.limewater", "Slaked Lime Cauldron")
    rm.lang("item.minecraft.cooked_beef", "Whatever Food Was Inside the Can")

def generate_item_models():
    print('\tGenerating item models...')
    for fluid in SIMPLE_FLUIDS:
        water_based_fluid(rm, fluid)
    
    rm.item_model('suet', 'artisanal:item/suet').with_lang(lang('suet'))
    rm.item_model('pork_fat', 'artisanal:item/pork_fat').with_lang(lang('pork_fat'))
    rm.item_model('bear_fat', 'artisanal:item/bear_fat').with_lang(lang('bear_fat'))
    rm.item_model('poultry_fat', 'artisanal:item/poultry_fat').with_lang(lang('poultry_fat'))
    rm.item_model('soap', 'artisanal:item/soap').with_lang('Soap')
    
    rm.item_model('trimmed_feather', 'artisanal:item/trimmed_feather').with_lang(lang('trimmed_feather'))
    rm.item_model('soaked_feather', 'artisanal:item/soaked_feather').with_lang(lang('soaked_feather'))
    rm.item_model('tempered_feather', 'artisanal:item/tempered_feather').with_lang(lang('tempered_feather'))
    rm.item_model('quill', 'artisanal:item/quill').with_lang(lang('quill'))
    
    rm.item_model(('food', 'cleaned_sugarcane'), 'artisanal:item/food/cleaned_sugarcane').with_lang(lang('cleaned_sugarcane'))
    rm.item_model('wet_bagasse', 'artisanal:item/wet_bagasse').with_lang(lang('wet_bagasse'))
    rm.item_model('dry_bagasse', 'artisanal:item/dry_bagasse').with_lang(lang('dry_bagasse'))
    rm.item_model('perishable_sugar', 'artisanal:item/perishable_sugar').with_lang(lang('perishable_sugar'))
    rm.item_model('non_perishable_sugar', 'artisanal:item/non_perishable_sugar').with_lang('Non-Perishable Sugar')
    
    rm.item_model('milk_flakes', 'artisanal:item/milk_flakes').with_lang(lang('milk_flakes'))
    rm.item_model('powdered_milk', 'artisanal:item/powdered_milk').with_lang(lang('powdered_milk'))
    
    for metal in MAGNIFYING_GLASS_METALS:
        rm.item_model(('metal', 'magnifying_glass', f'{metal}'), f'artisanal:item/metal/magnifying_glass/{metal}').with_lang(lang(f'{metal}_magnifying_glass'))
        rm.item_model(('metal', 'magnifying_glass_frame', f'{metal}'), f'artisanal:item/metal/magnifying_glass_frame/{metal}').with_lang(lang(f'{metal}_magnifying_glass_frame'))
    
    rm.item_model(('metal', 'tinplate'), 'artisanal:item/metal/tinplate').with_lang(lang('tinplate'))
    rm.item_model(('metal', 'tin_can'), 'artisanal:item/metal/tin_can').with_lang(lang('tin_can'))
    rm.item_model(('metal', 'sealed_tin_can'), 'artisanal:item/metal/sealed_tin_can').with_lang(lang('sealed_tin_can'))
    rm.item_model(('metal', 'sterilized_tin_can'), 'artisanal:item/metal/sterilized_tin_can').with_lang(lang('sterilized_tin_can'))
    rm.item_model(('metal', 'dirty_tin_can'), 'artisanal:item/metal/dirty_tin_can').with_lang(lang('dirty_tin_can'))
    rm.item_model(('metal', 'dented_tin_can'), 'artisanal:item/metal/dented_tin_can').with_lang(lang('dented_tin_can'))
    rm.item_model(('metal', 'dirty_dented_tin_can'), 'artisanal:item/metal/dirty_dented_tin_can').with_lang(lang('dirty_dented_tin_can'))
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            rm.item_model(('metal', 'can_opener', metal), f'artisanal:item/metal/can_opener/{metal}').with_lang(lang(f'{metal} can opener'))
            rm.item_model(('metal', 'circle_blade', metal), f'artisanal:item/metal/circle_blade/{metal}').with_lang(lang(f'{metal} circle blade'))
            
    
def generate_models():
    print('Generating models...')
    generate_item_models()

def generate_anvil_recipes():
    print('\tGenerating anvil recipes...')
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        anvil_recipe(rm, ('metal', 'magnifying_glass_frame', metal), f'tfc:metal/rod/{metal}', f'artisanal:metal/magnifying_glass_frame/{metal}', metal_data.tier, Rules.bend_last, Rules.hit_any, Rules.bend_not_last)
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            anvil_recipe(rm, ('metal', 'circle_blade', metal), f'tfc:metal/ingot/{metal}', (2, f'artisanal:metal/circle_blade/{metal}'), metal_data.tier, Rules.shrink_third_last, Rules.hit_second_last, Rules.hit_last)
    
    
    
    anvil_recipe(rm, ('metal', 'tin_can'), 'artisanal:metal/tinplate', 'artisanal:metal/tin_can', 1, Rules.bend_not_last, Rules.hit_not_last, Rules.hit_last)
    welding_recipe(rm, ('metal', 'tinplate_from_iron'), 'tfc:metal/double_sheet/wrought_iron', 'tfc:metal/sheet/tin', item_stack_provider((4, 'artisanal:metal/tinplate'), cap_heat=METALS['tin'].melt_temperature - 1), 0)
    welding_recipe(rm, ('metal', 'tinplate_from_steel'), 'tfc:metal/double_sheet/steel', 'tfc:metal/sheet/tin', item_stack_provider((8, 'artisanal:metal/tinplate'), cap_heat=METALS['tin'].melt_temperature - 1), 0)
    anvil_recipe(rm, ('metal', 'repair_tin_can'), 'artisanal:metal/dented_tin_can', 'artisanal:metal/tin_can', 1, Rules.hit_third_last, Rules.hit_second_last, Rules.hit_last)
    

def generate_barrel_recipes():
    print('\tGenerating barrel recipes...')
    barrel_sealed_recipe(rm, ('soaked_feather'), 'Soaking Feather', 8000, 'artisanal:trimmed_feather', '200 minecraft:water', 'artisanal:soaked_feather', None)
    barrel_instant_fluid_recipe(rm, ('soap_fluid'), '9 #artisanal:rendered_fats', '1 tfc:lye', '10 artisanal:soap')
    barrel_sealed_recipe(rm, ('soap_solid'), 'Solidifying Soap', 8000, None, '125 artisanal:soap', 'artisanal:soap', None, None)
    
    barrel_instant_recipe(rm, ('soapy_water'), 'artisanal:soap', '1000 minecraft:water', None, '1000 artisanal:soapy_water')
    
    disable_recipe(rm, 'tfc:barrel/clean_jar')
    disable_recipe(rm, 'tfc:barrel/clean_jute_net')
    disable_recipe(rm, 'tfc:barrel/clean_sealed_jar')
    disable_recipe(rm, 'tfc:barrel/clean_soup_bowl')
    disable_recipe(rm, 'firmalife:barrel/clean_hematitic_wine_bottle')
    disable_recipe(rm, 'firmalife:barrel/clean_olivine_wine_bottle')
    disable_recipe(rm, 'firmalife:barrel/clean_volcanic_wine_bottle')
    disable_recipe(rm, 'firmalife:barrel/clean_any_bowl')
    disable_recipe(rm, 'tfc:barrel/sugar')
    
    barrel_sealed_recipe(rm, 'clean_jute_net_water', 'Cleaning Jute Net', 8000, 'tfc:dirty_jute_net', '100 minecraft:water', output_item='tfc:jute_net')
    barrel_sealed_recipe(rm, 'clean_soup_bowl_water', 'Cleaning Bowl', 8000, '#tfc:dynamic_bowl_items', '100 minecraft:water', output_item=item_stack_provider(empty_bowl=True))
    barrel_sealed_recipe(rm, 'clean_jar_water', 'Cleaning Jar', 8000, '#tfc:foods/preserves', '100 minecraft:water', output_item='tfc:empty_jar')
    barrel_sealed_recipe(rm, 'clean_sealed_jar_water', 'Cleaning Sealed Jar', 8000, '#tfc:foods/sealed_preserves', '100 minecraft:water', output_item='tfc:empty_jar')
    barrel_sealed_recipe(rm, 'clean_sugarcane_water', 'Cleaning Sugarcane', 8000, not_rotten('tfc:food/sugarcane'), '100 minecraft:water', output_item=item_stack_provider('artisanal:food/cleaned_sugarcane', copy_food=True))
    barrel_sealed_recipe(rm, 'clean_hematitic_wine_bottle_water', 'Cleaning Wine Bottle', 8000, 'firmalife:hematitic_wine_bottle', '100 minecraft:water', output_item='firmalife:empty_hematitic_wine_bottle')
    barrel_sealed_recipe(rm, 'clean_olivine_wine_bottle_water', 'Cleaning Wine Bottle', 8000, 'firmalife:olivine_wine_bottle', '100 minecraft:water', output_item='firmalife:empty_olivine_wine_bottle')
    barrel_sealed_recipe(rm, 'clean_volcanic_wine_bottle_water', 'Cleaning Wine Bottle', 8000, 'firmalife:volcanic_wine_bottle', '100 minecraft:water', output_item='firmalife:empty_volcanic_wine_bottle')
    barrel_sealed_recipe(rm, 'clean_any_bowl_water', 'Cleaning Bowl', 8000, '#firmalife:foods/washable', '100 minecraft:water', output_item=item_stack_provider(other_modifier='firmalife:empty_pan'))
    barrel_sealed_recipe(rm, 'clean_tin_can_water', 'Cleaning Tin Can', 8000, 'artisanal:metal/dirty_tin_can', '100 minecraft:water', output_item='artisanal:metal/tin_can')
    barrel_sealed_recipe(rm, 'clean_dented_tin_can_water', 'Cleaning Dented Tin Can', 8000, 'artisanal:metal/dirty_dented_tin_can', '100 minecraft:water', output_item='artisanal:metal/dented_tin_can')
    
    
    barrel_instant_recipe(rm, 'clean_jute_net_soapy_water', 'tfc:dirty_jute_net', '100 artisanal:soapy_water', output_item='tfc:jute_net')
    barrel_instant_recipe(rm, 'clean_soup_bowl_soapy_water', '#tfc:dynamic_bowl_items', '100 artisanal:soapy_water', output_item=item_stack_provider(empty_bowl=True))
    barrel_instant_recipe(rm, 'clean_jar_soapy_water', '#tfc:foods/preserves', '100 artisanal:soapy_water', output_item='tfc:empty_jar')
    barrel_instant_recipe(rm, 'clean_sealed_jar_soapy_water', '#tfc:foods/sealed_preserves', '100 artisanal:soapy_water', output_item='tfc:empty_jar')
    barrel_instant_recipe(rm, 'clean_sugarcane_soapy_water', not_rotten('tfc:food/sugarcane'), '100 artisanal:soapy_water', output_item=item_stack_provider('artisanal:food/cleaned_sugarcane', copy_food=True))
    barrel_instant_recipe(rm, 'clean_hematitic_wine_bottle_soapy_water', 'firmalife:hematitic_wine_bottle', '100 artisanal:soapy_water', output_item='firmalife:empty_hematitic_wine_bottle')
    barrel_instant_recipe(rm, 'clean_olivine_wine_bottle_soapy_water', 'firmalife:olivine_wine_bottle', '100 artisanal:soapy_water', output_item='firmalife:empty_olivine_wine_bottle')
    barrel_instant_recipe(rm, 'clean_volcanic_wine_bottle_soapy_water', 'firmalife:volcanic_wine_bottle', '100 artisanal:soapy_water', output_item='firmalife:empty_volcanic_wine_bottle')
    barrel_instant_recipe(rm, 'clean_any_bowl_soapy_water', '#firmalife:foods/washable', '100 artisanal:soapy_water', output_item=item_stack_provider(other_modifier='firmalife:empty_pan'))
    barrel_instant_recipe(rm, 'clean_tin_can_soapy_water', 'artisanal:metal/dirty_tin_can', '100 artisanal:soapy_water', output_item='artisanal:metal/tin_can')
    barrel_instant_recipe(rm, 'clean_dented_tin_can_soapy_water', 'artisanal:metal/dirty_dented_tin_can', '100 artisanal:soapy_water', output_item='artisanal:metal/dented_tin_can')
    
    
    disable_recipe(rm, 'tfc:barrel/candle')
    barrel_sealed_recipe(rm, 'candle', 'Candle', 4000, '#forge:string', '40 #artisanal:rendered_fats', 'tfc:candle')
    
    disable_recipe(rm, 'firmaciv:barrel/large_waterproof_hide_tallow')
    barrel_sealed_recipe(rm, 'large_waterproof_hide_rendered_fat', 'Large Waterproof Hide', 8000, 'tfc:large_prepared_hide', '100 #artisanal:rendered_fats', 'firmaciv:large_waterproof_hide')
    
    barrel_instant_recipe(rm, 'dry_bagasse', 'artisanal:wet_bagasse', None, 'artisanal:dry_bagasse', '200 artisanal:sugarcane_juice')
    barrel_sealed_recipe(rm, 'filtered_sugarcane_juice', 'Filtering Sugarcane Juice', 8000, 'tfc:jute_net', '250 artisanal:sugarcane_juice', 'tfc:dirty_jute_net', '250 artisanal:filtered_sugarcane_juice')
    barrel_sealed_recipe(rm, 'alkalized_sugarcane_juice', 'Alkalizing Sugarcane Juice', 8000, 'tfc:powder/lime', '500 artisanal:filtered_sugarcane_juice', None, '500 artisanal:alkalized_sugarcane_juice')
    barrel_sealed_recipe(rm, 'clarified_sugarcane_juice', 'Clarifying Sugarcane Juice', 8000, 'tfc:jute_net', '250 artisanal:alkalized_sugarcane_juice', 'tfc:dirty_jute_net', '250 artisanal:clarified_sugarcane_juice')
    
    barrel_sealed_recipe(rm, 'paper', 'Bleaching Paper', 1000, 'tfc:unrefined_paper', '25 tfc:lye', 'minecraft:paper')
    
    barrel_instant_recipe(rm, 'milk', 'artisanal:powdered_milk', '100 minecraft:water', None, '100 minecraft:milk')
    
    disable_recipe(rm, 'tfc:barrel/limewater')
    
    disable_recipe(rm, 'tfc:barrel/rum')
    barrel_sealed_recipe(rm, ('rum'), 'Fermenting Rum', 72000, None, '1 artisanal:molasses', None, '1 tfc:rum')
    
    
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
        
    
    damage_shapeless(rm, 'crafting/pumpkin_pie', (not_rotten('#tfc:foods/dough'), not_rotten('tfc:food/pumpkin_chunks'), '#tfc:knives', not_rotten('minecraft:egg'), not_rotten('#tfc:sweetener')), 'minecraft:pumpkin_pie').with_advancement('tfc:pumpkin')
    rm.crafting_shaped('crafting/cake', ['AAA', 'BEB', 'CCC'], {'A': fluid_item_ingredient('100 #tfc:milks'), 'B': not_rotten('#tfc:sweetener'), 'E': not_rotten('minecraft:egg'), 'C': not_rotten('#tfc:foods/grains')}, 'tfc:cake').with_advancement('#tfc:foods/grains')
    disable_recipe(rm, 'tfc:crafting/cake')
    
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        rm.crafting_shapeless(('crafting', 'metal', 'magnifying_glass', metal), (f'artisanal:metal/magnifying_glass_frame/{metal}', 'tfc:lens'), f'artisanal:metal/magnifying_glass/{metal}')
        extra_products_shapeless(rm, ('crafting', 'metal', 'magnifying_glass', f'{metal}_uncraft'), (f'artisanal:metal/magnifying_glass/{metal}'), f'artisanal:metal/magnifying_glass_frame/{metal}', 'tfc:lens')
    
    for grain in GRAINS:
        rm.crafting_shapeless(f'crafting/{grain}_dough', (not_rotten('tfc:food/%s_flour' % grain), fluid_item_ingredient('100 firmalife:yeast_starter'), not_rotten('#tfc:sweetener')), (4, 'firmalife:food/%s_dough' % grain)).with_advancement('tfc:food/%s_grain' % grain)
        disable_recipe(rm, f'firmalife:crafting/{grain}_dough')
    for gem in GEMS:
        catalyst_shapeless(rm, ('crafting', gem + '_cut'), ('tfc:ore/%s' % gem, 'tfc:sandpaper', '#artisanal:magnifying_glasses'), 'tfc:gem/%s' % gem).with_advancement('tfc:sandpaper')
        disable_recipe(rm, f'tfc:{gem}_cut')
    for i in range(1, 6 + 1):
        damage_shapeless(rm, ('crafting', f'can_{i}'), (heatable_ingredient('artisanal:metal/tin_can', 120), 'tfc:powder/flux', '#tfc:hammers', *([not_rotten('#artisanal:foods/can_be_canned')] * i)), item_stack_provider('artisanal:metal/sealed_tin_can', meal=canning_modifier, other_modifier='artisanal:homogenous_ingredients'))
    
    for openable_can_item in OPENABLE_CAN_ITEMS:
        rm.recipe(('crafting', f'open_{openable_can_item}_hammer'), 'tfc:extra_products_shapeless_crafting',
            {
                "__comment__": "This file was automatically created by mcresources",
                "recipe": {
                    "type": "tfc:damage_inputs_shapeless_crafting",
                    "recipe": {
                        "type": "tfc:advanced_shapeless_crafting",
                        "ingredients": [utils.ingredient(f'artisanal:metal/{openable_can_item}'), utils.ingredient("#tfc:hammers")],
                        "result": item_stack_provider(other_modifier="artisanal:extract_canned_food"),
                        "primary_ingredient": utils.ingredient(f"artisanal:metal/{openable_can_item}")
                    }
                },
                "extra_products": [
                    item_stack_provider("artisanal:metal/dirty_dented_tin_can")
                ]
            }
        )
        rm.recipe(('crafting', f'open_{openable_can_item}_can_opener'), 'tfc:extra_products_shapeless_crafting',
            {
                "__comment__": "This file was automatically created by mcresources",
                "recipe": {
                    "type": "tfc:damage_inputs_shapeless_crafting",
                    "recipe": {
                        "type": "tfc:advanced_shapeless_crafting",
                        "ingredients": [utils.ingredient(f'artisanal:metal/{openable_can_item}'), utils.ingredient("#artisanal:can_openers")],
                        "result": item_stack_provider(other_modifier="artisanal:extract_canned_food"),
                        "primary_ingredient": utils.ingredient(f"artisanal:metal/{openable_can_item}")
                    }
                },
                "extra_products": [
                    item_stack_provider("artisanal:metal/dirty_tin_can")
                ]
            }
        )
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            rm.crafting_shaped(('crafting', 'metal', 'can_opener', metal), ['MBR', 'B  ', 'R  '], {'M': 'tfc:brass_mechanisms', 'B': f'artisanal:metal/circle_blade/{metal}', 'R': '#artisanal:rods/metal'}, f'artisanal:metal/can_opener/{metal}')    
    
    advanced_shapeless(rm, ('crafting', 'metal', 'remove_can_traits'), ('artisanal:metal/sterilized_tin_can'), remove_many_traits(item_stack_provider('artisanal:metal/sterilized_tin_can', other_modifier='artisanal:copy_dynamic_food'), 'tfc:charcoal_grilled', 'tfc:wood_grilled', 'tfc:burnt_to_a_crisp'), primary_ingredient='artisanal:metal/sterilized_tin_can')
    
    
def generate_heat_recipes():
    print("\tGenerating heat recipes...")
    
    for metal in MAGNIFYING_GLASS_METALS:
        metal_data = METALS[metal]
        heat_recipe(rm, ('metal', 'magnifying_glass', metal), f'artisanal:metal/magnifying_glass/{metal}', metal_data.melt_temperature, 'tfc:lens', f'50 tfc:metal/{metal}')
        heat_recipe(rm, ('metal', 'magnifying_glass_frame', metal), f'artisanal:metal/magnifying_glass_frame/{metal}', metal_data.melt_temperature, None, f'50 tfc:metal/{metal}')
    
    heat_recipe(rm, ('metal', 'sterilized_tin_can'), not_rotten('artisanal:metal/sealed_tin_can'), 150, remove_many_traits(item_stack_provider('artisanal:metal/sterilized_tin_can', other_modifier='artisanal:copy_dynamic_food_never_expires'), 'tfc:charcoal_grilled', 'tfc:wood_grilled', 'tfc:burnt_to_a_crisp'))
    
    for metal, metal_data in METALS.items():
        if 'tool' in metal_data.types:
            heat_recipe(rm, ('metal', 'circle_blade', metal), f'artisanal:metal/circle_blade/{metal}', metal_data.melt_temperature, result_fluid=f'50 tfc:metal/{metal}')
    


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
        simple_pot_recipe(rm, f'tallow_{i}', [utils.ingredient('artisanal:suet')] * i, f'{100 * i} minecraft:water', f'{100 * i} tfc:tallow', None, 2000, 600)
        simple_pot_recipe(rm, f'lard_{i}', [utils.ingredient('artisanal:pork_fat')] * i, f'{100 * i} minecraft:water', f'{100 * i} artisanal:lard', None, 2000, 600)
        simple_pot_recipe(rm, f'lard_{i}_from_bear', [utils.ingredient('artisanal:bear_fat')] * i, f'{100 * i} minecraft:water', f'{100 * i} artisanal:lard', None, 2000, 600)
        simple_pot_recipe(rm, f'schmaltz_{i}', [utils.ingredient('artisanal:poultry_fat')] * i, f'{100 * i} minecraft:water', f'{100 * i} artisanal:schmaltz', None, 2000, 600)
        
    
    scalable_pot_recipe(rm, ('condensed_milk'), '2 minecraft:milk', '1 artisanal:condensed_milk', None, 3000, 100)
    scalable_pot_recipe(rm, ('milk_flakes'), '100 artisanal:condensed_milk', None, [{'item': 'artisanal:milk_flakes'}], 3000, 100)
    scalable_pot_recipe(rm, ('salt'), '125 tfc:salt_water', None, [{'item': 'tfc:powder/salt'}], 2000, 300)
    scalable_pot_recipe(rm, ('perishable_sugar'), '200 artisanal:sugarcane_juice', '20 artisanal:molasses', [{'item': 'artisanal:perishable_sugar'}], 2000, 107)
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
            })
            disable_recipe(rm, f'tfc:pot/jam_{fruit}_{count}')
        
        for fruit in FL_FRUITS:
            ing = not_rotten(has_trait('firmalife:food/%s' % fruit, 'firmalife:dried', True))
            rm.recipe(('pot', 'jam_%s_%s' % (fruit, count)), 'tfc:pot_jam', {
                'ingredients': [ing] * count + [utils.ingredient('#tfc:sweetener')],
                'fluid_ingredient': fluid_stack_ingredient('100 minecraft:water'),
                'duration': 500,
                'temperature': 300,
                'result': utils.item_stack('%s firmalife:jar/%s' % (count, fruit)),
                'texture': 'firmalife:block/jar/%s' % fruit
            })
            disable_recipe(rm, f'firmalife:pot/jam_{fruit}_{count}')
        
        
    
def generate_quern_recipes():
    print('\tGenerating quern recipes...')
    quern_recipe(rm, ('food', 'cleaned_sugarcane'), not_rotten('artisanal:food/cleaned_sugarcane'), 'artisanal:wet_bagasse')
    quern_recipe(rm, ('powdered_milk'), 'artisanal:milk_flakes', {'item': 'artisanal:powdered_milk', 'count': 2})

def generate_vat_recipes():
    print('\tGenerating vat recipes...')
    vat_recipe(rm, 'sugar_water', not_rotten('#tfc:sweetener'), '1000 minecraft:water', output_fluid='500 firmalife:sugar_water')
    disable_recipe(rm, 'firmalife:vat/sugar_water')
    
    
    
    
    
def generate_recipes():
    print('Generating recipes...')
    generate_anvil_recipes()
    generate_barrel_recipes()
    generate_crafting_recipes()
    generate_heat_recipes()
    generate_mixing_recipes()
    generate_pot_recipes()
    generate_quern_recipes()
    generate_vat_recipes()

def generate_entity_tags():
    print('\tGenerating entity tags...')
    rm.entity_tag('drops_suet', 'tfc:cow', 'tfc:goat', 'tfc:yak', 'tfc:alpaca', 'tfc:sheep', 'tfc:musk_ox', 'tfc:deer', 'tfc:caribou', 'tfc:bongo', 'tfc:gazelle', 'tfc:moose', 'tfc:wildebeest')
    rm.entity_tag('drops_pork_fat', 'tfc:pig', 'tfc:boar')
    rm.entity_tag('drops_bear_fat', '#tfc:bears', 'tfc:panda')
    rm.entity_tag('drops_poultry_fat', 'tfc:chicken', 'tfc:duck', 'tfc:quail', 'tfc:grouse', 'tfc:pheasant', 'tfc:turkey', 'tfc:peafowl')

def generate_fluid_tags():
    print('\tGenerating fluid tags...')
    rm.fluid_tag('rendered_fats', 'tfc:tallow', 'artisanal:lard', 'artisanal:schmaltz')
    rm.fluid_tag('tfc:ingredients', '#artisanal:rendered_fats', 'artisanal:soap', 'artisanal:soapy_water', 'artisanal:sugarcane_juice', 'artisanal:filtered_sugarcane_juice', 'artisanal:alkalized_sugarcane_juice', 'artisanal:clarified_sugarcane_juice', 'artisanal:molasses', 'artisanal:petroleum')
    rm.fluid_tag('tfc:drinkables', 'artisanal:sugarcane_juice', 'artisanal:molasses', 'artisanal:condensed_milk')
    rm.fluid_tag('tfc:usable_in_jug', '#tfc:ingredients')
    
def generate_item_tags():
    print('\tGenerating item tags...')
    rm.item_tag('tfc:sweetener', 'artisanal:perishable_sugar', 'artisanal:non_perishable_sugar')
    rm.item_tag('firmalife:sweetener', 'artisanal:perishable_sugar', 'artisanal:non_perishable_sugar')
    rm.item_tag('fats', 'artisanal:bear_fat', 'artisanal:pork_fat', 'artisanal:poultry_fat', 'artisanal:suet')
    rm.item_tag('tfc:firepit_kindling', 'artisanal:dry_bagasse')
    rm.item_tag('magnifying_glasses', *[f'artisanal:metal/magnifying_glass/{metal}' for metal in MAGNIFYING_GLASS_METALS])
    rm.item_tag('crafting_catalysts', '#artisanal:magnifying_glasses')
    rm.item_tag('foods/can_be_canned', *[f'#tfc:foods/{tag}' for tag in CANNABLE_FOOD_TAGS], '#firmalife:foods/flatbreads', '#firmalife:foods/slices')
    rm.item_tag('can_openers', *[f'artisanal:metal/can_opener/{metal}' for metal in METALS if 'tool' in METALS[metal].types])
    rm.item_tag('rods/metal', *[f'tfc:metal/rod/{metal}' for metal in METALS if 'utility' in METALS[metal].types])

def generate_tags():
    print('Generating tags...')
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