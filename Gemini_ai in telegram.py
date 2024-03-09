import telebot
import google.generativeai as genai

# Replace with your Telegram bot token 
bot_token = "YOUR_BOT_TOKEN
bot = telebot.TeleBot(bot_token)

# Replace with your Gemini API key (essential for actual Gemini integration)
gemini_api_key = "YOUR_GEMINI_API_KEY"


def generate_response(text):
    """
    Generates a response using the Gemini API or a fallback mechanism.

    Args:
        text (str): The user's input message.

    Returns:
        str: The generated response from Gemini or a placeholder message.
    """

    try:
        # Configure Gemini API (if secret key is available)
        genai.configure(api_key=gemini_api_key)

        generation_config = {
            "temperature": 0.5,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2059,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        convo = model.start_chat(history=[])
        convo.send_message(text)
        output = convo.last.text

        return output

    except (KeyError, ConnectionError):  # Handle missing API key or connection errors
        return "Sorry, I'm unable to access the connect right now. Try again! and check your internet connection"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I'm a Gemini AI bot. I can have text-to-text conversations like ChatGPT.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    response = generate_response(text)
    bot.reply_to(message, response)


bot.polling()
