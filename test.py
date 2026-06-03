import random

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["♤", "♡", "♢", "♧"]
raise_range = {"AA", "QQ", "AKs", "AQs", "AKo"}
options = {"raise", "fold"}

def generate_hand():
    def generate_card():
        rank = random.choice(ranks)
        suit = random.choice(suits)
        return rank, suit
    
    def get_hand_notation(hand):
        hand_notation = ""

        first_card = hand[0]
        second_card = hand[1]

        first_rank = first_card[0]
        first_suit = first_card[1]

        second_rank = second_card[0]
        second_suit = second_card[1]

        if first_rank == second_rank:
            hand_notation = first_rank + second_rank
        elif first_suit == second_suit:
            hand_notation = first_rank + second_rank + "s"
        else:
            hand_notation = first_rank + second_rank + "o"

        return hand_notation

    card_1 = generate_card()
    card_2 = generate_card()

    while card_2 == card_1:
        card_2 = generate_card()

    hand = card_1, card_2
    hand = sorted(hand, key=lambda card: ranks.index(card[0]), reverse=True)

    hand_notation = get_hand_notation(hand)

    return hand, hand_notation

print(generate_hand())