import tkinter
from tkinter import Scrollbar
import requests



window=tkinter.Tk()
window.title("AI chatbot")

label = tkinter.Text(window, bg="white", width=100, height=30)
scrollbar = Scrollbar(window)
scrollbar.pack(side="right", fill="y")
scrollbar.config(command=label.yview)
label.config(yscrollcommand=scrollbar.set)
label.pack(fill="both", expand=True)

# Create the user's input field
textentry = tkinter.Entry(window, fg='red', width=100)

textentry.pack()


def apicall():
    text=textentry.get()
    form_data= {
        'conversation_id':  0,
        'query': text
    }
    label.insert('end', f"User: {text}\n",)
    query= requests.post('http://127.0.0.1:5000/api/question', data=form_data)
    textentry.delete(0,'end')

    # print(query.text)
    label.insert('end', f"Chatbot: {query.json()['result']['answer']}\n")


# Create the send button
button = tkinter.Button(window, text="Send", command=apicall)
button.pack()


window.mainloop()

