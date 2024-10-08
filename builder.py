from customtkinter import *
import os
import threading
import google.generativeai as genai
import discord
from discord.ext import commands

def main():
    def build():
        API = api.get()
        TOKEN = token.get()

        if not API or not TOKEN:
            print("API key or Token is missing")
            return
    
        os.environ['DISCORD_BOT_TOKEN'] = TOKEN
        os.environ['GEMINI_API_KEY'] = API

        with open("Bot.py", "w") as e:
            e.write(f"""
import os
import google.generativeai as genai
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
Bot = commands.Bot(command_prefix="!", intents=intents)

token = os.getenv('DISCORD_BOT_TOKEN')
api_key = os.getenv('GEMINI_API_KEY')

def mains():
    @Bot.event
    async def on_ready():
        await Bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Streaming(name='vscode', url="https://github.com/SStorm21"))
        print("Bot is Online \\n -------------------")

    @Bot.command()
    async def i(ctx, *, input_):
        try:
            genai.configure(api_key=api_key)
            generation_config = {{
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }}
            model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(input_)
            await ctx.send(response.text)
        except Exception as e:
            await ctx.send(f"Error: {{str(e)}}")
    
    Bot.run(token)
""")
        threading.Thread(target=run_bot).start()

    def run_bot():
        import Bot 
        Bot.mains()


    window = CTk()
    window.configure(bg_color="black")
    window.geometry("300x400")
    window.resizable(0, 0)
    window.title("SCWG-1.0")
    
    logo = CTkLabel(window, text="Simple ChatBot\nwith Gemini", font=("bold", 33))
    logo2 = CTkLabel(window, text="@StormShell", font=("bold", 12))
    logo3 = CTkLabel(window, text="prefix is !i", font=("bold", 20))

    token = CTkEntry(window, placeholder_text="Bot token..", width=200)
    api = CTkEntry(window, placeholder_text="Gemini API key..", width=200)
    start = CTkButton(window, text="Run", command=build)
    
    logo.pack(side="top")
    logo2.pack(side="bottom")
    logo3.pack(side="bottom")
    token.place(x=50, y=150)
    api.place(x=50, y=180)
    start.pack(side='bottom', pady=49)
    
    window.mainloop()

main()
