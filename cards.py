class Card:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags or set()


    def __repr__(self):
        return f"Card('{self.name}', {self.tags})"

CARD_TEMPLATES = {
    "wizard":{"name":"Wizard","tags":{"wizard"}},
    "totem":{"name":"Totem","tags":{"totem"}},
    "sacred_oil":{"name":"Sacred Oil", "tags":{"expensive","sacred"}},
    "sacred_perfume":{"name":"Sacred Perfume", "tags":{"odorous","sacred"}},
    "chicken":{"name":"Chicken", "tags":{"raw_food"}},
    "rubber_chicken":{"name":"Rubber Chicken", "tags":{"raw_food"}},
    "baby":{"name":"Baby", "tags":{"baby"}},
    "blessed_baby":{"name":"Blessed Baby", "tags":{"baby","sacred"}}
}

def make_card(key):
    t = CARD_TEMPLATES[key]
    return Card(t["name"], set(t["tags"]))