from imports import Counter, logging
from constants import TOP_WORDS_COUNT, WORDS_OVER_THRESHOLD


def process_analysis_results(cleaned_text, common_words_list):

    # Most common word
    word_counter = Counter(cleaned_text.split())
    most_common_word, most_common_count = word_counter.most_common(1)[0]

    # Store different word lengths
    word_length_results = []

    # Iterate over word lengths
    for unique_letter_word_length in range(5, 18):
        unique_num_letter_words = {word for word in cleaned_text.split() if len(word) == unique_letter_word_length}

        # Append results current word length to the list
        word_length_results.append({
            "word_length": unique_letter_word_length,
            "unique_words": unique_num_letter_words
        })

    words_over_threshold = {word: count for word, count in word_counter.items() if count > WORDS_OVER_THRESHOLD}
    top_words = dict(word_counter.most_common(TOP_WORDS_COUNT))

    # Word counter excluding common words const
    filtered_word_counter = {word: count for word, count in word_counter.items() if word not in common_words_list}

    # Top words from the filtered_word_counter
    unique_top_words = sorted(
        filtered_word_counter,
        key=lambda word: filtered_word_counter[word],
        reverse=True
    )[:TOP_WORDS_COUNT]

    logging.info(f"The most common word is '{most_common_word}' appearing {most_common_count} times\n")

    # Unique words by word length
    for result in word_length_results:
        word_length = result["word_length"]
        unique_words = result["unique_words"]

        logging.info(f"Unique {word_length}-letter words: {len(unique_words)}")
        logging.info({f"Word {i + 1}": word for i, word in enumerate(unique_words)})
        logging.info(f"{word_length}-letter words complete\n")

    # Words over threshold
    logging.info(f"Words that appear more than {WORDS_OVER_THRESHOLD} times:")
    logging.info("\n".join("{}: {} times".format(word, word_counter[word]) for word in words_over_threshold))
    logging.info("---\n")

    # Top words by frequency
    logging.info(f"Top {TOP_WORDS_COUNT} words and their frequencies:")
    logging.info("\n".join("{}: {} times".format(word, frequency) for word, frequency in top_words.items()))
    logging.info("---\n")

    # Unique top words by frequency
    logging.info(
        f"Unique Top {TOP_WORDS_COUNT} "
        f"words (excluding certain common words, pronouns, single characters, and numbers):"
    )
    logging.info("\n".join("{}: {} times".format(word, filtered_word_counter[word]) for word in unique_top_words))
    logging.info("---\n")

    result = {
        "most_common_word": most_common_word,
        "word_length_results": word_length_results,
        "words_over_threshold": words_over_threshold,
        "top_words": top_words,
        "unique_top_words": unique_top_words,
    }

    return result
