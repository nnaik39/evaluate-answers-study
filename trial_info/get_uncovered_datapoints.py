import json 

covered_datapoints = json.load(open('covered_datapoints.json'))
all_answers = json.load(open('all_answers.json'))

# Make a new file with t

pilotexp = []

for item in all_answers:
    found = False 
    for datapoint in covered_datapoints:
        if (item['filename'] == datapoint['image'] and item['category'] == datapoint['context'] and item['question'] == datapoint['question']):
            found = True 
            break
    
    if (not found):
        pilotexp.append(item)

with open("new_pilot_exp.json", "w") as f:
    f.write(json.dumps(pilotexp, indent = 4))