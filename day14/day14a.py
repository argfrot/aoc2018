from collections import deque

def run(num_generations):
    scoreboard = [3, 7] # the scores at each generation
    elves = [0, 1] # position of each of the elves
    while(len(scoreboard) < num_generations+10):
        next_score = sum(scoreboard[i] for i in elves)
        digits = list(int(x) for x in str(next_score))
        scoreboard.extend(digits)
        elves = list((i+scoreboard[i]+1)%len(scoreboard) for i in elves)
        #print(f'{round}: {scoreboard} -- {elves}')

    result = ''.join(str(s) for s in scoreboard[num_generations:num_generations+10])
    #print(f'{result}')
    return result

def run_target(target_sequence):
    scoreboard = [3, 7] # the scores at each generation
    elves = [0, 1] # position of each of the elves
    match_at = 0 # record where we are in the target_sequence

    rounds = 0
    while(match_at < len(target_sequence)):
        rounds += 1
        next_score = sum(scoreboard[i] for i in elves)
        digits = list(int(x) for x in str(next_score))
        for digit in digits:
            scoreboard.append(digit)
            # this target finding is specific to the current problem
            # don't handle cases where the search string has repeating subsequences e.g. 010101
            # would need more complex state machine; here we always reset to first digit
            if int(target_sequence[match_at]) == digit:
                match_at += 1
                if match_at == len(target_sequence):
                    break
            elif int(target_sequence[0]) == digit:
                match_at = 1
            else:
                match_at = 0
        elves = list((i+scoreboard[i]+1)%len(scoreboard) for i in elves)

    return len(scoreboard) - len(target_sequence)

if __name__ == "__main__":
    for gens in [5, 9, 18, 2018, 640441]:
        print(f'{gens}: {run(gens)}')

    for targets in ["01245", "51589", "92510", "59414", "640441"]:
        t = list(int(i) for i in targets)
        print(f'{targets}: {run_target(t)}')
