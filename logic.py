import ollama

def get_ai_response(text):
    if not text.strip():
        return "Messaggio vuoto."
    response = ollama.chat(model='qwen2.5:0.5b', messages=[
        {'role': 'system', 'content': 'Short and concise answers. If you do not know the answer, say "I don\'t know".'},
        {'role': 'user', 'content': text},
    ])
    return response['message']['content']