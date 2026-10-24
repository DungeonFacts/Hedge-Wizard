from dataclasses import dataclass
from events import make_event

@dataclass()
class Game:
    inventory: list
    events: list
    turn: int 
    day: int 
    event_queue: list


    def deploy_card(self, card, verb, slot):
        """Place a card from inventory into a slot"""
        if card in self.inventory:
            if verb.place_card(card,slot) is True:
                self.inventory.remove(card)
                return True


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
        self.events.append(new_event)
        return self.events
    

    def conclude_event(self, event): #incomplete WIP
        """Acknowledge a completed event and remove it from the active event list"""
        if event in self.events:
            event.ack()
            if event.is_blocking() is False:
                self.events.remove(event)
                return True


    def make_failure(self, event):
        """An event which fails spawns its failure result"""
        new_event = event.fails_to
        return self.add_event(new_event)


    def make_becomes(self, event):
        """An event which completes before its deadline spawns its becomes field"""
        new_event = event.becomes
        return self.add_event(new_event)


    def queue_event():
        #add an event to the event queue
        pass


    def choose_event():
        #the player chooses an event from the active list to read, fill, claim, or acknowledge.
        pass


    def end_turn(self): #very much WIP
        ticked_events = []
        failed_events = []
        for event in self.events:
            if event.is_blocking() is True:
                return False
        for event in self.events:
            if event.tick() is True:
                ticked_events.append(event)
            elif event.tick() is False:
                failed_events.append(event)
        #should end_turn stop here, and let start_turn do the following?
        for event in ticked_events:
            self.make_becomes(event)
        for event in failed_events:
            self.make_failure(event)


    def start_turn():
        #spawn new events
        pass


    def end_day():
        #conclude the current day and prepare for the next
        pass
