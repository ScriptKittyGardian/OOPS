import random
import math

def xprint(string,newLine):
    if(not newline):
        print(string, end="", flush=True)
    else:
        print(string)


#Global variables:
levelUpHealth = 4
levelUpStrength = 1

dungeonW = 10
dungeonH = 10
dungeonSize = 5
levelTypes = list()
upStairRooms = [None] * dungeonSize
downStairRooms = [None] * dungeonSize
standardAdjectives = [
    "dank",
    "cramped",
    "dark",
    "depressing",
    "large",
    "wet",
    "damp",
    "stupidly large",
    "hilariously small"
]

standardNouns = [
    "water puddles",
    "discarded shackles",
    "ruined carpets",
    "rotting wood",
    "loose bricks",
    "scurrying mice"
    ]
for i in range(dungeonSize):
    levelTypes.append("standard")

    
def RollDice(sides,rolls=1):
    total = 0
    for i in range(0,rolls):
        total += random.randint(1,sides)
    return total
    
class Stats:
    def __init__(self,level,health,strength,armorclass):
        self.maxHealth = health
        self.health = health
        self.strength = strength
        self.maxStrength = strength
        self.armorclass = armorclass
        self.level = level
    def Display(self):
        print("Level: {0}".format(self.level))
        print("Health(c/m): {0} | {1}".format(self.health,self.maxHealth))
        print("Strength(c/m): {0} | {1}".format(self.strength,self.maxStrength))
        print("AC: {0}".format(10 + self.armorclass))



def CombineStats(toAdd,toChange,subtract=False):
    if(not subtract):
        toChange.health = toChange.health + toAdd.health
        toChange.strength = toChange.strength + toAdd.health
        toChange.armorclass = toChange.armorclass + toAdd.armorclass
        toChange.level = toChange.level + toAdd.level
    else:
        toChange.health = toChange.health - toAdd.health
        toChange.strength = toChange.strength - toAdd.health
        toChange.armorclass = toChange.armorclass - toAdd.armorclass
        toChange.level = toChange.level - toAdd.level
                

class Buff:
    def __init__(self,name,statchange,duration):
        self.name = name
        self.statchange = statchange
        self.duration = duration
    
class Entity:
    def __init__(self,name,stats):
        self.stats = stats
        self.name = name
        self.inventory = list()
        self.weapon = None
        self.xp = 10 + RollDice(10,self.stats.level)
    def GetStats(self):
        return self.stats
    def GetName(self):
        return self.name + "(Level {0})".format(self.stats.level)
    def SetStats(self,new):
        self.stats = new
    def DropLoot(self):
        global playerXp
        if(len(self.inventory) != 0):
            currentRoom.AddItem(self.inventory)
            print("The {0} dropped:".format(self.GetName()))
            ShowItems(self.inventory)
        if(self.weapon != None):
            currentRoom.AddItem(self.weapon)
        comparativeLevel = self.stats.level - playerStats.level
        if(comparativeLevel < 1):
            comparativeLevel = 1
        toAdd = self.xp * comparativeLevel
        if(toAdd > 0):
            print("You gained {0} XP.".format(toAdd))
            playerXp += toAdd

    def Turn(self):
        return
    
    def __del__(self):
            self.DropLoot()
            print("The {0} is dead!".format(self.GetName()))


class Item:
    def __init__(self,name,description,modifier=0,bc=""):
        self.name = name
        self.description = description
        self.modifier = modifier
        self.bc = bc
        self.inspected = True
    def Describe(self):
        print(self.description)
    def Inspect(self):
        self.inspected = True
        print("A {0}".format(self.GetName()))
    def GetName(self):
        toPrint = ''
        if(self.inspected):
            if(self.bc != ''):
                toPrint = self.bc.capitalize() + ' '
            if(self.modifier != 0):
                if(self.modifier > 0):
                    toPrint += '+{0} '.format(self.modifier)
                else:
                    toPrint += '{0} '.format(self.modifier)
            toPrint += self.name
            return toPrint
        return self.name
    def Use(self):
        print("You can't use this!")
        return False
    def Drink(self,stats):
        print("You can't drink that!")
        return False
    def Equip(self):
        print("You can't equip this!")
        return False
    def Loot(self):
        print("You take the {0}.".format(self.name))
        return True

