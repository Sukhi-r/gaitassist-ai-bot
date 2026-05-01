from flask import Flask, render_template, request, jsonify
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import random

app = Flask(__name__)

# Load dataset
with open('dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

questions = [item['question'] for item in data]
answers = [item['answer'] for item in data]

# Train TF-IDF vectorizer with advanced parameters
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
    max_features=1000,
    sublinear_tf=True,  # Apply sublinear tf scaling
    min_df=1,
    max_df=0.95
)
question_vectors = vectorizer.fit_transform(questions)

# Rule-based keywords for topic detection (enhanced accuracy)
RULES = {
    'cerebral_palsy': ['cerebral palsy', 'cp', 'spastic', 'ataxic', 'dyskinetic', 'motor control', 'CP patients'],
    'diabetic_neuropathy': ['diabetes', 'neuropathy', 'nerve damage', 'blood sugar', 'diabetic', 'sensation', 'peripheral'],
    'fall_detection': ['fall', 'falling', 'prevent fall', 'detect fall', 'wearable', 'accelerometer', 'alert', 'elderly'],
    'gait': ['walking', 'gait', 'stride', 'cadence', 'posture', 'limping', 'walk', 'step', 'heel strike', 'toe-off']
}

def get_topic_from_rules(user_input):
    """Extract topic using rule-based keywords"""
    user_lower = user_input.lower()
    scores = {}
    
    for topic, keywords in RULES.items():
        score = 0
        for keyword in keywords:
            if keyword in user_lower:
                score += 1
        scores[topic] = score
    
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    return 'general'

def boost_relevant_answers(similarity_scores, detected_topic):
    """Boost answers relevant to detected topic"""
    boosted_scores = similarity_scores.copy()
    
    # Boost answers that match the detected topic
    if detected_topic != 'general':
        topic_keywords = RULES.get(detected_topic, [])
        for idx, answer in enumerate(answers):
            boost_factor = 1.0
            for keyword in topic_keywords:
                if keyword in answer.lower():
                    boost_factor += 0.15
            boosted_scores[idx] *= boost_factor
    
    return boosted_scores

def get_help_response(user_input, level='support'):
    """Provide conversational help, medical, and emergency guidance"""
    user_lower = user_input.lower()
    
    if level == 'emergency':
        return """🚨 EMERGENCY HELP:

It sounds serious. If there is sudden weakness, loss of consciousness, severe pain, or anything life-threatening, call emergency services now:
• USA: 911
• UK: 999
• India: 102
• Europe: 112

Please get help from someone nearby and do not delay."""
    
    if level == 'support':
        if any(term in user_lower for term in ['numb', 'numbness', 'tingle', 'tingling', 'leg pain', 'knee pain', 'leg hurt', 'shooting pain']):
            return """I hear you — numbness and pain in the leg can feel worrying, especially when it starts after walking.

That doesn't mean you need to panic. It often means the nerves or muscles are irritated, and getting a therapist or doctor to check the walking pattern can be really helpful.

For now, rest when it hurts, wear comfortable shoes, and try gentle movement instead of pushing through the pain. A professional can guide the next step."""
        
        if any(term in user_lower for term in ['what should i do', 'should i see', 'need help', 'can i', 'advice', 'what can i do']):
            return """That makes sense — asking what to do is a good move.

In many cases, the best next step is to let a doctor or physiotherapist see how you walk. They can check your posture, leg strength, and the way your feet hit the floor. If the pain or numbness is strong, it's a good idea not to keep pushing through it."""
        
        if any(term in user_lower for term in ['dizzy', 'dizziness', 'lightheaded', 'faint', 'fainting']):
            return """I hear you — feeling dizzy when you run can be unsettling.

It often happens when your body is trying to adjust to speed, breathing, or blood flow. Try slowing down a bit, taking regular breaks, and staying hydrated. If it keeps happening, showing a doctor or therapist exactly how it feels can help them figure it out."""
        
        if any(term in user_lower for term in ['fall', 'falling', 'unsteady', 'balance', 'wobbly', 'lose balance', 'lost my balance', 'almost fell']):
            return """If you feel like you might fall, that is a really helpful signal to be careful.

Try moving more slowly, using support like a railing or a walking aid, and choosing stable shoes. Balance exercises with a therapist can also make a big difference, and it's okay to get extra help so you feel safer."""
        
        return """💡 SUPPORT & RESOURCES:

I'm here to help you understand gait issues and find the right support.
• Physical therapists can work on walking and balance.
• Occupational therapists can help with daily movement.
• A doctor can check for nerve, muscle, or joint issues.
• A neurologist or orthopedist may be helpful if the problem is more serious.

It can feel better once someone explains it clearly. Asking for support early is smart, and I'm here to help you figure out what to ask them."""
    
    return """ℹ️ HELP AVAILABLE:

This chatbot is here to explain gait analysis, cerebral palsy, diabetic neuropathy, and fall prevention. If you want urgent or medical advice, please contact a professional."""

