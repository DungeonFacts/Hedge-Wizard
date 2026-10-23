# Hedge Wizard: Design Notes

Last updated: 2026-10-16. Prototype stage: rules layer only, tested with pytest, no UI yet.

This document records what has been decided and why. The code is the source of truth for what is built; this is the source of truth for intent. Each section marks what is **Decided**, **Built**, or **Not built**. Open questions are collected at the end.

## 1. Concept

You play a village wizard. Your time goes to personal projects (carving glyphs, collecting reagents, appeasing spirits) and to helping villagers (blessing babies, calling rain, healing boils).

Mechanically it is a turn-based, Cultist Simulator-style game: **verb boxes** have **slots**, you fill slots with **cards**, time ticks, and tasks resolve and hand back results.

**Why turn-based.** Cultist Simulator runs in real time with pause, which builds tension but was frustrating, and the pause button got used so often that the game was effectively turn-based anyway. Here the tension comes from planning, not reflexes.

**Core theme: time and resource management.** Ingredients and hours are finite, and good planning is the skill. You could carve a totem in one uninterrupted day, but a potion needs stirring, a new mother wants a blessing for her baby, and the berries get eaten by birds if they are not picked in the morning. Time ticks globally, so poor planning can leave two deadlines that cannot both be met.

## 2. Time model

- **Decided.** One turn is one hour. A day is 12 turns.
- **Decided.** Turn flow: display tasks, assign resources, press End Turn. This is deliberate planning (what can wait, what cannot, whether two countdowns collide), not a scramble to fill boxes.
- **Decided.** Each day is a reset: tasks are dismissed at day's end. The only cross-day state committed so far is **inventory**.
- **Decided.** Unmet tasks can come back. An unseen medical-aid villager has a 50% chance of returning the next day; a missed social visit goes back into the event queue.
- **Decided.** Overnight and multi-day actions are for later.
- **Decided.** When progress and a deadline land on the same tick, progress completion resolves first.

## 3. Scarcity

- **Decided.** Two things are scarce: the number of boxes, and the number of agents.
- **Decided.** In the prototype there is one wizard, and at most one verb can run unattended. Homunculi and summoned spirits as extra agents come after the prototype.
- **Decided.** Attended tasks have a slot that needs the Wizard card, and only progress while it is filled. Unattended tasks (a brewing potion) have no wizard slot.

## 4. Cards

- **Decided.** Everything that is not a verb is a card. Inventory is a list of cards, and villagers are cards.
- **Decided.** A card is a name plus a **set of tags**. Tags are free-form strings, and there is no master list of valid tags for now.
- **Decided.** Stations (altar, alchemy table, firepit) are cards that are usually returned and sometimes modified, not a separate concept.
- **Decided.** A card can be consumed (sacred oil in a blessing), replaced by another card (chicken becomes meal), or returned (the Wizard card).
- **Decided.** Cards are never modified in place. To change a card, replace it with a different card. This avoids emergent edge cases such as a knife that somehow gains Consecrated, Edible and Taboo. If tag editing is ever needed, it will be designed separately.
- **Built.** Card templates are plain data in `CARD_TEMPLATES` (name plus tags). `make_card(key)` mints a fresh `Card` and gives it its own copy of the tag set. Never share a Card object or a tag set between two places: the game has one wizard and many totems, and each totem must be its own object.
- **Not built.** Card expiry (stale reagents, melting ice). It is not needed for the prototype.

Tags make choices interesting. Any of sacred oil, incense or perfume can satisfy a "sacred" slot, but oil is expensive, incense carries an Unpleasant tag, and perfume may trigger a villager's allergy.

## 5. Slots

- **Built.** A slot holds at most one card and has `required_tags`. A card is accepted only if it has **all** required tags and the slot is empty. Removing returns the card to the caller, who decides where it goes.
- **Built.** Every slot has a **fate** that applies when its box completes: `KEEP` (the card stays and is returned to the player), `CONSUME` (the card is removed and dropped), or `REPLACE` (the card is swapped for a fresh card made from a template key).
- **Built.** `force_card` places a card without checking tags. It is for system-driven placement (results, replacements), not for player input.
- **Decided.** Slots are never deleted, only locked and possibly not drawn.
- **Decided.** Slots are addressed by object (or index), not by name. The player-facing label comes from the required tags.

## 6. Verb boxes and events

A box has a name, a list of slots, a duration in ticks, a progress counter, a state, and a list of result card keys.

**States.** `UNLOADED` (some slot empty), `LOADED` (all slots filled), `RUNNING`, `COMPLETED`.

**Rules.** *Built.*
- `update_state` recomputes the state from the slots. `COMPLETED` is final. All slots filled means `LOADED`; any empty slot means `UNLOADED`, including for a `RUNNING` box, in which case progress is kept.
- `start()` works only from `LOADED`.
- `tick()` advances progress only while `RUNNING`. When progress reaches the duration, the box sets `COMPLETED` **first**, then applies slot fates, then spawns results. The order matters: consuming a card empties a slot, and `update_state` would otherwise drop a running box back to `UNLOADED`.
- Adding a slot to a running box stops it (`UNLOADED`) and keeps progress. This lets a craft suddenly demand an extra reagent or assistant. Adding a slot to a `COMPLETED` box leaves it `COMPLETED`.
- Interrupting an interruptible task (removing the wizard from Carve Totem) puts the box back to `UNLOADED` with progress kept. Putting the card back and starting again resumes it.
- Results are a **list** of card keys, so duplicates are allowed (a set would drop them). Each result is a fresh card in a new pre-filled slot. A box with no results is valid.

