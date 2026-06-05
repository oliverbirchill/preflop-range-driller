import random
import csv
import os

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["♤", "♡", "♢", "♧"]
options = {"raise", "fold"}

def get_ranges():
    ranges = {}

    with open("ranges.csv", mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        
        for row in csv_reader:
            position = row[0].upper().strip()
            hand = row[1].strip()

            if position not in ranges:
                ranges[position] = {hand}
            else:
                ranges[position].add(hand)

    return ranges

def get_position(ranges):
    while True:
        position = input("Which position do you want to practise? UTG/HJ/CO/BTN/SB: ").upper().strip()

        if position in ranges:
            return position

        print("Please enter a valid position: UTG/HJ/CO/BTN/SB.")
        
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

def get_correct_action(position, hand_notation, ranges):
    return "raise" if hand_notation in ranges[position] else "fold"

def normalize_answer(answer):
    answer = answer.lower().strip()

    if answer == "r":
        return "raise"
    elif answer == "f":
        return "fold"
    else:
        return answer
    
def get_user_answer(prompt):
    user_answer = normalize_answer(input(prompt))

    while user_answer not in options:
        user_answer = normalize_answer(input(f"Please type raise/r or fold/f. \n{prompt}"))

    return user_answer

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

def show_missed_hands(missed_hands):
    print("\nYou got the following hands wrong. Please review below: ")
    
    for missed_hand in missed_hands:
        ascii_display, hand_notation, user_answer, correct_action, position = missed_hand
        print(ascii_display)
        print(f"{hand_notation}: you said {user_answer}, correct answer was {correct_action}.\n")

def retry_missed_hands(missed_hands, raise_ranges):
    hands_still_missed = []

    for counter, missed_hand in enumerate(missed_hands):
        ascii_display, hand_notation, user_answer, correct_action, position = missed_hand

        print(f"\nMissed hand review {counter + 1}/{len(missed_hands)} - {position}")
        print(ascii_display)
        user_answer = get_user_answer(f"{position}: raise or fold? ")

        correct_action = get_correct_action(position, hand_notation, raise_ranges)

        if user_answer == correct_action:
            print(f"Correct!")
        else:
            hands_still_missed.append((ascii_display, hand_notation, user_answer, correct_action, position))
            print(f"That's still not right :( According to your ranges, you should {correct_action} {hand_notation}.")

    return hands_still_missed

def run_quiz(raise_ranges):
    score = 0
    missed_hands = []

    position = get_position(raise_ranges)
    number_of_questions = get_number_of_questions()

    for question_number in range(number_of_questions):
        hand, hand_notation = generate_hand()
        ascii_hand_display = display_ascii_hand(hand)

        print(f"\nQuestion {question_number + 1}/{number_of_questions} - {position}")
        print(ascii_hand_display)
        user_answer = get_user_answer(f"{position}: raise or fold? ")

        correct_action = get_correct_action(position, hand_notation, raise_ranges)

        if user_answer == correct_action:
            score += 1
            print(f"Correct! Your score is now {score}.")
        else:
            missed_hands.append((ascii_hand_display, hand_notation, user_answer, correct_action, position))
            print(f"Incorrect! According to your ranges, you should {correct_action} {hand_notation}. Your score is {score}.")

        save_hand_result(position, hand_notation, user_answer, correct_action)
                
    print(f"Your final score is {score}/{number_of_questions} or {round(score / number_of_questions * 100)}%.")

    if missed_hands:
        show_missed_hands(missed_hands)

        missed_hand_review = get_yes_no_answer("Would you like to retry your missed hands? ")

        if missed_hand_review == "yes":
            hands_still_missed = retry_missed_hands(missed_hands, raise_ranges)

            while hands_still_missed:
                hands_still_missed = retry_missed_hands(hands_still_missed, raise_ranges)

    print(read_hand_history())

def get_yes_no_answer(prompt):
    valid_options = ["yes", "y", "no", "n"]
    yes_no_answer = input(prompt).strip().lower()

    while yes_no_answer not in valid_options:
        yes_no_answer = input(f"Please answer yes/y or no/n. \n{prompt}").strip().lower()

    if yes_no_answer == "y" or yes_no_answer == "yes":
        yes_no_answer = "yes"
    else:
        yes_no_answer = "no"

    return yes_no_answer

def save_hand_result(position, hand_notation, user_answer, correct_action):
    file_needs_header = not os.path.exists("hand_history.csv") or os.stat("hand_history.csv").st_size == 0
    result = ""

    if user_answer == correct_action:
        result = "correct"
    else:
        result = "incorrect"

    with open("hand_history.csv", mode="a", newline="") as file:
        csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        if file_needs_header:
            csv_writer.writerow(["position", "hand_notation", "user_answer", "correct_action", "result"])

        csv_writer.writerow([position, hand_notation, user_answer, correct_action, result])

def read_hand_history():
    stats = {}

    with open("hand_history.csv", mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for row in csv_reader:
            position = row[0]
            hand_notation = row[1]
            result = row[4]
            key = (position, hand_notation)
            
            if key not in stats:
                stats[key] = {
                    "seen": 0,
                    "correct": 0,
                    "incorrect": 0,
                    "weakness": 0,
                }

            stats[key]["seen"] += 1

            if result == "correct":
                stats[key]["correct"] += 1
                stats[key]["weakness"] = max(stats[key]["weakness"] -1, 0)
            elif result == "incorrect":
                stats[key]["incorrect"] += 1
                stats[key]["weakness"] += 1

        return stats

def main():
    raise_ranges = get_ranges()
    active = True

    while active:
        run_quiz(raise_ranges)
        play_again = get_yes_no_answer("Would you like to play again? ")

        if play_again == "no":
            active = False

if __name__ == "__main__":
    main()