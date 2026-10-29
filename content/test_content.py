from models import Slot, SlotFate, VerbBox, VerbBoxState
from cards import make_card
from events import make_event
from game import Game

def test_upgrade_augury():
    r1 = make_card("augury_reagent_1")
    r2 = make_card("augury_reagent_1")
    e = make_event("upgrade_augury_reagent")
    game = Game(inventory=[r1,r2], active_events=[e], event_queue=[], turn=1, day=1)
    assert game.deploy_card(r1,e.verbbox,e.verbbox[0].slots[0]) is True