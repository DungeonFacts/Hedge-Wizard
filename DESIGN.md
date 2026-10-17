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