class Card:
    def __init__(self, name, tags=None, aspects=None):
        self.name = name
        self.tags = tags or set()
        self.aspects = aspects


    def __repr__(self):
        return f"Card('{self.name}', {self.tags})"

CARD_TEMPLATES = {
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

def make_card(key):
    t = CARD_TEMPLATES[key]
    return Card(t["name"], set(t["tags"]), t["aspects"])