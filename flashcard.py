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

    keywords = [word for word in word_tokens if word.isalnum() and word.lower() not in stop_words]
    return keywords

def summarize_text(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    summary = sentences[0] + " " + sentences[-1] if len(sentences) > 1 else sentences[0]
    return summary

def generate_flashcards(notes):
    keywords = extract_keywords(notes)
    flashcards = defaultdict(list)

    for keyword in keywords:
        keyword_sentences = [sent for sent in sent_tokenize(notes) if keyword in sent]
        explanation = summarize_text(" ".join(keyword_sentences))

        flashcards[explanation].append(keyword)

    return flashcards

def format_flashcards(flashcards):
    formatted_flashcards = []
    for answer, questions in flashcards.items():
        formatted_flashcards.append(f"Q: {', '.join(questions)}\nA: {answer}\n")
    return formatted_flashcards

if __name__ == "__main__":
    student_notes = """
    Your example text goes here.
    """
    
    flashcards = generate_flashcards(student_notes)
    formatted_flashcards = format_flashcards(flashcards)

    # Display the generated flashcards
    for flashcard in formatted_flashcards:
        print(flashcard)
'''
'''
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load the SpaCy language model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)

    # Keep words that are alphanumeric and not in stopwords
    keywords = [word for word in word_tokens if word.isalpha() and word.lower() not in stop_words]
    return list(set(keywords))  # Remove duplicates

def summarize_text(text, keyword):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    # Find a relevant sentence for the keyword
    for sent in sentences:
        if keyword.lower() in sent.lower():  # Ensure case-insensitivity
            return sent.strip()  # Return the first relevant sentence

    return ""  # Return an empty string if no sentence is found

def generate_flashcards(notes):
    keywords = extract_keywords(notes)
    flashcards = defaultdict(list)

    for keyword in keywords:
        # Get the relevant sentence for the keyword
        explanation = summarize_text(notes, keyword)
        if explanation:
            flashcards[explanation].append(keyword)

    return flashcards

def format_flashcards(flashcards):
    formatted_flashcards = []
    for answer, questions in flashcards.items():
        # Ensure no keyword in the answer repeats itself
        unique_questions = [q for q in questions if q.lower() not in answer.lower()]
        unique_questions = list(set(unique_questions))  # Remove duplicates
        
        # Generate a concise answer
        concise_answer = answer.replace(",","").replace(".", "").replace("(", "").replace(")", "").split()
        concise_answer = list(set(concise_answer))  # Remove duplicates from the answer
        concise_answer = " ".join(word for word in concise_answer if word not in unique_questions)  # Remove keywords

        if unique_questions and concise_answer:  # Only add if there are unique questions and a concise answer
            formatted_flashcards.append(f"Q: {', '.join(unique_questions)}\nA: {concise_answer}\n")
    
    return formatted_flashcards

if __name__ == "__main__":
    student_notes = """
    Natural Language Processing (NLP) is a field of artificial intelligence (AI) that focuses on the interaction between computers and humans through natural language. Its primary goal is to enable computers to understand, interpret, and generate human language in a way that is both meaningful and useful.
    Key Components of NLP:
    1. Text Understanding: NLP involves tasks such as parsing, part-of-speech tagging, named entity recognition (NER), syntactic and semantic analysis to understand the structure and meaning of text.
    2. Language Generation: This includes tasks like text summarization, machine translation, and dialogue systems where the computer generates human-like text.
    3. Information Retrieval: NLP helps in retrieving relevant information from large collections of text, such as search engines or question-answering systems.
    4. Sentiment Analysis: Determines the sentiment or opinion expressed in a piece of text, whether it's positive, negative, or neutral.
    5. Speech Recognition: Converts spoken language into text, enabling applications like voice assistants and dictation software.
    6. Language Modeling: Involves predicting the next word in a sentence or generating coherent text based on a given input.
    Applications of NLP:
    • Chatbots and Virtual Assistants: NLP powers the conversational abilities of chatbots like Siri, Alexa, and Google Assistant, enabling them to understand and respond to user queries.
    • Machine Translation: Facilitates instant translation between languages, such as Google Translate, making global communication more accessible.
    • Text Summarization: Automatically generates concise summaries of longer texts, useful for quickly digesting large volumes of information.
    Challenges in NLP:
    • Ambiguity: Natural language is often ambiguous, and the same sentence can have multiple interpretations.
    Recent Advances:
    • Transformer Models: Models like BERT (Bidirectional Encoder Representations from Transformers) have significantly advanced various NLP tasks by capturing contextual information effectively.
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
