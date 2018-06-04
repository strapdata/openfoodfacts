import json

from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Text, Double, DateTime, Integer, List


class EsQuery(Text):
    """
    Dummy column used to make elasticsearch queries from within CQL :
        `SELECT * FROM keyspace.table where es_query='{ "query": { "match_all": { } } }'`
    """

    def __init__(self):
        super().__init__(custom_index=True)

    def to_database(self, value):
        if type(value) is dict:
            value = json.dumps(value)
        return value

    def to_python(self, value):
        return None


class Product(Model):
    code = Text(primary_key=True)
    url = Text()
    es_query = EsQuery()
    creator = Text()
    created_t = DateTime()
    last_modified_t = DateTime()
    product_name = Text()
    generic_name = Text()
    quantity = Text()
    packaging = List(Text)
    packaging_tags = List(Text)
    brands = Text()
    brands_tags = List(Text)
    categories = Text()
    categories_tags = List(Text)
    categories_fr = List(Text)
    origins = Text()
    origins_tags = List(Text)
    manufacturing_places = Text()
    manufacturing_places_tags = List(Text)
    labels = Text()
    labels_tags = List(Text)
    labels_fr = List(Text)
    emb_codes = Text()
    emb_codes_tags = List(Text)
    first_packaging_code_geo = Text()
    cities = Text()
    cities_tags = List(Text)
    purchase_places = Text()
    stores = Text()
    countries = Text()
    countries_tags = List(Text)
    countries_fr = List(Text)
    ingredients_text = Text()
    allergens = Text()
    allergens_fr = List(Text)
    traces = Text()
    traces_tags = List(Text)
    traces_fr = List(Text)
    serving_size = Text()
    serving_quantity = Double()
    no_nutriments = Text()
    additives_n = Integer()
    additives = Text()
    additives_tags = List(Text)
    additives_fr = List(Text)
    ingredients_from_palm_oil_n = Integer()
    ingredients_from_palm_oil = Text()
    ingredients_from_palm_oil_tags = List(Text)
    ingredients_that_may_be_from_palm_oil_n = Integer()
    ingredients_that_may_be_from_palm_oil = Text()
    ingredients_that_may_be_from_palm_oil_tags = List(Text)
    nutrition_grade_uk = Text()
    nutrition_grade_fr = List(Text)
    pnns_groups_1 = Text()
    pnns_groups_2 = Text()
    states = Text()
    states_tags = List(Text)
    states_fr = List(Text)
    main_category = Text()
    main_category_fr = List(Text)
    image_url = Text()
    image_small_url = Text()
    image_ingredients_url = Text()
    image_ingredients_small_url = Text()
    image_nutrition_url = Text()
    image_nutrition_small_url = Text()
    energy_100g = Double()
    energy_from_fat_100g = Double(db_field="energy-from-fat_100g")
    fat_100g = Double()
    saturated_fat_100g = Double(db_field="saturated-fat_100g")
    butyric_acid_100g = Double(db_field="butyric-acid_100g")
    caproic_acid_100g = Double(db_field="caproic-acid_100g")
    caprylic_acid_100g = Double(db_field="caprylic-acid_100g")
    capric_acid_100g = Double(db_field="capric-acid_100g")
    lauric_acid_100g = Double(db_field="lauric-acid_100g")
    myristic_acid_100g = Double(db_field="myristic-acid_100g")
    palmitic_acid_100g = Double(db_field="palmitic-acid_100g")
    stearic_acid_100g = Double(db_field="stearic-acid_100g")
    arachidic_acid_100g = Double(db_field="arachidic-acid_100g")
    behenic_acid_100g = Double(db_field="behenic-acid_100g")
    lignoceric_acid_100g = Double(db_field="lignoceric-acid_100g")
    cerotic_acid_100g = Double(db_field="cerotic-acid_100g")
    montanic_acid_100g = Double(db_field="montanic-acid_100g")
    melissic_acid_100g = Double(db_field="melissic-acid_100g")
    monounsaturated_fat_100g = Double(db_field="monounsaturated-fat_100g")
    polyunsaturated_fat_100g = Double(db_field="polyunsaturated-fat_100g")
    omega_3_fat_100g = Double(db_field="omega-3-fat_100g")
    alpha_linolenic_acid_100g = Double(db_field="alpha-linolenic-acid_100g")
    eicosapentaenoic_acid_100g = Double(db_field="eicosapentaenoic-acid_100g")
    docosahexaenoic_acid_100g = Double(db_field="docosahexaenoic-acid_100g")
    omega_6_fat_100g = Double(db_field="omega-6-fat_100g")
    linoleic_acid_100g = Double(db_field="linoleic-acid_100g")
    arachidonic_acid_100g = Double(db_field="arachidonic-acid_100g")
    gamma_linolenic_acid_100g = Double(db_field="gamma-linolenic-acid_100g")
    dihomo_gamma_linolenic_acid_100g = Double(db_field="dihomo-gamma-linolenic-acid_100g")
    omega_9_fat_100g = Double(db_field="omega-9-fat_100g")
    oleic_acid_100g = Double(db_field="oleic-acid_100g")
    elaidic_acid_100g = Double(db_field="elaidic-acid_100g")
    gondoic_acid_100g = Double(db_field="gondoic-acid_100g")
    mead_acid_100g = Double(db_field="mead-acid_100g")
    erucic_acid_100g = Double(db_field="erucic-acid_100g")
    nervonic_acid_100g = Double(db_field="nervonic-acid_100g")
    trans_fat_100g = Double(db_field="trans-fat_100g")
    cholesterol_100g = Double()
    carbohydrates_100g = Double()
    sugars_100g = Double()
    sucrose_100g = Double()
    glucose_100g = Double()
    fructose_100g = Double()
    lactose_100g = Double()
    maltose_100g = Double()
    maltodextrins_100g = Double()
    starch_100g = Double()
    polyols_100g = Double()
    fiber_100g = Double()
    proteins_100g = Double()
    casein_100g = Double()
    serum_proteins_100g = Double(db_field="serum-proteins_100g")
    nucleotides_100g = Double()
    salt_100g = Double()
    sodium_100g = Double()
    alcohol_100g = Double()
    vitamin_a_100g = Double(db_field="vitamin-a_100g")
    beta_carotene_100g = Double(db_field="beta-carotene_100g")
    vitamin_d_100g = Double(db_field="vitamin-d_100g")
    vitamin_e_100g = Double(db_field="vitamin-e_100g")
    vitamin_k_100g = Double(db_field="vitamin-k_100g")
    vitamin_c_100g = Double(db_field="vitamin-c_100g")
    vitamin_b1_100g = Double(db_field="vitamin-b1_100g")
    vitamin_b2_100g = Double(db_field="vitamin-b2_100g")
    vitamin_pp_100g = Double(db_field="vitamin-pp_100g")
    vitamin_b6_100g = Double(db_field="vitamin-b6_100g")
    vitamin_b9_100g = Double(db_field="vitamin-b9_100g")
    folates_100g = Double()
    vitamin_b12_100g = Double(db_field="vitamin-b12_100g")
    biotin_100g = Double()
    pantothenic_acid_100g = Double(db_field="pantothenic-acid_100g")
    silica_100g = Double()
    bicarbonate_100g = Double()
    potassium_100g = Double()
    chloride_100g = Double()
    calcium_100g = Double()
    phosphorus_100g = Double()
    iron_100g = Double()
    magnesium_100g = Double()
    zinc_100g = Double()
    copper_100g = Double()
    manganese_100g = Double()
    fluoride_100g = Double()
    selenium_100g = Double()
    chromium_100g = Double()
    molybdenum_100g = Double()
    iodine_100g = Double()
    caffeine_100g = Double()
    taurine_100g = Double()
    ph_100g = Double()
    fruits_vegetables_nuts_100g = Double(db_field="fruits-vegetables-nuts_100g")
    fruits_vegetables_nuts_estimate_100g = Double(db_field="fruits-vegetables-nuts-estimate_100g")
    collagen_meat_protein_ratio_100g = Double(db_field="collagen-meat-protein-ratio_100g")
    cocoa_100g = Double()
    chlorophyl_100g = Double()
    carbon_footprint_100g = Double(db_field="carbon-footprint_100g")
    nutrition_score_fr_100g = Double(db_field="nutrition-score-fr_100g")
    nutrition_score_uk_100g = Double(db_field="nutrition-score-uk_100g")
    glycemic_index_100g = Double(db_field="glycemic-index_100g")
    water_hardness_100g = Double(db_field="water-hardness_100g")
    choline_100g = Double()
    phylloquinone_100g = Double()
    beta_glucan_100g = Double(db_field="beta-glucan_100g")
    inositol_100g = Double()
    carnitine_100g = Double()

    def to_dict(self):
        json_dict = dict(self)
        del json_dict['es_query']
        return json_dict
