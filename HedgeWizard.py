from models import Card, Slot, VerbBox, VerbBoxState

wizard = Card("Wizard", {"wizard"})
chicken = Card("Chicken", {"raw_food"})
totem  = Card("Totem", {"totem"})
carve_totem = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=5)

assert carve_totem.is_loaded() is False  # Should return False since the slot is not filled
assert carve_totem.start() is False
assert carve_totem.state == VerbBoxState.UNLOADED
#print(carve_totem.state) #correctly returns VerbBoxState.UNLOADED
assert carve_totem.place_card(chicken, carve_totem.slots[0]) is False
assert carve_totem.place_card(wizard, carve_totem.slots[0]) is True
assert carve_totem.state == VerbBoxState.LOADED
assert carve_totem.is_loaded() is True
assert carve_totem.start() is True
assert carve_totem.state == VerbBoxState.RUNNING
assert carve_totem.tick() is True
assert carve_totem.progress == 1
assert carve_totem.remove_card(carve_totem.slots[0]) is wizard
assert carve_totem.state == VerbBoxState.UNLOADED
assert carve_totem.start() is False
assert carve_totem.progress == 1
assert carve_totem.place_card(chicken, carve_totem.slots[0]) is False
assert carve_totem.place_card(wizard, carve_totem.slots[0]) is True
assert carve_totem.state == VerbBoxState.LOADED
assert carve_totem.is_loaded() is True
assert carve_totem.start() is True
assert carve_totem.state == VerbBoxState.RUNNING
assert carve_totem.tick() is True
assert carve_totem.progress == 2
assert carve_totem.tick() is True
assert carve_totem.tick() is True
#assert carve_totem.tick() is True
#assert carve_totem.tick() is False
assert carve_totem.state == VerbBoxState.RUNNING
#assert carve_totem.add_slot(totem, {"totem"}) is not False
assert carve_totem.add_slot() is not False
assert carve_totem.state == VerbBoxState.UNLOADED
#assert carve_totem.state == VerbBoxState.COMPLETED
assert len(carve_totem.slots) == 2