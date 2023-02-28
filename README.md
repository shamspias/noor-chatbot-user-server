# Noor Chatbot Backend System
This is a chatbot backend system built using Python and Django, with the Django REST framework for API development. It uses Celery as a task queue for asynchronous processing.

## Installation
To install this chatbot backend system, simply clone the repository and install the necessary dependencies:
```
git clone https://github.com/shamspias/noor-chatbot-user-server.git
cd chatbot-backend
pip install -r requirements.txt

```
## Configuration
Before you can use the chatbot backend system, you will need to configure it with your WhatsApp and/or Telegram API keys. Create a .env file in the root directory of the project and add the following variables:
```
WHATSAPP_API_KEY=your_whatsapp_api_key
TELEGRAM_API_KEY=your_telegram_api_key
GPT3_API_KEY=your_gpt3_api_key

```
You will also need to configure your Celery settings in the settings.py file.

## Usage
To start the chatbot backend system, run the following command:
```
python manage.py runserver

```
This will start the Django development server on port 8000. You can then use the API endpoints to interact with the chatbot system.

## API Endpoints

- `/api/messages/`: This endpoint allows you to send and receive messages from the chatbot. You can send messages using the POST method, and receive messages using the GET method.

- `/api/media/`: This endpoint allows you to upload media files to the chatbot system. You can upload media files using the POST method.

- `/api/subscribers/`: This endpoint allows you to manage your list of subscribers. You can add subscribers using the POST method, and retrieve and update subscribers using the GET and PUT methods, respectively.