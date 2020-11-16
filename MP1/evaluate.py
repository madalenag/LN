import sys
arg_list = sys.argv

#f_expected = open(arg_list[1], "r")
#f_predicted = open(arg_list[2], "r")

#expected_lines = f_expected.readlines()
#predicted_lines = f_predicted.readlines()

with open(arg_list[1]) as f:
   count = sum(1 for _ in f)

correct_labels = 0
with open(arg_list[1]) as f1, open(arg_list[2]) as f2:
    for line1, line2 in zip(f1, f2):
        if line1 == line2:
            correct_labels += 1

accuracy = (correct_labels/count) * 100

print("accuracy =",accuracy)
