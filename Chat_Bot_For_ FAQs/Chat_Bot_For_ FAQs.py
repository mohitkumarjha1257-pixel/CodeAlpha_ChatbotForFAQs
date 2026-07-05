import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ssl

# =====================================================================
# macOS SSL Certificate Bypass 
# Fixes [SSL: CERTIFICATE_VERIFY_FAILED] errors during NLTK downloads
# =====================================================================
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# =====================================================================
# Download required NLTK data packages
# =====================================================================
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True) 

# =====================================================================
# 1. Collect FAQs (Questions and Answers)
# =====================================================================
faqs = {
    "What are your working hours?": "We are open from 9 AM to 5 PM, Monday to Friday.",
    "How can I reset my password?": "You can reset your password by clicking on 'Forgot Password' on the login screen.",
    "Do you offer refunds?": "Yes, we offer a 30-day money-back guarantee on all our products.",
    "How do I contact support?": "You can contact support via email at support@codealpha.tech.",
    "Where is the company located?": "CodeAlpha is a leading software development company, operating remotely and globally."
}

questions = list(faqs.keys())
answers = list(faqs.values())

# =====================================================================
# 2. Preprocess the Text
# =====================================================================
lemmatizer = nltk.stem.WordNetLemmatizer()

def preprocess(text):
    """Tokenizes and lemmatizes the input text."""
    tokens = nltk.word_tokenize(text.lower())
    return " ".join([lemmatizer.lemmatize(token) for token in tokens])

# Preprocess all FAQ questions for the model
preprocessed_questions = [preprocess(q) for q in questions]

# Create TF-IDF vectors from the preprocessed questions
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(preprocessed_questions)

# =====================================================================
# 3. Match User Questions using Cosine Similarity
# =====================================================================
def get_best_response(user_query):
    """Finds the most similar FAQ using cosine similarity."""
    preprocessed_query = preprocess(user_query)
    query_vector = vectorizer.transform([preprocessed_query])
    
    similarities = cosine_similarity(query_vector, faq_vectors)
    best_match_idx = np.argmax(similarities)
    
    # Threshold check: ensures the bot doesn't answer unrelated questions
    if similarities[0][best_match_idx] > 0.2:
        return answers[best_match_idx]
    else:
        return "I'm sorry, I don't quite understand. Could you try rephrasing your question?"

# =====================================================================
# 4. Command-Line Chat UI
# =====================================================================
def chat():
    """Initializes the chat interface."""
    print("\n" + "="*50)
    print("🤖 CodeAlpha FAQ Chatbot Initialized")
    print("Type 'quit' or 'exit' to stop the chat.")
    print("="*50 + "\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Bot: Goodbye! Good luck with your CodeAlpha projects.")
            break
            
        response = get_best_response(user_input)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    chat()