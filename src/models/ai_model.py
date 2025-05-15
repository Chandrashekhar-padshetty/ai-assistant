from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from difflib import SequenceMatcher

class AIModel:
    def __init__(self, model_name="distilbert-base-uncased-distilled-squad"):
        """
        Initialize the AI model by loading a pre-trained transformer model
        and its tokenizer from Hugging Face.
        """
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
        self.model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

    def predict(self, question, context="This is a sample context for testing."):
        """
        Predict the answer to a question based on the given context.
        :param question: The question to answer.
        :param context: The context in which to find the answer.
        :return: The predicted answer as a string.
        """
        print(f"Question: {question}")
        print(f"Context: {context}")

        # Tokenize the input
        inputs = self.tokenizer(question, context, return_tensors="pt", truncation=True)
        print(f"Tokenized Inputs: {inputs}")

        # Get model outputs
        outputs = self.model(**inputs)
        print(f"Model Outputs: {outputs}")

        # Extract the start and end logits
        answer_start = outputs.start_logits.argmax()
        answer_end = outputs.end_logits.argmax()
        print(f"Answer Start: {answer_start}, Answer End: {answer_end}")

        # Decode the answer
        answer = self.tokenizer.decode(inputs["input_ids"][0][answer_start:answer_end + 1])
        print(f"Raw Predicted Answer: {answer}")

        # Validate the answer
        if answer.strip() == "":
            print("Invalid or empty answer detected.")
            return "The context does not contain a valid answer to the question."

        # Check for similarity with the context
        similarity_threshold = 0.6  # Adjust this threshold as needed
        similarity = SequenceMatcher(None, answer, context).ratio()
        print(f"Answer similarity with context: {similarity}")

        if similarity < similarity_threshold:
            print("Answer is not sufficiently similar to the context.")
            return "The context does not contain a valid answer to the question."

        # Confidence threshold (optional, can be tuned)
        start_confidence = outputs.start_logits[0, answer_start].item()
        end_confidence = outputs.end_logits[0, answer_end].item()
        print(f"Start Confidence: {start_confidence}, End Confidence: {end_confidence}")

        # Apply a stricter confidence threshold
        confidence_threshold = 5.0  # Example threshold, can be adjusted
        if start_confidence < confidence_threshold or end_confidence < confidence_threshold:
            print("Low confidence in the predicted answer.")
            return "The model is not confident enough in its answer. Please try rephrasing the question or providing more context."

        return answer