class Equippable(Item):
    def __init__(self,name,description,equipSlot,modifier=0,bc=''):
        self.name = name
        self.description = description
        self.equipSlot = equipSlot
        self.statChange = Stats(0,0,0,0)
        self.modifier = modifier
        self.bc = bc
        self.inspected = False

    def Equip(self):
        if(playerEquipment[self.equipSlot] == None):
            playerEquipment[self.equipSlot] = self
            CombineStats(self.statChange,playerStats)
            return True
        elif(playerEquipment[self.equipSlot] == self):
            print("This is already equipped!")
            return False
        else:
            print("There is something in that slot.")
            return False
    def Unequip(self):
        if(self.bc != 'cursed'):
            CombineStats(self.statChange,playerStats,True)
            return True
        else:
            self.inspected = True
            return False
        
class Room:
    def __init__(self,name,description,items,x=0,y=0,floorNumber=0,stairs=''):
        self.name = name
        self.description = description
        self.items = items
        self.entityList = list()
        self.x = x
        self.y = y
        self.stairs = stairs
        self.floorNumber = floorNumber
        self.movement = {
            "north" : None,
            "east" : None,
            "south" : None,
            "west" : None}
    def AddItem(self,toAdd):
        self.items.append(toAdd)
    def AddEntity(self,toAdd):
        self.entityList.append(toAdd)
    def GetItems(self):
        return self.items
    def InitializeMovement(self,floor):
        if(self.y - 1 >= 0):
            test = floor[self.x][self.y - 1]
            if(test != 0):
                self.movement["north"] = test
        if(self.y + 1 <  dungeonH):
            test = floor[self.x][self.y + 1]
            if(test != 0):
                self.movement["south"] = test
        if(self.x - 1 >= 0):
            test = floor[self.x - 1][self.y]
            if(test != 0):
                self.movement["west"] = test
        if(self.x + 1 >= 0):
            test = floor[self.x + 1][self.y]
            if(test != 0):
                self.movement["east"] = test

    def DescribeMovement(self):
        for i in self.movement.keys():
            if(self.movement[i] != None):
                print("There is a door to the {0}.".format(i))
        if(self.stairs != ''):
            print("There are stairs {0}.".format(self.stairs))
    def Move(self,direction):
        global dungeonLevel
        if(direction in self.movement):
            if(self.movement[direction] != None):
                print("You move to the {0}.".format(direction))
                ChangeRoom(self.movement[direction])
                return True
            else:
                print("There is no door in that direction.")
                return False
        elif(direction == self.stairs):
            if(self.stairs == "down"):
                dungeonLevel += 1
                print("You go down the stairs.  Welcome to dungeon level {0}.".format(dungeonLevel))
                ChangeRoom(upStairRooms[dungeonLevel])
            else:
                if(dungeonLevel != 0):
                    dungeonLevel -= 1
                    print("You go up the stairs.  Welcome to dungeon level {0}.".format(dungeonLevel))
                    ChangeRoom(downStairRooms[dungeonLevel])
                else:
                    if(input("Are you sure you want to exit the dungeon? (y/n)") == "y"):
                        print("{0} was a coward and left the dungeon.".format(playerName))
                        exit()
                               
                
                
        else:
            print("That is not a valid direction")
                
    def DescribeItems(self):
        if len(self.items) == 0:
            print("There are no items in this room!")
        else:
            print("The following items are in this room:")
            for i in self.items:
                print(i.GetName())
    def Describe(self):
        print("You are in " + self.description.lower())
        if(len(self.items) > 0):
            print("Items in this room:")
            ShowItems(self.items)
        if(len(self.entityList) > 0):
            print("Monsters in this room:")
            ShowItems(self.entityList)
        self.DescribeMovement()

    def Inspect(self):
        if len(self.items) == 0:
            print("There are no items here!")
            return
        print("Which one would you like to inspect?")
        ShowItems(self.items)
        playerInput = int(input())
        if playerInput < len(self.items):
            self.items[playerInput].Describe()
        else:
            print("That isn't here.")
    def CheckForDead(self):
        for i in range(0,len(self.entityList)):
            if(self.entityList[i].stats.health <= 0):
                del(self.entityList[i])
                self.CheckForDead()
                break
    def UpdateEntities(self):
        self.CheckForDead()
        for i in range(0,len(self.entityList)):
            self.entityList[i].Turn()
    

