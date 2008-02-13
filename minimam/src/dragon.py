from warrior import Warrior
from rogue   import Rogue
from wizard  import Wizard
from priest  import Priest

# Dragon inherits the advantages of all other classes.
# IMPORTANT NOTE: Warrior comes after Rogue
# because Warrior has better defenseRoll method.

class Dragon(Rogue, Warrior, Wizard, Priest):
  pass

  
