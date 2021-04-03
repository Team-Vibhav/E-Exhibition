from flask import Flask, render_template, request ,jsonify
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
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
         context = request.form.get("context")
        
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


if __name__ == "__main__":
    app.run(debug=True)
