import random, time, sys             # import the modules we want to use.

print('Hello.')

# This is a guess the number game.

while True:

    secretNumber = random.randint(1, 20)
    print('I am thinking of a number between 1 and 20.\nCan you guess which?')

    repetitivePhrase = False
    guessesTaken = 0
    numbersTried = []

    # Ask the player to guess 6 times.

    while guessesTaken < 6:

        invalid = False
        if repetitivePhrase:
            if guessesTaken != 0:
                print('Take another guess. You have guessed ' + str(guessesTaken) + ' out of 6 times.')
            else:
                print('Take a guess.')
        repetitivePhrase = True
        guess = input()
        if guess == '':
            print('Please enter a number.') # Ensure an input.
            continue
        validCharacters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for character in guess:
            if character not in validCharacters:
                invalid = True              # Ensure integer inputs.
                break
        if invalid:
            print('Please enter a valid natural number.')
            continue
        else:
            guess = int(guess)
            if guess in numbersTried:       # Ensure different inputs.
                print('You might as well try different numbers.')  
                continue
            if guess < 1 or guess > 20:     # Ensure number inputs within 1 and 20.
                print('Please enter a number within the range.')
                continue
            numbersTried.append(guess)
        if guess < secretNumber:
            if guessesTaken + 1 < 6:
                print('Your guess is too low.')
        elif guess > secretNumber:
            if guessesTaken + 1 < 6:
                print('Your guess is too high.')
        else:
            guessesTaken += 1
            break    # This condition is the correct guess!

        guessesTaken += 1
    

    if guess == secretNumber:
        if guessesTaken == 1:
            print('Amazing! You have guessed my number in 1 guess!')
        elif guessesTaken == 6:
            print('Phew! You guessed my number in 6 guesses!')
        else:
            print('Good job! You guessed my number in ' + str(guessesTaken) + ' guesses!')
    else:
        print('Nope. The number I was thinking of was ' + str(secretNumber) + '.')


    time.sleep(1)
    while True:
        print('Do you want to play again?\n(y)es / (n)o')
        play = input()
        if play.upper() == 'N' or play.upper() == 'NO':
            despedides = ['Thanks for playing!', 'Sorry to see you go.', 'Hope to see you soon!', 'Well played!', 'Goodbye!', 'Cheerio!', 'Farewell.', 'Ciao!', 'Oh...']
            print(despedides[random.randint(0,8)])
            time.sleep(1.2)
            sys.exit()                  # Asks to play again or else terminate the program.
        if play.upper() == 'Y' or play.upper() == 'YES':
            break
