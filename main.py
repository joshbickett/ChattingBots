import os
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, button_dialog
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.shortcuts import button_dialog
from colorama import Fore, Style as ColoramaStyle

import openai

openai.api_key = os.environ.get('OPENAI_KEY')

def api_call(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7
    )
    return response

# your functions and code here

def start_conversation(system_1, system_2, initial_message):
    print("starting conversation")

    system_1_initial = {"role": "user", "content": initial_message}
    system_2_initial = {"role": "assistant", "content": initial_message}

    bot_1_conversation = [system_1, system_1_initial]
    bot_2_conversation = [system_2, system_2_initial]

    bot_1_name = system_1["content"].split(".")[0][8:]
    bot_2_name = system_2["content"].split(".")[0][8:]

    print(Fore.YELLOW + f"{bot_2_name}: " + initial_message + ColoramaStyle.RESET_ALL + "\n")

    for i in range(10):
        bot_1_response = api_call(bot_1_conversation)
        if bot_1_response is None or "choices" not in bot_1_response:
            print("Error with bot 1 api_call")
            break

        bot_1_response = bot_1_response["choices"][0]["message"]["content"]
        print(Fore.CYAN + f"{bot_1_name}: " + bot_1_response + ColoramaStyle.RESET_ALL + "\n")

        guest_response_s = {"role": "user", "content": bot_1_response}
        guest_response_g = {"role": "assistant", "content": bot_1_response}

        bot_2_conversation = bot_2_conversation[-8:] + [guest_response_s]  # keep only the last 8 messages to make room for 2 new ones

        bot_2_response = api_call(bot_2_conversation)
        if bot_2_response is None or "choices" not in bot_2_response:
            print("Error with bot 2 api_call")
            break

        bot_2_response = bot_2_response["choices"][0]["message"]["content"]
        print(Fore.GREEN + f"{bot_2_name}: " + bot_2_response + ColoramaStyle.RESET_ALL + "\n")

        server_response_g = {"role": "user", "content": bot_2_response}
        server_response_s = {"role": "assistant", "content": bot_2_response}

        bot_1_conversation = bot_1_conversation[-8:] + [guest_response_g, server_response_g]  # keep only the last 8 messages to make room for 2 new ones
        bot_2_conversation = bot_2_conversation + [server_response_s]  # Add the bot 2's response to the bot 2 conversation

        # stop condition
        if 'bye' in bot_1_response.lower():
            print('Someone said bye')
            break    
        # Add pause and check for continuation every 10th message
        if (i+1) % 5 == 0:
            user_continue = button_dialog(
                title='Continue conversation',
                text='Do you want to continue the conversation?',
                buttons=[
                    ('Yes', True),
                    ('No', False),
                ],
                style=style
            ).run()
            
            if not user_continue:
                print('Conversation ended by user.')
                break


# Define style
style = PromptStyle.from_dict({
    'dialog': 'bg:#88ff88',
    'button': 'bg:#ffffff #000000',
    'dialog.body': 'bg:#44cc44 #ffffff',
    'dialog shadow': 'bg:#003800',
})


def main():
    message_dialog(
        title='Chatting Bots',
        text='Have AIs talk about any topic you want.',
        style=style
    ).run()

    os.system('clear')  # Clears the terminal screen

    bot_1_name = prompt('Enter a name for bot 1: ')
    bot_1_detail = prompt(f'Describe {bot_1_name} (optional): ')
    bot_1 = { "role": "system", "content": f"You are {bot_1_name}. {bot_1_detail}. Get into your role as much as possible. Your goal is to engage in the conversation. Don't forget to ask who you're talking to if they don't mention it. If you don't have a name, you can just share a little about yourself. Try to keep your responses short, but engaging."}

    bot_2_name = prompt('Enter a name for bot 2: ')
    bot_2_detail = prompt(f'Describe {bot_2_name} (optional): ')
    bot_2 = { "role": "system", "content": f"You are {bot_2_name}. {bot_2_detail}. Get into your role as much as possible. Your goal is to engage in the conversation. Don't forget to ask who you're talking to if they don't mention it. If you don't have a name, you can just share a little about yourself. Try to keep your responses short, but engaging."}

    os.system('clear')  # Clears the terminal screen

    initial_message = prompt(f'Enter the initial message from {bot_2_name}:')

    # Now use the provided initial message
    start_conversation(bot_1, bot_2, initial_message)


if __name__ == "__main__":
    main()