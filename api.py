from flask import Flask, render_template, request ,jsonify
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import cont

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

MAX_LEN = 320

app = Flask(__name__)

@app.route("/")
def index_page():
    return "Question Answering API for E-Exhibition"

@app.route("/predict", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
         ques = request.form.get("question")
         contextqna = request.form.get("contextqna")
         context = cont.CONTEXT[contextqna]
        
         QA_input = {
         'question': ques,
         'context': context
         }    
         prediction = nlp(QA_input)
         if prediction['score']>0.19:
            return jsonify(prediction)
         else:
            return "Change The Question Please." 
    return "MODEL FAILED"

@app.route("/add_context",methods=["POST"])
def add_context():
    if request.method=="POST":
        context_no = request.form.get("context_no")
        new_context = request.form.get("new_context")

        #cont.CONTEXT[context_no] = new_context
        cont.CONTEXT.update({context_no:new_context})
        print(cont.CONTEXT)

        return "Context Changed Successfully"
    return "Unsuccessful Change"

@app.route("/show_contexts",methods=["GET"])
def show_contexts():
    return cont.CONTEXT



if __name__ == "__main__":
    app.run(debug=True)