class Armor(Equippable):
    def __init__(self,name,description,armorType,acChange,modifier=0,bc=''):
        self.name = name
        self.description = description
        self.equipSlot = armorType
        self.statChange = Stats(0,0,0,acChange + (modifier*-1))
        self.ac = acChange
        self.inspected = True
        self.modifier=modifier
        self.bc = bc

        
    

class Sword(Equippable):
    def __init__(self,name,description,diceNumber,diceValue,modifier=0,bc=''):
        self.name = name
        self.description = description
        self.diceNumber = diceNumber
        self.diceValue = diceValue
        self.equipSlot = "weapon"
        self.statChange = Stats(0,0,0,0)
        self.bc = bc
        self.modifier = modifier
        self.inspected = False
    def Describe(self):
        print(self.description)
        print("This item does " + str(self.diceNumber) + "d" + str(self.diceValue) + " damage.")

def ShowItems(thing):
    for i in range(0,len(thing)):
        print(str(i) + ' - ' + thing[i].GetName())


def GetItem(text):
    if(len(inventory) == 0):
        print("You have no items!")
        return -1
    ShowItems(inventory)
    put = int(input(text))
    if(put < len(inventory)):
        return put
    else:
        print("You don't have that item!")
        return -1
def TakeCommands():
    global playerWeapon
    while True:
        command = input("Input command:")
        if(command == "inspect room"):
            currentRoom.Inspect()
        if(command == "rest"):
            return
        if(command == "stop"):
            exit()
        if(command == "inspect"):
            if(len(inventory) > 0):
                ShowItems(inventory)
                selection = int(input("Item to inspect:"))
                if(selection < len(inventory)):
                    inventory[selection].Inspect()
                    return
                else:
                    print("You do not have that item!")
            else:
                print("You have nothing to inspect.")
        if(command == "loot"):
            if(len(currentRoom.GetItems()) > 0):
                ShowItems(currentRoom.items)
                selection = int(input("Item to loot:"))
                if(selection < len(currentRoom.GetItems())):
                    if(currentRoom.items[selection].Loot()):
                        inventory.append(currentRoom.items[selection])
                        del(currentRoom.items[selection])
                        return
                else:
                    print("That item is not in this room.")
        if(command == "inventory"):
            if(len(inventory) > 0):
                ShowItems(inventory)
                for key, item in playerEquipment.items():
                    if(item != None):
                        print("{0}: {1}".format(key.capitalize(),item.GetName()))
            else:
                print("You have nothing in your inventory.")
        if(command == "describe room"):
            currentRoom.Describe()
        if(command == "attack"):
            targets = currentRoom.entityList
            if(len(targets) == 0):
                print("Nothing to attack!")
            else:
                ShowItems(targets)
                selection = int(input("Target to attack:"))
                if(selection < len(targets)):
                    Attack(playerStats,targets[selection].stats,playerEquipment["weapon"],"self",targets[selection].name)
                    return
                else:
                    print("That monster is not here.")
        if(command == "drop"):
            toDrop = GetItem("Item to drop:")
            if(toDrop != -1):
                currentRoom.AddItem(inventory[toDrop])
                print("You drop the {0}".format(inventory[toDrop].GetName()))
                del(inventory[toDrop])
                return
        if(command == "wield"):
            toWield = GetItem("Item to wield:")
            if(toWield != -1):
                if(hasattr(inventory[toWield],'diceValue')):
                    if(inventory[toWield].Equip()):
                        print("You are now wielding the {0}".format(inventory[toWield].GetName()))
                        return
                else:
                    print("You can not wield that!")
            elif(len(inventory) > 0):
                playerWeapon = None
                print("You raise your fists.")
        if(command == "wear"):
            toWield = GetItem("Item to wear:")
            if(toWield != -1):
                if(hasattr(inventory[toWield],'ac')):
                    if(inventory[toWield].Equip()):
                        print("You are now wearing the {0}".format(inventory[toWield].GetName()))
                        return
                else:
                    print("You can not wear that!")
        if(command == "unequip"):
            for key, item in playerEquipment.items():
                if(item != None):
                    print("{0}: {1}".format(key.capitalize(),item.GetName()))
            slot = input("From what slot?")
            slot.lower()
            if(slot in playerEquipment):
                if(playerEquipment[slot] == None):
                    print("There is nothing in that slot!")
                else:
                    if(playerEquipment[slot].Unequip()):
                        print("You have unequipped the {0}.".format(playerEquipment[slot].GetName()))
                        playerEquipment[slot] = None
                    else:
                        print("You can't unequip cursed items!")
                    return
            else:
                print("That is not a valid slot.")
                
        if(command == "stats"):
            print("An adventurer named {0}".format(playerName))
            print("Currently on dungeon level {0}".format(dungeonLevel))
            playerStats.Display()
        if(command == "drink"):
            toUse = GetItem("Item to drink:")
            if(toUse != -1):
                if(inventory[toUse].Drink(playerStats)):
                    return
        if(command == "move"):
            currentRoom.DescribeMovement()
            direction = input("Move in which direction?")
            if(currentRoom.Move(direction)):
                return
            
            
                


