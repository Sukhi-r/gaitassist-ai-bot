import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = 'dataset.json'


def load_dataset():
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
    questions = [item['question'] for item in data]
    answers = [item['answer'] for item in data]
    return data, questions, answers


def train_vectorizer(questions):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    question_vectors = vectorizer.fit_transform(questions)
    return vectorizer, question_vectors


def save_dataset(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


data, questions, answers = load_dataset()
vectorizer, question_vectors = train_vectorizer(questions)


def retrain():
    global data, questions, answers, vectorizer, question_vectors
    data, questions, answers = load_dataset()
    vectorizer, question_vectors = train_vectorizer(questions)


def get_response(user_input):
    user_vector = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vector, question_vectors)

    index = similarity.argmax()
    score = float(similarity[0][index])

    if score < 0.3:
        return None, score
    return answers[index], score


def main():
    print("GaitAssist AI Bot Ready! (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == 'exit':
            print('Bot: Goodbye!')
            break

        response, score = get_response(user_input)
        if response:
            print('Bot:', response)
            continue

        print("Bot: I don't know that one yet. Ask another question or type 'teach' to add it.")
        teach = input('Would you like to teach me this question? (yes/no): ').strip().lower()
        if teach in ('yes', 'y'):
            answer_text = input('Enter the answer you want me to learn: ').strip()
            if answer_text:
                data.append({'question': user_input, 'answer': answer_text})
                save_dataset(data)
                retrain()
                print('Bot: Thanks! I learned a new answer.')
            else:
                print('Bot: No answer was given. I did not learn it.')
        else:
            print("Bot: Okay, let's try another question.")


if __name__ == '__main__':
    main()
