# Expected format of spell is below...
#
#"Spell Name"
#"nth Circle Subtype"
#"Cantrip - Cantrip Name" (arcane spells only)
#Body 1
#Body 2
#Body 3 etc.
# blank line

# Here are the fields we want to populate:
# Spell Name (parent)
# Speed (action, reaction, ritual)
# Spell level (first circle, second circle etc)
# Spell type (arcane, divine, primal)
  ## Spell subtype (Aetheric Divination, eg. Only for arcane and primal spells. Arcane spells have 2 descriptors, Primal spells usually have 1)
  ## Cantrip (only for arcane spells)
  ## Miracle subtype (blessing/curse/divination/summons, death domain etc. Divine miracles only)

# Content (spell description)
# Attack (is it an attack spell, yes or no)
  # Attack dice (number of dice rolled)
  # Attack range (contact, or # paces)
  # Attack area (point, cone, beam, bolt etc.)

#How to do all of the above (psuedocode):
#0. Define constants. Set spell type.
#1. Check if we're at a line break. If we are, reset line counter and enter newline. If not, read line, proceed below based on lineCounter.
#2. Read line 0. Save as spell name var. Increase line counter.
#3. Read line 1. Save as spell level var, spell/miracle subtype, miracle domain. Increase line counter.
#3a. Read line 2. Arcane spells: save as cantrip. increase line counter. Everyone else: read body (see below).
#4. Read body line-by-line. Save as content var. If keywords reaction or ritual are detected, set speed var.

import re
filename = 'MM all divine miracles raw.txt'


CLEANL = re.compile('‭') 
CLEANR = re.compile('‬') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANL, '', re.sub(CLEANR, '', raw_html))
  cleantext = cleantext.replace('"','\\"')
  return cleantext


def printSpellName(spellName):
	spellNameLine = '"' + spellName + '": {'
	print(spellNameLine)

def printSpellType(SPELLTYPE):
	spellTypeLine = '\t"Spell Type": "' + SPELLTYPE + '",'
	print(spellTypeLine)

def setSpeed(content):
	if content.find("reaction" or "Reaction") != -1:
		return "Reaction"
	elif content.find("ritual" or "Ritual") != -1:
		return "Ritual"
	else:
		return "Action"


def printSpeed(speed):
	speedLine = '\t"Speed": "' + speed + '",'
	print(speedLine)
	speed = "Action"


def printSpellLevel(line):
	spellLevelList = []
	spellLevelList = line.split()
	spellLevel = spellLevelList[0]
	spellLevelLine = '\t"Spell Level": "' + spellLevel + ' Circle",'
	print(spellLevelLine)


def printSubtype(line):
	subtypeList = []
	subtypeList = line.split()
	del subtypeList[0:2]
	if SPELLTYPE == "Arcane":
		spellSubtypeLine = '\t"Spell Subtype": "' + ' '.join(subtypeList) + '",'
		print(spellSubtypeLine)
	elif SPELLTYPE == "Divine":
		miracleSubtypeLine = '\t"Miracle Subtype": "' + ' '.join(subtypeList) + '",'
		print(miracleSubtypeLine)
	elif SPELLTYPE == "Primal":
		spellSubtypeLine = '\t"Spell Subtype": "' + ' '.join(subtypeList) + '",'
		print(spellSubtypeLine)


def printCantrip(line):
	cantripList = []
	cantripList = line.split(' - ')
	cantrip = cantripList[1]
	cantripLine = '\t"Cantrip": "' + cantrip + '",'
	print(cantripLine)


def printContent(content):
	print('\t"Content": "' + content + '"\n},')


spellName = ""
SPELLTYPE = "Divine"
speed=""
spellLevel = ""
subtype = ""
cantrip = ""
content=""

lineCounter = 0
num_lines = 0
numSpells = 0

with open(filename) as file_object:
	for line in file_object:
		cleanLine = cleanhtml(line).lstrip().rstrip()
		if cleanLine != '':
			if lineCounter == 0:
				spellName = cleanLine
			elif lineCounter == 1:
				spellLevel = cleanLine
				subtype = cleanLine
			elif lineCounter == 2:
				if SPELLTYPE == "Arcane":
					cantrip = cleanLine
				elif SPELLTYPE == "Primal" or "Divine":
					content = content + cleanLine
			elif lineCounter == 3:
				if SPELLTYPE == "Arcane":
					content = content + cleanLine
				elif SPELLTYPE == "Primal" or "Divine":
					content = content + " " + cleanLine
			elif lineCounter >3:
				content = content + " " + cleanLine
			lineCounter += 1

		if cleanLine == '':
			printSpellName(spellName)
			speed = setSpeed(content)
			printSpeed(speed)
			printSpellLevel(spellLevel)
			printSpellType(SPELLTYPE)
			printSubtype(subtype)
			if SPELLTYPE == "Arcane":
				printCantrip(cantrip)
			printContent(content)
			print(cleanLine)
			
			content=""
			lineCounter = 0
			numSpells += 1
			
		num_lines += 1
			
	print (f"\nI read {num_lines} lines and printed {numSpells} spells!")
