import json
import numpy as np
from weighted_levenshtein import dam_lev

# higher costs = 2
higher_costs_1 = np.full(128, 2, dtype=np.float64)
higher_costs_2 = np.full((128,1), 2, dtype=np.float64)

# lower_costs_0.5
higher_costs_1 = np.full(128, 0.5, dtype=np.float64)
higher_costs_2 = np.full((128, 128), 0.5, dtype=np.float64)


# open dict
f = open("2018S2-90049P1-data/dict.txt")
my_dict = f.readlines()
f.close()
full_num_dict = {}
for i in range(25):
    full_num_dict[i] = []
for word in my_dict:
    if len(word) < 25:
        full_num_dict[len(word)].append(word.strip())
    
with open('dict_len.txt', 'w') as file:
    file.write(json.dumps(full_num_dict)) 

f_len_dict = open("dict_len.txt", "r")
f_len_dict_array = []
for lines in f_len_dict:
    f_len_dict_array.append(lines)
f_len_dict_array = json.loads(f_len_dict_array[0])


# init result dict
res_dict = {}

# open wiki files
f_mis = open("2018S2-90049P1-data/wiki_misspell.txt","r")
f_cor = open("2018S2-90049P1-data/wiki_correct.txt","r")

# store misspelled lines to array
f_mis_array = []
for line in f_mis:
    f_mis_array.append(line)
# store correct lines to array
f_cor_array = []
for line in f_cor:
    f_cor_array.append(line)
    
count = 0

# read wiki misspell file line by line
# for line in f_mis:
while count < 4453:
    string = f_mis_array[count].strip()
    bestv = 10000000
    bests = ""
    smallest_list = []
    # compare with dict lines
    for num in range(len(string)-2, len(string)+3):
        for word in f_len_dict_array[str(num)]:
   # for entry in my_dict:
        # string is lines in target doc
        # entry is lines in dict 
            thisv = dam_lev(string, word.strip(), insert_costs=higher_costs_1)
          #  thisv = editdistance.eval(string, word.strip())
            if (thisv > 0 and thisv < bestv):
                bestv = thisv
                bests = word.strip()
                smallest_list = [bests]
            elif (thisv == bestv):
                smallest_list.append(word.strip())

    print({"result_s": smallest_list, "distance": bestv, "match": f_cor_array[count].strip() in smallest_list, "original": f_cor_array[count].strip()})

    # save to res dict
    res_dict[string] = {"result_s": smallest_list, "distance": bestv, "match": f_cor_array[count].strip() in smallest_list, "original": f_cor_array[count].strip()}
    count += 1
    print("count",count)
    
# save result as json to file    
import json
with open('res_edit_distance_dam_insert.txt', 'w') as file:
    file.write(json.dumps(res_dict)) 
     
# evaluation
true_count = 0
count_all = 0
for res in res_dict:
    count_all += len(res_dict[res]['result_s'])
    if res_dict[res]['match']: true_count += 1   
    
with open('evaluation.txt', 'a') as file:
    # precision
    # recall
     file.write(json.dumps({"precision_edit_distance_dam_insert": (float(true_count) / count_all)})) 
     file.write(json.dumps({"recall_edit_distance_dam_insert":(float(true_count) / len(res_dict))})) 
     
print("precision - edit distance", (float(true_count) / count_all)) 
print("recall - edit distance", (float(true_count) / len(res_dict))) 

     

# accuracy
