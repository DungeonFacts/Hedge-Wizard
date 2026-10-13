import models

wizard = models.Card("Wizard", {"wizard"})
totem  = models.Card("Totem", {"totem"})
carve_totem = models.VerbBox("Carve Totem", slots=[models.Slot(required_tags={"wizard"})], duration=5)

assert carve_totem.is_loaded() is False  # Should return False since the slot is not filled
assert carve_totem.start() is False
#assert carve_totem.state == VerbBoxState.UNLOADED
print(carve_totem.state) #correctly returns VerbBoxState.UNLOADED
assert carve_totem.place_card(wizard, [0]) is True