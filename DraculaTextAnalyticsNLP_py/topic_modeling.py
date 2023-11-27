from imports import logging, time, hashlib, corpora, LdaMulticore, CoherenceModel, defaultdict
from tokenize_text import tokenized_text_cache, tokenized_text_cache_lock


def topic_modeling(cleaned_text, num_topics=5, passes=12, workers=4):
    logging.info("Initiating Topic Modeling\n")
    start_time = time.time()  # Record the start time

    with tokenized_text_cache_lock:
        # Use the cleaned text for querying the cache
        cleaned_text_hash = hashlib.md5(cleaned_text.encode()).hexdigest()

        # Retrieve tokens from the cache using the cleaned text hash
        tokens_info = tokenized_text_cache.get(cleaned_text_hash, None)

    if tokens_info is None:
        logging.warning("Tokens not found in cache. Tokenize the text first.")
        return

    # Extract tokens_str and doc from the cache
    tokens_str, doc = tokens_info

    try:
        # Create a dictionary and corpus based on the tokenized text
        dictionary = corpora.Dictionary([tokens_str.split()])
        corpus = [dictionary.doc2bow(tokens_str.split())]

        # Train the LDA model with a specified number of passes and workers
        lda_model = LdaMulticore(corpus, num_topics=num_topics, id2word=dictionary, passes=passes, workers=workers)

        # Print the topics
        topics = lda_model.print_topics()
        logging.info("LDA Topics:")
        for i, topic in enumerate(topics):
            logging.info(f"Topic {i + 1}: {topic}")

        top_words_modeling = get_top_words_modeling(lda_model, num_topics)
        coherence_score = get_coherence_score(lda_model, corpus, [tokens_str.split()], dictionary)
        topic_overlaps = explore_topic_overlaps(num_topics, top_words_modeling)

        for topic_id in range(num_topics):
            logging.info(f"Top Words in Topic {topic_id + 1}:\n{top_words_modeling[f'Topic {topic_id + 1}']}")

        logging.info(f"Topic Coherence Score: {coherence_score}")

        for comparison, common_words_modeling in topic_overlaps.items():
            logging.info(f"{comparison}: {common_words_modeling}")

    except Exception as e:
        logging.error(f"An error occurred during topic modeling: {e}")

    finally:
        # Record the finish time
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Topic Modeling finished. Duration: {duration:.2f} seconds.\n")


def get_top_words_modeling(lda_model, num_topics, num_words=5):
    top_words = {}
    for topic_id in range(num_topics):
        words = lda_model.show_topic(topic_id, topn=num_words)
        top_words[f"Topic {topic_id + 1}"] = [word for word, _ in words]
    return top_words


def get_coherence_score(lda_model, corpus, texts, dictionary):
    coherence_model = CoherenceModel(model=lda_model, texts=texts, corpus=corpus, dictionary=dictionary,
                                     coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    return coherence_score


def explore_topic_overlaps(num_topics, top_words):
    topic_overlaps = defaultdict(list)
    for i in range(num_topics):
        for j in range(i + 1, num_topics):
            common_words_modeling = set(top_words[f"Topic {i + 1}"]) & set(top_words[f"Topic {j + 1}"])
            topic_overlaps[f"Topic {i + 1} vs Topic {j + 1}"] = list(common_words_modeling)
    return topic_overlaps
