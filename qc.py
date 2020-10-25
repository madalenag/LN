
import sys
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn import svm

def split_dev(model):
    f_labels=open("DEV-labels.txt", "w")
    f_questions=open("DEV-questions.txt", "w")

    f_dev=open("DEV.txt", "r")
    dev_lines = f_dev.readlines()

    for l in dev_lines:
        split = l.split(' ',1)
        split_label = split[0].split(':', 1)

        f_questions.write(split[1])

        if model == '-coarse':
            f_labels.write(split_label[0]+'\n')
        else:
            f_labels.write(split[0]+'\n')

    f_dev.close()
    f_labels.close()
    f_questions.close()

#begginig

arg_list = sys.argv
model = arg_list[1]

split_dev(model)

f_train = open(arg_list[2], "r")
f_dev_questions = open(arg_list[3], "r")

train_lines = f_train.readlines()
dev_questions_lines = f_dev_questions.readlines()

train_questions = []
train_labels = []

dev_questions = []

#split questions and labels into different lists from TRAIN (considering the model)
for l in train_lines:
    split = l.split(' ',1)
    split_label = split[0].split(':', 1)

    train_questions.append(split[1])
    if model == '-coarse':
        train_labels.append(split_label[0])
    else:
        train_labels.append(split[0])

#put question from DEV in a list
for l in dev_questions_lines:
    dev_questions.append(l)

f_train.close()
f_dev_questions.close()

#pre processing

# Interface lemma tokenizer from nltk with sklearn
class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def process (question):
    question = question.lower()
    question = question.translate(str.maketrans('', '', string.punctuation))
    question = question.replace('\n', '')
    return question


#apply preprocessing to all questions both from TRAIN and DEV
train_questions = list(map(process, train_questions))
dev_questions = list(map(process, dev_questions))

stop_words = set(stopwords.words('english'))
exclude_words = set(("what", "where", "how", "when", "why"))
new_stop_words = stop_words.difference(exclude_words)

tokenizer=LemmaTokenizer()
token_stop = tokenizer(' '.join(new_stop_words))

tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= token_stop, tokenizer= tokenizer)

train_data = tfidfvectorizer.fit_transform(train_questions)
dev_data = tfidfvectorizer.transform(dev_questions)


#train
clf =  svm.SVC(kernel='linear')
clf.fit(train_data, train_labels)

#predict
dev_predict = clf.predict(dev_data)


for i in dev_predict:
    print(i)
