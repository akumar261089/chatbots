from flask import Flask, request, jsonify, render_template
import openai
# Importing modules
import re
from nltk.corpus import wordnet

openai.api_key_path = "/home/abhi/chatgptKey"
initail =[
                {"role": "system", "content": "You are a helpful assistant."}
            ]
Conversation=[]
def chat_with_gpt(prompt):
    Conversation.append({"role": "user", "content": prompt})
    try:
        print("requesting hcatgpt  "+ prompt)
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=initail + Conversation[-4:]
        )
        print("complete")
        #print(response)
        responsetoreturn=re.sub('```','<code> ',response.choices[0].message.content,1)
        Conversation.append(response.choices[0].message)
    except Exception as e:
        print(e)
        responsetoreturn="error"
        
    #print(responsetoreturn)

    return(responsetoreturn)



app =Flask(__name__)
@app.route('/')
def welcome():
    return render_template('index.html')

@app.post("/input")
def intraction():
    if request.is_json:
        print(request)
        jsonInput= request.get_json()
        userInput=jsonInput["input"]
        answer=chat_with_gpt(userInput)
        print(answer)
        return answer,201
    return {"error": "Request must be json"}
