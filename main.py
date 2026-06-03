import random

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["♤", "♡", "♢", "♧"]
raise_range = {"AA", "QQ", "AKs", "AQs", "AKo"}
options = {"raise", "fold"}

def generate_hand():
    rank_1 = random.choice(ranks)
    rank_2 = random.choice(ranks)

    if rank_1 == rank_2:
        return rank_1 + rank_2
    else:
        hand = "".join(sorted(rank_1 + rank_2, key=ranks.index, reverse=True))
        suit_or_offsuit = random.choice(["s", "o"])
        return hand + suit_or_offsuit
    
def get_correct_action(hand):
    return "raise" if hand in raise_range else "fold"

def normalize_answer(answer):
    answer = answer.lower().strip()

    if answer == "r":
        return "raise"
    elif answer == "f":
        return "fold"
    else:
        return answer

score = 0
number_of_questions = int(input("How many questions would you like me to ask? "))

for question_number in range(number_of_questions):
    hand = generate_hand()
    user_answer = normalize_answer(input(f"{hand}. Raise or fold? "))

    while user_answer not in options:
        print("That doesn't look to be a correct input... Please enter raise or fold.")
        user_answer = normalize_answer(input(f"{hand}. Raise or fold? "))

    if user_answer == get_correct_action(hand):
        score += 1
        print(f"Correct! Your score is now {score}")
    else:
        print(f"Incorrect! Your score is {score}")
            

        
        
