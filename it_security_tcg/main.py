"""Interaktives Terminal-Spiel fuer das IT-Security-TCG.

Start:
    python -m it_security_tcg          # Spiel starten
    python -m it_security_tcg --cards  # nur die Kartensammlung ansehen
"""

from __future__ import annotations

import argparse
import sys

from .cards import CATEGORIES, DECK, Rarity
from .display import RESET, BOLD, cards_side_by_side, print_card
from .game import best_category, deal, resolve_round

BANNER = r"""
 ___ _____   ___                 _ _         _____ ___ ___
|_ _|_   _| / __| ___ __ _  _ _ (_) |_ _  _ |_   _/ __/ __|
 | |  | |   \__ \/ -_) _| || | '_| |  _| || |  | || (_ | (_ |
|___| |_|   |___/\___\__|\_,_|_| |_|\__|\_, |  |_| \___\___|
                                        |__/
        Das Sammelkartenspiel rund um IT-Angriffe
"""


def show_collection() -> None:
    """Zeigt alle Karten, nach Seltenheit gruppiert."""
    print(BANNER)
    print(f"{BOLD}Die Kartensammlung ({len(DECK)} Karten){RESET}\n")
    for rarity in reversed(list(Rarity)):  # Legendaer zuerst
        cards = [c for c in DECK if c.rarity is rarity]
        if not cards:
            continue
        print(f"{rarity.color}{BOLD}=== {rarity.label} "
              f"({rarity.symbol}) - {len(cards)} Karten ==={RESET}\n")
        for card in cards:
            print_card(card)
            print()


def _prompt_category() -> str:
    """Fragt die Spielerin/den Spieler nach einer Kategorie."""
    keys = list(CATEGORIES.keys())
    print("\nWaehle eine Kategorie:")
    for i, key in enumerate(keys, 1):
        print(f"  {i}) {CATEGORIES[key]}")
    while True:
        choice = input("> ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Spiel beendet. Bis bald!")
            sys.exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        # auch Namen erlauben
        for key in keys:
            if choice == CATEGORIES[key].lower() or choice == key:
                return key
        print("Ungueltige Eingabe. Zahl 1-4 eingeben (oder 'q' zum Beenden).")


def play(seed: int | None = None) -> None:
    """Hauptschleife des Quartett-Minispiels."""
    print(BANNER)
    print("Willkommen! Ihr spielt Quartett nach dem Top-Trumps-Prinzip.")
    print("Wer am Zug ist, waehlt eine Kategorie - der hoehere Wert gewinnt")
    print("beide Karten. Ziel: alle Karten erobern.\n")
    print("Tipp: jederzeit 'q' eingeben, um zu beenden.\n")

    human, cpu = deal(seed)
    pot: list = []
    chooser_is_human = True
    round_no = 0
    max_rounds = 300  # Sicherheitsnetz gegen Endlosschleifen

    while human.alive and cpu.alive and round_no < max_rounds:
        round_no += 1
        chooser = human if chooser_is_human else cpu
        other = cpu if chooser_is_human else human

        print("=" * 70)
        print(f"{BOLD}Runde {round_no}{RESET}  |  "
              f"Du: {len(human.hand)} Karten   "
              f"Computer: {len(cpu.hand)} Karten"
              + (f"   Pott: {len(pot)}" if pot else ""))
        print("=" * 70)

        human_top = human.draw_top()

        if chooser_is_human:
            print("\nDeine oberste Karte:")
            print_card(human_top)
            category = _prompt_category()
        else:
            category = best_category(cpu.draw_top())
            print(f"\nDer Computer ist am Zug und waehlt: "
                  f"{BOLD}{CATEGORIES[category]}{RESET}")
            input("(Enter zum Aufdecken) ")

        # Karten nebeneinander zeigen (vor dem Entfernen)
        print("\n" + cards_side_by_side(human.draw_top(), cpu.draw_top(),
                                        highlight=category))
        h_val = human.draw_top().value(category)
        c_val = cpu.draw_top().value(category)
        print(f"\n{CATEGORIES[category]}:  Du {BOLD}{h_val}{RESET}  "
              f"vs.  Computer {BOLD}{c_val}{RESET}")

        winner, pot = resolve_round(chooser, other, category, pot)

        if winner is None:
            print(f"{BOLD}Gleichstand!{RESET} Die Karten wandern in den Pott "
                  f"({len(pot)} Karten liegen bereit).")
            # Bei Gleichstand behaelt derselbe Spieler das Wahlrecht
        elif winner is human:
            print(f"{BOLD}\033[32mDu gewinnst die Runde!{RESET}")
            chooser_is_human = True
        else:
            print(f"{BOLD}\033[31mDer Computer gewinnt die Runde.{RESET}")
            chooser_is_human = False

        input("\n(Enter fuer die naechste Runde) ")

    # ------------------------------------------------------------------
    print("=" * 70)
    if human.alive and not cpu.alive:
        print(f"{BOLD}\033[32mGLUECKWUNSCH - du hast alle Karten erobert!{RESET}")
    elif cpu.alive and not human.alive:
        print(f"{BOLD}\033[31mDer Computer hat gewonnen. Naechstes Mal!{RESET}")
    else:
        # Rundenlimit erreicht -> nach Kartenzahl entscheiden
        if len(human.hand) > len(cpu.hand):
            print(f"{BOLD}\033[32mNach Punkten gewinnst du "
                  f"({len(human.hand)} zu {len(cpu.hand)} Karten)!{RESET}")
        elif len(cpu.hand) > len(human.hand):
            print(f"{BOLD}\033[31mNach Punkten gewinnt der Computer "
                  f"({len(cpu.hand)} zu {len(human.hand)} Karten).{RESET}")
        else:
            print(f"{BOLD}Unentschieden!{RESET}")
    print("=" * 70)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="IT-Security-TCG - Sammelkartenspiel rund um IT-Angriffe.")
    parser.add_argument("--cards", action="store_true",
                        help="nur die Kartensammlung anzeigen")
    parser.add_argument("--seed", type=int, default=None,
                        help="Zufalls-Seed fuer reproduzierbares Mischen")
    args = parser.parse_args(argv)

    try:
        if args.cards:
            show_collection()
        else:
            play(seed=args.seed)
    except (KeyboardInterrupt, EOFError):
        print("\nSpiel abgebrochen. Bis bald!")


if __name__ == "__main__":
    main()
