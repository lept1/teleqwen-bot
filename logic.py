import ollama

def get_ai_response(text):
    if not text.strip():
        return "Messaggio vuoto."
    response = ollama.chat(model='qwen2.5:0.5b', messages=[
        {'role': 'system', 'content': 'Act as a learned scholar from the Elizabethan era. You must address the user with utmost courtesy, employing archaic vocabulary, historical idioms, and traditional pronouns (such as thou, thee, and thine). Maintain this vintage persona across all topics, no matter how modern the query.'},
        {'role': 'user', 'content': text},
    ])
    return response['message']['content']

if __name__ == '__main__':
    while True:
        user_input = input("Tu: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        ai_response = get_ai_response(user_input)
        print(f"AI: {ai_response}")