import sys
import time
import random

# --- Simple Text Adventure: Dark-Fantasy Dungeon ---
# Player inventory, state, and life points
inventory = {}  # Now a dict: item -> count
current_stage = 'entrance'
life_points = 3  # Player starts with 3 HP
game_over = False

def slow_print(text):
    # Prints text slowly for effect
    for c in text:
        print(c, end='', flush=True)
        time.sleep(0.01)
    print()

def get_input(prompt):
    return input(prompt).strip().lower()

def add_to_inventory(item):
    # Add an item to inventory, allowing multiples
    if item in inventory:
        inventory[item] += 1
    else:
        inventory[item] = 1

def show_inventory():
    # Display current inventory and life points
    if inventory:
        inv_str = ', '.join(f"{k} x{v}" if v > 1 else k for k, v in inventory.items())
    else:
        inv_str = 'Empty'
    slow_print(f"Inventory: {inv_str} | HP: {life_points}")

def entrance():
    global life_points
    torch_found = 'torch' in inventory
    slow_print("You stand at the entrance of a ruined dungeon. It's pitch black inside.")
    while True:
        slow_print("Options: [enter] the dungeon, [look] around, [rest], [inventory], [leave]")
        choice = get_input("> ")
        if choice == 'look':
            if not torch_found:
                slow_print("You find a rusty torch on the ground.")
                add_to_inventory('torch')
                torch_found = True
            else:
                slow_print("You see only the dark entrance and your own footprints.")
        elif choice == 'rest':
            if life_points < 3:
                life_points += 1
                slow_print("You rest and recover 1 HP.")
            else:
                slow_print("You are already at full health.")
        elif choice == 'inventory':
            show_inventory()
        elif choice == 'enter':
            if 'torch' in inventory:
                slow_print("You light the torch and step into the darkness...")
                return 'hallway'
            else:
                slow_print("It's too dark to enter safely. Maybe you need a light source.")
        elif choice == 'leave':
            slow_print("You decide this place is too dangerous and leave. Game over.")
            return 'end'
        else:
            slow_print("I don't understand that.")

def hallway():
    global life_points
    # Track if items have been found and/or taken
    found = {'sword': 'sword' in inventory, 'shield': 'shield' in inventory, 'potion': False}
    taken = {'sword': 'sword' in inventory, 'shield': 'shield' in inventory, 'potion': False}
    trap_triggered = False
    slow_print("You walk down a damp hallway. Shadows flicker on the walls.")
    while True:
        opts = ["[forward] deeper", "[search] the area", "[inventory]", "[rest]"]
        for item in ['sword', 'shield', 'potion']:
            if found[item] and not taken[item]:
                opts.append(f"[take {item}]")
        slow_print("Options: " + ', '.join(opts))
        choice = get_input("> ")
        if choice == 'search':
            # Only reveal items not yet found or taken
            for item in ['sword', 'shield', 'potion']:
                if not found[item]:
                    if item == 'sword':
                        slow_print("You find a battered sword leaning against the wall.")
                    elif item == 'shield':
                        slow_print("You find an old shield half-buried in rubble.")
                    elif item == 'potion':
                        slow_print("You find a healing potion hidden in a crack.")
                    found[item] = True
                    break
            else:
                slow_print("You find nothing else of use.")
        elif choice == 'rest':
            if life_points < 3:
                life_points += 1
                slow_print("You rest and recover 1 HP.")
            else:
                slow_print("You are already at full health.")
        elif choice == 'inventory':
            show_inventory()
        elif choice.startswith('take '):
            item = choice[5:]
            if found.get(item) and not taken.get(item):
                add_to_inventory(item)
                taken[item] = True
                slow_print(f"You pick up the {item}.")
            else:
                slow_print("There's nothing like that here.")
        elif choice == 'forward':
            # Random chance to trigger a trap
            if not trap_triggered and random.random() < 0.4:
                slow_print("A hidden trap springs! You are hit by darts.")
                if 'shield' in inventory:
                    slow_print("Your shield blocks most of the darts, but you lose 1 HP.")
                    life_points -= 1
                else:
                    slow_print("You are struck! You lose 2 HP.")
                    life_points -= 2
                trap_triggered = True
                if life_points <= 0:
                    slow_print("You collapse from your wounds. Game over.")
                    return 'end'
            else:
                slow_print("You move deeper into the dungeon...")
                return 'chamber'
        else:
            slow_print("I don't understand that.")

def chamber():
    global life_points
    slow_print("You enter a vast chamber. A monstrous shadow stirs in the gloom!")
    monster_alive = True
    while monster_alive:
        opts = ["[attack]", "[defend]", "[run]", "[inventory]", "[use potion]"]
        slow_print("Options: " + ', '.join(opts))
        choice = get_input("> ")
        if choice == 'attack':
            if 'sword' in inventory:
                slow_print("You slash at the monster with your sword!")
                slow_print("The beast howls and collapses. You are victorious!")
                monster_alive = False
            else:
                slow_print("You have no weapon! The monster overpowers you. You lose 2 HP.")
                life_points -= 2
                if life_points <= 0:
                    slow_print("You have been defeated. Game over.")
                    return 'end'
        elif choice == 'defend':
            if 'shield' in inventory:
                slow_print("You block the monster's attack with your shield and counter! The beast flees.")
                monster_alive = False
            else:
                slow_print("You try to defend yourself, but without a shield, you lose 1 HP.")
                life_points -= 1
                if life_points <= 0:
                    slow_print("You have been defeated. Game over.")
                    return 'end'
        elif choice == 'run':
            slow_print("You flee back to the hallway, heart pounding.")
            return 'hallway'
        elif choice == 'inventory':
            show_inventory()
        elif choice == 'use potion':
            if inventory.get('potion', 0) > 0:
                slow_print("You drink the potion and recover to full health!")
                life_points = 3
                inventory['potion'] -= 1
                if inventory['potion'] == 0:
                    del inventory['potion']
            else:
                slow_print("You don't have a potion.")
        else:
            slow_print("I don't understand that.")
    slow_print("You search the chamber and find a hidden exit to the outside. You have survived the dungeon!")
    return 'end'

def main():
    slow_print("--- Dark-Fantasy Dungeon Adventure ---")
    global current_stage
    while current_stage != 'end':
        if current_stage == 'entrance':
            current_stage = entrance()
        elif current_stage == 'hallway':
            current_stage = hallway()
        elif current_stage == 'chamber':
            current_stage = chamber()
    slow_print("Thank you for playing!")

if __name__ == "__main__":
    main()