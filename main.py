from f_utils import get_input
input_str = get_input()



from typing import List, Tuple, Dict

STOP_WORDS = ["a", "ourselves", "about", "out", "above", "over", "after", "own", "again", "same", "against", "shan't", "all", "she", "am", "she'd", "an", "she'll", "and", "she's", "any", "should", "are", "shouldn't", "aren't", "so", "as", "some", "at", "such", "be", "than", "because", "that", "been", "that's", "before", "the", "being", "their", "below", "theirs", "between", "them", "both", "themselves", "but", "then", "by", "there", "can't", "there's", "cannot", "these", "could", "they", "couldn't", "they'd", "did", "they'll", "didn't", "they're", "do", "they've", "does", "this", "doesn't", "those", "doing", "through", "don't", "to", "down", "too", "during", "under", "each", "until", "few", "up", "for", "very", "from", "was", "further", "wasn't", "had", "we", "hadn't", "we'd", "has", "we'll", "hasn't", "we're", "have", "we've", "haven't", "were", "having", "weren't", "he", "what", "he'd", "what's", "he'll", "when", "he's", "when's", "her", "where", "here", "where's", "here's", "which", "hers", "while", "herself", "who", "him", "who's", "himself", "whom", "his", "why", "how", "why's", "how's", "with", "i", "won't", "i'd", "would", "i'll", "wouldn't", "i'm", "you", "i've", "you'd", "if", "you'll", "in", "you're", "into", "you've", "is", "your", "isn't", "yours", "it", "yourself", "it's", "yourselves", "its", "nor", "itself", "not", "let's", "of", "me", "off", "more", "on", "most", "once", "mustn't", "only", "my", "or", "myself", "other", "no", "ought", "ours", "our"]

import re

# Basic rule-based lemmatizer without importing libraries

# Dictionary for irregular forms
irregular_forms = {
    "children": "child",
    "men": "man",
    "women": "woman",
    "mice": "mouse",
    "geese": "goose",
    "feet": "foot",
    "teeth": "tooth",
    "oxen": "ox",
    "dice": "die",
    # Add more irregular forms as needed
}

# Function for lemmatization
def lemmatize(word):
    # Check if the word is in the irregular forms dictionary
    if word in irregular_forms:
        return irregular_forms[word]
    
    # Plural to singular (regular)
    if re.match(r'.*ies$', word):
        return re.sub(r'ies$', 'y', word)
    elif re.match(r'.*ves$', word):
        return re.sub(r'ves$', 'f', word)
    elif re.match(r'.*s$', word):
        return re.sub(r's$', '', word)
    
    # Past tense to present (regular)
    if re.match(r'.*ed$', word):
        if re.match(r'.*ied$', word):
            return re.sub(r'ied$', 'y', word)
        elif re.match(r'.*ed$', word):
            return re.sub(r'ed$', '', word)
    
    # Present participle to base form (regular)
    if re.match(r'.*ing$', word):
        if re.match(r'.*ying$', word):
            return re.sub(r'ying$', 'ie', word)
        elif re.match(r'.*ing$', word):
            return re.sub(r'ing$', '', word)
    
    # Return the word as is if no rules apply
    return word



class Sentence:
    def __init__(self, initial_text: str):
        self.__text = initial_text
        self.__ponctuation = self.__text[-1] if self.__text[-1] in [".", "!", "?"] else None
        self.__normalised_text = initial_text.lower() if self.__ponctuation is None else initial_text[:-1].lower()
        # all non-alphanumeric characters are removed
        self.__normalised_text = re.sub(r'[^a-z0-9 ]', '', self.__normalised_text)
        self.__words = self.__normalised_text.split(" ")
        self.__important_words = list(set([lemmatize(word) for word in self.__words if word not in STOP_WORDS and len(word) > 1]))

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
    
    def get_q_a_max_indexes(self, invert_duplicates: bool = False) -> Tuple[List[Tuple[int, int]], Dict[int, List[int]]]:
        """Return the couples (q, a) from the matrix"""
        couples = []
        duplicate_a_couples = dict()
        for i, row in enumerate(self.__matrix):
            for j, element in enumerate(row):
                column = [row[j] for row in self.__matrix]
                if element == max(row) and element > 0:
                    couples.append((i, j))
                    if column.count(max(row)) > 1 and j not in duplicate_a_couples:
                        if invert_duplicates:
                            duplicate_a_couples[i] = [j for j, e in enumerate(row) if e == max(row)]
                        else:
                            duplicate_a_couples[j] = [i for i, e in enumerate(column) if e == max(row)]
        
        # remove duplicate couples if len key < 2
        res_duplicate_a_couples = dict()
        for key, value in duplicate_a_couples.items():
            if len(value) >= 2:
                res_duplicate_a_couples[key] = value
                                            
        return couples, res_duplicate_a_couples


