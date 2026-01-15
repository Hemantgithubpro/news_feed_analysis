import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Any, List

class NLPEngine:
    def __init__(self):
        print("Loading NLP models...")
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        print("NLP models loaded.")

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Perform Sentiment Analysis and Named Entity Recognition.
        """
        # Sentiment Analysis
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        sentiment_score = sentiment_scores['compound']
        
        if sentiment_score >= 0.05:
            sentiment_label = "POSITIVE"
        elif sentiment_score <= -0.05:
            sentiment_label = "NEGATIVE"
        else:
            sentiment_label = "NEUTRAL"

        # Entity Recognition
        doc = self.nlp(text)
        entities = []
        seen_entities = set()
        
        for ent in doc.ents:
            if ent.text not in seen_entities and ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT", "EVENT"]:
                entities.append({"text": ent.text, "label": ent.label_})
                seen_entities.add(ent.text)

        # Keyword Extraction (Simple Frequency based for now, or use spaCy noun chunks)
        # Using noun chunks as simple keywords
        keywords = list(set([chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]))[:10]

        return {
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
            "entities": entities,
            "keywords": keywords
        }

nlp_engine = NLPEngine()
