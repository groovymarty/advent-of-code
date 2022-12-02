totscore = 0
# map from input letter ABC or XYZ to R=Rock, P=Paper, S=Scissors
otherPlayDecode = {"A": "R", "B": "P", "C": "S"}
# map from play RPS to score for that play
playScore = {"R": 1, "P": 2, "S": 3}
# map from play RPS to the opponent's play which it beats (R defeats S, etc.)
beats = {"R": "S", "S": "P", "P": "R"}
# same thing but which opponent's play it loses to (R loses to P, etc.)
losesTo = {"R": "P", "S": "R", "P": "S" }
with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        # get other player's play, ABC, and map to RPS
        otherPlay = otherPlayDecode[line[0:1]]
        # what is the desired outcome? X=lose, Y=draw, Z=win
        outcome = line[2:3]
        if outcome == "Y":
            myPlay = otherPlay
            score = 3  # draw
        elif outcome == "Z":
            myPlay = losesTo[otherPlay]
            score = 6  # I win
        elif outcome == "X":
            myPlay = beats[otherPlay]
            score = 0  # I lose
        # add points for my play
        score += playScore[myPlay]
        totscore += score
print(totscore)
