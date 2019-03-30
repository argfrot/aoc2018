def get_data():
    with open('input.txt', 'r') as f:
        values = [line for line in f.readlines()]
    return values

def is_one_diff(word1, word2):
    diff_count = 0
    for c1,c2 in zip(word1,word2):
        if c1 != c2:
            diff_count += 1
            if diff_count > 1:
                return False
    return diff_count == 1

def find_one_diff_words(word_list):
    for i, word in enumerate(word_list):
        for other_word in word_list[i+1:]:
            if is_one_diff(word, other_word):
                return word, other_word

def remove_one_diff(word1, word2):
    for c1,c2 in zip(word1, word2):
        if c1 == c2:
            yield c1

values = get_data()
words = find_one_diff_words(values)
print(''.join(remove_one_diff(*words)))
