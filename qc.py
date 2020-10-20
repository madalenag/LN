
import sys
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score

f_labels=open("DEV-labels.txt", "w")
f_questions=open("DEV-questions.txt", "w")

f_dev=open("DEV.txt", "r")
dev_lines = f_dev.readlines()

for l in dev_lines:
    split = l.split(' ',1)
    f_labels.write(split[0]+'\n')
    f_questions.write(split[1])

f_dev.close()
f_labels.close()
f_questions.close()


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

arg_list = sys.argv

f_train = open(arg_list[2], "r")
f_dev_questions = open(arg_list[3], "r")
f_dev_labels = open(arg_list[4], "r")

model = arg_list[1]

train_lines = f_train.readlines()
dev_questions_lines = f_dev_questions.readlines()
dev_labels_lines = f_dev_labels.readlines()

train_questions = []
train_labels = []

dev_questions = []
dev_labels = []

for l in train_lines:
    split = l.split(' ',1)
    split_label = split[0].split(':', 1)

    train_questions.append(split[1])
    if model == '-coarse':
        train_labels.append(split_label[0])
    else:
        train_labels.append(split[0])

for l in dev_questions_lines:
    dev_questions.append(l)

for l in dev_labels_lines:
    split_label = l.split(':', 1)
    if model == '-coarse':
        dev_labels.append(split_label[0])
    else:
        dev_labels.append(l.replace('\n', ''))

f_train.close()
f_dev_questions.close()
f_dev_labels.close()
#pre processing
print(dev_labels)

# TODO: stemming

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

train_questions = list(map(process, train_questions))
dev_questions = list(map(process, dev_questions))

stop_words = set(stopwords.words('english'))
exclude_words = set(("what", "where", "how", "when", "why"))
new_stop_words = stop_words.difference(exclude_words)

tokenizer=LemmaTokenizer()
token_stop = tokenizer(' '.join(new_stop_words))

tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= new_stop_words)#, tokenizer= tokenizer)

train_data = tfidfvectorizer.fit_transform(train_questions)
dev_data = tfidfvectorizer.transform(dev_questions)

#train
clf = ExtraTreesClassifier(n_estimators=100, random_state=0)
clf.fit(train_data, train_labels)

#predict
dev_predict = clf.predict(dev_data)


 #evaluating

print(accuracy_score(dev_labels, dev_predict))
