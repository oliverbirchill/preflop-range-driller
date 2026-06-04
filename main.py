import random

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["♤", "♡", "♢", "♧"]
raise_range = {"AA", "QQ", "AKs", "AQs", "AKo"}
options = {"raise", "fold"}

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

def generate_hand():
    card_1 = generate_card()
    card_2 = generate_card()

    while card_2 == card_1:
        card_2 = generate_card()

    hand = card_1, card_2
    hand = sorted(hand, key=lambda card: ranks.index(card[0]), reverse=True)

    hand_notation = get_hand_notation(hand)

    return hand, hand_notation

def get_number_of_questions():
    while True:
        answer = input("How many questions would you like me to ask? ")

        try:
            number = int(answer)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if number <= 0 :
            print("Please enter a number greater than 0.")
            continue

        return number

def get_correct_action(hand_notation):
    return "raise" if hand_notation in raise_range else "fold"

def normalize_answer(answer):
    answer = answer.lower().strip()

    if answer == "r":
        return "raise"
    elif answer == "f":
        return "fold"
    else:
        return answer
    
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
 
score = 0
number_of_questions = get_number_of_questions()

for question_number in range(number_of_questions):
    hand, hand_notation = generate_hand()
    ascii_hand_display = display_ascii_hand(hand)
    print(ascii_hand_display)
    user_answer = normalize_answer(input("Raise or fold? "))

    while user_answer not in options:
        print(ascii_hand_display)
        user_answer = normalize_answer(input("Raise or fold? "))

    correct_action = get_correct_action(hand_notation)

    if user_answer == correct_action:
        score += 1
        print(f"Correct! Your score is now {score}.")
    else:
        print(f"Incorrect! According to your ranges, you should {correct_action} {hand_notation}. Your score is {score}.")
            
print(f"Your final score is {score}/{number_of_questions} or {round(score / number_of_questions * 100)}%.")