def make_conversational(answer, user_input):
    """Transform direct answers into friendly, conversational responses"""
    user_lower = user_input.lower()
    
    starters = [
        "Hey, good question. ",
        "I get where you're coming from. ",
        "Nice, let's look at that together. ",
        "I like this one. ",
        "That is a helpful thing to ask. ",
        "You are asking a really smart question. ",
        "Okay, let's break this down. ",
        "This is something I can help you with. ",
        "I'm here to help, so ",
        "Good thinking — ",
    ]
    
    if 'my mom' in user_lower:
        starters.extend([
            "I hear you — for your mom, ",
            "That sounds important for your mom. ",
            "For your mom's situation, ",
        ])
    elif 'i ' in user_lower or 'me ' in user_lower or 'my ' in user_lower:
        starters.extend([
            "For you, ",
            "If you're going through that, ",
            "When you feel that way, ",
        ])
    
    starter = random.choice(starters)
    
    connectors = [
        "Here is the simple version: ",
        "It usually works like this: ",
        "Let me say it this way: ",
        "The easy way to think about it is: ",
        "What it means is: ",
        "In plain terms: ",
        "The main idea is: ",
        "To keep it simple: ",
    ]
    connector = random.choice(connectors)
    
    if len(answer) > 220:
        sentences = answer.split('. ')
        formatted_answer = ''
        for i, sentence in enumerate(sentences[:3]):
            formatted_answer += sentence.strip() + '. '
        
        follow_ups = [
            "\n\nDoes that make sense? I can explain any part again.",
            "\n\nThat's the main idea. Want me to go deeper on anything?",
            "\n\nI hope that helps. Feel free to ask a bit more if you want.",
            "\n\nIn a few words, that's how it works. Want another example?",
            "\n\nLet me know if you'd like me to explain one part more clearly.",
        ]
        formatted_answer += random.choice(follow_ups)
    else:
        formatted_answer = answer
        closings = [
            "\n\nDoes that make sense? Anything else you'd like to know?",
            "\n\nHope that helps! What else can I tell you?",
            "\n\nThat is the short version. Want to hear more?",
            "\n\nGot it. Want me to explain it in a different way?",
            "\n\nThere you go! Feel free to ask a follow-up.",
            "\n\nIf you want, I can go into more detail on that.",
            "\n\nI'm right here if you want to ask another question.",
            "\n\nYou can ask me for another example if you like.",
        ]
        formatted_answer += random.choice(closings)
    
    final_response = starter + connector + formatted_answer
    return final_response

def get_response(user_input):
    """Advanced ensemble approach with conversational responses"""
    
    user_lower = user_input.lower()
    emergency_phrases = ['911', 'ambulance', 'critical', 'dying', 'unconscious', 'loss of consciousness', 'sudden paralysis', 'severe bleeding']
    support_phrases = ['need help', 'what should i do', 'should i see', 'should i', 'can i', 'need a doctor', 'advice', 'help me']
    symptom_phrases = ['pain', 'hurt', 'numb', 'numbness', 'tingle', 'tingling', 'dizzy', 'dizziness', 'swelling', 'weakness']
    balance_phrases = ['i might fall', 'might fall', 'almost fell', 'lose balance', 'lost my balance', 'feel unsteady', "can't keep balance", "can't keep balance", 'feel wobbly']
    question_words = ['what', 'should', 'do', 'how', 'why']
    
    if any(term in user_lower for term in emergency_phrases):
        return get_help_response(user_input, level='emergency'), 1.0
    
    if any(term in user_lower for term in support_phrases):
        return get_help_response(user_input, level='support'), 1.0
    
    if any(term in user_lower for term in balance_phrases):
        return get_help_response(user_input, level='support'), 1.0
    
    # If it is symptom-based but not explicitly asking for emergency support,
    # treat it as a support-style response if the user asks a related question.
    if any(term in user_lower for term in symptom_phrases) and any(word in user_lower for word in question_words):
        return get_help_response(user_input, level='support'), 1.0
    
    # Step 2: Detect topic using rules
    detected_topic = get_topic_from_rules(user_input)
    
    # Step 3: Get TF-IDF similarity scores
    user_vector = vectorizer.transform([user_input])
    similarity_scores = cosine_similarity(user_vector, question_vectors)[0]
    
    # Step 4: Boost scores based on detected topic
    boosted_scores = boost_relevant_answers(similarity_scores, detected_topic)
    
    # Step 5: Find best match
    best_idx = boosted_scores.argmax()
    confidence_score = float(boosted_scores[best_idx])
    
    # Normalize confidence between 0 and 1
    confidence_score = min(confidence_score, 1.0)
    
    # Check if confidence is too low
    if confidence_score < 0.1:
        low_confidence_responses = [
            "Hmm, I'm not totally sure about that one. Could you rephrase it? I'm better with questions about gait, cerebral palsy, diabetic neuropathy, or fall detection.",
            "I'm not getting a clear match. Try asking in another way, and I can help with gait-related walking questions.",
            "That looks a bit outside my main topics. If you ask about gait, walking patterns, CP, neuropathy, or fall prevention, I can help more clearly.",
            "I want to help, but I need a clearer question. Can you ask it again with gait, balance, or walking in mind?",
        ]
        return random.choice(low_confidence_responses), confidence_score
    
    best_answer = answers[best_idx]
    conversational_answer = make_conversational(best_answer, user_input)
    return conversational_answer, confidence_score


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get', methods=['POST'])
def chatbot_response():
    user_input = request.json.get('message', '')
    reply, confidence = get_response(user_input)
    return jsonify({
        'reply': reply,
        'confidence': round(confidence * 100, 1)
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)


