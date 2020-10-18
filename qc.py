
import sys
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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

f_train=open(arg_list[2], "r")

train_lines = f_train.readlines()

train_dict = dict()

for l in train_lines:
    split = l.split(' ',1)
    if split[0] in train_dict:
        # append the new number to the existing array at this slot
        train_dict[split[0]].append(split[1])
    else:
        # create a new array in this slot
        train_dict[split[0]] = [split[1]]

#print(train_dict['LOC:other'])

#pre processing

#TODO: stopwords



# TODO: stemming

def process (question):
    question = question.lower()
    question = question.translate(str.maketrans('', '', string.punctuation))
    question = question.rstrip()

    stop_words = set(stopwords.words('english'))
    exclude_words = set(("what", "where", "how", "when", "why"))
    new_stop_words = stop_words.difference(exclude_words)
    word_tokens = word_tokenize(question)
    filtered_sentence = [w for w in word_tokens if not w in new_stop_words]
    return filtered_sentence

for key in train_dict:
    train_dict[key] = list(map(process, train_dict[key]))


# TODO:  tokenization

print(train_dict['LOC:other'])
