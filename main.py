from f_utils import get_input
input_str = get_input()



from typing import List, Tuple

STOP_WORDS = ["a", "ourselves", "about", "out", "above", "over", "after", "own", "again", "same", "against", "shan't", "all", "she", "am", "she'd", "an", "she'll", "and", "she's", "any", "should", "are", "shouldn't", "aren't", "so", "as", "some", "at", "such", "be", "than", "because", "that", "been", "that's", "before", "the", "being", "their", "below", "theirs", "between", "them", "both", "themselves", "but", "then", "by", "there", "can't", "there's", "cannot", "these", "could", "they", "couldn't", "they'd", "did", "they'll", "didn't", "they're", "do", "they've", "does", "this", "doesn't", "those", "doing", "through", "don't", "to", "down", "too", "during", "under", "each", "until", "few", "up", "for", "very", "from", "was", "further", "wasn't", "had", "we", "hadn't", "we'd", "has", "we'll", "hasn't", "we're", "have", "we've", "haven't", "were", "having", "weren't", "he", "what", "he'd", "what's", "he'll", "when", "he's", "when's", "her", "where", "here", "where's", "here's", "which", "hers", "while", "herself", "who", "him", "who's", "himself", "whom", "his", "why", "how", "why's", "how's", "with", "i", "won't", "i'd", "would", "i'll", "wouldn't", "i'm", "you", "i've", "you'd", "if", "you'll", "in", "you're", "into", "you've", "is", "your", "isn't", "yours", "it", "yourself", "it's", "yourselves", "its", "nor", "itself", "not", "let's", "of", "me", "off", "more", "on", "most", "once", "mustn't", "only", "my", "or", "myself", "other", "no", "ought", "ours", "our"]

class Sentence:
    def __init__(self, initial_text: str):
        self.__text = initial_text
        self.__ponctuation = self.__text[-1] if self.__text[-1] in [".", "!", "?"] else None
        self.__normalised_text = initial_text.lower() if self.__ponctuation is None else initial_text[:-1].lower()
        self.__words = self.__normalised_text.split(" ")
        self.__important_words = [word for word in self.__words if word not in STOP_WORDS]

    def __str__(self):
        return self.__text
    
    def __repr__(self):
        return self.__text
    
    @property
    def text(self):
        return self.__text
    
    @property
    def words(self):
        return self.__words
    
    @property
    def important_words(self):
        return self.__important_words
    

class MatchMatrix:
    def __init__(self, questions: List[Sentence], answers: List[Sentence]):
        self.__questions = questions
        self.__answers = answers
        self.__matrix = [[0 for _ in range(len(answers))] for _ in range(len(questions))]

    def __str__(self):
        aff = ""
        for i, question in enumerate(self.__questions):
            for j, answer in enumerate(self.__answers):
                aff += f"{self.__matrix[i][j]} "
            aff += "\n"
        # now print the questions and the answers
        aff += "Questions:\n"
        for question in self.__questions:
            aff += f" - {question}\n"
        aff += "Answers:\n"
        for answer in self.__answers:
            aff += f" - {answer}\n"
        return aff
    
    def __repr__(self):
        return str(self.__matrix)
    
    @property
    def matrix(self):
        return self.__matrix
    
    def compute_matrix(self, only_importants: bool = True, substring: bool = False):
        """important words in common between questions and answers"""
        for i, question in enumerate(self.__questions):
            for j, answer in enumerate(self.__answers):
                if only_importants:
                    q_words = question.important_words
                    a_words = answer.important_words
                else:
                    q_words = question.words
                    a_words = answer.words
                if substring:
                    self.__matrix[i][j] = 1 if question.text in answer.text else 0
                else:
                    self.__matrix[i][j] = len(set(q_words).intersection(set(a_words)))
    
    def get_q_a_max(self):
        """Return the couples (q, a) from the matrix"""
        couples = []
        for i, row in enumerate(self.__matrix):
            for j, element in enumerate(row):
                if element == max(row):
                    couples.append((self.__questions[i], self.__answers[j]))
        return couples


def split_paragraph_to_sentences(paragraph: str, separators: List[str] = [".", "!", "?"]) -> List[str]:
    """Split a paragraph to sentences"""
    sentences = []
    sentence = ""
    for char in paragraph:
        sentence += char
        if char in separators:
            sentences.append(sentence)
            sentence = ""
    return sentences

def split_input(input_text) -> Tuple[list[Sentence], list[Sentence], list[Sentence]]:
    """Split the input text to return the text, the questions and the answers
    input text must be :
    text\n
    question1\nquestion2\n...\n
    answer1;answer2;...
    """
    lines = input_text.split("\n")

    text = [Sentence(sentence_str) for sentence_str in split_paragraph_to_sentences(lines[0])]
    questions = [Sentence(question) for question in lines[1:-1]]
    answers = [Sentence(answer) for answer in lines[-1].split(";")]
    
    return text, questions, answers


def match_answers_sentence(text_sentences: List[Sentence], answers: List[Sentence]) -> List[Sentence]:
    """Return the sentences in text that contains the answers, or part of the answers.
    if N answers are in the same sentence, we split the sentence to N sentences"""
    matched_matrix = MatchMatrix(answers, text_sentences)
    matched_matrix.compute_matrix(substring=True)
    # if the sum of colums is > 1, then two answers are in the same sentence, we split the sentence
    print(matched_matrix)
    couples = matched_matrix.get_q_a_max()
    print(couples)

    

    


# this program aims to match the questions with the answers given in the input text

def main():
    text, questions, answers = split_input(input_str)
    match_answers_sentence(text, answers)

if __name__ == "__main__":
    main()