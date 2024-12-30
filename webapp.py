
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    name = None
    if request.method == "POST":
        # Get the name from the form submission
        name = request.form.get('name')
    return render_template("index.html", name=name)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    # Simple chatbot response logic
    if user_message.lower() == "hello":
        bot_response = "Hi there! How can I assist you today?"
    elif user_message.lower() == "bye":
        bot_response = "Goodbye! Have a great day!"
    else:
        bot_response = "I'm here to help! What do you want to know?"
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)



