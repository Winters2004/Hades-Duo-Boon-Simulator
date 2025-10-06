import flet as ft
from database import get_gods, get_boons_for_god
from buttons import pick_boon, reset_boons, remove_boon

#metadata for visuals
GOD_META = {
    "Aphrodite":  {"emoji": "💗", "color": "#EC407A"},
    "Apollo":     {"emoji": "🌟", "color": "#E7EA48"},
    "Ares":       {"emoji": "🗡️", "color": "#E53935"},
    "Demeter":    {"emoji": "❄️", "color": "#8CECED"},
    "Hephaestus": {"emoji": "⚒️", "color": "#F4F5BC"},
    "Hera":       {"emoji": "🌀", "color": "#00918A"},
    "Hestia":     {"emoji": "🔥", "color": "#E57035"},
    "Poseidon":   {"emoji": "🌊", "color": "#0288D1"},
    "Zeus":       {"emoji": "⚡", "color": "#FBC02D"},
}

def main(page: ft.Page):
    page.title = "Hades Duo Boon Simulator"
    page.window_width = 1920
    page.window_height = 1080
    page.window_icon = "zag.ico"
    page.padding = 20
    page.bgcolor = "#00230E"

    #state
    player_boons = []

    #dropdowns
    gods = get_gods()
    god_dd = ft.Dropdown(label="Choose a God", options=[ft.dropdown.Option(g) for g in gods], width=320)
    boon_dd = ft.Dropdown(label="Choose a Boon", options=[], width=320)

    def on_god_change(e):
        if not god_dd.value:
            boon_dd.options = []
            boon_dd.value = None
        else:
            items = get_boons_for_god(god_dd.value)
            boon_dd.options = [ft.dropdown.Option(b) for b in items]
            boon_dd.value = None
        page.update()

    god_dd.on_change = on_god_change

    #columns
    picked_column = ft.Column(spacing=8, expand=True)
    duo_column = ft.Column(spacing=8, expand=True)
    duo_column.controls.append(ft.Text("No duo boons unlocked yet.", italic=True, size=12))

    #buttons
    pick_button = ft.ElevatedButton(
        "Pick Boon",
        width=140,
        on_click=lambda e: pick_boon(e, god_dd, boon_dd, player_boons, picked_column, duo_column, page, GOD_META)
    )
    
    reset_button = ft.ElevatedButton(
        "Reset Boons",
        width=140,
        on_click=lambda e: reset_boons(e, player_boons, picked_column, duo_column, page, god_dd, boon_dd)
    )
    remove_button = ft.ElevatedButton(
        "Remove Boon",
        width=140,
        on_click=lambda e: remove_boon(e, god_dd, boon_dd, player_boons, picked_column, duo_column, page)
    )

    #cards
    choose_card = ft.Card(
        content=ft.Container(
            content=ft.Column([ft.Text("Choose a Boon", size=18, weight="bold"), god_dd, boon_dd, pick_button, reset_button, remove_button]),
            padding=20, 
            height=550, 
            width=250, 
            bgcolor="#101D6B", 
            border_radius=8
        )
    )
    chosen_card = ft.Card(
        content=ft.Container(
            content=ft.Column([ft.Text("Chosen Boons", size=18, weight="bold"), picked_column]),
            padding=20, 
            height=550, 
            width=300, 
            bgcolor="#101D6B", 
            border_radius=8
        )
    )
    duo_card = ft.Card(
        content=ft.Container(
            content=ft.Column([ft.Text("Available Duo Boons", size=18, weight="bold"), duo_column], scroll="auto"),
            padding=20, 
            height=550, 
            width=300, 
            bgcolor="#A101D6B", 
            border_radius=8
        )
    )

    page.add(ft.Row([choose_card, chosen_card, duo_card], 
                    alignment=ft.MainAxisAlignment.SPACE_AROUND, expand=True))

ft.app(target=main)
