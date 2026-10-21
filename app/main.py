import json
from pathlib import Path

# Find the object root regardless of the terminal's working directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "data" / "clinic_faqs.json"

# Load the knowledge base and store it in memory
def load_knowledge_base():
    """Load FAQ documents from the JSON knowledge base."""
    with KNOWLEDGE_BASE_PATH.open() as file:
        documents = json.load(file)

    return documents

def search_faqs(query: str, documents: list[dict]) -> list[dict] : # -> list[dict] In Python, -> is the return type hint arrow. -> str means the function will return text (a string). • -> int means the function will return a whole number (an integer).
    """Search the knowledge base for documents that match the query."""
    query_words = set(query.lower().split()) # Convert the query to lowercase and split it into words
    results = [] # Initialize an empty list to store the search results

    for document in documents:
        searchable_text = (document["question"] + " " + document["answer"]).lower() # Convert the question and answer to lowercase and combine them into a single string

        document_words = set(searchable_text.split()) # Split the searchable text into words
        matching_words = query_words.intersection(document_words) # Find the words that match the query

        if matching_words: # If there are any matching words, add the document to the results
            results.append({
                "id": document["id"],
                "question": document["question"],
                "answer": document["answer"],
                "score": len(matching_words) # Calculate the score as the number of matching words
            })

        results.sort(key=lambda x: x["score"], reverse=True) # Sort the results by score in descending order

    return results

def main():
    documents = load_knowledge_base() # Load the knowledge base
    query = input("Ask the clinic assistant a question: ") # Get the user's query
    results = search_faqs(query, documents) # Search the knowledge base for documents that match the query

    if not results:
        return f"I couldn't find any relevant information from the knowledge base for your query."

    best_match = results[0]

    return f"Question: {best_match['question']}\nAnswer: {best_match['answer']}"

if __name__ == "__main__":
    print(main())