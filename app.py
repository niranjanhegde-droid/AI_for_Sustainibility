from flask import Flask, render_template, request, redirect, flash
from models import db, Complaint
from rag_engine import SustainabilityRAG
app = Flask(__name__)

app.config['SECRET_KEY'] = 'green-campus-ai'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///green_campus.db'

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------------------
# AI Issue Classification
# ---------------------------

def classify_issue(text):

    text = text.lower()

    water_keywords = [
        "water","leak","leakage","pipe","pipeline",
        "tap","faucet","drain","drainage","sewage",
        "sewer","overflow","tank","water tank",
        "rainwater","harvesting","hydration",
        "washroom","toilet","restroom",
        "bathroom","sink","plumbing",
        "water wastage","water usage",
        "water conservation","flood",
        "burst pipe","water flow"
    ]

    energy_keywords = [
    "electricity","electrical","energy",
    "power","voltage","current",
    "wire","wiring","cable",
    "light","lights","lighting",
    "bulb","tube light","led",
    "fan","fans","ac","air conditioner",
    "generator","battery","inverter",
    "solar","renewable energy",
    "switch","switchboard",
    "power cut","power failure",
    "power fluctuation",
    "electric shock",
    "short circuit",
    "sparking",
    "fire",
    "energy wastage"
]
    waste_keywords = [
    "waste","garbage","trash",
    "plastic","paper waste",
    "food waste","dry waste",
    "wet waste","recycle",
    "recycling","bin","dustbin",
    "litter","littering",
    "pollution","contamination",
    "compost","composting",
    "e-waste","electronic waste",
    "disposal","segregation",
    "single use plastic",
    "chemical waste",
    "hazardous waste"
]

    water_score = sum(
        1 for word in water_keywords
        if word in text
    )

    energy_score = sum(
        1 for word in energy_keywords
        if word in text
    )

    waste_score = sum(
        1 for word in waste_keywords
        if word in text
    )

    scores = {
        "Water": water_score,
        "Energy": energy_score,
        "Waste": waste_score
    }

    category = max(scores, key=scores.get)

    if scores[category] == 0:
        return "Other"

    return category


# ---------------------------
# Priority Detection
# ---------------------------

def detect_priority(text):

    text = text.lower()

    high_words = [
        "major",
        "critical",
        "emergency",
        "danger",
        "flood",
        "overflow",
        "burst",
        "burst pipe",
        "sparking",
        "electric shock",
        "short circuit",
        "fire",
        "hazardous",
        "chemical spill",
        "chemical waste",
        "explosion",
        "sewage overflow"
    ]

    medium_words = [
        "leak",
        "leakage",
        "broken",
        "damaged",
        "wastage",
        "power issue",
        "dustbin full",
        "light left on",
        "fan not working"
    ]

    if any(word in text for word in high_words):
        return "High"

    if any(word in text for word in medium_words):
        return "Medium"

    return "Low"

# ---------------------------
# Local RAG Retrieval
# ---------------------------

def retrieve_context(question):

    with open(
        "sustainability_knowledge.txt",
        "r",
        encoding="utf-8"
    ) as f:

        knowledge = f.read()

    question = question.lower()

    if "water" in question:
        return knowledge.split("Energy")[0]

    elif "energy" in question or \
         "electricity" in question:
        return knowledge

    elif "waste" in question:
        return knowledge

    return knowledge


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report", methods=["GET", "POST"])
def report():

    if request.method == "POST":

        title = request.form["title"]

        description = request.form["description"]

        full_text = f"{title} {description}"

        category = classify_issue(full_text)

        priority = detect_priority(full_text)

        complaint = Complaint(
            title=title,
            description=description,
            category=category,
            priority=priority
        )

        db.session.add(complaint)
        db.session.commit()

        flash(
            "Issue submitted successfully!",
            "success"
        )

        return redirect("/dashboard")

    return render_template(
        "report_issue.html"
    )


@app.route("/dashboard")
def dashboard():

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    total = Complaint.query.count()

    water = Complaint.query.filter_by(
        category="Water"
    ).count()

    energy = Complaint.query.filter_by(
        category="Energy"
    ).count()

    waste = Complaint.query.filter_by(
        category="Waste"
    ).count()

    score = max(
        0,
        100 - (total * 2)
    )

    return render_template(
        "dashboard.html",
        complaints=complaints,
        total=total,
        water=water,
        energy=energy,
        waste=waste,
        score=score
    )
rag = SustainabilityRAG()
@app.route(
    "/chatbot",
    methods=["GET", "POST"]
)
def chatbot():

    answer = ""

    if request.method == "POST":

        question = request.form["question"]

        retrieved_context = rag.retrieve(
            question
        )

        answer = f"""
AI Sustainability Recommendation

Based on the available sustainability knowledge:

{retrieved_context}

Recommended Action:

• Monitor the issue regularly
• Implement preventive measures
• Conduct periodic sustainability audits
"""

    return render_template(
        "chatbot.html",
        answer=answer
    )

import os

port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )