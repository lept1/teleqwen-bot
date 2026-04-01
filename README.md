# teleqwen-bot
A simple chatbot on telegram using the smallest and dumbest llm

# roadmap

## Fase 1: Configurazione dell'Ambiente
 * Crea una cartella di progetto:
   mkdir telegram-llm-bot && cd telegram-llm-bot

 * Crea un ambiente virtuale (consigliato):
   python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

 * Installa le dipendenze:
   pip install python-telegram-bot ollama pytest pytest-mock

 * Configura l'LLM:
   * Scarica e avvia Ollama.
   * Scarica il modello da terminale: ollama pull qwen2.5:0.5b
     
## Fase 2: Registrazione del Bot
 * Apri Telegram e cerca @BotFather.
 * Invia /newbot e scegli un nome e uno username per il bot.
 * Copia il Token API ricevuto. Lo useremo più avanti.

## Fase 3: Esercizio TDD (Sviluppo Logica)
Iniziamo separando la logica dell'IA dal codice di Telegram.
### Step 3.1: Scrittura del primo test (test_logic.py)
Crea un file di test per definire cosa ti aspetti dalla funzione che interroga Qwen.
```
import pytest
from logic import get_ai_response

def test_get_ai_response_valid_input(mocker):
    # Mockiamo la chiamata a Ollama per non dipendere dal modello nei test
    mock_ollama = mocker.patch('ollama.chat')
    mock_ollama.return_value = {'message': {'content': 'Ciao, come posso aiutarti?'}}
    
    res = get_ai_response("Ciao")
    assert res == "Ciao, come posso aiutarti?"

def test_get_ai_response_empty_input():
    # Testiamo un caso limite senza mock
    res = get_ai_response("")
    assert res == "Messaggio vuoto."
```

### Step 3.2: Implementazione della logica (logic.py)
Scrivi il codice minimo per far passare i test sopra.
```
import ollama

def get_ai_response(text):
    if not text.strip():
        return "Messaggio vuoto."
    
    response = ollama.chat(model='qwen2.5:0.5b', messages=[
        {'role': 'system', 'content': 'Rispondi in modo conciso e in italiano.'},
        {'role': 'user', 'content': text},
    ])
    return response['message']['content']
```
Esegui i test con il comando: pytest

## Fase 4: Implementazione del Bot Telegram
Crea il file principale bot.py che utilizzerà la logica testata nella Fase 3.
 * Crea bot.py:
```
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from logic import get_ai_response

TOKEN = 'IL_TUO_TOKEN_QUI'

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Mostra lo stato "sta scrivendo..."
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Usa la logica testata
    answer = get_ai_response(user_text)
    
    await update.message.reply_text(answer)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Bot in ascolto...")
    app.run_polling()
```

## Fase 5: Verifica Finale e Deployment
 * Esegui un'ultima volta i test: Assicurati che tutto sia verde.
 * Avvia il bot: python bot.py
 * Test su Telegram: Invia un messaggio al tuo bot e osserva la velocità di risposta di Qwen 0.5B.

## Suggerimenti extra per Qwen 0.5B:
 * Prompt Injection: Se il bot risponde in inglese, prova ad appesantire il system content in logic.py forzando l'italiano con un tono imperativo.
 * Timeout: Ollama è locale, quindi la latenza è minima, ma se il tuo PC è sotto sforzo, potresti aggiungere una gestione dei timeout nel file logic.py.
