import requests
import json

# Establish URLS for the game to 
deck_url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6"
deck_response = requests.get(deck_url).json()
deck_id = deck_response['deck_id']

def player_bust(player_score, deck_id):
    if player_score > 21:
        print('Player Bust')
    else:
        # Ask for another hit.
        prompt = '>'
        print(f'You currently have {player_score}. Do you want anothet hit? Y/N')
        input(prompt)
        if input == 'Y' or 'y':
            hit(deck_id)
        else:
            return player_score

def first_turn(deck_id):
    ''' The first turn of the game. Two cards will be drawn from the deck.'''
    draw_cards_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2"
    draw_response = requests.get(draw_cards_url).json()

    # Lookup the cards in the response data.
    # The 0th card in the response is the player. The 1st is the dealer.
    card_1 = draw_response['cards'][0]['value'] + " of " + draw_response['cards'][0]['suit']
    card_2 = draw_response['cards'][1]['value'] + " of " + draw_response['cards'][1]['suit']
    print(f'The player has: {card_1}')
    print(f'The dealer has: {card_2}')

    # Scrape the value key from the dict in the response data. Add to players score. 
    player_score = player_score + draw_response['cards'][0]['value'] + draw_response['cards'][1]['value']

    # Shuffle the deck.
    shuffle_deck_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/"

    return player_score

def hit(deck_id):
    ''' Player chooses to HIT to continue. Draw 1 card.'''
    draw_cards_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"
    hit_response = requests.get(draw_cards_url).json()

    # Get the card and the value.
    hit_card = hit_response['cards'][0]['value'] + " of " + hit_response['cards'][0]['suit']
    print(f'The player chose to HIT. They get a {hit_card}')

    # Update the player score
    player_score = player_score + hit_response['cards'][0]['value']

    # Check if the player busted. Invoke function. If they didn't the program passes back here. 
    player_bust(player_score, deck_id)

    return player_score

# Commence the game.
player_score = 0
print(f'It\'s time to begin the game. Your deck id is {deck_id}')
first_turn(deck_id)
print(f'Your current score is {player_score}')
prompt = '>'
print(f'Do you wish to hit? Y/N')
input(prompt)
print(f'Your final score is {player_score}')
