import random

def xprint(string,newLine):
    if(not newline):
        print(string, end="", flush=True)
    else:
        print(string)



    
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
    def GetStats(self):
        return self.stats
    def GetName(self):
        return self.name + "(Level {0})".format(self.stats.level)
    def SetStats(self,new):
        self.stats = new
    def Turn(self):
        return



class Item:
    def __init__(self,name,description):
        self.name = name
        self.description = description
    def Describe(self):
        print(self.description)
    def GetName(self):
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
    def __init__(self,name,description,equipSlot):
        self.name = name
        self.description = description
        self.equipSlot = equipSlot
        self.statChange = Stats(0,0,0,0)

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
        CombineStats(self.statChange,playerStats,True)
        
class Room:
    def __init__(self,name,description,items):
        self.name = name
        self.description = description
        self.items = items
        self.entityList = list() 
    def describe(self):
        print(self.description)
    def AddItem(self,toAdd):
        self.items.append(toAdd)
    def AddEntity(self,toAdd):
        self.entityList.append(toAdd)
    def GetItems(self):
        return self.items
    def DescribeItems(self):
        if len(self.items) == 0:
            print("There are no items in this room!")
        else:
            print("The following items are in this room:")
            for i in self.items:
                print(i.GetName())
    def Describe(self):
        print(self.description)
        if(len(self.items) > 0):
            print("Items in this room:")
            ShowItems(self.items)
        if(len(self.entityList) > 0):
            print("Monsters in this room:")
            ShowItems(self.entityList)
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
            print("You don't have that item.")
     
    def UpdateEntities(self):
        for i in range(0,len(self.entityList)):
            if(self.entityList[i].stats.health <= 0):
                del(self.entityList[i])
            else:
                self.entityList[i].Turn()
    

class Armor(Equippable):
    def __init__(self,name,description,armorType,acChange):
        self.name = name
        self.description = description
        self.equipSlot = armorType
        self.statChange = Stats(0,0,0,acChange)
        self.ac = acChange
        
    

class Sword(Equippable):
    def __init__(self,name,description,diceNumber,diceValue):
        self.name = name
        self.description = description
        self.diceNumber = diceNumber
        self.diceValue = diceValue
        self.equipSlot = "weapon"
        self.statChange = Stats(0,0,0,0)
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
                    inventory[selection].Describe()
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
                    playerEquipment[slot].Unequip()
                    print("You have unequipped the {0}.".format(playerEquipment[slot].GetName()))
                    playerEquipment[slot] = None
                    return
            else:
                print("That is not a valid slot.")
                
        if(command == "stats"):
            print("An adventurer named {0}".format(playerName))
            playerStats.Display()
        if(command == "drink"):
            toUse = GetItem("Item to drink:")
            if(toUse != -1):
                if(inventory[toUse].Drink(playerStats)):
                    return
            
                


class Goblin(Entity):
    def __init__(self,level=1,name="Goblin"):
        self.stats = Stats(level,RollDice(8,level),RollDice(2,level),0)
        self.weapon = None
        self.name = name
        if(RollDice(8) <= level):
            self.weapon = items['rustySword']()
        self.canMove = True

    def Turn(self):
        if(self.canMove):
            Attack(self.stats,playerStats,self.weapon,self.name)
        
    def __del__(self):
        print("The Goblin is dead!")




def Attack(aStats,dStats,aWep,attacker,defender=''):
    #damage roll
    if(aWep == None):
        weaponName = "bare hands"
    else:
        weaponName = aWep.name
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
        damageDealt += RollDice(aWep.diceValue,aWep.diceNumber)
    if(attacker == "self"):
        print("You deal {0} damage!".format(str(damageDealt)))
    else:
        print("The {0} deals {1} damage!".format(attacker,str(damageDealt)))
        print("You have {0} health.".format(dStats.health - damageDealt))
    dStats.health -= damageDealt


class HealthPotion(Item):
    def Drink(self,stats,user="self"):
        stats.health = stats.health + RollDice(10)
        if(stats.health > stats.maxHealth):
            stats.health = stats.maxHealth
        if(user == "self"):
            print("You feel much better.")
            print("You now have {0} health.".format(stats.health))
        else:
            print("The {0} drinks a health potion!".format(user))
        return True


levelOneLoot = []


playerEquipment = {
    "helmet" : None,
    "chestplate" : None,
    "boots" : None,
    "weapon" : None,
    "amulet" : None,
    "ring" : None
    }



#item definitions go here

def rustySword():
    return Sword("Rusty Sword","A very rusty sword",1,6)
def healthPotion():
    return HealthPotion("Health Potion","A magical draught that restores 1d10 hitpoints.")
def rustyChestplate():
    return Armor("Rusty Chestplate","A very rusty chestplate.  It looks uncomfortable.","chestplate",-2)
currentRoom = Room("stone room","A dank stone room, filled with bricks and water puddles.",list())
playerStats = Stats(1,10,3,0)
playerWeapon = None
playerName = input("What is your name:")
inventory = list()
items = {
    'rustySword' : rustySword,
    'healthPotion' : healthPotion,
    'rustyChestplate' : rustyChestplate
    }
mons = {
    'goblin' : Goblin
    }


currentRoom.AddItem(items['rustySword']())
currentRoom.AddItem(items['healthPotion']())
currentRoom.AddItem(items['rustyChestplate']())
currentRoom.AddEntity(mons['goblin'](3))
currentRoom.AddEntity(mons['goblin']())


while True:
    TakeCommands()
    currentRoom.UpdateEntities()



