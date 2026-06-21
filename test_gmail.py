from tools.gmail_tool import authenticate_gmail

service = authenticate_gmail()

results = service.users().messages().list(
    userId='me',
    maxResults=5
).execute()

messages = results.get('messages', [])

print("\nLAST 5 EMAILS\n")

for msg in messages:

    message = service.users().messages().get(
        userId='me',
        id=msg['id']
    ).execute()


    headers = message['payload']['headers']

    sender = ""
    subject = ""

    for h in headers:

        if h['name'] == 'From':
            sender = h['value']

        elif h['name'] == 'Subject':
            subject = h['value']


    print("--------------------")
    print("FROM:", sender)
    print("SUBJECT:", subject)