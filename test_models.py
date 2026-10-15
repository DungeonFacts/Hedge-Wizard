from models import Slot, VerbBox, VerbBoxState
from cards import make_card

def test_make_card_results_are_not_identical():
    a = make_card("wizard")
    b = make_card("wizard")
    assert (a == b) is False
    assert (a.name == b.name) is True
    return True


def test_slot_accepts_valid_card():
    a = make_card("wizard")
    slot = Slot(required_tags={"wizard"})
    slot.place_card(a)
    assert slot.is_filled() is True
    return True


def test_slot_rejects_wrong_tag():
    altar = Slot(required_tags={"sacred"})
    a = make_card("chicken")
    altar.place_card(a)
    assert altar.is_filled() is False
    return True


def test_slot_remove_card():
    altar = Slot(required_tags={"sacred"})
    a = make_card("sacred_oil")
    altar.place_card(a)
    assert altar.is_filled() is True
    altar.remove_card()
    assert altar.is_filled() is False
    return True


def test_slot_rejects_if_already_filled():
    altar = Slot(required_tags={"sacred"})
    a = make_card("sacred_oil")
    altar.place_card(a)
    assert altar.is_filled() is True
    b = make_card("sacred_perfume")
    altar.place_card(b)
    assert altar.card.tags == {"expensive","sacred"}
    return True


def test_basic_box_lifecycle():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2)
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
    a.tick()
    assert a.state == VerbBoxState.COMPLETED
    assert a.progress == 2
    return True


def test_interrupt_box_lifecycle():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2)
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
    return True

def test_add_slot():
    a = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=2)
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
    assert a.start() == False
    a.place_card(c, a.slots[1])
    assert a.state == VerbBoxState.LOADED
    a.start()
    a.tick()
    assert a.state == VerbBoxState.COMPLETED
    a.add_slot(card=None, required_tags=None)
    assert len(a.slots) == 3
    assert a.state == VerbBoxState.COMPLETED
    return True