**Decided, not built.**
- **Acknowledging results.** The player must acknowledge a finished event; the box does not vanish silently. A message window on conclusion is planned, with an optional auto-close setting later. A finished box becomes dismissible when it is `COMPLETED` and every slot is empty.
- **Interruptibility.** Some tasks can be left freely (carving). Some cannot (a rain dance: its slots disappear, meaning they are locked and hidden, while it runs). Some can be left at a price (leave foraging for a pixie's request and you earn a blessing; abandon lunch to bless a baby and the chicken burns). This needs an `interruptible` property on events.
- **Events as data.** An event definition holds input slots (required tags and fate), results, narrative text per stage (available, running, complete), a deadline duration, failure outputs, and a `becomes` field naming the next event (`None` means it ends). Events are looked up by name, so definitions can refer to each other.
- **Chaining.** `becomes` replaces the idea of a persistent workstation. Carve Totem chains into itself so you can carve another. A shared Angry Villager failure event is reused instead of writing bespoke failures.

## 7. Deadlines and failure (not built)

- **Decided.** A deadline keeps counting after a task has started. On a tie, progress completion resolves first.
- **Decided.** Consequences of missing a deadline vary: the event is shuffled back into the queue, it vanishes harmlessly, or it imposes a penalty (an Angry Villager card, stolen reagents, bad karma with a spirit).
- **Decided.** An angry villager can be appeased the next day. Three angry villagers is game over. Angering the rain god is a harder debt to repair.
- **Implementation note.** Deadlines must count down in every state except `COMPLETED`, so `tick()` cannot do all its work inside the `RUNNING` branch.

## 8. Winning, losing, randomness

- **Decided.** Prototype win: solve all of the day's problems. Loss: three angry villagers.
- **Decided.** Long-term win ideas: accumulate enough karma to become the rain god's heir, or survive 100 days and die of old age.
- **Decided.** The prototype is fully deterministic. Possible RNG later: rain dance success scaling with incense burned, foraging results, 1d3 coins as payment. It may stay deterministic if that is more fun.

## 9. Scenarios

| Scenario | Shape | Status |
|---|---|---|
| **Carve Totem** | One wizard slot. Interruptible. Returns the wizard and a totem. Chains into itself. | Interrupt and resume, result spawn: tested. Reset via `becomes`: not built. |
| **Bless Baby** | Wizard (keep), baby (replace with blessed baby), reagent (consume). One tick. Ignored for 3 ticks gives an Angry Villager and cannot be completed. | Fates: built. Deadline and failure: not built. |
| **Rain Dance** | Wizard plus villager. Slots hidden while running (non-interruptible). Returns the wizard and a reward. | Not built. |
| Burn Totem, Lignify Chicken | Consume-only and replace-only examples. | Tested. |
| Consecrate Knife | Oil consumed, knife replaced by a consecrated knife. | Expressible with current fates; no test yet. |

## 10. Code layout and principles

- `cards.py`: `Card`, `CARD_TEMPLATES`, `make_card`.
- `models.py`: `SlotFate`, `Slot`, `VerbBoxState`, `VerbBox`.
- `HedgeWizard.py`: entry point (a stub).
- `test_models.py`: pytest suite. Every test builds its own fresh objects with `make_card`.

**Principles.**
- A method knows only about `self` and its arguments. Slots and boxes **enforce rules and report back** (a bool, or the removed card). The game loop and the UI decide what to do with that.
- Methods named `is_...` are pure questions. They never change state.
- Dependencies point one way: `models` imports `cards`, tests import code, and code never imports tests.
- Still to write: a `Game` object that owns the boxes and the turn counter, with an `end_turn()` that ticks every box. After that, a console interface (lists first), then a real UI.

**How this is developed.** The author writes the code, as a way of learning Python. Claude acts as tutor and reviewer: it explains, assigns small pieces, and reviews code instead of handing over finished modules.

## 11. Open questions

- What carries across days besides inventory (angry villagers? karma?).
- Placing a card into a `COMPLETED` box is currently allowed at the rules layer, on the assumption that the UI will not offer it. Revisit once there is a console loop with no UI to hide it.
- How a consume-only event acknowledges its outcome, given that all slots are empty the moment it completes.
- Whether tag editing is ever needed, or replacement is always enough.
- What replacing a villager card costs: a replaced card loses its individual identity.
- Where event definitions live and in what format (a Python dictionary now, possibly JSON later).
- Whether inputs are consumed when a task completes (current behavior) or when it starts.

###### Update 10/19/2026 ######

- Answers to open questions:
    Inventory carries over between days (which can include angry villagers). Some events may respawn the next day (permanent ones such as "Carve Totem" and renewable ones such as "Herb Box").
    Placing cards into a completed box will not be offered by the UI.
    Events require acknowledgement for any resolution method, so consume-only events will follow this standard.
    Standardizing on replacement minimizes edge cases. "Play the hand you are dealt" is preferred over trying to custom-build a perfect solution to every problem.
    Replacing villagers will have some generic cases (Angry Villagers can accumulate and end the game) but others will be bespoke questline-style progressions.
    For now we'll build in dictionaries, JSON can come later (this is a stretch goal for learning, mostly).
    Inputs will continue to be consumed when the task completes. For interruptible tasks this lets us swap cards, uninterruptible ones will simply block the slot. (Which reminds me that I'll need to ask if Events have an Interruptible flag.)

- Architecture update:
    The new Event class and list of events currently live in events.py, which also holds the templates for the functions make_event and make_slot. Events can spawn with slots (e.g. something given to the player at the start of an event), with verbs (most events will focus on the action the player chooses to take), or with both slots and a verb. For now, Events can have an arbitrary number of slots, and one only verb.
    Naming convention for factory functions is make_foo.

- With Events added to the code base, our next objective is the event.tick() function which determines what happens, exactly, when the 'End Turn' button is pressed. Broadly, each event should check for status, progress on verbs should increment, check for completion, decrement the deadline on non-completed events, and return to the player to set up the next turn. Deadline is defined as the number of turns remaining before the event expires. There are four salient test cases:
    1. Normal completion: an event with a RUNNING verb box updates to COMPLETED. Results for the verb box spawn (and can be claimed the next turn). The deadline counter no longer measures whether a pending job can fail, so it can decremented to 0. The event waits for the player to take any kept or spawned cards, and acknowledge completion before dismissing.
    2. Expiry: an event with an UNLOADED verb box that the player has chosen not to fill this turn. At End Turn, no verbs should advance, the deadline is decremented. If doing so renders the event unachievable (i.e. the deadline is less than the event duration minus progress), it will display its fail state (note that this can be as mild as the card returning to the event queue, or as extreme as spawning negative cards).
    3. Tie case: a RUNNING event with a Deadline of 1 and a (Duration - Progress) of 1. These are likely to be the majority of results. Decrementing the Deadline first would result in failure, and as such we run verb.tick() and increment progress first, check for completion, and then decrement the Deadline to 0 in cases of a tie. This is effectively a special case of Normal Completion.
    4. Deadline = None. These are tasks that never expire. The most obvious use case is for tasks that can be done indefinitely at any time, and long-term progression 'questline' style events. RUNNING verbs will need to progress and possibly complete and spawn results, but no deadline check is necessary.

- As such, basic sketch of the event.tick() function:
    1. Check the status of each event.
    2. Events with no status (such as a plain message window) halt the tick() and force the player to acknowledge.
    3. For events that were already COMPLETED, halt the tick() and force the player to acknowledge the events.
    4. Report to the engine to HALT if there are unacknowledged events. If not, proceed to tick remaining events.
    5. For events with a LOADED verb status, run verb.start() and verb.tick().
    6. For events with a RUNNING verb status, increment verb progress (verb.tick()).
    7. For events that thereby update to a COMPLETED status, spawn results. Then, decrement the deadline.
    8. For events with an UNLOADED verb status, decrement the deadline.
    9. For events that now have a deadline < (duration - progress), flag for replacement with failstate.
    10. For events that have a deadline of None, they will pass on UNLOADED, start() and tick() on LOADED, tick() on RUNNING, and halt to require acknowledgement if they were already COMPLETED.
    11. Pass to the engine that End Turn should either HALT, or that all Events have been ticked.

## Update 10/23/26

Work is complete for the events module and associated tests, and we are ready to begin implementing the game module. For a first pass, the game module will need to do the following:
    1. Track a list of cards in inventory
    2. Track a list of events currently active
    3. A start_day function to increment the day counter, spawn events at the beginning of the day, which needs a list of eligible and queued events from the previous day
    4. Track the current turn number, starting at 1 and incrementing when game.end_turn is called
    5. A next_event function which results the becomes and fails_to properties of completed events
    6. Tracks card position between functions (e.g. if a card is removed from a verb, it should be placed in player inventory, and vice versa). Events only know what we give them, game controls moving cards between instances.
    7. Players will need a way to choose an event to read, and functions for placing/removing cards thereunto, and a way to return to the board overview.
    8. Players will need a function acknowledge an event when it is complete.
    9. Close an event when the event is acknowledged. This will require a function which removes the event from the event list.
    10. An end_turn function which does the following:
        a. Checks every event for is_blocking, and stops to alert the player of events to acknowledge
        b. If no events are blocking, tick the remaining events.
        c. Result failures with new events
        d. Ongoing and completing events remain on board for the player to collect results next turn
        e. Increment the turn counter
        f. Return control to the player
        g. If it's the last turn of the day, allow the player to collect their results, and replace End Turn with End Day
    11. end_day will evaluate any remaining events to see if they dismiss or return to the event queue, checks inventory to pass over to the next day, increments the day counter, and returns to start_day