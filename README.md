#Calorie Calculator

Telegram bot to calculate calories based on python-telegram-botlibrary and google cloud function.

Keywords: ConversationHandler, Webhook, google-cloud-funciton, python, telegram, bot


Deployment:

`gcloud functions deploy md_bot_calc --source=. --set-env-vars "TELEGRAM_TOKEN=<token>" --runtime python37 --trigger-http --project=<gcf-project>`

Webhook setup:

`curl "https://api.telegram.org/bot<token>/setWebhook?url=https://us-central1-<gcf-project>.cloudfunctions.net/md_bot_calc"`

