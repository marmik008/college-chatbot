from flask import Flask, render_template, request, jsonify
import re
import difflib

app = Flask(__name__)

# Predefined Knowledge Base (Intents, Keywords, and Answers)
KNOWLEDGE_BASE = [
    {
        "intent": "greeting",
        "keywords": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "start"],
        "reply": "Hello! 👋 Welcome to the College Help Desk. Ask me anything regarding courses, admissions, fees, library, or placements!"
    },
    {
        "intent": "courses",
        "keywords": ["course", "courses", "branch", "branches", "program", "programs", "diploma", "degree", "engineering", "btech"],
        "reply": "Our college offers Diploma & B.Tech degree programs in:\n• Computer Engineering\n• Information Technology\n• Mechanical Engineering\n• Civil Engineering\n• Electrical Engineering"
    },
    {
        "intent": "fees",
        "keywords": ["fee", "fees", "cost", "tuition", "payment", "installment", "scholarship", "charges"],
        "reply": "Tuition fees are ₹45,000 per semester for engineering courses. Government scholarships (MYSY, Digital Gujarat) and tuition fee waivers (TFWS) are applicable for eligible candidates."
    },
    {
        "intent": "admission",
        "keywords": ["admission", "apply", "eligibility", "acpc", "cutoff", "process", "documents", "entrance", "form"],
        "reply": "Admissions are conducted through state centralized counseling (ACPC) and management quotas. Requirements include 10th/12th marksheets, entrance test rank, and category certificates."
    },
    {
        "intent": "hostel",
        "keywords": ["hostel", "accommodation", "stay", "room", "mess", "food", "residence"],
        "reply": "Separate on-campus hostel facilities are available for boys and girls with 24/7 security, Wi-Fi, laundry, and mess facilities (₹35,000/term including food)."
    },
    {
        "intent": "placements",
        "keywords": ["placement", "placements", "package", "salary", "jobs", "companies", "recruitment", "internship"],
        "reply": "The training & placement cell assists students across all semesters. Top recruiters include TCS, Infosys, L&T, and local tech hubs, with an average package of 4.5 LPA."
    },
    {
        "intent": "library",
        "keywords": ["library", "books", "reading", "digital library", "journals", "timing"],
        "reply": "The central library holds over 30,000 books, international research journals, and 50+ computer terminals with IEEE digital access. Open Monday to Saturday: 8:00 AM - 7:00 PM."
    },
    {
        "intent": "contact",
        "keywords": ["contact", "phone", "number", "email", "address", "location", "help desk", "call"],
        "reply": "📍 Campus Address: College Road, Academic Zone\n📞 Phone: +91 79 2345 6789\n✉️ Email: admissions@college.edu\n🌐 Website: www.college.edu"
    }
]

def clean_text(text):
    return re.findall(r'\b\w+\b', text.lower())

def match_query(user_message):
    words = clean_text(user_message)
    if not words:
        return "Please type a question so I can assist you!"
    
    best_intent = None
    max_score = 0

    for item in KNOWLEDGE_BASE:
        score = 0
        for word in words:
            # Check exact keyword hits
            if word in item["keywords"]:
                score += 2
            # Check fuzzy keyword matches (e.g. typos like 'fees' vs 'fee')
            elif difflib.get_close_matches(word, item["keywords"], n=1, cutoff=0.8):
                score += 1

        if score > max_score:
            max_score = score
            best_intent = item

    # If confidence score is sufficient, return intent reply
    if best_intent and max_score >= 1:
        return best_intent["reply"]
    
    # Fallback response
    return "I couldn't find a direct answer to that. Would you like to reach our help desk directly?\n\n📞 Phone: +91 79 2345 6789\n✉️ Email: support@college.edu"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json() or {}
    message = payload.get("message", "")
    response_text = match_query(message)
    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(debug=True, port=5000)