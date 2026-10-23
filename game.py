from dataclasses import dataclass
from events import Event

@dataclass()
class Game:
    inventory: list
    events: list
    turn: int 
    day: int 
    event_queue: list


    def deploy_card(self, card, verb, slot):
        if card in self.inventory:
            if verb.place_card(card,slot) is True:
                self.inventory.remove(card)
                return True


    def retrieve_card(self, verb, slot):
        if slot.card is not None:
            card = verb.remove_card(slot)
            self.inventory.append(card)
            return True
