import vonage
import pandas as pd

client = vonage.Client(key="b0bc2441", secret="VKxfdTfkP3YNMXK5")
sms = vonage.Sms(client)

messages = [
    {
        "from": "Amazon",
        "to": "40722101097",
        "text": "Message 1",
    },
    {
        "from": "Amazon",
        "to": "40722101097",
        "text": "Message 2",
    },
    {
        "from": "Amazon",
        "to": "40722101097",
        "text": "Message 3",
    },
    # Add more messages as needed
]

failed_numbers = []

for message in messages:
    responseData = sms.send_message(message)

    if responseData["messages"][0]["status"] != "0":
        failed_numbers.append(message["to"])
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

df_failed_numbers = pd.DataFrame(failed_numbers, columns=["Failed Numbers"])
print(df_failed_numbers)