class Goblin(Entity):
    def __init__(self,level=1,name="Goblin"):
        self.stats = Stats(level,RollDice(8,level),RollDice(2,level),0)
        self.weapon = None
        self.name = name
        self.inventory = list()
        self.xp = 10 + RollDice(10,self.stats.level)
        if(RollDice(8) <= level):
            self.weapon = items['rustySword'](random.choice(['','cursed','']),random.randint(-2,1))
            self.xp += 10
        self.canMove = True
    def Turn(self):
        if(self.canMove):
            Attack(self.stats,playerStats,self.weapon,self.name)
        

class Kobold(Entity):
    def __init__(self,level=1,name="Kobold"):
        self.stats = Stats(level,RollDice(4,level),RollDice(3,level),0)
        self.weapon = None
        self.name = name
        self.inventory = list()
        self.xp = 12 + RollDice(10,self.stats.level)
        if(RollDice(8) <= level):
            self.weapon = items['rustyScimitar'](random.choice(['','cursed','']),random.randint(-2,1))
            self.xp += 12
        self.canMove = True
    def Turn(self):
        if(self.canMove):
            Attack(self.stats,playerStats,self.weapon,self.name)
            




def Attack(aStats,dStats,aWep,attacker,defender=''):
    #damage roll
    if(aWep == None):
        weaponName = "bare hands"
    else:
        weaponName = aWep.GetName()
    if(attacker == "self"):
        print("You attack the " + defender + " with your " + weaponName + "!")
    else:
        print("The {0} swings their {1}!".format(attacker,weaponName)) 
    d20 = RollDice(20)
    if(dStats.armorclass >= 0):
        target = 10 + dStats.armorclass + aStats.level
    else:
        target = 10 + random.randint(dStats.armorclass,0) + aStats.level
    if(d20 >= target):
        if(attacker == "self"):
            print("You miss!")
        else:
            print("You dodge!")
        return
    damageDealt = RollDice(3,aStats.strength) #initial strength damage
    if(aWep != None):
        damageDealt += RollDice(aWep.diceValue,aWep.diceNumber) + aWep.modifier
    if(attacker == "self"):
        print("You deal {0} damage!".format(str(damageDealt)))
    else:
        print("The {0} deals {1} damage!".format(attacker,str(damageDealt)))
        print("You have {0} health.".format(dStats.health - damageDealt))
    dStats.health -= damageDealt


class HealthPotion(Item):
    def Drink(self,stats,user="self"):
        stats.health = stats.health + RollDice(10) + self.modifier
        if(stats.health > stats.maxHealth):
            stats.health = stats.maxHealth
        if(user == "self"):
            print("You feel much better.")
            print("You now have {0} health.".format(stats.health))
        else:
            print("The {0} drinks a health potion!".format(user))
        return True
class WeaknessPotion(Item):
    def Drink(self,stats,user="self"):
        stats.strength = stats.strength - RollDice(3) - self.modifier
        if(stats.strength < 1):
            stats.strength = 1
        if(user == "self"):
            print("You feel much weaker.")
            print("You now have {0} strength.".format(stats.strength))
        else:
            print("The {0} drinks a weakness potion!".format(user))
        return True
