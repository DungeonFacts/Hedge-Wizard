from models import Slot, VerbBox, VerbBoxState
from cards import make_card


carve_totem = VerbBox("Carve Totem", slots=[Slot(required_tags={"wizard"})], duration=5)


print(make_card("wizard"))

