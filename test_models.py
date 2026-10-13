from models import Card, Slot, VerbBox, VerbBoxState

wizard = Card("Wizard", {"wizard"})
chicken = Card("Chicken", {"raw_food"})
sacred_oil = Card("Sacred Oil", {"sacred", "expensive"})
altar_slot = Slot(required_tags={"sacred"})
altar = VerbBox("Altar", slots=[altar_slot], duration=1)
totem = VerbBox("Totem", slots=[Slot(required_tags={"wizard"})], duration=5)

assert altar_slot.place_card(sacred_oil) is True  # Should return True since sacred_oil has the "sacred" tag
assert altar_slot.is_filled() is True  # Should return True since the slot is now filled with sacred_oil
assert altar_slot.place_card(sacred_oil) is False  # Should return False since the slot is already filled
assert altar_slot.remove_card() is sacred_oil  # Should return the sacred_oil card that was removed
assert not altar_slot.is_filled()  # Should return False since the slot is now empty
assert altar_slot.place_card(chicken) is False  # Should return False since chicken does not have the "sacred" tag
assert not altar_slot.is_filled()  # Should return False since the slot is still empty
assert altar.start() is False  # Should return False since the slot is not filled
assert altar.place_card(sacred_oil, altar_slot) is True  # Should return True since sacred_oil has the "sacred" tag
assert altar.tick() is False  # Should return False since the verb box is not running
assert altar.start() is True  # Should return True since the slot is now filled
assert altar.start() is False  # Should return False since the verb box is already running
assert altar.tick() is True  # Should return True since the verb box is running
assert altar.progress == 1  # Should return True since the progress is now 1
assert altar.tick() is False  # Should return False since the verb box is completed
assert totem.is_loaded() is False  # Should return False since the slot is not filled
assert totem.place_card(chicken, totem.slots[0]) is False  # Should return False since chicken does not have the "wizard" tag
assert totem.place_card(wizard, totem.slots[0]) is True  # Should return True since wizard has the "wizard" tag
assert totem.is_loaded() is True  # Should return True since the slot is now filled
assert totem.start() is True  # Should return True since the slot is filled
assert totem.start() is False  # Should return False since the verb box is already running
assert totem.tick() is True  # Should return True since the verb box is running
assert totem.progress == 1  # Should return True since the progress is now 1
assert totem.remove_card(totem.slots[0]) is wizard  # Should return the wizard card that was removed
assert totem.is_loaded() is False  # Should return False since the slot is now empty
assert totem.start() is False  # Should return False since the slot is not filled
assert totem.tick() is False  # Should return False since the verb box is not running
assert totem.place_card(wizard, totem.slots[0]) is True  # Should return True since wizard has the "wizard" tag
assert totem.start() is True  # Should return True since the slot is filled
assert totem.tick() is True  # Should return True since the verb box is running
totem.tick()  # Progress is now 3
totem.tick()  # Progress is now 4
assert totem.progress == 4  # Should return True since the progress is now 4
totem.tick()  # Progress is now 5, should complete
assert totem.state == VerbBoxState.COMPLETED  # Should return True since the verb box is completed