class StrengthPotion(Item):
    def Drink(self,stats,user="self"):
        stats.strength = stats.strength + RollDice(3) + self.modifier
        if(stats.strength > stats.maxStrength):
            stats.strength = stats.maxStrength
        if(user == "self"):
            print("You feel much stronger.")
            print("You now have {0} strength.".format(stats.strength))
        else:
            print("The {0} drinks a strength potion!".format(user))
        return True
levelOneLoot = []

#Equipment table
playerEquipment = {
    "helmet" : None,
    "chestplate" : None,
    "boots" : None,
    "weapon" : None,
    "amulet" : None,
    "ring" : None
    }



#item definitions go here

def rustySword(bc='',modifier=0):
    return Sword("Rusty Sword","A very rusty sword",1,3,modifier,bc)
def rustyScimitar(bc='',modifier=0):
    return Sword("Rusty Scimitar","A very rusty scimitar",2,2,modifier,bc)
def shinySword(bc='',modifier=0):
    return Sword("Shiny Sword","A very shiny sword",1,6,modifier,bc)
def healthPotion(bc='',modifier=0):
    return HealthPotion("Health Potion","A magical draught that restores 1d10 hitpoints.",modifier,bc)
def strengthPotion(bc='',modifier=0):
    return StrengthPotion("Strength Potion","A magical draught that restores 1d3 strength.",modifier,bc)
def weaknessPotion(bc='',modifier=0):
    return WeaknessPotion("Weakness Potion","A magical draught that subtracts 1d3 strength.",modifier,bc)
def rustyChestplate(bc='',modifier=0):
    return Armor("Rusty Chestplate","A very rusty chestplate.  It looks uncomfortable.","chestplate",-2,modifier,bc)
def rustyHelmet(bc='',modifier=0):
    return Armor("Rusty Helmet","A very rusty helmet.  Your head won't like you for this.","helmet",-1,modifier,bc)
def rustyBoots(bc='',modifier=0):
    return Armor("Rusty Boots","A very rusty pair of boots.  They won't slow you down, but you'll wonder why you're wearing them.",-1,modifier,bc)
def shinyChestplate(bc='',modifier=0):
    return Armor("Shiny Chestplate","A very shiny chestplate.  It looks almost robust.","chestplate",-3,modifier,bc)
def shinyHelmet(bc='',modifier=0):
    return Armor("Shiny Helmet","A very shiny helmet.  It's a pity there isn't anyone else in this dungeon, because this helmet looks F.A.B.U.L.O.U.S!","helmet",-2,modifier,bc)
def shinyBoots(bc='',modifier=0):
    return Armor("Shiny Boots","A very shiny pair of boots.  Try not to admire them and watch where you're walking.",-2,modifier,bc)

items = {
    'healthPotion' : healthPotion,
    #Rusty armor set
    'rustyChestplate' : rustyChestplate,
    'rustyHelmet' : rustyHelmet,
    'rustyBoots' : rustyBoots,
    'rustySword' : rustySword,
    #Shiny armor set
    'shinyChestplate' : shinyChestplate,
    'shinyHelmet' : shinyHelmet,
    'shinyBoots' : shinyBoots,
    'shinySword' : shinySword,
    'strengthPotion' : strengthPotion,
    'weaknessPotion' : weaknessPotion
    }

lootTable = list()
#Level 0 loot
lootTable.append(['rustyHelmet',
                  'rustyBoots',
                  'rustyChestplate',
                  'rustySword',
                  'healthPotion'])
#Level 1 Loot
lootTable.append(['shinyChestplate',
                  'shinyHelmet',
                  'shinyBoots',
                  'shinySword'])
mons = {
    'goblin' : Goblin,
    'kobold' : Kobold
    }
enemyTable = list()
#level 0 Monsters
enemyTable.append(['goblin','kobold'])
def GenerateDescription(levelNumber):
    lt = levelTypes[levelNumber]
    if lt == "standard":
        adj = standardAdjectives[random.randint(0,len(standardAdjectives) - 1)]
        nounIndex = random.randint(0,len(standardNouns) - 1)
        n1 = standardNouns[nounIndex]
        newIndex = random.randint(0,len(standardNouns) - 1)
        while newIndex == nounIndex:
            newIndex = random.randint(0,len(standardNouns) - 1)
        n2 = standardNouns[newIndex]
        return "A {0} stone room, filled with {1} and {2}.".format(adj,n1,n2)

