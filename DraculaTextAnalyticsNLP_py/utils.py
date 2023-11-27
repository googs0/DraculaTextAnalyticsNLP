
# Convert all text to lowercase keeping only alphanumeric and whitespace chars
# Split and join text into words with single spaces
def convert_cleaned_str(text):
    cleaned_text = ''.join(c.lower() if c.isalnum() or c.isspace() else ' ' for c in text)
    return ' '.join(cleaned_text.split())
