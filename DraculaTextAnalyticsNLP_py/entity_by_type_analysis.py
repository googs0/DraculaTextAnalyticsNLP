from imports import logging, time, re


def analyze_entities_by_type(doc):
    logging.info("Initiating Entities by Type")
    start_time = time.time()

    # Initialize dictionary to store named entities by type
    named_entities = {"PERSON": set(), "GPE": set(), "ORG": set(), "DATE": set(), "TIME": set(), "CARDINAL": set(),
                      "MONEY": set()}

    filtered_entities = []

    for ent in doc.ents:
        ent_text = ent.text.lower()
        ent_label = ent.label_

        # Find the entity context
        start_context = max(0, ent.start - 4)
        end_context = min(len(doc), ent.end + 4)
        entity_context = " ".join([token.text for token in doc[start_context:end_context]])

        # Filtering criteria
        if ent_label in named_entities:
            ent_text_without_chapter = ent_text.replace('chapter', '').strip()
            ent_text_possessive = move_lone_s_in_entity(ent_text_without_chapter)
            ent_text_am_pm = concat_am_pm(ent_text_possessive)
            ent_text_modified = replace_space_with_colon(ent_text_am_pm)

            if ent_text_modified.endswith(" am") or ent_text_modified.endswith(" pm"):
                ent_label = 'TIME'

            filtered_entities.append((ent_text_modified, ent_label, entity_context))

    for ent_text, ent_label, entity_context in filtered_entities:
        logging.info(
            f"{ent_text}, Label: {ent_label}, (Context: {entity_context})"
        )

    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Entities by Type finished. Duration: {duration:.2f} seconds.\n")

    return named_entities


def move_lone_s_in_entity(entity_text):
    entity_text = entity_text.strip()

    if entity_text.endswith(" s"):
        last_s_index = entity_text.rfind("s")

        # Replace the last ' s' with " 's " and shift to the word directly to the left
        entity_text = entity_text[:last_s_index - 1] + "'s " + entity_text[last_s_index + 1:]

    if " s " in entity_text:
        last_s_index = entity_text.rfind(" ")
        entity_text = entity_text[:last_s_index - 1] + "'s " + entity_text[last_s_index + 1:]

    return entity_text


def concat_am_pm(entity_text):
    entity_text = entity_text.strip()

    if entity_text.endswith(" a m") or entity_text.endswith(" p m"):
        # Find the index of the last space before 'am' or 'pm'
        last_space_index = entity_text.rfind(" ")

        # Concatenate 'am' or 'pm' 
        entity_text = entity_text[:last_space_index] + entity_text[last_space_index + 1:]

    return entity_text


def replace_space_with_colon(entity_text):
    # Regular expression pattern for am/pm time (i.e "6 46 pm" -> "6:46 pm")
    pattern = r'(\d) (\d)(\d)'

    # Check if the pattern is present in the entity text
    if re.search(pattern, entity_text):
        # Replace the space with ":"
        entity_text = re.sub(r'(\d) (\d)(\d)', r'\1:\2\3', entity_text)

    return entity_text
