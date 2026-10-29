from models import SlotFate

TEST_CARD_TEMPLATES = {
    "wizard":{"name":"Wizard","tags":{"wizard"},"aspects":None},
    "totem":{"name":"Totem","tags":{"totem"},"aspects":None},
    "sacred_oil":{"name":"Sacred Oil", "tags":{"expensive","sacred"},"aspects":None},
    "sacred_perfume":{"name":"Sacred Perfume", "tags":{"odorous","sacred"},"aspects":None},
    "chicken":{"name":"Chicken", "tags":{"raw_food"},"aspects":None},
    "rubber_chicken":{"name":"Rubber Chicken", "tags":{"raw_food"},"aspects":None},
    "baby":{"name":"Baby", "tags":{"baby"},"aspects":None},
    "blessed_baby":{"name":"Blessed Baby", "tags":{"baby","sacred"},"aspects":None},
    "tea_leaves":{"name":"Tea Leaves", "tags":{"reagent","raw_food"},"aspects":None},
    "tea":{"name":"Tea", "tags":{"edible"},"aspects":None},
    "bogweed":{"name":"Bogweed", "tags":{"reagent"}, "aspects":{"herbalism":2,"alchemy":2},}
}

TEST_EVENT_TEMPLATES = {
    "intro":{
        "name":"Introduction",
        "narrative_text":"Welcome to Hedge Wizard. Click the button below to start the game.",
        "deadline":None,
        "slots":None,
        "verbbox":None,
        "becomes":"welcome",
        "fails_to":None
        },
    "welcome":{
        "name":"Welcome",
        "narrative_text":"This card represents you, the wizard. Click it to add it to your tableau.",
        "deadline":None,
        "slots":[{"card":"wizard", "required_tags":{"wizard"}}],
        "verbbox":None,
        "becomes":"get_started",
        "fails_to":None
        },
    "get_started":{
        "name":"Let's Get Started",
        "narrative_text":"In this game, you'll receive tasks to resolve by playing your cards. Let's start by having your wizard carve a totem.",
        "deadline":1,
        "slots":None,
        "verbbox":{
            "name":"A Wizard Is You",
            "slots":[{"required_tags":{"wizard"}}],
            "duration":0,
            "results":["totem"]
            },
        "becomes":None,
        "fails_to":None
        },
    "your_first_potion":{
        "name":"Brew Your First Potion",
        "narrative_text":"To get you started, here's a reagent you can brew into a potion. Place it in the slot below, and brew it!",
        "deadline":1,
        "slots":[{"card":"tea_leaves", "required_tags":{"reagent","raw_food"}}],
        "verbbox":{
            "name":"Brew Some Tea",
            "slots":[{"required_tags":{"reagent","raw_food"}, "fate":SlotFate.REPLACE, "replacement":"tea"}],
            "duration":1,
            "results":[]
            },
        "becomes":None,
        "fails_to":None
        },
    "carve_totem":{
        "name":"Carve A Totem",
        "narrative_text":"Any spare time can be spent carving totems, which are used in many rituals. They take a few turns, but you can interrupt the work at any time.",
        "deadline":None,
        "slots":None,
        "verbbox":{
            "name":"Carve a Totem",
            "slots":[{"required_tags":{"wizard"}}],
            "duration":2,
            "results":["totem"]
            },
        "becomes":"carve_totem",
        "fails_to":None
        },
    "sacrifice_totem":{
        "name":"Sacrifice A Totem",
        "narrative_text":"The spirits demand a sacrifice. Give them a totem before they grow angry!",
        "deadline":1,
        "slots":None,
        "verbbox":{
            "name":"Sacrifice a Totem",
            "slots":[{"required_tags":{"totem"}, "fate":SlotFate.CONSUME}],
            "duration":1,
            "results":[]
            },
        "becomes":None,
        "fails_to":"angry_spirits"
        }
    }