from imports import logging, time, nlp, Counter


def extract_part_of_speech_tags(tokens_str, doc, view_all=False):
    logging.info("Initiating POS Tagging")
    start_time = time.time()

    doc = doc if doc else nlp(tokens_str)

    pos_tag = [(token.text, token.pos_) for token in doc]
    pos_tags_for_count = [token.pos_ for token in doc]

    # View_all will log every POS tag in text with context surrounding that tag
    if view_all:
        logging.info("Part of Speech Tags:")
        for i, (word, pos) in enumerate(pos_tag):
            context = " ".join([token.text for token in doc[max(0, i - 2):i + 3]])
            logging.info(f"{word} : {pos} (Context: {context})")
        logging.info("---\n")

    # Count occurrences of each tag
    pos_tag_counts = Counter(pos_tags_for_count)

    logging.info("Part of Speech Tags (Counts):")
    for pos_tag, count in pos_tag_counts.items():
        logging.info(f"{pos_tag}: {count} times")

    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Part of Speech Tagging finished. Duration: {duration:.2f} seconds.\n")
