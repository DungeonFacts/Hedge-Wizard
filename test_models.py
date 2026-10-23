from models import Slot, SlotFate, VerbBox, VerbBoxState
from cards import make_card
from events import make_event

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


def test_all_fates_combined():
    bless_baby = VerbBox("Bless Baby", slots=([Slot(required_tags={"wizard"}), Slot(required_tags={"baby"}, fate=SlotFate.REPLACE, replacement="blessed_baby"), Slot(required_tags={"sacred"}, fate=SlotFate.CONSUME)]), duration=1)
    baby = make_card("baby")
    wizard = make_card("wizard")
    oil = make_card("sacred_oil")
    bless_baby.place_card(wizard, bless_baby.slots[0])
    bless_baby.place_card(baby, bless_baby.slots[1])
    bless_baby.place_card(oil, bless_baby.slots[2])
    assert bless_baby.slots[0].card.name == 'Wizard'
    assert bless_baby.slots[1].card.name == 'Baby'
    assert bless_baby.slots[2].card.name == 'Sacred Oil'
    bless_baby.start()
    bless_baby.tick()
    assert bless_baby.state is VerbBoxState.COMPLETED
    assert bless_baby.slots[0].card.name == 'Wizard'
    assert bless_baby.slots[1].card.name == 'Blessed Baby'
    assert bless_baby.slots[2].card is None


def test_event_basic():
    welcome = make_event("welcome")
    assert welcome.name == "Welcome"
    assert welcome.narrative_text == "This card represents you, the wizard. Click it to add it to your tableau."
    assert welcome.deadline == None
    assert welcome.slots[0].required_tags == {'wizard'}
    assert welcome.becomes == "get_started"


def test_events_spawn_different_slots():
    a = make_event("welcome")
    b = make_event("welcome")
    assert a is not b
    assert a.slots[0] is not b.slots[0]
    assert a.slots[0].card is not b.slots[0].card
    assert a.slots[0].card.name == "Wizard"
    assert b.slots[0].card.name == "Wizard"


def test_events_spawn_different_verbboxes():
    a = make_event("get_started")
    b = make_event("get_started")
    assert a is not b
    assert a.verbbox is not b.verbbox


def test_event_box_contents_are_built_and_not_shared():
    a = make_event("get_started")
    b = make_event("get_started")
    assert a.verbbox.slots[0].required_tags == {"wizard"}
    assert a.verbbox.slots[0].card is None
    assert a.verbbox.results == ["totem"]
    assert a.verbbox.slots[0] is not b.verbbox.slots[0]
    assert a.verbbox.results is not b.verbbox.results


def test_complex_event_box():
    a = make_event("your_first_potion")
    b = make_event("your_first_potion")
    assert a.slots[0].card.name == "Tea Leaves"
    assert a.slots[0] is not b.slots[0]
    assert a.slots[0].card is not b.slots[0].card
    assert a.verbbox.slots[0].card == None


def test_event_message_window_is_blocker():
    intro = make_event("intro")
    assert intro.is_blocking() is True
    intro.ack()
    assert intro.is_blocking() is False


def test_empty_gift_window_is_blocker():
    welcome = make_event("welcome")
    assert welcome.slots[0].card.name == "Wizard"
    assert welcome.is_blocking() is True
    welcome.slots[0].remove_card()
    assert welcome.slots[0].card is None
    assert welcome.acknowledged is False
    assert welcome.slots[0].is_filled() is False
    assert welcome.is_blocking() is True
    welcome.ack()
    assert welcome.is_blocking() is False


def test_unclaimed_completed_event_is_blocking():
    a = make_event("your_first_potion")
    assert a.slots[0].card.name == "Tea Leaves"
    assert a.verbbox.slots[0].card == None
    assert a.is_blocking() is True
    removed_card = a.slots[0].remove_card()
    a.verbbox.place_card(removed_card,a.verbbox.slots[0])
    assert a.slots[0].card is None
    #should not block because this will become loaded
    assert a.is_blocking() is False
    assert a.verbbox.state == VerbBoxState.LOADED
    a.verbbox.start()
    a.verbbox.tick()
    assert a.verbbox.state == VerbBoxState.COMPLETED
    assert a.is_blocking() is True
    assert a.verbbox.slots[0].fate is SlotFate.REPLACE
    assert a.verbbox.slots[0].card.name == "Tea"
    #test that removing tea still requires acknowledgement
    a.verbbox.slots[0].remove_card()
    assert a.verbbox.slots[0].card is None
    assert a.is_blocking() is True
    a.ack()
    assert a.is_blocking() is False


def test_player_may_pass_after_claiming_gift():
    a = make_event("your_first_potion")
    a.slots[0].remove_card()
    assert a.is_blocking() is False


def test_verb_only_events_block_without_ack():
    a = make_event("get_started")
    wizard = make_card("wizard")
    assert a.slots is None
    a.verbbox.place_card(wizard,a.verbbox.slots[0])
    assert a.verbbox.slots[0].card is wizard
    a.verbbox.start()
    a.verbbox.tick()
    assert a.verbbox.state == VerbBoxState.COMPLETED
    a.verbbox.slots[0].remove_card()
    a.verbbox.slots[1].remove_card()
    assert a.verbbox.slots[0].card is None
    assert a.verbbox.slots[1].card is None
    assert a.is_blocking() is True
    a.ack()
    assert a.is_blocking() is False


def test_event_without_deadline_ticks():
    a = make_event("carve_totem")
    assert a.tick() is True
    assert a.verbbox.progress == 0
    wizard = make_card("wizard")
    a.verbbox.place_card(wizard,a.verbbox.slots[0])
    assert a.verbbox.slots[0].card.name == "Wizard"
    assert a.tick() is True
    assert a.verbbox.progress == 1
    assert a.tick() is True
    assert a.verbbox.progress == 2
    assert a.verbbox.slots[1].card.name == "Totem"
    assert a.tick() is True
    assert a.verbbox.progress == 2
    assert a.is_blocking() is True


def test_event_with_deadline_ticks():
    a = make_event("sacrifice_totem")
    totem = make_card("totem")
    a.verbbox.place_card(totem,a.verbbox.slots[0])
    assert a.verbbox.progress == 0
    assert a.verbbox.slots[0].card.name == "Totem"
    assert a.tick() is True
    assert a.verbbox.progress == 1
    assert a.verbbox.slots[0].card is None
    assert a.is_blocking() is True


def test_event_with_deadline_can_fail():
    a = make_event("sacrifice_totem")
    assert a.is_blocking() is False
    assert a.deadline == 1
    assert a.tick() is False
    assert a.deadline == 0
    assert a.verbbox.progress == 0
    assert a.verbbox.duration == 1
    #game.end_turn will now replace this with event.fails_to