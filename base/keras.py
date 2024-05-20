from transformers import pipeline

def Text_sum():
    return pipeline("summarization", model="facebook/bart-large-cnn")