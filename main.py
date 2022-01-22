from collections import Counter
from pprint import pprint


def count_letters(words1):
    letter_frequency = Counter()
    for word in words1:
        for letter in word:
            letter_frequency[letter] += 1
    return letter_frequency


def only_alphanum_ascii_words(words1):
    filtered_words = []
    for word in words1:
        if word.isascii() and word.isalpha():
            filtered_words.append(word)
    return filtered_words


def filter_x_letter_word(words1, length=5):
    x_letter_words = []
    for word in words1:
        if len(word) == length:
            x_letter_words.append(word)
    return x_letter_words


# Press the green button in the gutter to run the script.
def find_words_containing_all_these_letters(words1, letters1):
    good_words = []
    for word in words1:
        if all(letter in word for letter in letters1):
            good_words.append(word)
    return good_words


def remove_words_containing(words1, letters1):
    filtered_words = []
    for word in words1:
        if any(letter in word for letter in letters1):
            continue
        else:
            filtered_words.append(word)
    return filtered_words


def words_with_letters_at_specific_places(words1, letters_at_indices):
    filtered_words = []
    for word in words1:
        if all(word[index] == letter for letter, index in letters_at_indices.items()):
            filtered_words.append(word)
    return filtered_words


if __name__ == '__main__':
    words = [line.strip() for line in open("/usr/share/dict/words")]
    words = [word.lower() for word in words]
    WORD_LENGTH = 5
    five_letter_words = filter_x_letter_word(words, length=WORD_LENGTH)

    filtered_five_letter_words = only_alphanum_ascii_words(five_letter_words)

    letter_counts = count_letters(filtered_five_letter_words)

    pprint(letter_counts)
    # print(f"Number of words in dictionary: {len(words)}")
    # print(f"Number of five letter words: {len(five_letter_words)}")
    print(f"Number of filtered five letter words: {len(filtered_five_letter_words)}")
    print(f"A filtered five letter word: {filtered_five_letter_words[300]}")
    letters = [letter for letter, frequency in letter_counts.most_common(WORD_LENGTH)]
    best_words = find_words_containing_all_these_letters(filtered_five_letter_words, letters)
    print(best_words)
    current_words = remove_words_containing(filtered_five_letter_words, ['a', 'r', 'o', 's'])
    print(current_words)
    current_words = words_with_letters_at_specific_places(current_words, {'e': 4})
    print(f"The number of possible answers are: {len(current_words)}")
    print(f"The best current guesses are: {current_words}")
    current_words = remove_words_containing(current_words, ['j', 'u', 'y'])
    current_words = words_with_letters_at_specific_places(current_words, {'e': 4, 'c': 3})
    print(f"The number of possible answers are: {len(current_words)}")
    print(f"The best current guesses are: {current_words}")

    current_letter_counts = count_letters(current_words)
    print(current_letter_counts)
    # letters = [letter for letter, frequency in current_letter_counts.most_common(WORD_LENGTH + 1)]
    words_to_search_through = remove_words_containing(filtered_five_letter_words, ['a', 'r', 'o', 's', 'e'])
    print(f"Possible words to use: {len(words_to_search_through)}")
    current_letter_counts.pop('e')  # Fjern den ene bokstaven vi vet fantes
    trash = []
    for first_letter, frequency in current_letter_counts.most_common(len(current_letter_counts) - 1):
        trash.append(first_letter)
        for second_letter, frequency in current_letter_counts.most_common(len(current_letter_counts) - 1):
            if second_letter in trash or second_letter == first_letter:
                continue
            for third_letter, frequency in current_letter_counts.most_common(len(current_letter_counts) - 1):
                if third_letter in trash or third_letter == second_letter or third_letter == first_letter:
                    continue
                for fourth_letter, frequency in current_letter_counts.most_common(len(current_letter_counts) - 1):
                    if fourth_letter in trash or fourth_letter == third_letter or fourth_letter == second_letter or fourth_letter == first_letter:
                        continue
                    for fifth_letter, frequency in current_letter_counts.most_common(len(current_letter_counts) - 1):
                        if fifth_letter in trash or fifth_letter == third_letter or fifth_letter == fourth_letter or fifth_letter == second_letter or fifth_letter == first_letter:
                            continue
                        letters_to_use = [first_letter, second_letter, third_letter, fourth_letter, fifth_letter]
                        best_words = find_words_containing_all_these_letters(words_to_search_through, letters_to_use)
                        if len(best_words) != 0:
                            break
    print(best_words)
