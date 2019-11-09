from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


#create black magic
fire = Spell('Fire', 25, 600, "black")
thunder = Spell('Thunder', 25, 600, "black")
blizzard = Spell('Blizzard', 25, 600, "black")
meteor = Spell('Meteor', 40, 1200, "black")
quake = Spell('Quake', 14, 140, "black")

#Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item('MegaElixer', 'elixer', "Fully restores party's HP/MP", 9999)

grenade = Item("Granade", "attack", "Deals 500 damage", 500)

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spell = [fire, meteor, curaga]

#Instantiate People         
player1 = Person('Valos:', 3260, 132, 300, 34, player_spells, player_items)
player2 = Person('Nick :', 4160, 188, 311, 34, player_spells, player_items)
player3 = Person('Robot:', 3089, 174, 288, 34, player_spells, player_items)

enemy2 = Person('Imp  :', 1250, 130, 560, 325, enemy_spell,[])
enemy1 = Person('Magus:', 11200, 701, 525, 25, enemy_spell,[])
enemy3 = Person('Imp  :', 1250, 130, 560, 325, enemy_spell,[])

players =[player1, player2, player3]
enemys = [enemy2, enemy1, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)


while running:
    print("#######################################\n\n")
    print("NAME              HP                              MP")
    
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemys:
        enemy.get_enemy_stats()
    
    for player in players:
        
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1
        
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemys)
            
            enemys[enemy].take_damage(dmg)
            print("You attacked " + enemys[enemy].name + "for", dmg, "points of damage.")

            if enemys[enemy].get_hp() == 0:
                print(enemys[enemy].name + " has dies.")
                del enemys[enemy]
                
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue
            
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            
            
            current_mp = player.get_mp()
            
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            print(spell.type)
            
            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name + " heals for", str(magic_dmg), "HP:" + bcolors.ENDC)
            elif spell.type == 'black':
                
                enemy = player.choose_target(enemys)
                
                enemys[enemy].take_damage(magic_dmg)
                
                print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage to " + enemys[enemy].name + bcolors.ENDC)

                if enemys[enemy].get_hp() == 0:
                    print(enemys[enemy].name + " has dies.")
                    del enemys[enemy]
                    
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose Item:")) - 1
            
            if item_choice == -1:
                continue
            
            item = player.items[item_choice]["item"]

            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + '\n' + "None left..." + bcolors.ENDC)
                continue
            
            player.items[item_choice]['quantity'] -= 1

            
            

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == 'elixer':

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    
                print(bcolors.OKGREEN + "\n" + item.name + "fully restores HP/MP" + bcolors.ENDC)
            elif item.type == 'attack':

                enemy = player.choose_target(enemys)
                
                enemys[0].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " Deals ", str(item.prop), "points of damage to" + enemys[enemy].name + bcolors.ENDC)

                if enemys[enemy].get_hp() == 0:
                    print(enemys[enemy].name + " has dies.")
                    del enemys[enemy]

    #check if battle is over    
    defeated_enemies = 0
    defeated_players = 0
    
    for enemy in enemys:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + bcolors.BOLD + "You Win!" + bcolors.ENDC)
        running = False

    #check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + " Your enemies have defeated You!" + bcolors.ENDC)
        running = False
    
    print('\n')
    #enemy attack phase 
    for enemy in enemys:        
        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemys[0].generate_damage()
            
            players[target].take_damage(enemy_dmg)
            print(enemy.name + "attacks " + players[target].name + "for", enemy_dmg, "points of damage.")

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals" + enemy.name + " for", str(magic_dmg), "HP:" + bcolors.ENDC)
            elif spell.type == 'black':

                target = random.randrange(0, 3)
                                
                players[target].take_damage(magic_dmg)
                
                print(bcolors.OKBLUE + "\n" + enemy.name + spell.name + "deals", str(magic_dmg), "points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has dies.")
                    del enemys[enemy]
            
