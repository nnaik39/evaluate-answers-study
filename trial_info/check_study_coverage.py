import json 

data = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-evaluate-answers-study-export (2).json'))
pilot_exp = json.load(open('pilot_exp.json'))

all_original_answers = json.load(open('all_answers.json'))

coverage_pair = {}

for participant in data:
    for trial in data[participant]:
        if ((trial['picture'], trial['category'], trial['question']) not in coverage_pair):
            coverage_pair[(trial['picture'], trial['category'], trial['question'])] = []
        coverage_pair[(trial['picture'], trial['category'], trial['question'])].append(trial['q1'])

        if (trial['comments'] != ''):
            print(trial['comments'])
        if (trial['glb_comments'] != ''):
            print(trial['glb_comments'])

new_pilot_exp = {}
new_pilot_exp['images'] = []

num_covered = 0

for (img, ctxt, q) in coverage_pair:
    pilot_exp_entry = {}
    
    for item in pilot_exp['images']:
        if (item['filename'] == img and item['category'] == ctxt and item['question'] == q):
            pilot_exp_entry = item 

    if (len(coverage_pair[(img, ctxt, q)]) >= 3):
        num_covered += 1
    else:
        new_pilot_exp['images'].append(pilot_exp_entry)

for answer in all_original_answers:
    # If it's not in the coverage pair, then add it!
    found = False 

    for (img, ctxt, q) in coverage_pair:
        if (answer['filename'] == img and answer['category'] == ctxt and answer['question'] == q):
            found = True 

    if (not found):
        new_pilot_exp['images'].append(answer)

print("Number fully covered: ", num_covered)

with open('new_pilot_exp.json', 'w') as f:
    f.write(json.dumps(new_pilot_exp, indent = 4))