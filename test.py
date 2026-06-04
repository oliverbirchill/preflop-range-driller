def display_ascii_card(card):
    rank = card[0]
    suit = card[1]
    
    return [
        "┌─────┐",
        f"│{rank}    │",
        f"│  {suit}  │",
        f"│    {rank}│",
        "└─────┘",
    ]

def display_ascii_hand(hand):
    first_card_lines = display_ascii_card(hand[0])
    second_card_lines = display_ascii_card(hand[1])

    combined_lines = []

    for left_line, right_line in zip(first_card_lines, second_card_lines):
        combined_lines.append(left_line + " " + right_line)

    return "\n".join(combined_lines)
    
print(display_ascii_hand((("K", "♥️"), ("J", "♦️"))))