from dataclasses import dataclass
from events import EventState, make_event
from models import VerbBoxState

@dataclass()
class Game:
    inventory: list
    active_events: list
    turn: int 
    day: int 
    event_queue: list


    def deploy_card(self, card, verb, slot):
        """Place a card from inventory into a slot"""
        if card in self.inventory:
            if verb.place_card(card,slot) is True:
                self.inventory.remove(card)
                return True
            else:
                return False
        else:
            return False


    def retrieve_card(self, verb, slot):
        """Remove a card from the target slot and place it in inventory"""
        if slot.card is not None:
            if verb is None:
                card = slot.remove_card()
                self.inventory.append(card)
                return True
            else:
                card = verb.remove_card(slot)
                self.inventory.append(card)
                return True


    def add_event(self, event):
        """Create a new event instance in game"""
        new_event = make_event(event)
        self.active_events.append(new_event)
    

    def conclude_event(self, event):
        """Acknowledge a completed event and remove it from the active event list"""
        if event in self.active_events:
            event.ack()
            if event.is_blocking() is True:
                event.acknowledged = False
                return False
            else:
                self.active_events.remove(event)
                return True


    def queue_results(self):
        """Add results from completed and failed events to the event queue"""
        for event in self.active_events:
            if (event.state == EventState.SUCCESS) and (event.becomes is not None):
                self.event_queue.append(event.becomes)
            elif (event.state == EventState.FAILED) and (event.fails_to is not None):
                self.event_queue.append(event.fails_to)


    def queue_event(self):
        #add an event to the event queue
        pass


    def choose_event(self):
        #the player chooses an event from the active list to read, fill, claim, or acknowledge.
        pass


    def end_turn(self):
        for event in self.active_events:
            if event.is_blocking() is True:
                return False
        for event in self.active_events:
            event.tick()
            if event.verbbox.state == VerbBoxState.COMPLETED:
                event.state = EventState.SUCCESS
                return True
            elif event.deadline > (event.verbbox.duration - event.verbbox.progress):
                event.state = EventState.FAILED
                return True


    def start_turn(self):
        """Increment turn count, spawn queued events, empty event queue"""
        self.turn += 1
        turn_queue = list(self.event_queue)
        self.event_queue.clear()
        for event in turn_queue:
            self.add_event(event)


    def end_day(self):
        #conclude the current day and prepare for the next
        pass
