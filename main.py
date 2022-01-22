#!/usr/bin/python
import argparse
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


def find_best_words_for_these_letters(words1, letters1):
    good_words = Counter()
    for word in words1:
        how_many = 0
        for letter in letters1:
            if letter in word:
                how_many += 1
        if how_many > 0:
            good_words[word] = how_many
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


def parse_arguments():
    parser = argparse.ArgumentParser(description='Find a word to use for a word puzzle')
    parser.add_argument('--dictionary_file', metavar='FILENAME', type=str,
                        help='Filepath to the dictionary file to use', default='ubuntu_words.txt')
    parser.add_argument('--word_length', metavar='N', type=int, help='How many characters in the words in the puzzle',
                        default=5)
    parser.add_argument('--find_word_for_given_letters', metavar='LETTERS', type=str,
                        help='Find a word which contains the given letters')
    parser.add_argument('--ban_list', metavar='LETTERS', type=str,
                        help='Define letters that should not be used in the word from find_word_for_given_letters')
    return parser.parse_args()


def correct_spot_in_solution_dict(input_from_user):
    letters_at_correct_spot_in_solution_word = {}
    for key_value_comma_separated in input_from_user:
        k, v = key_value_comma_separated.split(',')
        letters_at_correct_spot_in_solution_word[k] = int(v)
    return letters_at_correct_spot_in_solution_word


def ask_user_for_results():
    letters_present_in_solution_word = list(input(
        "Letters from the word you chose present in the correct word (example: atc): "))
    correct_spots_in_solution = {}
    if len(letters_present_in_solution_word) != 0:
        correct_spot_letters_from_user1 = input(
            f"If any of these {letters_present_in_solution_word} letters were in the correct location, "
            f"write them here at their correct spot (example: a,3 c,0): ").split()
        correct_spots_in_solution = correct_spot_in_solution_dict(correct_spot_letters_from_user1)
    return letters_present_in_solution_word, correct_spots_in_solution


def do_one_iteration_of_selecting_a_word(current_possible_solution_words, letters_tried,
                                         correct_spot_letters_from_user_from_last,
                                         letters_present_in_solution_from_last, words_to_select_next_guess_from):
    letter_counts = count_letters(current_possible_solution_words)
    most_frequent_letters = [letter for letter, frequency in letter_counts.most_common(WORD_LENGTH)]
    letter_counts_copy = letter_counts.copy()
    for letter in letters_tried:
        letter_counts_copy.pop(letter)
    most_frequent_letters_excluding_banned_letters = letter_counts_copy
    best_words = find_words_containing_all_these_letters(words_to_select_next_guess_from, most_frequent_letters)
    for ind in range(len(most_frequent_letters_excluding_banned_letters) - WORD_LENGTH):
        if len(best_words) == 0:
            freqs = most_frequent_letters_excluding_banned_letters.most_common(len(letter_counts))
            most_frequent_letters = [letter for letter, frequency in freqs[ind:ind + WORD_LENGTH]]
            # Fant ingen som har alle de mest frekvente. Prøv med mindre frekvente?
            best_words = find_words_containing_all_these_letters(words_to_select_next_guess_from, most_frequent_letters)
        else:
            break
    if len(best_words) == 0:
        print(f"Sorry, there are no words that have {WORD_LENGTH} unused letters, use your own intuition to choose "
              f"what to use to find the solution from these possible solution words:")
        pprint(letters_present_in_solution_from_last)
    else:
        print(best_words)
    # Keep track of which words/letters have been tried
    letters_tried.extend(most_frequent_letters)
    # Ask user how using the word went. We can't know which word they used.
    # However, we can know that the word they used contained all the letters we looked for.
    # Maybe we can use that somehow later?
    letters_present_in_solution, letters_in_correct_spot = ask_user_for_results()
    letters_present_in_solution.extend(letters_present_in_solution_from_last)
    letters_in_correct_spot.update(correct_spot_letters_from_user_from_last)
    if len(letters_present_in_solution) != 0:
        # Remove letters that are not present in the solution word
        letters_to_remove = most_frequent_letters.copy()
        for letter in letters_present_in_solution:
            if letter in letters_to_remove:
                letters_to_remove.remove(letter)
        current_possible_solution_words = remove_words_containing(current_possible_solution_words, letters_to_remove)
        if len(letters_in_correct_spot) != 0:
            current_possible_solution_words = words_with_letters_at_specific_places(current_possible_solution_words,
                                                                                    letters_in_correct_spot)
    else:
        current_possible_solution_words = current_possible_solution_words
    print(f"The number of possible answers are: {len(current_possible_solution_words)}")
    print(f"The best current guesses for the solution word are: ")
    pprint(current_possible_solution_words)
    return best_words, letters_tried, letters_in_correct_spot, current_possible_solution_words


