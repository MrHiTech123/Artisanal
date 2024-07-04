import json

from alcs_funcs import *
from mcresources import ResourceManager

SIMPLE_FLUIDS = (
    'lard',
    'schmaltz',
    'soapy_water',
    'soap',
    'sugarcane_juice',
    'filtered_sugarcane_juice',
    'alkalized_sugarcane_juice',
    'clarified_sugarcane_juice',
    'molasses',
    'condensed_milk',
    'petroleum'
)


rm = ResourceManager('artisanal')
forge_rm = ResourceManager('forge')

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
    
def scalable_pot_recipe(rm: ResourceManager, name_parts: utils.ResourceIdentifier, fluid: str, output_fluid: str = None, output_items: Json = None, duration: int = 2000, temp: int = 300):
    rm.recipe(('pot', name_parts), 'artisanal:scalable_pot', {
        'ingredients': [],
        'fluid_ingredient': fluid_stack_ingredient(fluid),
        'duration': duration,
        'temperature': temp,
        'fluid_output': fluid_stack(output_fluid) if output_fluid is not None else None,
        'item_output': [utils.item_stack(item) for item in output_items] if output_items is not None else None
    })


def generate_drinkables():
    print('\tGenerating drinkables...')
    drinkable(rm, ('molasses'), 'artisanal:molasses', thirst=-1, food={'hunger': 4, 'saturation': 0, 'vegetables': 3, 'fruit': 3})
    
def generate_lamp_fuels():
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
    food_item(rm, ('maple_sugar'), 'afc:maple_sugar', Category.other, 0, 0, 0, 0)
    food_item(rm, ('birch_sugar'), 'afc:birch_sugar', Category.other, 0, 0, 0, 0)
    
    
    
def generate_item_heats():
    print('\tGenerating item heats...')
    item_heat(rm, ('sand'), '#forge:sand', 0.8, None, None)
    
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
    
    
    
def generate_models():
    print('Generating models...')
    generate_item_models()

def generate_barrel_recipes():
    print('\tGenerating barrel recipes...')
    barrel_sealed_recipe(rm, ('soaked_feather'), 'Soaking Feather', 8000, 'artisanal:trimmed_feather', '200 minecraft:water', 'artisanal:soaked_feather', None)
    barrel_instant_fluid_recipe(rm, ('soap_fluid'), '1 tfc:lye', '1 #artisanal:rendered_fats', '2 artisanal:soap')
    barrel_sealed_recipe(rm, ('soap_solid'), 'Solidifying Soap', 8000, None, '500 artisanal:soap', 'artisanal:soap', None, None)
    
    barrel_instant_recipe(rm, ('soapy_water'), 'artisanal:soap', '1000 minecraft:water', None, '1000 artisanal:soapy_water')
    
    disable_recipe(rm, 'tfc:barrel/clean_jar')
    disable_recipe(rm, 'tfc:barrel/clean_jute_net')
    disable_recipe(rm, 'tfc:barrel/clean_sealed_jar')
    disable_recipe(rm, 'tfc:barrel/clean_soup_bowl')
    disable_recipe(rm, 'tfc:barrel/sugar')
    
    barrel_sealed_recipe(rm, 'clean_jute_net_water', 'Cleaning Jute Net', 8000, 'tfc:dirty_jute_net', '100 minecraft:water', output_item='tfc:jute_net')
    barrel_sealed_recipe(rm, 'clean_soup_bowl_water', 'Cleaning Bowl', 8000, '#tfc:dynamic_bowl_items', '100 minecraft:water', output_item=item_stack_provider(empty_bowl=True))
    barrel_sealed_recipe(rm, 'clean_jar_water', 'Cleaning Jar', 8000, '#tfc:foods/preserves', '100 minecraft:water', output_item='tfc:empty_jar')
    barrel_sealed_recipe(rm, 'clean_sealed_jar_water', 'Cleaning Sealed Jar', 8000, '#tfc:foods/sealed_preserves', '100 minecraft:water', output_item='tfc:empty_jar')
    barrel_sealed_recipe(rm, 'clean_sugarcane_water', 'Cleaning Sugarcane', 8000, not_rotten('tfc:food/sugarcane'), '100 minecraft:water', output_item=item_stack_provider('artisanal:food/cleaned_sugarcane', copy_food=True))
    
    barrel_instant_recipe(rm, 'clean_jute_net_soapy_water', 'tfc:dirty_jute_net', '100 artisanal:soapy_water', output_item='tfc:jute_net')
    barrel_instant_recipe(rm, 'clean_soup_bowl_soapy_water', '#tfc:dynamic_bowl_items', '100 artisanal:soapy_water', output_item=item_stack_provider(empty_bowl=True))
    barrel_instant_recipe(rm, 'clean_jar_soapy_water', '#tfc:foods/preserves', '100 artisanal:soapy_water', output_item='tfc:empty_jar')
    barrel_instant_recipe(rm, 'clean_sealed_jar_soapy_water', '#tfc:foods/sealed_preserves', '100 artisanal:soapy_water', output_item='tfc:empty_jar')
    barrel_instant_recipe(rm, 'clean_sugarcane_soapy_water', not_rotten('tfc:food/sugarcane'), '100 artisanal:soapy_water', output_item=item_stack_provider('artisanal:food/cleaned_sugarcane', copy_food=True))
    
    
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
    barrel_sealed_recipe(rm, ('rum'), 'Fermenting Rum', 72000, None, '500 artisanal:molasses', None, '500 tfc:rum')
    
    