def GenerateRoom(levelNumber,x,y):
    return Room("stone room",GenerateDescription(levelNumber),list(),x,y,levelNumber)

def GenerateDungeon(levelNumber):
    global currentRoom
    toReturn = [[0 for x in range(dungeonW + 1)] for y in range(dungeonH + 1)] 
    numberOfRooms = random.randint(3,20)
    generatedRooms = list()
    generationCandidates = list()
    x = random.randint(0,dungeonW - 1)
    y = random.randint(0,dungeonH - 1)
    firstRoom = GenerateRoom(levelNumber,x,y)
    toReturn[x][y] = firstRoom
    generatedRooms.append(firstRoom)
    generationCandidates.append(firstRoom)
    for i in range(0,numberOfRooms):
        if(len(generationCandidates) > 0):
            testX = generationCandidates[0].x
            testY = generationCandidates[0].y
            generateX = testX
            generateY = testY
            side = random.randint(0,3)
            change = False
            for s in range(0,4):
                if(side == 0):
                    if(generateX - 1 >= 0 ):
                        if(toReturn[testX - 1][testY] == 0):
                            generateX -= 1
                            change = True
                            break                            
                elif(side == 1):
                    if(generateY - 1 >= 0):
                        if(toReturn[testX][testY - 1] == 0):
                            generateY -= 1
                            change = True
                            break
                elif(side == 2):
                    if(generateX + 1 < dungeonW):
                        if(toReturn[testX + 1][testY] == 0):
                            generateX += 1
                            change = True
                            break
                elif(side == 3):
                    if(generateY + 1 < dungeonH):
                        if(toReturn[testX][testY + 1] == 0):
                            generateY += 1
                            change = True
                            break
                side += 1
                if(side > 3):
                    side = 0
            if(change):
                newRoom = GenerateRoom(levelNumber,generateX,generateY)
                toReturn[generateX][generateY] = newRoom
                generatedRooms.append(newRoom)
                generationCandidates.append(newRoom)
                if(random.randint(0,4) != 1):
                    del(generationCandidates[0])
            else:
                del(generationCandidates[0])
        else:
            break
    spawnRoom = random.randint(0,len(generatedRooms) - 1)
    roomModify = generatedRooms[spawnRoom]
    roomModify.stairs = "up"
    upStairRooms[levelNumber] = roomModify
    for i in generatedRooms:
        i.InitializeMovement(toReturn)
    #ChangeRoom(roomModify)
    del(generatedRooms[spawnRoom])
    downStairs = random.randint(0,len(generatedRooms) - 1)
    generatedRooms[downStairs].stairs = "down"
    #generatedRooms[downStairs].InitializeMovement(toReturn)
    downStairRooms[levelNumber] = generatedRooms[downStairs]
    return toReturn




def ChangeRoom(newRoom):
    global currentRoom
    currentRoom = newRoom
    currentRoom.Describe()
playerName = input("What is your name:")
dungeon = list()
for i in range(dungeonSize) :
    dungeon.append(GenerateDungeon(i))
ChangeRoom(upStairRooms[0])


#currentRoom = Room("stone room","A dank stone room, filled with bricks and water puddles.",list())
playerStats = Stats(1,10,3,0)
dungeonLevel = 0
playerWeapon = None
playerXp = 0
inventory = list()
xpTarget = 10



currentRoom.AddItem(items['rustySword']('blessed',2))
currentRoom.AddItem(items['healthPotion']())
currentRoom.AddItem(items['rustyChestplate']())
#currentRoom.AddEntity(mons['goblin']())

def CheckLevelUp():
    global xpTarget
    if(playerXp >= xpTarget):
        playerStats.maxHealth += levelUpHealth
        playerStats.maxStrength += levelUpStrength
        playerStats.strength += levelUpStrength
        playerStats.health += levelUpHealth
        playerStats.level += 1
        print("Welcome to level {0}".format(playerStats.level))
        xpTarget = xpTarget * 2
    
while True:
    CheckLevelUp()
    TakeCommands()
    currentRoom.UpdateEntities()



