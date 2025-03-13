from transformers import pipeline

# Initialize the Hugging Face pipeline for text generation
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

def completion_with_chatgpt(text: str, model: str = "EleutherAI/gpt-neo-1.3B") -> str:
    # Generate a response using the Hugging Face model
    response = generator(
        text,
        max_new_tokens=2024,  # Increase tokens
        num_return_sequences=1,
        temperature=0.7,  # Balance randomness & coherence
        top_p=0.9,  # Helps avoid extreme randomness
        return_full_text=True  # Ensures the full response is returned
    )
    return response[0]["generated_text"]
