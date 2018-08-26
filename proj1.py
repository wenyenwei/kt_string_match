import editdistance

# open dict
f = open("2018S2-90049P1-data/dict.txt")
my_dict = f.readlines()
f.close()

# init result dict
res_dict = {}

# open wiki files
f_mis = open("2018S2-90049P1-data/wiki_misspell.txt","r")
f_cor = open("2018S2-90049P1-data/wiki_correct.txt","r")

# store correct lines to array
f_cor_array = []
for line in f_cor:
    f_cor_array.append(line)
    
count = 0

# read wiki misspell file line by line
for line in f_mis:
    string = line.strip()
    bestv = 10000000
    bests = ""
    # compare with dict lines
    for entry in my_dict:
        # string is lines in target doc
        # entry is lines in dict 
        thisv = editdistance.eval(string, entry.strip())
        if (thisv < bestv):
            bestv = thisv
            bests = entry.strip()
    print(string, bests, bestv, f_cor_array[count].strip(), bests == f_cor_array[count].strip())
    
    # save to res dict
    res_dict[string] = {"result_s": bests, "distance": bestv, "match": bests == f_cor_array[count].strip()}
    count += 1
    
# save result as json to file    
import json

with open('res_edit_distance.txt', 'w') as file:
     file.write(json.dumps(res_dict)) 
     
# evaluation
# accuracy
true_count = 0
for res in res_dict:
    if res_dict[res]['match']: true_count += 1   
    
with open('evaluation.txt', 'w') as file:
     file.write(json.dumps({"accuracy_edit_distance":(float(true_count) / len(res_dict))})) 
print("accuracy - edit distance", (float(true_count) / len(res_dict))) 
# precision
     
# recall