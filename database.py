import sqlite3

DB_FILE = "hades.db"

#Database gatherers
def get_gods():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT god FROM boons ORDER BY god")
        return [row[0] for row in c.fetchall()]

def get_boons_with_abilities(god):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT name, ability FROM boons WHERE god=? ORDER BY name", (god,))
        return [(row[0], row[1]) for row in c.fetchall()]

def get_ability_of_boon(ability):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT ability FROM boons WHERE name = ? LIMIT 1", (ability,))
        row = c.fetchone()
        return row[0] if row else None

def get_boons_for_god(god):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM boons WHERE god=? ORDER BY name", (god,))
        return [row[0] for row in c.fetchall()]

def check_duo_boons(player_boons):
    available = []
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, description FROM duo_boons")
        for duo_id, name, description in c.fetchall():
            c.execute("SELECT god, boon_name FROM duo_reqs WHERE duo_id=?", (duo_id,))
            reqs = c.fetchall()
            satisfied = True
            for god, boon_req in reqs:
                player_boons_for_god = [pb_b for pb_g, pb_b in player_boons if pb_g == god]

                #If any boons for god is a requirement
                if boon_req.lower() == "any":
                    if not player_boons_for_god:
                        satisfied = False

                #If a boon for god is not a requirement
                elif boon_req.startswith("NOT_"):
                    excluded_boon = boon_req[4:]
                    if not player_boons_for_god:
                        satisfied=False
                    elif excluded_boon in player_boons_for_god:
                        satisfied = False

                #If two or more boons for god is a requirement
                elif "|" in boon_req:
                    options = [b.strip() for b in boon_req.split("|")]
                    if not any(opt in player_boons_for_god for opt in options):
                        satisfied = False

                else:
                    if boon_req not in player_boons_for_god:
                        satisfied = False

                if not satisfied:
                    break

            if satisfied:
                available.append((name, description))
    return available
