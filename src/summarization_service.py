import nltk
from rake_nltk import Rake
from transformers import pipeline
import os

# Download NLTK stopwords
nltk.download('stopwords')
nltk.download('punkt')

class Summarizer:
    def __init__(self, model_name="t5-small"):
        print(f"Loading summarization model: {model_name}...")
        # Use a lightweight pipeline for speed
        self.summarizer = pipeline("summarization", model=model_name, device=-1) # -1 for CPU
        self.rake = Rake()

    def extract_keywords(self, text, top_n=5):
        """
        Extracts keywords using RAKE.
        """
        self.rake.extract_keywords_from_text(text)
        keywords = self.rake.get_ranked_phrases()
        return keywords[:top_n]

    def generate_summary(self, text, max_length=60, min_length=20):
        """
        Generates a 1-2 sentence summary using a Transformer model.
        """
        if len(text.split()) < 20:
            return text  # Too short to summarize meaningfully
        
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Summarization error: {e}")
            return "Summary generation failed for this segment."

if __name__ == "__main__":
    # Test
    sample_segment = (
        "The economy is facing significant challenges as inflation continues to rise. "
        "The Federal Reserve is contemplating further interest rate hikes to stabilize the market. "
        "Experts suggest that these measures are necessary to prevent a long-term recession, "
        "although they acknowledge the immediate burden on consumers and small businesses."
    )
    
    gen = Summarizer()
    print("\nKeywords:", gen.extract_keywords(sample_segment))
    print("\nSummary:", gen.generate_summary(sample_segment))
