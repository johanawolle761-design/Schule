"""Tests fuer Kartendeck und Spiellogik des IT-Security-TCG."""

from collections import deque

from it_security_tcg.cards import CATEGORIES, DECK, Rarity
from it_security_tcg.game import Player, best_category, deal, resolve_round


def test_deck_size_and_uniqueness():
    assert len(DECK) == 20
    names = [c.name for c in DECK]
    assert len(names) == len(set(names)), "Kartennamen muessen eindeutig sein"


def test_card_values_in_range():
    for card in DECK:
        for key in CATEGORIES:
            val = card.value(key)
            assert 0 <= val <= 100, f"{card.name}.{key} = {val} ausserhalb 0-100"


def test_all_rarities_present():
    present = {c.rarity for c in DECK}
    assert present == set(Rarity)


def test_legendary_cards_are_stronger_on_average():
    def avg(r):
        cards = [c for c in DECK if c.rarity is r]
        return sum(c.gesamtstaerke for c in cards) / len(cards)

    assert avg(Rarity.LEGENDAER) > avg(Rarity.EPISCH) > avg(Rarity.HAEUFIG)


def test_deal_splits_deck():
    human, cpu = deal(seed=1)
    assert len(human.hand) + len(cpu.hand) == len(DECK)
    assert len(human.hand) == len(cpu.hand)


def test_deal_is_reproducible_with_seed():
    a1, b1 = deal(seed=7)
    a2, b2 = deal(seed=7)
    assert [c.name for c in a1.hand] == [c.name for c in a2.hand]


def test_resolve_round_higher_value_wins():
    strong = [c for c in DECK if c.name == "Ransomware"][0]     # Schaden 98
    weak = [c for c in DECK if c.name == "Adware"][0]           # Schaden 25
    p1 = Player("A", [strong])
    p2 = Player("B", [weak])
    winner, pot = resolve_round(p1, p2, "schaden", [])
    assert winner is p1
    assert pot == []
    assert len(p1.hand) == 2 and len(p2.hand) == 0


def test_resolve_round_tie_goes_to_pot():
    # Zwei Karten mit gleichem Wert kuenstlich erzeugen
    card = DECK[0]
    p1 = Player("A", [card])
    p2 = Player("B", [card])
    winner, pot = resolve_round(p1, p2, "schaden", [])
    assert winner is None
    assert len(pot) == 2
    assert len(p1.hand) == 0 and len(p2.hand) == 0


def test_pot_is_awarded_to_next_winner():
    strong = [c for c in DECK if c.name == "Ransomware"][0]
    weak = [c for c in DECK if c.name == "Adware"][0]
    p1 = Player("A", [strong])
    p2 = Player("B", [weak])
    pot = [DECK[5], DECK[6]]  # 2 Karten liegen im Pott
    winner, new_pot = resolve_round(p1, p2, "schaden", pot)
    assert winner is p1
    assert new_pot == []
    assert len(p1.hand) == 1 + 1 + 2  # eigene + gegnerische + Pott


def test_best_category_picks_max():
    card = [c for c in DECK if c.name == "Wurm"][0]  # Verbreitung 98 = Max
    assert best_category(card) == "verbreitung"
