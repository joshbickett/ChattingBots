import os
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, button_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory
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

guest_system = { "role": "system", "content": "You are at a restaurant. You just saw the menu and the server just walked up and said hi."}
server_system = { "role": "system", "content": "You a server at a restaurant. Try to keep the conversation short and to the point so you can get to all your tables"}

def start_conversation(system_1, system_2, initial_message):
    print("starting conversation")

    
    print("server: ", initial_message)
    
    server_initial_g = { "role": "user", "content": initial_message }
    server_initial_s = { "role": "assistant", "content": initial_message}
    
    guest_conversation = [system_1, server_initial_g]
    server_conversation = [system_2, server_initial_s]


    for i in range(10):
        guest_r = api_call(guest_conversation)
        if guest_r is None or "choices" not in guest_r:
            print("Error with guest api_call")
            break

        guest_r = guest_r["choices"][0]["message"]["content"]
        print('sys 1: ', guest_r)

        guest_response_s = { "role": "user", "content": guest_r }
        guest_response_g = { "role": "assistant", "content": guest_r }

        server_conversation = server_conversation[-8:] + [guest_response_s]  # keep only the last 8 messages to make room for 2 new ones

        server_r = api_call(server_conversation)
        if server_r is None or "choices" not in server_r:
            print("Error with server api_call")
            break

        server_r = server_r["choices"][0]["message"]["content"]
        print("sys 2: ", server_r)

        server_response_g = { "role": "user", "content": server_r }
        server_response_s = { "role": "assistant", "content": server_r }

        guest_conversation = guest_conversation[-8:] + [guest_response_g, server_response_g]  # keep only the last 8 messages to make room for 2 new ones
        server_conversation = server_conversation + [server_response_s]  # Add the server's response to the server conversation
        
        # stop condition
        if 'order' in guest_r.lower():
            print('Guest made an order. Stopping the conversation.')
            break


# Define style
style = Style.from_dict({
    'dialog': 'bg:#88ff88',
    'button': 'bg:#ffffff #000000',
    'dialog.body': 'bg:#44cc44 #ffffff',
    'dialog shadow': 'bg:#003800',
})


def main():
    message_dialog(
        title='Restaurant Simulation',
        text='Welcome to the Restaurant Conversation Simulation.',
        style=style
    ).run()

    os.system('clear')  # Clears the terminal screen

    initial_message = prompt('Enter the initial message for the server: ')

    button_dialog(
        title='Starting the conversation',
        text='Do you want to start the conversation with the message: ' + initial_message,
        buttons=[
            ('Yes', True),
            ('No', False),
        ],
        style=style
    ).run()

    os.system('clear')  # Clears the terminal screen

    # Now use the provided initial message
    start_conversation(guest_system, server_system, initial_message)



if __name__ == "__main__":
    main()