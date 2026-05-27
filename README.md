# teleqwen-bot
A simple chatbot on telegram using the smallest and dumbest llm

# roadmap

## [X] Fase 1: Configurazione dell'Ambiente
 * Crea una cartella di progetto:
   mkdir telegram-llm-bot && cd telegram-llm-bot

 * Crea un ambiente virtuale (consigliato):
   python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

 * Installa le dipendenze:
   pip install python-telegram-bot ollama pytest pytest-mock

 * Configura l'LLM:
   * Scarica e avvia Ollama.
   * Scarica il modello da terminale: ollama pull [model name]
     
## [X] Fase 2: Registrazione del Bot
 * Apri Telegram e cerca @BotFather.
 * Invia /newbot e scegli un nome e uno username per il bot.
 * Copia il Token API ricevuto. Lo useremo più avanti.

## [X] Fase 3: Esercizio TDD (Sviluppo Logica)
Iniziamo separando la logica dell'IA dal codice di Telegram.
### Step 3.1: Scrittura del primo test (test_logic.py)
Crea un file di test per definire cosa ti aspetti dalla funzione che interroga Qwen.

### Step 3.2: Implementazione della logica (logic.py)
Scrivi il codice minimo per far passare i test sopra.
Esegui i test con il comando: pytest

## [x] Fase 4: Implementazione del Bot Telegram
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

## [x] Fase 5: Verifica Finale e Deployment
 * Esegui un'ultima volta i test: Assicurati che tutto sia verde.
 * Avvia il bot: python bot.py
 * Test su Telegram: Invia un messaggio al tuo bot e osserva la velocità di risposta di Qwen 0.5B.

## [x] Fase 6: Dockerfile

- Build dell'immagine (il Dockerfile installa Ollama CLI e scarica il modello `qwen2.5:0.5b` durante la build):

```bash
docker build -t teleqwen-bot:latest .
```

- Eseguire il container passando la variabile d'ambiente `TELEGRAM_BOT_TOKEN`:

```bash
docker run --rm -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" teleqwen-bot:latest
```

Nota: l'immagine scaricherà il modello Ollama (`qwen2.5:0.5b`) durante la build.

## [-] Fase 7: Webhook
Predisporre il bot ad utilizzare i webhook e non stare sempre in polling, per futura implementazione su cloudrun o lambda
Da settare anche su telegram il webhook

```
https://api.telegram.org/bot<IL_TUO_TELEGRAM_TOKEN>/setWebhook?url=<IL_TUO_URL_PUBBLICO>/webhook
```

## [] Fase 8: Deployment su Cloud Run/lambda

L'app ora usa la modalità webhook: esporrà un endpoint POST in `/webhook/<TELEGRAM_BOT_TOKEN>`.
Imposta la variabile d'ambiente `WEBHOOK_BASE` nel formato `https://<service-url>` (es. l'URL fornito da Cloud Run) in modo che il container registri automaticamente il webhook con Telegram.

Esempio di deploy su Cloud Run (sostituisci `PROJECT_ID`, `REGION` e `SERVICE-URL`):

```bash
# Build & push con Cloud Build
gcloud builds submit --tag gcr.io/PROJECT_ID/teleqwen-bot

# Deploy su Cloud Run, impostando le env vars
gcloud run deploy teleqwen-bot \
  --image gcr.io/PROJECT_ID/teleqwen-bot \
  --region REGION \
  --platform managed \
  --set-env-vars TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN",WEBHOOK_BASE="https://SERVICE-URL" \
  --allow-unauthenticated
```

Dopo il deploy, Cloud Run fornirà l'URL pubblico: usa quel valore come `WEBHOOK_BASE`.

## [] Fase 9: Sviluppo Pipeline ci/cd con github action e terraform


