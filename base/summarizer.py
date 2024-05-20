from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from .keras import Text_sum

# Load pre-trained model
model = load_model(r'model.h5')

# Load tokenizer 
tokenizer = Tokenizer()  # Use your own tokenizer if available

# def summarize(scrapeArticles):
#     # Preprocess input text
#     #  Tokenization and padding
#     sequences = tokenizer.texts_to_sequences([scrapeArticles])
#     padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

#     # Generate summary
#     summary = model.predict(padded_sequences)

#     return summary

# # Example usage
# input_text = "Your input text goes here."
# summary = summarize_text(scrapeArticles)
# print("Summary:", summary)





# def summarize(scrapeArticles):
#     summarizeText = Text_sum()
#     finalText = summarizeText(scrapeArticles, max_length=400, min_length=30, do_sample=False)
#     return finalText

def summarize(scrapeArticles):
    max_length = 400  # Maximum length for summarization
    min_length = 100   # Minimum length for summarization

    if len(scrapeArticles) <= max_length:
        # If the length of scrapeArticles is within the max length, summarize directly
        summarizeText = Text_sum()
        finalText = summarizeText(scrapeArticles, max_length=max_length, min_length=min_length, do_sample=False)
    else:
        # If the length exceeds max length, slice the text and summarize
        sliced_text = scrapeArticles[:max_length]
        summarizeText = Text_sum()
        finalText = summarizeText(sliced_text, max_length=max_length, min_length=min_length, do_sample=False)
    
    return finalText
