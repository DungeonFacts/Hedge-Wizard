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


    def make_failure():
        #an event which cannot meet its deadline procs its fails_to consequence
        pass


    def make_becomes():
        #an event which completes before its deadline spawns its becomes field
        pass


    def queue_event():
        #add an event to the event queue
        pass


    def acknowledge_event():
        #a completed event or message window is closes and is removed from the event queue
        pass


    def choose_event():
        #the player chooses an event from the active list to read, fill, claim, or acknowledge.
        pass


    def end_turn():
        #check events for blockers, tick events
        pass


    def start_turn():
        #spawn new events
        pass


    def end_day():
        #conclude the current day and prepare for the next
        pass
