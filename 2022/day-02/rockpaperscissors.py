totscore = 0
# map from input letter ABC or XYZ to R=Rock, P=Paper, S=Scissors
otherPlayDecode = {"A": "R", "B": "P", "C": "S"}
myPlayDecode = {"X": "R", "Y": "P", "Z": "S"}
# map from play RPS to score for that play
playScore = {"R": 1, "P": 2, "S": 3}
# map from play RPS to the opponent's play which it beats (R defeats S, etc.)
beats = {"R": "S", "S": "P", "P": "R"}
with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        # get other player's play, ABC, and map to RPS
        otherPlay = otherPlayDecode[line[0:1]]
        # get my play, XYZ, and map to RPS
        myPlay = myPlayDecode[line[2:3]]
        # get score for may play (R=1, P=2, S=3)
        score = playScore[myPlay]
        # add points based on who won or lost
        if myPlay == otherPlay:
            score += 3  # draw
        elif beats[myPlay] == otherPlay:
            score += 6  # I win!!
        else:
            score += 0  # I lost.. :-(
        totscore += score
print(totscore)
