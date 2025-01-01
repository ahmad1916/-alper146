
import os
import torch
from PIL import Image
from flask import Flask, render_template, request, jsonify
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights
from transformers import pipeline

# Set the environment variable to avoid TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'  # Optional: Avoid protobuf issues

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize ResNet Model for Image Recognition (Fixed pretrained warning)
model = resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()

# Initialize NLP Pipeline (Hugging Face)
nlp_pipeline = pipeline("text-generation", model="gpt2")

# Predefined responses for chatbot
CHAT_RESPONSES = {
    "hello": "Hi there! How can I assist you today?",
    "hi": "Hello! What can I do for you?",
    "hey": "Hey! How's your day going? How can I help?",
    "good morning": "Good morning! I hope your day is off to a great start.",
    "good afternoon": "Good afternoon! How can I assist you today?",
    "good evening": "Good evening! Let me know if you need any help.",
    "bye": "Goodbye! Have a great day!",
    "see you later": "Take care! I'm here if you need me again.",
    "thank you": "You're welcome! I'm glad I could help.",
    "thanks": "No problem! Let me know if you need anything else.",
    "how are you": "I'm just a bot, but I'm here to help! How can I assist you?",
    "what's up": "Not much, just ready to assist you! What's up with you?",
    "who are you": "I'm a virtual assistant chatbot. I'm here to answer your questions and assist you.",
    "what can you do": "I can help with answering questions, providing information, and chatting with you. Try asking something!",
    "help": "Sure! Ask me anything about our services or general queries.",
    "what is your name": "I'm just a humble chatbot, but you can call me Assistant!",
    "how old are you": "I was created recently, so I guess I'm pretty young in human years.",
    "where are you from": "I exist in the digital world, but I'm here to make your life easier wherever you are!",
    "who created you": "I was created by talented developers to assist you. Cool, right?",
    "tell me a joke": "Why don't skeletons fight each other? Because they don't have the guts!",
    "another joke": "Sure! Why did the math book look sad? Because it had too many problems.",
    "tell me a fun fact": "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
    "give me a riddle": "Sure! I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? (Answer: An echo!)",
    "what is the weather today": "I'm not connected to live weather data, but I can give general advice. Always good to carry an umbrella just in case!",
    "what time is it": "I can't check the time, but I know it's always a good time to ask questions!",
    "how's the traffic": "I can't check traffic directly, but I suggest using a navigation app for real-time updates.",
    "what is the meaning of life": "That’s a deep question! Some say it's 42. Others believe it's about happiness and making connections.",
    "tell me something interesting": "Did you know octopuses have three hearts, and two of them stop beating when they swim?",
    "do you have feelings": "I'm just a bot, so I don't have feelings, but I enjoy helping you out!",
    "what is ai": "AI stands for Artificial Intelligence, the technology that allows machines to mimic human behavior and decision-making.",
    "what is python": "Python is a popular programming language known for its simplicity and versatility. It's used for web development, AI, data science, and more!",
    "how do I learn programming": "Great question! Start with beginner-friendly languages like Python. There are many free resources online, such as tutorials and coding platforms.",
    "recommend a book": "Sure! If you like fiction, try 'The Hobbit.' For non-fiction, 'Sapiens' is a great choice.",
    "movie recommendation": "If you're into sci-fi, try 'Inception.' For comedy, 'The Grand Budapest Hotel' is a fun watch.",
    "how can I improve my skills": "Consistent practice and learning are key. Set goals, follow tutorials, and don't be afraid to make mistakes.",
    "how do I stay motivated": "Break tasks into small steps, celebrate progress, and remind yourself why you started.",
    "tell me about space": "Space is vast and full of wonders. Did you know a day on Venus is longer than its year?",
    "what is the largest planet": "The largest planet in our solar system is Jupiter. It's a gas giant with a storm larger than Earth!",
    "how do I stay healthy": "Eat balanced meals, stay active, and get enough rest. Mental health is just as important as physical health!",
    "exercise tips": "Start with light exercises like walking or stretching, and gradually increase intensity. Consistency is key!",
    "covid advice": "Wash your hands frequently, wear a mask in crowded places, and stay updated with health guidelines.",
    "tell me about technology": "Technology is evolving rapidly. From AI to renewable energy, the future is exciting!",
    "future of ai": "AI is expected to revolutionize industries, automate tasks, and improve efficiency in many fields.",
    "tell me about ankara university": "Ankara University, established in 1946, is the first higher education institution founded in Turkey after the formation of the Turkish Republic. It offers a wide range of programs across various fields, including social sciences, natural sciences, humanities, health sciences, and engineering. The university is known for its rich history and commitment to education and research. [Source: https://en.wikipedia.org/wiki/Ankara_University]",
    "salam": "Queen of the Sinapon",
    

    # Science-related responses
    "what is science": "Science is the study of the natural world based on facts learned through experiments and observation. It helps us understand how the world around us works.",
    "what is physics": "Physics is the branch of science that deals with the study of matter, energy, and the interactions between them. It explains the fundamental forces of nature.",
    "what is chemistry": "Chemistry is the branch of science that studies the properties, composition, and behavior of matter. It explains how substances interact and combine to form new substances.",
    "what is biology": "Biology is the science of life and living organisms. It studies how organisms function, grow, and interact with their environments.",
    "tell me a fun science fact": "Did you know that water can boil and freeze at the same time? This phenomenon is called the 'triple point' and occurs under specific pressure and temperature conditions.",
    "what is the theory of relativity": "The theory of relativity, developed by Albert Einstein, explains how space and time are linked for objects that are moving at a constant speed. It revolutionized our understanding of physics and gravity.",
    "what is evolution": "Evolution is the process by which different kinds of living organisms have developed and diversified from earlier forms during the history of the Earth.",
    "what is the big bang theory": "The Big Bang Theory explains that the universe began as a singularity about 13.8 billion years ago and expanded rapidly. It is the leading explanation for the origin of the universe.",

    # Turkey-specific information
    "overview": "Turkey, officially the Republic of Türkiye, is a country mainly located in Anatolia in West Asia, with a smaller part called East Thrace in Southeast Europe. It borders the Black Sea to the north; Georgia, Armenia, Azerbaijan, and Iran to the east; Iraq, Syria, and the Mediterranean Sea to the south; and the Aegean Sea, Greece, and Bulgaria to the west. Turkey is home to over 85 million people; most are ethnic Turks, while ethnic Kurds are the largest ethnic minority. Officially a secular state, Turkey has a Muslim-majority population. Ankara is Turkey's capital and second-largest city, while Istanbul is its largest city and economic and financial center. Other major cities include İzmir, Bursa, and Antalya.",
    "geography": "Turkey has coastal plains, a high central plateau, and various mountain ranges; its climate is temperate with harsher conditions in the interior. Turkey is home to three biodiversity hotspots and is prone to frequent earthquakes. It is highly vulnerable to climate change.",
    "history": "Turkey was first inhabited by modern humans during the Late Paleolithic. Important ancient sites like Göbekli Tepe, which is over 12,000 years old, are located in Turkey. The region has been home to various civilizations, including the Hittites, Romans, Byzantines, and Ottomans. The Ottoman Empire ruled until the early 20th century, and the Republic of Turkey was founded in 1923 by Mustafa Kemal Atatürk.",
    "culture": "Turkey has a rich and diverse culture, influenced by its long history and geographic location at the crossroads of Europe and Asia. The country is known for its cuisine, which includes dishes like kebabs, baklava, and Turkish delight. It also has a rich tradition of art, music, and literature.",
    "biodiversity": "Turkey is home to several biodiversity hotspots. It has diverse ecosystems, ranging from forests to steppes and wetlands. Its rich flora and fauna are under threat from climate change and human activities."
}



# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = CHAT_RESPONSES.get(user_message.lower(), "I'm not sure. Ask me anything else!")

    return jsonify({"response": response})


@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"response": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"response": "No selected file"})

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            img = Image.open(filepath).convert("RGB")
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            img_t = preprocess(img).unsqueeze(0)

            with torch.no_grad():
                outputs = model(img_t)
                _, predicted_idx = torch.max(outputs, 1)

                return jsonify({"response": f"Detected class index: {predicted_idx.item()}"})

        except Exception as e:
            return jsonify({"response": f"Image uploaded but could not be analyzed. Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)


