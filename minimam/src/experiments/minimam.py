import random

class Character:
	def __init__(self, name="", classname="monster", level=0, health="healthy"):
		self.name = name
		self.classname = classname
		self.level = level
		self.health = health
		self.escaping = False
		self.escaped = False

	def attackRoll(self):
		roll = random.randrange(6) + 1
		print " %s's roll: %s + %s (level)" % (self.name, roll, self.level),
		roll = roll + self.level
		if self.classname == "warrior" or self.classname == "dragon":
			print "+ 1 (%s)" % self.classname,
			roll = roll + 1	
		if self.health == "injured":
			print " - 1 (injured)",
			roll = roll - 1
		print "= %s" % roll
		return roll

	def defenseRoll(self):
		roll = random.randrange(6) + 1
		print " %s's roll: %s + %s (level)" % (self.name, roll, self.level),
		roll = roll + self.level
		if self.escaping and (self.classname == "rogue" or self.classname == "dragon"):
			print "+ 1 (escaping %s)" % self.classname,
			roll = roll + 1
		elif self.classname == "warrior" or self.classname == "dragon":
			print "+ 1 (%s)" % self.classname,
			roll = roll + 1
		if self.health == "injured":
			print "- 1 (injured)",
			roll = roll - 1
		print "= %s" % roll
		return roll

	def fight(self, other):
		print "%s is attacking %s." % (self.name, other.name)
		attack = self.attackRoll()
		defense = other.defenseRoll()
		if attack > defense:
			other.escaping = False
			if self.classname == "wizard" or self.classname == "dragon":
				other.health = "incapacitated"
				print " %s blasted %s with a fireball!" % (self.name, other.name)
			elif other.health == "injured":
				other.health = "incapacitated"
				print " %s incapacitated %s." % (self.name, other.name)
			else:
				other.health = "injured"
				print " %s injured %s." % (self.name, other.name)
		else:
			print " The attack failed."
		
	def heal(self, other):
		print "%s healed %s" % (self.name, other.name),
		if other.health == "injured":
			other.health = "healthy"
			print "and %s is now healthy" % other.name
		elif other.health == "incapacitated":
			other.health = "injured"
			print "but %s is still injured" % other.name


	def menu(self):
		report()
		print "%s's turn:" % self.name
		print "0. escape"
		actions = {0: "escape"}
		targets = {0: None}
		i = 1
		for character in NPCs:
			if character.escaped: continue
			if character.health == "incapacitated": continue
			print "%s. attack %s" % (i, character.name)
			actions[i] = "attack"
			targets[i] = character
			i = i + 1
		if self.classname == "priest" or self.classname == "dragon":
			for character in PCs:
				if character.escaped: continue
				if character.health == "healthy": continue
				print "%s. heal %s" % (i, character.name)
				actions[i] = "heal"
				targets[i] = character
				i = i + 1
		while True:
			try:
				choice = int(raw_input())
				action = actions[choice]
				target = targets[choice]
			except:
				continue
			break
		if   action == "escape": self.escaping = True
		elif action == "attack": self.fight(target)
		elif action == "heal":   self.heal(target)

	def ai(self):
		# weak minions flee when injured
		if self.level == 0 and self.health == "injured":
			print "%s is trying to escape" % self.name
			self.escaping = True
			return

		# heal allies who are injured but not trying to escape
		if self.classname == "priest" or self.classname == "dragon":
			for character in NPCs:
				if character.escaping: continue
				if character.health != "injured": continue
				self.heal(character)
				return
		targets = []
		for character in PCs:
			if character.escaped: continue
			if character.health == "incapacitated": continue
			targets.append(character)

		# use fireball on healthy enemy who is not trying to escape
		if self.classname == "wizard" or self.classname == "dragon":
			best = []
			for character in targets:
				if character.escaping: continue
				if character.health != "healthy": continue
				best.append(character)
			if len(best) > 0:
				self.fight(random.choice(best))
				return

		# attack a random enemy
		self.fight(random.choice(targets))

	def __repr__(self):
		str = "%s, %s level %s %s" % (self.name, self.health, self.level, self.classname)
		if self.escaped: str = str + " (escaped)" 
		return str 

PCs = (Character("The Lone Ninja", "rogue",   1),
       Character("Kronenburg",     "warrior", 1),
       Character("Sankti Monyos",  "priest",  1),
       Character("Necromangler",   "wizard",  1))

NPCs = (Character("goblin A"),
        Character("goblin B"),
        Character("goblin C"),
        Character("goblin D"),
        Character("goblin E"),
        Character("Smoggy", "dragon", 2))

def report():
	print "Good Guys:"
	for character in PCs:
		print "\t%s" % character
	print "Bad Guys:"
	for character in NPCs:
		print "\t%s" % character

def allDead(party):
	for character in party:
		if character.health != "incapacitated":
			return False
	return True

def allGone(party):
	for character in party:
		if character.health != "incapacitated":
			if character.escaped != True:
				return False
	return True

def alternate(team1, team2):
	merged = []
	i = 0
	while i < len(team1) and i < len(team2):
		merged.append(team1[i])
		merged.append(team2[i])
		i = i + 1
	if i < len(team1):
		merged = merged + team1[i:]
	if i < len(team2):
		merged = merged + team2[i:]

	return merged
	

def initiative(team1, team2):
	first1 = []
	last1 = []
	for character in team1:
		if character.classname == "rogue" or character.classname == "dragon":
			first1.append(character)
		else:
			last1.append(character)
	first2 = []
	last2 = []
	for character in team2:
		if character.classname == "rogue" or character.classname == "dragon":
			first2.append(character)
		else:
			last2.append(character)

	return alternate(first1, first2) + alternate(last1, last2)

def play():
	order = initiative(PCs, NPCs)
	while True:
		for character in order:
			if allDead(PCs):
				report()
				print "Thy partie hathe beene slained..."
				return
			if allGone(PCs):
				report()
				print "Thy partie hathe fledde lyke cowardes..."
				return
			if allGone(NPCs):
				report()
				print "Thou arte victorious!"
				return

			if character.health == "incapacitated" or character.escaped:
				continue
			if character.escaping:
				character.escaped = True
				print "%s escaped." % character.name
				continue

			if character in PCs:  character.menu()
			if character in NPCs: character.ai()

play()