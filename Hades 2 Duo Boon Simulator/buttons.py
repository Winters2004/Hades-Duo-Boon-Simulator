import flet as ft
from database import get_boons_with_abilities, get_ability_of_boon, check_duo_boons

#Helper to render picked boon row
def make_picked_row(god, boon, GOD_META):
    meta = GOD_META.get(god)
    left = ft.Text(f"{meta['emoji']}  {god}", weight="bold", size=14, color=meta["color"])
    right = ft.Text(boon, size=14, color=meta["color"])
    spacer = ft.Container(expand=True)
    return ft.Container(ft.Row([left, spacer, right]), padding=8, bgcolor="#88B1B0", border_radius=6)


def update_boon_options(god_dd, boon_dd, player_boons):
    boon_dd.options = []
    boon_dd.value = None
    if not god_dd.value:
        return

    items = get_boons_with_abilities(god_dd.value)
    #compute abilities already chosen
    existing_abilities = set()
    for _, b in player_boons:
        ab = get_ability_of_boon(b)
        if ab:
            existing_abilities.add(ab)

    opts = []
    for name, ability in items:
        #skip exact duplicate picks
        if (god_dd.value, name) in player_boons:
            continue
        #skip if ability already taken
        if ability and ability in existing_abilities:
            continue
        opts.append(ft.dropdown.Option(name))

    boon_dd.options = opts
    boon_dd.value = None


def pick_boon(e, god_dd, boon_dd, player_boons, picked_column, duo_column, page, GOD_META):
    if not god_dd.value or not boon_dd.value:
        page.update()
        return

    if (god_dd.value, boon_dd.value) in player_boons:
        page.update()
        return

    #ability uniqueness
    new_ability = get_ability_of_boon(boon_dd.value)
    if new_ability:
        existing_abilities = [get_ability_of_boon(b) for _, b in player_boons]
        if new_ability in existing_abilities:
            page.update()
            return

    #max 4 distinct gods allowed
    chosen_gods = {g for g, _ in player_boons}
    if god_dd.value not in chosen_gods and len(chosen_gods) >= 4:
        page.update()
        return

    player_boons.append((god_dd.value, boon_dd.value))
    picked_column.controls.append(make_picked_row(god_dd.value, boon_dd.value, GOD_META))

    #refresh duo boons
    duo_column.controls.clear()
    available = check_duo_boons(player_boons)
    if available:
        duo_column.controls.append(ft.Text("🔥 Duo Boons Available:", weight="bold"))
        for name, desc in available:
            duo_column.controls.append(
                ft.Container(
                    ft.Column([ft.Text(name, weight="bold"), ft.Text(desc, size=12)], spacing=6),
                    padding=10,
                    bgcolor="#10D220",
                    border_radius=6,
                )
            )
    else:
        duo_column.controls.append(ft.Text("No duo boons unlocked yet.", italic=True, size=12))

    #update the boon dropdown to reflect newly blocked abilities / removed items
    update_boon_options(god_dd, boon_dd, player_boons)

    page.update()


def reset_boons(e, player_boons, picked_column, duo_column, page, god_dd=None, boon_dd=None):
    player_boons.clear()
    picked_column.controls.clear()
    duo_column.controls.clear()
    duo_column.controls.append(ft.Text("No duo boons unlocked yet.", italic=True, size=12))

    #reset dropdowns if provided
    if god_dd:
        god_dd.value = None
    if boon_dd:
        boon_dd.options = []
        boon_dd.value = None

    page.update()

def remove_boon(e, god_dd, boon_dd, player_boons, picked_column, duo_column, page):
    if not god_dd.value or not boon_dd.value:
        return

    #if this boon is not in the list, nothing to remove
    if (god_dd.value, boon_dd.value) not in player_boons:
        return

    #remove from state
    player_boons.remove((god_dd.value, boon_dd.value))

    #remove from the picked_column
    to_remove = None
    for ctrl in picked_column.controls:
        if isinstance(ctrl, ft.Container) and isinstance(ctrl.content, ft.Row):
            texts = [c for c in ctrl.content.controls if isinstance(c, ft.Text)]
            if len(texts) == 2:
                left, right = texts
                if god_dd.value in left.value and boon_dd.value == right.value:
                    to_remove = ctrl
                    break
    if to_remove:
        picked_column.controls.remove(to_remove)

    #refresh duo boons after removal
    duo_column.controls.clear()
    from database import check_duo_boons
    available = check_duo_boons(player_boons)
    if available:
        duo_column.controls.append(ft.Text("🔥 Duo Boons Available:", weight="bold"))
        for name, desc in available:
            duo_column.controls.append(
                ft.Container(
                    ft.Column([ft.Text(name, weight="bold"), ft.Text(desc, size=12)], spacing=6),
                    padding=10,
                    bgcolor="#10D220",
                    border_radius=6,
                )
            )
    else:
        duo_column.controls.append(ft.Text("No duo boons unlocked yet.", italic=True, size=12))

    #update the boon dropdown so removed ability becomes available again
    update_boon_options(god_dd, boon_dd, player_boons)

    page.update()
