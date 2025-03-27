import ollama

def completion_with_chatgpt(text: str, model: str = "deepseek-r1:latest") -> str:
    """
    Generate a response using an Ollama DeepSeek model.
    
    Parameters:
        text (str): The input prompt.
        model (str): The Ollama model to use (default: "deepseek-r1:latest").
    
    Returns:
        str: The generated response.
    """
    response = ollama.chat(model=model, messages=[{"role": "user", "content": text}])
    return response["message"]["content"]
