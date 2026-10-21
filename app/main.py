import json
import re # regex
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent # root of the project
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "data" / "clinic_faqs.json"

# common words that usually contribute little to the meaning of the question
STOP_WORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were",
    "do", "does", "did", "i", "you", "we", "they", "he",
    "she", "it", "who", "what", "where", "when", "why",
    "how", "can", "could", "would", "should", "please",
    "me", "my", "your", "our", "to", "of", "for", "in",
    "on", "at", "and", "or", "be", "have", "has", "had",
    "tell", "about", "offer"
}

def tokenize(text: str) -> set[str]: # returns a set of tokens from the text string
    """Convert text into lowercase words and remove common words."""
    words = re.findall(r"\b[a-z0-9]+\b", text.lower()) # this line finds all the words in the text that are alphanumeric and returns them as a list
    return {word for word in words if word not in STOP_WORDS} # this line removes the common words from the list

def load_knowledge_base() -> list[dict]: # -> list[dict] is the return type of the function meaning, "->"  the function will return something that is a list of dictionaries
    """Load FAQ documents from the JSON knowledge base."""
    with KNOWLEDGE_BASE_PATH.open("r", encoding="utf-8") as file: # this line opens the knowledge base file
        return json.load(file) # this line loads the knowledge base file into a list of dictionaries

def search_faqs(query: str, documents: list[dict]) -> list[dict]: # -> list[dict] is the return type of the function meaning, "->"  the function will return something that is a list of dictionaries
    """Rank FAQ documents by keyword overlap with the query."""
    query_words = tokenize(query) # this line tokenizes the query into a set of words

    if not query_words:
        return [] # if the query is empty, return an empty list

    results = [] # this line creates an empty list to store the results

    for document in documents:
        question_words = tokenize(document["question"]) # this line tokenizes the question into a set of words
        answer_words = tokenize(document["answer"]) # this line tokenizes the answer into a set of words

        # Question matches are more important than answer-only matches.
        question_matches = query_words & question_words # this line finds the words in the query that are also in the question
        answer_matches = query_words & (answer_words - question_words) # this line finds the words in the query that are also in the answer

        score = (
            2 * len(question_matches) # this line multiplies the number of question matches by 2
            + len(answer_matches) # this line adds the number of answer matches
        ) / (2 * len(query_words)) # this line divides the total score by the number of query words

        if score > 0.40:
            results.append({
                "id": document["id"],
                "question": document["question"],
                "answer": document["answer"],
                "score": round(score, 2) # this line rounds the score to 2 decimal places, meaning that it will be displayed as 0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10
            })

    results.sort(key=lambda item: item["score"], reverse=True) # this line sorts the results by score in descending order

    return results

def main():
    documents = load_knowledge_base() # this line loads the knowledge base into a list of dictionaries
    query = input("Ask the clinic assistant a question: ") # this line asks the user to enter a question

    results = search_faqs(query, documents) # this line searches the knowledge base for the query and returns the results

    if not results:
        return f"I couldn't find any relavent information for your question."

    best_match = results[0] # this line gets the first result

    return f"Question: {best_match['question']}\nAnswer: {best_match['answer']}\nScore: {best_match['score']}" # this line returns the best match


if __name__ == "__main__":
    print(main())

    # SCORE FORMULAE IN ALGORITHM = 
    # Score = 2Q + A / 2N

    # Q = number of matching words in the FAQ question.
    # A = number of matching words in the FAQ answer.
    # N = number of meaningful words in the user's query.