from models import Slot, SlotFate, VerbBox, VerbBoxState
from cards import make_card

def test_make_card_results_are_not_identical():
    a = make_card("wizard")
    b = make_card("wizard")
    assert a is not b
    assert (a.name == b.name) is True
    a.tags.add("extra")
    assert "extra" not in b.tags


def test_slot_accepts_valid_card():
    a = make_card("wizard")
    slot = Slot(required_tags={"wizard"})
    assert slot.place_card(a) is True
    assert slot.is_filled() is True
    assert slot.card is a


def test_slot_force_card_ignores_required_tags():
    totem = make_card("totem")
    slot = Slot(required_tags={"wizard"})
    assert slot.place_card(totem) is False
    assert slot.force_card(totem) is True
    assert slot.card == totem


def test_slot_rejects_wrong_tag():
    altar = Slot(required_tags={"sacred"})
    a = make_card("chicken")
    assert altar.place_card(a) is False
    assert altar.is_filled() is False


def test_slot_remove_card():
    altar = Slot(required_tags={"sacred"})
    a = make_card("sacred_oil")
    altar.place_card(a)
    assert altar.is_filled() is True
    assert altar.remove_card() is a
    assert altar.is_filled() is False


def test_slot_rejects_if_already_filled():
    altar = Slot(required_tags={"sacred"})
    a = make_card("sacred_oil")
    altar.place_card(a)
    assert altar.is_filled() is True
    b = make_card("sacred_perfume")
    assert altar.place_card(b) is False
    assert altar.card is a
    assert altar.card.tags == {"expensive","sacred"}


def test_basic_box_lifecycle():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2, results=["totem"])
    b = make_card("wizard")
    assert a.state == VerbBoxState.UNLOADED
    a.place_card(b, a.slots[0])
    assert a.state == VerbBoxState.LOADED
    assert a.progress == 0
    a.start()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 0
    a.tick()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 1
    assert len(a.slots) == 1
    a.tick()
    assert a.slots[1].card.name == 'Totem'
    assert len (a.slots) == 2
    assert a.state == VerbBoxState.COMPLETED
    assert a.progress == 2
    #test extra tick does not produce another slot
    a.tick()
    assert len (a.slots) == 2
    assert a.state == VerbBoxState.COMPLETED
    assert a.progress == 2

def test_empty_results_box():
    distraction = VerbBox("A Distraction", slots=[Slot(required_tags={"wizard"})], duration=1, results=None)
    wizard = make_card("wizard")
    distraction.place_card(wizard, distraction.slots[0])
    distraction.start()
    distraction.tick()
    assert distraction.state == VerbBoxState.COMPLETED
    assert len(distraction.slots) == 1


def test_multi_result_spawns_not_identical():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2, results=["totem","totem"])
    b = make_card("wizard")
    assert a.state == VerbBoxState.UNLOADED
    a.place_card(b, a.slots[0])
    assert a.state == VerbBoxState.LOADED
    assert a.progress == 0
    a.start()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 0
    a.tick()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 1
    assert len(a.slots) == 1
    a.tick()
    assert a.slots[0].card.name == 'Wizard'
    assert a.slots[1].card.name == 'Totem'
    assert a.slots[2].card.name == 'Totem'
    assert a.slots[1].card is not a.slots[2].card
    assert len (a.slots) == 3
    assert a.state == VerbBoxState.COMPLETED
    assert a.progress == 2


def test_interrupt_box_lifecycle():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2, results=["totem"])
    b = make_card("wizard")
    assert a.state == VerbBoxState.UNLOADED
    a.place_card(b, a.slots[0])
    assert a.state == VerbBoxState.LOADED
    assert a.progress == 0
    a.start()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 0
    a.tick()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 1
    a.remove_card(a.slots[0])
    assert a.state == VerbBoxState.UNLOADED
    assert a.progress == 1
    a.tick()
    assert a.state == VerbBoxState.UNLOADED
    assert a.progress == 1
    a.place_card(b, a.slots[0])
    assert a.state == VerbBoxState.LOADED
    assert a.progress == 1
    a.start()
    a.tick()
    assert a.state == VerbBoxState.COMPLETED
    assert a.progress == 2


def test_add_slot():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2, results=["totem"])
    b = make_card("wizard")
    c = make_card("chicken")
    assert a.state == VerbBoxState.UNLOADED
    a.place_card(b, a.slots[0])
    assert a.state == VerbBoxState.LOADED
    assert a.progress == 0
    a.start()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 0
    a.tick()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 1
    a.add_slot(card=None, required_tags=None)
    assert a.state == VerbBoxState.UNLOADED
    assert a.progress == 1
    assert a.start() == False
    a.place_card(c, a.slots[1])
    assert a.state == VerbBoxState.LOADED
    a.start()
    a.tick()
    assert a.state == VerbBoxState.COMPLETED
    a.add_slot(card=None, required_tags=None)
    assert len(a.slots) == 4
    assert a.state == VerbBoxState.COMPLETED

def test_rewards_duplicate_events_are_not_identical():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2, results=["totem"])
    b = make_card("wizard")
    c = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2, results=["totem"])
    d = make_card("wizard")
    assert a.state == VerbBoxState.UNLOADED
    a.place_card(b, a.slots[0])
    assert a.state == VerbBoxState.LOADED
    assert a.progress == 0
    a.start()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 0
    a.tick()
    assert a.state == VerbBoxState.RUNNING
    assert a.progress == 1
    a.tick()
    assert a.state == VerbBoxState.COMPLETED
    assert a.slots[1].card.name == 'Totem'
    c.place_card(d, c.slots[0])
    c.start()
    c.tick()
    c.tick()
    assert c.slots[1].card.name == 'Totem'
    assert a.slots[1].card is not c.slots[1].card


def test_consume():
    bonfire = VerbBox("Burn Totem", slots=[Slot(required_tags={"totem"}, fate=SlotFate.CONSUME)], duration=1)
    offering = make_card("totem")
    bonfire.place_card(offering, bonfire.slots[0])
    bonfire.start()
    bonfire.tick()
    assert not bonfire.slots[0].is_filled()


def test_replacement():
    lignify = VerbBox("Lignify Chicken", slots=[Slot(required_tags={"raw_food"}, fate=SlotFate.REPLACE, replacement="totem")], duration=1)
    chicken = make_card("chicken")
    lignify.place_card(chicken, lignify.slots[0])
    lignify.start()
    lignify.tick()
    assert lignify.slots[0].card.name == 'Totem'