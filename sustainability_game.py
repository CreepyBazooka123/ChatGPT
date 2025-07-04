import random

class GameSettings:
    def __init__(self):
        self.rounds = 5


def main_menu(settings: GameSettings):
    while True:
        print("\n-- Hauptmenü --")
        print("1. Spiel starten")
        print("2. Einstellungen")
        print("3. Über")
        print("4. Beenden")
        choice = input("Bitte wählen: ")
        if choice == '1':
            start_game(settings)
        elif choice == '2':
            settings_menu(settings)
        elif choice == '3':
            about()
        elif choice == '4':
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe. Bitte erneut versuchen.")


def settings_menu(settings: GameSettings):
    while True:
        print("\n-- Einstellungen --")
        print(f"1. Anzahl der Runden: {settings.rounds}")
        print("2. Zurück")
        choice = input("Bitte wählen: ")
        if choice == '1':
            try:
                value = int(input("Neue Anzahl der Runden eingeben: "))
                if value > 0:
                    settings.rounds = value
                else:
                    print("Bitte eine Zahl größer 0 eingeben.")
            except ValueError:
                print("Bitte eine gültige Zahl eingeben.")
        elif choice == '2':
            break
        else:
            print("Ungültige Eingabe. Bitte erneut versuchen.")


def about():
    print("\nDieses Spiel lehrt die korrekte Mülltrennung.")
    print("Treffe die richtige Entscheidung, um Punkte zu sammeln.")


def start_game(settings: GameSettings):
    trash_items = [
        ("Bananenschale", "Biomüll"),
        ("Plastikflasche", "Wertstoff"),
        ("Zeitung", "Papier"),
        ("Glasscherbe", "Glas"),
        ("Pizzakarton (dreckig)", "Restmüll"),
        ("Eierschale", "Biomüll"),
        ("Konservendose", "Wertstoff"),
        ("Alte Zeitschrift", "Papier"),
        ("Kaputtes Trinkglas", "Glas"),
        ("Staubsaugerbeutel", "Restmüll"),
    ]

    score = 0
    for _ in range(settings.rounds):
        item, correct_bin = random.choice(trash_items)
        print(f"\nWohin gehört '{item}'?")
        print("Optionen: Biomüll, Restmüll, Papier, Glas, Wertstoff")
        answer = input("Deine Wahl: ").strip().capitalize()
        if answer == correct_bin:
            print("Richtig!")
            score += 1
        else:
            print(f"Falsch! Richtige Antwort: {correct_bin}")
    print(f"\nSpiel beendet! Deine Punktzahl: {score}/{settings.rounds}")


if __name__ == "__main__":
    settings = GameSettings()
    main_menu(settings)
