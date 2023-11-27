from imports import logging, time, nlp


def summarize_text(token_str, doc, sentence_count=5):
    logging.info("Initiating Summary")
    start_time = time.time()

    doc = doc if doc else nlp(token_str)

    # Calculate sentence scores
    sentence_scores = {sent: sent.similarity(doc) for sent in doc.sents}

    # Sort sentences by score
    sorted_sentences = sorted(sentence_scores.keys(), key=lambda x: x.similarity(doc), reverse=True)

    # Select the top 'sentence_count' sentences as summary
    selected_sentences = sorted_sentences[:sentence_count]

    logging.info("Detailed Summary:")
    for i, sentence in enumerate(selected_sentences):
        importance_score = sentence_scores[sentence]
        logging.info(f"{i + 1}. {sentence.text} (Importance Score: {importance_score:.4f})")

    overall_summary = " ".join(sentence.text for sentence in selected_sentences)
    logging.info(f"Overall Summary:\n{overall_summary}" + "\n")

    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Summary finished. Duration: {duration:.2f} seconds.\n")
