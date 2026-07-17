"""Das Quartett-Minispiel (Top-Trumps-Prinzip) fuer das IT-Security-TCG.

Spielprinzip (Stein-Schere-Papier-artiger Wertevergleich):
  * Das Deck wird gemischt und gleichmaessig auf Spieler:in und Computer verteilt.
  * Wer am Zug ist, waehlt eine Kategorie (Schaden, Verbreitung, Tarnung,
    Komplexitaet).
  * Die oberste Karte beider Stapel wird verglichen - der hoehere Wert gewinnt
    und nimmt beide Karten (ans Ende des eigenen Stapels).
  * Bei Gleichstand wandern die Karten in einen Pott, der beim naechsten
    Gewinn dazukommt.
  * Wer am Ende alle Karten besitzt, gewinnt.
"""

from __future__ import annotations

import random
from collections import deque

from .cards import CATEGORIES, Card, get_deck


class Player:
    """Ein Spieler mit seinem Kartenstapel (als Warteschlange)."""

    def __init__(self, name: str, cards: list[Card], is_human: bool = False):
        self.name = name
        self.hand: deque[Card] = deque(cards)
        self.is_human = is_human

    @property
    def alive(self) -> bool:
        return len(self.hand) > 0

    def draw_top(self) -> Card:
        return self.hand[0]

    def remove_top(self) -> Card:
        return self.hand.popleft()

    def add_cards(self, cards: list[Card]) -> None:
        self.hand.extend(cards)


def deal(seed: int | None = None) -> tuple[Player, Player]:
    """Mischt das Deck und teilt es auf zwei Spieler auf."""
    deck = get_deck()
    rng = random.Random(seed)
    rng.shuffle(deck)
    half = len(deck) // 2
    human = Player("Du", deck[:half], is_human=True)
    cpu = Player("Computer", deck[half:], is_human=False)
    return human, cpu


def best_category(card: Card) -> str:
    """Waehlt die staerkste Kategorie einer Karte (CPU-Strategie)."""
    return max(CATEGORIES, key=card.value)


def resolve_round(chooser: Player, other: Player, category: str,
                  pot: list[Card]) -> tuple[Player | None, list[Card]]:
    """Wertet eine Runde aus.

    Rueckgabe: (Gewinner der Runde oder None bei Gleichstand, aktualisierter Pott).
    Die Karten werden dem Gewinner bereits hinzugefuegt.
    """
    c_card = chooser.remove_top()
    o_card = other.remove_top()
    stake = [c_card, o_card] + pot

    c_val = c_card.value(category)
    o_val = o_card.value(category)

    if c_val > o_val:
        chooser.add_cards(stake)
        return chooser, []
    if o_val > c_val:
        other.add_cards(stake)
        return other, []
    # Gleichstand -> Karten in den Pott
    return None, stake
