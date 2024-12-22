'''import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict

nltk.download('punkt')
nltk.download('stopwords')


nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)

    
    keywords = [word for word in word_tokens if word.isalpha() and word.lower() not in stop_words]
    return list(set(keywords))  
def summarize_text(text, keyword):
    sentences = sent_tokenize(text)
    
    
    for sentence in sentences:
        if keyword.lower() in sentence.lower():  
            return sentence.strip()  

    return ""  

def generate_flashcards(notes):
    keywords = extract_keywords(notes)
    flashcards = defaultdict(list)

    for keyword in keywords:
        
        explanation = summarize_text(notes, keyword)
        if explanation:
            flashcards[keyword].append(explanation)

    return flashcards

def format_flashcards(flashcards):
    formatted_flashcards = []
    for keyword, explanations in flashcards.items():
        
        question = f"What is {keyword}?"  
        
        answer = explanations[0] if explanations else "No answer available."

        
        formatted_flashcards.append(f"Q: {question}\nA: {answer}\n")
    
    return formatted_flashcards

if __name__ == "__main__":
    student_notes = """
    Augmented Reality (AR) is a technology that superimposes digital information and images onto the real
    world, a user's view of reality, using a device's camera and display.
    
    Characteristics of Augmented Reality Systems:
    1. 4. Registered in 3D: AR systems register virtual objects in 3D space, allowing users to view them from different angles.
    2. Privacy and security: AR systems can raise privacy and security concerns, such as tracking user
    location and behavior.
    """
    
    flashcards = generate_flashcards(student_notes)
    formatted_flashcards = format_flashcards(flashcards)

    # Display the generated flashcards
    for flashcard in formatted_flashcards:
        print(flashcard)
'''
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from collections import defaultdict
from joblib import Parallel, delayed

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def extract_keywords(text):
    """Extract keywords from text, excluding stopwords."""
    stop_words = set(stopwords.words("english"))
    nlp = spacy.load("en_core_web_sm")  # Load SpaCy model locally in the function
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if token.is_alpha and token.text.lower() not in stop_words]
    return list(set(keywords))

def summarize_text(text, keyword):
    """Summarize text by finding the most relevant sentence for a given keyword."""
    sentences = sent_tokenize(text)
    nlp = spacy.load("en_core_web_sm")  # Load SpaCy model locally in the function
    keyword_doc = nlp(keyword)
    scored_sentences = [(nlp(sentence).similarity(keyword_doc), sentence) for sentence in sentences]
    best_sentence = max(scored_sentences, key=lambda x: x[0])[1] if scored_sentences else ""
    return best_sentence.strip()

def generate_flashcards(notes):
    """
    Generate flashcards from the given notes.
    - Each flashcard consists of a keyword and an explanation.
    - Adjusts questions to be contextually relevant based on the explanation.
    """
    flashcards = {}
    
    # Example logic to parse notes into keywords and explanations
    lines = notes.split("\n")
    for line in lines:
        if ":" in line:
            keyword, explanation = line.split(":", 1)
            keyword = keyword.strip()
            explanation = explanation.strip()

            # Adjust the question if explanation starts with a keyword
            if "determines" in explanation.lower() or "is" in explanation.lower():
                question_keyword = explanation.split(":")[0] if ":" in explanation else explanation.split()[0]
                flashcards[f"What is {question_keyword.strip()}?"] = explanation
            else:
                flashcards[f"What is {keyword}?"] = explanation
    
    return flashcards
def generate_flashcards_chunk(chunk):
    """
    Process a chunk of notes to generate flashcards.
    """
    flashcards = {}
    for line in chunk:
        if ":" in line:
            keyword, explanation = line.split(":", 1)
            flashcards[keyword.strip()] = explanation.strip()
    return flashcards

from joblib import Parallel, delayed

def generate_flashcards(notes):
    """
    Generate flashcards from the input notes.
    """
    # Split notes into lines
    lines = notes.splitlines()
    
    # Chunk the data for parallel processing
    chunk_size = max(1, len(lines) // 4)  # Divide into 4 chunks
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    
    # Use joblib for parallel processing
    flashcards_list = Parallel(n_jobs=-1)(
        delayed(generate_flashcards_chunk)(chunk) for chunk in chunks
    )
    
    # Combine the results from all chunks
    flashcards = {}
    for flashcard_chunk in flashcards_list:
        flashcards.update(flashcard_chunk)
    
    return flashcards

def format_flashcards(flashcards):
    """Format flashcards for display."""
    formatted_flashcards = []
    for keyword, explanations in flashcards.items():
        question = f"What is {keyword}?"
        answer = " ".join(explanations) if explanations else "No answer available."
        formatted_flashcards.append(f"Q: {question}\nA: {answer}\n")
    return formatted_flashcards

if __name__ == "__main__":
    student_notes = """
    Augmented Reality (AR) is a technology that superimposes digital information and images onto the real
    world, a user's view of reality, using a device's camera and display.

    Characteristics of Augmented Reality Systems:
    1. Registered in 3D: AR systems register virtual objects in 3D space, allowing users to view them from different angles.
    2. Privacy and security: AR systems can raise privacy and security concerns, such as tracking user
    location and behavior.
    """

    # Generate flashcards
    flashcards = generate_flashcards(student_notes)

    # Format flashcards for display
    formatted_flashcards = format_flashcards(flashcards)

    # Display the generated flashcards
    for flashcard in formatted_flashcards:
        print(flashcard)
