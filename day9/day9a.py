import datetime
import operator
import re
from collections import defaultdict, namedtuple
import heapq

def get_data(parser=str):
    with open('day9/input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

#9 players; last marble is worth 25 points
def parse_line(line):
    words = line.split()
    return (int(words[0]), int(words[6]))

class List(object):
    def __init__(self, value, next=None, previous=None):
        self.value = value
        self.next = next if next else self
        self.previous = previous if previous else self

def move(item, hops):
    if hops < 0:
        while(hops < 0):
            item = item.previous
            hops += 1
    else:
        while(hops > 0):
            item = item.next
            hops -= 1
    return item

def unlink(item):
    next = item.next
    next.previous = item.previous
    next.previous.next = next
    return next

def insert_after(item, value):
    new_item = List(value, next=item.next, previous=item)
    item.next = new_item
    new_item.next.previous = new_item
    return new_item

def to_list(root):
    l = [root.value]
    current_node = root.next
    while(current_node != root):
        l.append(current_node.value)
        current_node = current_node.next
    return l


def play_game(num_players, last_marble):
    points = [0]*num_players
    current_position = List(0)
    current_player = 1
    next_marble = 1

    while(next_marble <= last_marble):

        if next_marble % 23 == 0:
            next_position = move(current_position, -7)
            value = next_position.value
            next_position = unlink(next_position)
            points[current_player] += next_marble + value
        else:
            next_position = move(current_position, 1)
            next_position = insert_after(next_position, next_marble)

        current_position = next_position
        next_marble += 1
        current_player = (current_player+1)%num_players

    return max(points)


def play_game_naive(num_players, last_marble):
    points = [0]*num_players
    current_position = 0
    current_player = 1
    game_board = [0]
    next_marble = 1
    while(next_marble <= last_marble):
        if next_marble % 23 == 0:
            next_position = (current_position-7)%len(game_board)
            value = game_board[next_position]
            game_board.remove(value)
            points[current_player] += next_marble + value
        else:
            next_position = (current_position+1)%len(game_board)+1
            game_board.insert(next_position, next_marble)
        current_position = next_position
        next_marble += 1
        current_player = (current_player+1)%num_players
    return max(points)

def run():
    values = get_data(parser=parse_line)
    print(f'inputs => {values}')

    for game in values:
        high_score = play_game(*game)
        print(f'{high_score}')


if __name__ == "__main__":
    run()
