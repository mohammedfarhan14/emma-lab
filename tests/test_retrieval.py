
import unittest

from app.main import search_faqs, tokenize


SAMPLE_DOCUMENTS = [
    {
        "id": 1,
        "question": "What are the clinic opening hours?",
        "answer": "The clinic is open Monday to Friday, from 9:00 AM to 5:00 PM.",
        "category": "opening_hours",
    },
    {
        "id": 2,
        "question": "How can I book an appointment?",
        "answer": "You can request an appointment by calling the clinic during its opening hours.",
        "category": "appointments",
    },
    {
        "id": 5,
        "question": "How can I request a repeat prescription?",
        "answer": "Please submit your repeat prescription request through the clinic's approved prescription request process.",
        "category": "prescriptions",
    },
]


class TestRetrieval(unittest.TestCase):

    def test_tokenize_removes_common_words(self):
        self.assertEqual(
            tokenize("How can I book an appointment?"),
            {"book", "appointment"},
        )

    def test_finds_opening_hours(self):
        results = search_faqs(
            "What are the clinic opening hours?",
            SAMPLE_DOCUMENTS,
        )
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], 1)

    def test_finds_appointment(self):
        results = search_faqs(
            "How can I book an appointment?",
            SAMPLE_DOCUMENTS,
        )
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], 2)

    def test_finds_repeat_prescription(self):
        results = search_faqs(
            "How do I request a repeat prescription?",
            SAMPLE_DOCUMENTS,
        )
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], 5)

    def test_rejects_unrelated_question(self):
        results = search_faqs(
            "Does the clinic offer dental surgery?",
            SAMPLE_DOCUMENTS,
        )
        self.assertEqual(results, [])

    def test_rejects_stop_word_only_query(self):
        results = search_faqs("Who are you?", SAMPLE_DOCUMENTS)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
