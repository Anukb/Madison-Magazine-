from transformers import pipeline

def generate_summary(article_content):
    summarizer = pipeline('summarization')
    summary = summarizer(article_content, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']
