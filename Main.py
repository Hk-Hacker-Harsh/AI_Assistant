from ollama import chat
from ollama import ChatResponse

while True:
    inp = input("You : ")

    response: ChatResponse = chat(model='gemma3', messages=[
    {
        'role': 'user',
        'content': inp,
    },
    ])
    print("AI : " + response['message']['content'])