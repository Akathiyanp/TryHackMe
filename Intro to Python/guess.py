import random
secret = random.randint(1, 20)
guess = 0
tries = 0
print("I'm thinking a number between 1 and 20")


while guess != secret:
    guess = int(input("Enter a guess value: "))
    tries = tries + 1
    if guess < 1 or guess > 20:
        print("Guess number is out of range. Please Try again!")
    elif guess < secret:
        print("The number is too less!")
    elif guess > secret:
        print("The number is too high!")
    else:
        print('You got it in', tries, "tries!")

