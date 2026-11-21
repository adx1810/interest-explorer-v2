"""Interest Explorer: a small, local Flask career-interest discovery app."""
from flask import Flask, render_template, request

app = Flask(__name__)

CATEGORIES = {
    "technology": {
        "name": "Technology & Software", "short": "Technology",
        "summary": "making digital tools, improving systems, and solving problems through code",
        "careers": ["Software developer", "AI application developer", "IT specialist"],
        "experiments": [
            ("Build a tiny Python helper", "Make a text-based program that asks a question, checks an answer, and prints a useful response.", "45–60 min"),
            ("Sketch an app", "Draw three screens for an app that solves one everyday problem. Explain what each button does.", "30 min"),
        ],
        "focus": "You repeatedly chose practical digital tools and technical problem-solving.",
    },
    "business": {
        "name": "Business & Entrepreneurship", "short": "Business",
        "summary": "finding opportunities, planning products, and understanding what customers need",
        "careers": ["Business analyst", "Marketing specialist", "Entrepreneur"],
        "experiments": [
            ("Plan a zero-budget business", "Choose a real problem, define a customer, and write a one-page offer with three reasons someone might use it.", "45 min"),
            ("Compare two brands", "Look at their websites and write down their audiences, offers, and what makes them different.", "30 min"),
        ],
        "focus": "Your choices pointed toward opportunities, customers, and turning ideas into plans.",
    },
    "creative": {
        "name": "Creative & Design", "short": "Creative",
        "summary": "expressing ideas visually, designing experiences, and improving how things look and feel",
        "careers": ["UX designer", "Graphic designer", "Content designer"],
        "experiments": [
            ("Redesign an everyday screen", "Pick a confusing app screen and sketch a clearer version on paper or in a free design tool.", "45 min"),
            ("Create a three-piece mini brand", "Choose a fictional product and make a name, simple logo, and promotional post.", "45 min"),
        ],
        "focus": "You leaned toward visual expression, clear communication through design, and fresh ideas.",
    },
    "science": {
        "name": "Science & Research", "short": "Research",
        "summary": "asking careful questions, gathering evidence, and figuring out why things work",
        "careers": ["Research assistant", "Data analyst", "Environmental scientist"],
        "experiments": [
            ("Run a mini investigation", "Ask a testable question about everyday life, collect a small set of observations, and record what the evidence supports.", "45 min"),
            ("Explain a discovery", "Find a credible science article and summarize its question, method, and uncertainty in five sentences.", "30 min"),
        ],
        "focus": "You often preferred asking why, checking evidence, and investigating how things work.",
    },
    "people": {
        "name": "People & Communication", "short": "People",
        "summary": "supporting others, helping groups collaborate, and explaining ideas clearly",
        "careers": ["Teacher", "Human resources specialist", "Community program coordinator"],
        "experiments": [
            ("Teach something in five minutes", "Explain a skill you know to a friend or family member and ask which part was confusing.", "20 min"),
            ("Plan a group activity", "Design a simple event plan with roles, a schedule, and a way to collect feedback.", "40 min"),
        ],
        "focus": "You favored understanding people, communicating ideas, and helping groups work together.",
    },
}

# Three perspectives per area: curiosity, daily work, and creating something.
QUESTIONS = [
    ("What would you choose to build this weekend?", [
        ("A simple phone or computer app", "technology"), ("A small business idea", "business"),
        ("A poster or visual identity", "creative"), ("A way to test an interesting question", "science"),
        ("A useful event for people", "people")]),
    ("Which problem sounds most interesting?", [
        ("Automating a repetitive task", "technology"), ("Helping a shop reach more customers", "business"),
        ("Making an ugly website easier to use", "creative"), ("Understanding why an experiment failed", "science"),
        ("Helping two people communicate better", "people")]),
    ("Which video would you watch out of curiosity?", [
        ("How AI tools are built", "technology"), ("How startups find customers", "business"),
        ("Why great designs work", "creative"), ("How scientists test ideas", "science"),
        ("How people learn and communicate", "people")]),
    ("In a school project, what role would you try?", [
        ("Build the technical part", "technology"), ("Plan the budget and pitch", "business"),
        ("Design the presentation", "creative"), ("Research and fact-check", "science"),
        ("Coordinate and explain to the group", "people")]),
    ("What result would feel most satisfying?", [
        ("A working program", "technology"), ("An idea people would pay for", "business"),
        ("A design people enjoy using", "creative"), ("A question answered with evidence", "science"),
        ("Someone understanding something new", "people")]),
    ("What would you like to get better at?", [
        ("Coding", "technology"), ("Negotiating and planning", "business"),
        ("Visual storytelling", "creative"), ("Analyzing evidence", "science"),
        ("Public speaking and listening", "people")]),
    ("Which free online course would you sample first?", [
        ("Python basics", "technology"), ("Intro to entrepreneurship", "business"),
        ("Introduction to design", "creative"), ("Scientific reasoning", "science"),
        ("Communication skills", "people")]),
    ("What would you enjoy improving?", [
        ("A slow or confusing computer task", "technology"), ("A weak product offer", "business"),
        ("An unclear user interface", "creative"), ("A flawed explanation", "science"),
        ("A team discussion", "people")]),
    ("Which challenge would you attempt for an hour?", [
        ("Fix a bug in a small program", "technology"), ("Invent a way to attract customers", "business"),
        ("Sketch an original product", "creative"), ("Compare two competing explanations", "science"),
        ("Prepare a short helpful workshop", "people")]),
    ("Which kind of feedback would motivate you?", [
        ("Your tool made my job easier", "technology"), ("Your plan solved a business problem", "business"),
        ("Your design is clear and memorable", "creative"), ("Your reasoning is careful and accurate", "science"),
        ("You helped everyone feel included", "people")]),
    ("What would you research for fun?", [
        ("New apps and software", "technology"), ("Interesting products and businesses", "business"),
        ("Art, interfaces, and media", "creative"), ("Nature and scientific discoveries", "science"),
        ("Behavior and relationships", "people")]),
    ("If you could shadow someone for a day, who?", [
        ("A software engineer", "technology"), ("A product manager", "business"),
        ("A digital designer", "creative"), ("A researcher", "science"),
        ("A teacher or community organizer", "people")]),
    ("Which kind of uncertainty would you enjoy exploring?", [
        ("Will this code work?", "technology"), ("Will customers want this?", "business"),
        ("Will people understand this design?", "creative"), ("Does the evidence support this idea?", "science"),
        ("Will this explanation help someone?", "people")]),
    ("Which small achievement would you be proud to share?", [
        ("A tool I programmed", "technology"), ("A plan for a small venture", "business"),
        ("A portfolio of designs", "creative"), ("A short evidence-based report", "science"),
        ("An event I helped lead", "people")]),
    ("What would you try next week even without a grade?", [
        ("Make a simple chatbot", "technology"), ("Draft a business idea", "business"),
        ("Design a prototype", "creative"), ("Carry out a mini study", "science"),
        ("Teach someone a new skill", "people")]),
]