def method_name():
    global best_words
    letters_to_try = current_letter_counts.most_common(len(current_letter_counts))
    for letter_tried in letters_tried:
        if letter_tried in letters_to_try:
            letters_to_try.remove(letter_tried)
    trash = []
    for first_letter, _ in letters_to_try:
        # trash.append(first_letter)
        for second_letter, _ in letters_to_try:
            if second_letter in trash or second_letter == first_letter:
                continue
            for third_letter, _ in letters_to_try:
                if third_letter in trash or third_letter == second_letter or third_letter == first_letter:
                    continue
                for fourth_letter, _ in letters_to_try:
                    if fourth_letter in trash or fourth_letter == third_letter or fourth_letter == second_letter or fourth_letter == first_letter:
                        continue
                    for fifth_letter, _ in letters_to_try:
                        if fifth_letter in trash or fifth_letter == third_letter or fifth_letter == fourth_letter or fifth_letter == second_letter or fifth_letter == first_letter:
                            continue
                        letters_to_use = [first_letter, second_letter, third_letter, fourth_letter, fifth_letter]
                        best_words = find_words_containing_all_these_letters(words_to_select_next_guess_from,
                                                                             letters_to_use)
                        if len(best_words) != 0:
                            break
    print(best_words)


if __name__ == '__main__':
    args = parse_arguments()

    words = [line.strip() for line in open(args.dictionary_file)]
    words = [word.lower() for word in words]
    WORD_LENGTH = args.word_length
    x_letter_words = filter_x_letter_word(words, length=WORD_LENGTH)
    filtered_x_letter_words = only_alphanum_ascii_words(x_letter_words)
    # filtered_x_letter_words.sort()
    # filtered_x_letter_words = list(set(filtered_x_letter_words))  # Remove duplicates
    if args.find_word_for_given_letters is not None:
        if args.ban_list is not None:
            banned_letters = list(args.ban_list)
            copy_of_words = filtered_x_letter_words.copy()
            for word in copy_of_words:
                for banned_letter in banned_letters:
                    if banned_letter in word and word in filtered_x_letter_words:
                        filtered_x_letter_words.remove(word)
        pprint(find_best_words_for_these_letters(filtered_x_letter_words,
                                                 list(args.find_word_for_given_letters)).most_common(1))
        exit(0)

    letter_counts = count_letters(filtered_x_letter_words)

    pprint(letter_counts)
    print(f"Number of words in dictionary: {len(words)}")
    print(f"Number of {WORD_LENGTH} letter words: {len(x_letter_words)}")
    print(f"Number of ascii, english-alphabet {WORD_LENGTH} letter words: {len(filtered_x_letter_words)}")
    # print(f"A filtered five letter word: {filtered_x_letter_words[0]}")

    # Strategy:
    # Find words containing all the most frequent letters
    # Use one of those words to find which letters appear in the word
    # Remove all words containing letters that we now know don't appear
    # Find all words with a letter in the correct spot
    # TODO Penalize words with duplicated letters (deice -> two of letter e)
    letters_tried = []
    correct_spot_letters_from_user = []
    current_possible_solution_words = filtered_x_letter_words.copy()
    letters_present_in_solution_from_last = []
    words_to_select_next_guess_from = filtered_x_letter_words.copy()
    for i in range(4):
        # Hver runde: Finn det neste ordet.
        # Husk hvilke bokstaver som er brukt.
        # Husk hvilke bokstaver som finnes i ordet
        # Husk hvilke bokstaver som er på en spesifikk plass
        # Ved neste runde skal vi ta inn de mulige ordene det kan være, regne ut det som er mest sannsynlige fra de.
        best_words, letters_tried, correct_spot_letters_from_user, letters_present_in_solution_from_last = do_one_iteration_of_selecting_a_word(
            current_possible_solution_words, letters_tried=letters_tried,
            correct_spot_letters_from_user_from_last=correct_spot_letters_from_user,
            letters_present_in_solution_from_last=letters_present_in_solution_from_last,
            words_to_select_next_guess_from=words_to_select_next_guess_from)

        # calculate frequency of the possible solution words to find the next word to use.
        current_letter_counts = count_letters(letters_present_in_solution_from_last)
        print(f"Frequency for possible solution words: {current_letter_counts}")
        # letters = [letter for letter, frequency in current_letter_counts.most_common(WORD_LENGTH + 1)]

        # Remove all words that contain any of the letters we have already tried to use
        # They no longer providing any information, so we should not suggest them
        words_to_select_next_guess_from = remove_words_containing(filtered_x_letter_words, letters_tried)
        print(f"Possible words to use next: {len(words_to_select_next_guess_from)}")

    # method_name()
