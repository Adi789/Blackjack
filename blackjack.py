import random

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

dealer_wins = 0
player_wins = 0

def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    for suit in suits:
        # first number cards  1 to 10
        for card in range ( 1, 11 ):
            name = 'cards/{}_{}.{}'.format ( str ( card ), suit, extension )
            image = tkinter.PhotoImage ( file=name )
            card_images.append ( (card, image) )

        for card in face_cards:
            name = 'cards/{}_{}.{}'.format ( str ( card ), suit, extension )
            image = tkinter.PhotoImage ( file=name )
            card_images.append ( (10, image) )


def deal_cards(frame):
    # pop the next card
    next_card = deck.pop ( 0 )
    # need to add cards again to the back of the pack to avoid empty deck error
    # pop card from the top of the deck which is 0
    # pop retrieves the list and removes it as well from the specified position
    # add the image to a Label and display the label
    deck.append ( next_card )
    tkinter.Label ( frame, image=next_card[1], relief='raised' ).pack ( side='left' )
    # using pack manager to pack cards on left
    return next_card


def score_hands(hand):
    # calculate the total score of all cards in the list.
    # only one ace can have one value of 11
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]  # the first card
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        if score > 16 and ace:
            score -= 10
        ace = False
    return score

def initial_deal():
    deal_player ()
    dealer_hand.append ( deal_cards ( dealer_card_frame ) )
    dealer_score_label.set ( score_hands ( dealer_hand ) )
    deal_player ()



def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand

    dealer_card_frame.destroy ()
    dealer_card_frame = tkinter.Frame ( card_frame, background='green' )
    dealer_card_frame.grid ( row=0, column=1, sticky='ew', rowspan=2 )

    player_card_frame = tkinter.Frame ( card_frame, background='green' )
    player_card_frame.grid ( row=2, column=1, sticky="ew", rowspan=2 )

    # need to clear the result status when dealer or player wins
    result_text.set ( "" )
    # need to recreate the lists again
    dealer_hand = []
    player_hand = []
    initial_deal()

def deal_dealer():
    global dealer_wins
    global player_wins
    dealer_score = score_hands ( dealer_hand )
    while 0 < dealer_score < 17:
        dealer_hand.append ( deal_cards ( dealer_card_frame ) )
        dealer_score = score_hands ( dealer_hand )
        dealer_score_label.set ( dealer_score )
        player_score = score_hands ( player_hand )
    # playyers current score
    if player_score > 21:
        result_text.set ( "Dealer Wins, You Busted" )
        print(dealer_score)
        print("dealer wins is "+dealer_wins)
        dealer_wins +=1
        print("{} {}".format("dealer score",dealer_wins))
        score_label .set(dealer_wins)
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set ( " You win!!" )
        player_wins +=1
        print("{} {}".format("dealer score",player_wins))
        score_label.set(player_wins)
    elif dealer_score > player_score:
        result_text.set ( "Dealer wins!" )
        dealer_wins += 1
        score_label.set(dealer_wins)
        print("{} {}".format("dealer score",dealer_wins))

    else:
        result_text.set ( "Draw" )

def deal_player():
    global player_wins
    global dealer_wins
    player_hand.append ( deal_cards ( player_card_frame ) )
    player_score = score_hands ( player_hand )
    player_score_label.set ( player_score )

    if player_score > 21:
        result_text.set ( "Busted, Dealer Wins" )
        player_wins+=1
        score_label.set(player_wins)


    # global  player_ace
    # global player_score
    # card_value = deal_cards(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    #
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score >21:
    #     result_text.set("Dealer wins!!")
def shuffle():
    random.shuffle ( deck )

def play():
    initial_deal()
    mainWindow.mainloop ()


mainWindow = tkinter.Tk ()

mainWindow.title ( "BlackJack" )
mainWindow.geometry ( "640x480" )
mainWindow.configure ( background="grey" )

result_text = tkinter.StringVar ()
result = tkinter.Label ( mainWindow, textvariable=result_text )
result.grid ( row=0, column=1, columnspan=3 )

card_frame = tkinter.Frame ( mainWindow, relief="sunken", borderwidth=1, background="green" )
card_frame.grid ( row=1, column=0, sticky="ew", columnspan=4, rowspan=2 )

dealer_score_label = tkinter.IntVar ()
tkinter.Label ( card_frame, text="Dealer", background="green", fg='white' ).grid ( row=0, column=0 )
tkinter.Label ( card_frame, textvariable=dealer_score_label, background="green", fg="white" ).grid ( row=1, column=0 )

# embed the frame to hold card images
dealer_card_frame = tkinter.Frame ( card_frame, background="green" )
dealer_card_frame.grid ( row=0, column=1, sticky="ew", rowspan=2 )

######## SCORE BOARD
score_frame = tkinter.Frame ( mainWindow, relief="sunken", borderwidth=1, background="green" )
score_frame.grid ( row=1, column=2, sticky="ne", columnspan=3, rowspan=2 )

score_label = tkinter.IntVar()
tkinter.Label(score_frame, text = "Score", background = "white",fg ="black").grid(row = 1, column =0)
tkinter.Label(score_frame, textvariable =score_label, background = "green",fg = "white").grid(row = 2,column = 0)
####################################
player_score_label = tkinter.IntVar ()
# player_score = 0
# player_ace =  False
tkinter.Label ( card_frame, text="Player", background="green", fg="white" ).grid ( row=2, column=0 )
tkinter.Label ( card_frame, textvariable=player_score_label, background="green", fg="white" ).grid ( row=3, column=0 )

# embed frame again
player_card_frame = tkinter.Frame ( card_frame, background="green" )
player_card_frame.grid ( row=2, column=1, sticky="ew", rowspan=2 )

button_frame = tkinter.Frame ( mainWindow )
button_frame.grid ( row=3, column=0, columnspan=3, sticky='w' )

dealer_button = tkinter.Button ( button_frame, text="Dealer", command=deal_dealer )
dealer_button.grid ( row=0, column=0 )

player_button = tkinter.Button ( button_frame, text="Player", command=deal_player )
player_button.grid ( row=0, column=1 )
### a new button , clear the cards and reset the game and starts a new game.
# button name is new game

newgame_button = tkinter.Button ( button_frame, text="New Game", command=new_game )
newgame_button.grid ( row=0, column=2 )

shuffle_button = tkinter.Button ( button_frame, text="Shuffle Cards", command=shuffle )
shuffle_button.grid ( row=0, column=3 )
# load cards

cards = []
load_images ( cards )
print ( cards )

# create a new deck of cards and shuffle them
deck = list ( cards ) + list ( cards )
shuffle ()
# random.shuffle ( deck )
# replaced by shuffle function

# list to store the hand's
dealer_hand = []
player_hand = []

#new_game ()
# game begins with 2 cards for player and one for dealer
if __name__ == "__main__":
    play()