def analyze(answers):
    """Summarize choices. Scores indicate selections, not measured ability."""
    scores = {key: 0 for key in CATEGORIES}
    for answer in answers:
        if answer in scores:
            scores[answer] += 1
    answered = sum(scores.values())
    unsure = len(answers) - answered
    rank = sorted(scores, key=lambda key: (-scores[key], list(CATEGORIES).index(key)))
    # A tied or low-signal result should not be presented as a confident 'match'.
    leading_score = scores[rank[0]]
    leaders = [key for key in rank if scores[key] == leading_score] if leading_score else []
    primary = rank[0] if leading_score else None
    second = next((k for k in rank if k != primary and scores[k] > 0), None)
    if answered == 0:
        headline = "You're still exploring — and that's useful information."
        paragraph = (
            "You selected ‘I'm not sure yet’ for all 15 questions, so there is not enough evidence to identify a leading interest area. "
            "This does not mean you lack interests or abilities. "
            "It means these particular choices did not help you distinguish between the fields. "
            "Start with two short, low-pressure activities from different fields and notice which one you'd voluntarily continue. "
            "Keep notes on what was engaging, difficult, or surprising. "
            "Retake this quiz after some hands-on exploration to see whether your preferences become clearer."
        )
    else:
        first = CATEGORIES[primary]
        second_name = CATEGORIES[second]["name"].lower() if second else "other directions"
        if len(leaders) > 1:
            joined = ", ".join(CATEGORIES[k]["short"] for k in leaders[:3])
            headline = "You have a few equally strong directions to explore."
            opening = f"Your highest answer count is shared by {joined}, so the quiz does not identify one clear winner."
        elif leading_score <= 3:
            headline = "Your interests look varied right now."
            opening = f"Your most selected area was {first['name'].lower()}, but your responses are spread across several fields."
        else:
            headline = f"Your strongest current signal: {first['name']}"
            opening = f"Your selections most often pointed toward {first['name'].lower()}."
        paragraph = " ".join([
            opening,
            f"This area involves {first['summary']}.",
            f"A second direction worth testing is {second_name}.",
            f"You answered {answered} of the 15 questions with a specific interest and chose ‘not sure yet’ {unsure} time{'s' if unsure != 1 else ''}.",
            "These counts reflect what appealed to you today; they do not measure your skills, personality, or future success.",
            "Try one small activity in each promising field, then compare which task made you want to learn more."
        ])
    return {
        "scores": scores, "answered": answered, "unsure": unsure, "rank": rank,
        "primary": primary, "second": second, "leaders": leaders,
        "headline": headline, "paragraph": paragraph,
    }


@app.get("/")
def index():
    return render_template("index.html", questions=QUESTIONS)


@app.post("/results")
def results():
    answers = [request.form.get(f"q{i}") for i in range(len(QUESTIONS))]
    valid = set(CATEGORIES) | {"unsure"}
    if any(answer not in valid for answer in answers):
        return render_template("index.html", questions=QUESTIONS,
                               error="Please answer all 15 questions, even if your answer is ‘I'm not sure yet’."), 400
    data = analyze(answers)
    recommended = [key for key in data["rank"] if data["scores"][key] > 0][:2]
    # In cases of no clear signal, sample two contrasting fields rather than guessing.
    if not recommended:
        recommended = ["technology", "business"]
    elif len(recommended) == 1:
        recommended.append(next(k for k in CATEGORIES if k != recommended[0]))
    return render_template("results.html", categories=CATEGORIES, total=len(QUESTIONS),
                           recommended=recommended, **data)


if __name__ == "__main__":
    app.run(debug=True)