def split_paragraph_to_sentences(in_paragraph: str, separators: List[str] = [".", "!", "?"]) -> List[str]:
    """Split a paragraph to sentences"""
    sentences = []
    paragraph = in_paragraph + " "
    sentence = ""
    for i in range(len(in_paragraph)):
        char = paragraph[i]
        sentence += char
        if char in separators and paragraph[i+1] == " ":
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


def split_sentence_between_words(sentence: str, substrings: List[str]) -> List[str]:
    """Split a sentence between the substrings, split to ',', ';', ':', ' '"""
    # Find all occurrences of each substring
    positions = []
    for substring in substrings:
        start = sentence.find(substring)
        if start != -1:
            end = start + len(substring)
            positions.append((start, end))
    
    # Sort positions based on their start index
    positions.sort()
    
    # Extract parts of the sentence between these positions
    indexes_sep = []
    last_end = positions[0][1]
    first = True
    for start, end in positions[1:]:
        inter_sentence = sentence[last_end:start]
        for sep in [";", ",", ":", " "]:
            if sep in inter_sentence:
                index_sep = inter_sentence.index(sep) + last_end
                indexes_sep.append(index_sep + 1)
                last_end = index_sep + 1
                break
        else:
            indexes_sep.append(start)
            last_end = start

    # build the parts list
    parts = []
    for i, index in enumerate(indexes_sep):
        if i == 0:
            parts.append(sentence[:index])
        else:
            parts.append(sentence[indexes_sep[i-1]:index])
    parts.append(sentence[indexes_sep[-1]:])
    
    return parts
    
    
    

def match_answers_sentence(text_sentences: List[Sentence], answers: List[Sentence]) -> List[Tuple[Sentence, Sentence]]:
    """Return the sentences in text that contains the answers, or part of the answers.
    if N answers are in the same sentence, we split the sentence to N sentences"""
    matched_matrix = MatchMatrix(answers, text_sentences)
    matched_matrix.compute_matrix(substring=True)
    couples, duplicate_a_couples = matched_matrix.get_q_a_max_indexes()
    splitted_sentences = False
    for sts_index, ans_indexes in duplicate_a_couples.items():
        answer_list = [answers[i] for i in ans_indexes]
        # remove couple if the answer is a subseq of another answer
        for i, answer1 in enumerate(answer_list):
            for j, answer2 in enumerate(answer_list):
                if i != j and answer1.text in answer2.text:
                    couples.remove((ans_indexes[i], sts_index))
                    ans_indexes.pop(i)
        if len(ans_indexes) < 2:
            continue
                
        sentence_to_split = text_sentences[sts_index].text

        res = split_sentence_between_words(sentence_to_split, [subseq.text for subseq in answer_list])
        # remove the original sentence
        text_sentences.pop(sts_index)
        # add the new sentences
        text_sentences += [Sentence(sentence) for sentence in res]
        splitted_sentences = True
    
    if splitted_sentences:
        return match_answers_sentence(text_sentences, answers)
    
    return [(answers[i], text_sentences[j]) for i, j in couples]

def match_questions_sentence(text_sentences: List[Sentence], questions: List[Sentence]) -> List[Tuple[Sentence, Sentence]]:
    """Return the sentences in text that conntains words of the questions"""
    matched_matrix = MatchMatrix(questions, text_sentences)
    matched_matrix.compute_matrix(substring=False)
    print(matched_matrix)
    couples, duplicate_a_couples = matched_matrix.get_q_a_max_indexes(invert_duplicates=True)
    print(couples, duplicate_a_couples)
    res_couples = [couple for couple in couples if couple[0] not in duplicate_a_couples]
    print(res_couples)
    for q_i, sts in duplicate_a_couples.items():
        for sts_i in sts:
            if sts_i not in [couple[1] for couple in res_couples]:
                res_couples.append((q_i, sts_i))
                break
    print(res_couples)
    return [(questions[q_i], text_sentences[sts_i]) for q_i, sts_i in res_couples]

    

    

    


# this program aims to match the questions with the answers given in the input text

def main():
    text, questions, answers = split_input(input_str)
    matched_ans_text = match_answers_sentence(text, answers)
    text_sentences = [match[1] for match in matched_ans_text]
    matched_q_text = match_questions_sentence(text_sentences, questions)
    dict_text_ans = {match[1].text: match[0].text for match in matched_ans_text}
    matched_qna = [(match[0].text, dict_text_ans[match[1].text]) for match in matched_q_text]
    for q, a in matched_qna:
        print(f"Q: {q}\nA: {a}\n")
    

if __name__ == "__main__":
    main()