def generate_crafting_recipes():
    print('\tGenerating crafting recipes...')
    damage_shapeless(rm, ('crafting', 'trimmed_feather'), ('#tfc:knives', 'minecraft:feather'), 'artisanal:trimmed_feather')
    advanced_shapeless(rm, ('crafting', 'tempered_feather'), utils.ingredient_list(('artisanal:soaked_feather', {'type': 'tfc:heatable', 'min_temp': 350, 'ingredient': utils.ingredient('#forge:sand')})), {'item': 'artisanal:tempered_feather'})
    damage_shapeless(rm, ('crafting', 'quill'), ('#tfc:knives', 'artisanal:tempered_feather'), 'artisanal:quill')
    
    
    rm.crafting_shapeless(('crafting', 'writable_book'), ('minecraft:book', 'minecraft:black_dye', 'artisanal:quill'), 'minecraft:writable_book')
    rm.crafting_shapeless(('crafting', 'writable_book_from_dye'), ('minecraft:book', fluid_item_ingredient('100 tfc:black_dye'), 'artisanal:quill'), 'minecraft:writable_book')
    disable_recipe(rm, 'minecraft:writable_book')
    
    for wood in WOODS:
        rm.crafting_shaped(('crafting', 'wood', f'{wood}_scribing_table'), ['Q B', 'XXX', 'Y Y'], {'Q': 'artisanal:quill', 'B': 'minecraft:black_dye', 'X': f'tfc:wood/planks/{wood}_slab', 'Y': f'tfc:wood/planks/{wood}'}, f'tfc:wood/scribing_table/{wood}').with_advancement(f'tfc:wood/planks/{wood}')
        disable_recipe(rm, f'tfc:crafting/wood/{wood}_scribing_table')
    
    # TODO:
    #   Add scribing tables from AFC wood types
    
    damage_shapeless(rm, 'crafting/pumpkin_pie', (not_rotten('#tfc:foods/dough'), not_rotten('tfc:food/pumpkin_chunks'), '#tfc:knives', not_rotten('minecraft:egg'), not_rotten('#tfc:sweetener')), 'minecraft:pumpkin_pie').with_advancement('tfc:pumpkin')
    rm.crafting_shaped('crafting/cake', ['AAA', 'BEB', 'CCC'], {'A': fluid_item_ingredient('100 #tfc:milks'), 'B': not_rotten('#tfc:sweetener'), 'E': not_rotten('minecraft:egg'), 'C': not_rotten('#tfc:foods/grains')}, 'tfc:cake').with_advancement('#tfc:foods/grains')
    disable_recipe(rm, 'tfc:crafting/cake')
    
    
    
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
    scalable_pot_recipe(rm, ('perishable_sugar'), '200 artisanal:sugarcane_juice', '100 artisanal:molasses', [{'item': 'artisanal:perishable_sugar'}], 2000, 107)
    scalable_pot_recipe(rm, ('non_perishable_sugar'), '200 artisanal:clarified_sugarcane_juice', '100 artisanal:molasses', [{'item': 'artisanal:non_perishable_sugar'}], 2000, 107)
    scalable_pot_recipe(rm, ('maple_sap_concentrate'), '10 afc:maple_sap', '1 afc:maple_sap_concentrate')
    scalable_pot_recipe(rm, ('maple_syrup'), '5 afc:maple_sap_concentrate', '1 afc:maple_syrup')
    scalable_pot_recipe(rm, ('birch_sap_concentrate'), '10 afc:birch_sap', '1 afc:birch_sap_concentrate')
    scalable_pot_recipe(rm, ('birch_syrup'), '5 afc:birch_sap_concentrate', '1 afc:birch_syrup')
    
    disable_recipe(rm, 'afc:pot/maple_concentrate')
    disable_recipe(rm, 'afc:pot/maple_syrup')
    disable_recipe(rm, 'afc:pot/maple_syrup_half_batch')
    disable_recipe(rm, 'afc:pot/birch_concentrate')
    disable_recipe(rm, 'afc:pot/birch_syrup')
    
    
    
    for fruit in JAR_FRUITS:
        for count in (2, 3, 4):
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
    
def generate_quern_recipes():
    print('\tGenerating quern recipes...')
    quern_recipe(rm, ('food', 'cleaned_sugarcane'), not_rotten('artisanal:food/cleaned_sugarcane'), 'artisanal:wet_bagasse')
    quern_recipe(rm, ('powdered_milk'), 'artisanal:milk_flakes', {'item': 'artisanal:powdered_milk', 'count': 2})
        
def generate_recipes():
    print('Generating recipes...')
    generate_barrel_recipes()
    generate_crafting_recipes()
    generate_pot_recipes()
    generate_quern_recipes()

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

def generate_tags():
    print('Generating tags...')
    generate_entity_tags()
    generate_fluid_tags()
    generate_item_tags()

def main():
    generate_data()
    generate_loot_modifiers()
    generate_misc_lang()
    generate_models()
    generate_recipes()
    generate_tags()
    
    rm.flush()
    
    
    
main()