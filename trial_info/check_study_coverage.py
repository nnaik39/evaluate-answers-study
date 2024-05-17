import json 

data = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-evaluate-answers-study-export.json'))
pilot_exp = json.load(open('pilot_exp.json'))

all_original_experiments = json.load(open('all_answers.json'))

coverage_pair = {}

for participant in data:
    for trial in data[participant]:
        print("trial: ", trial)
        if ((trial['picture'], trial['category'], trial['question']) not in coverage_pair):
            coverage_pair[(trial['picture'], trial['category'], trial['question'])] = []
        coverage_pair[(trial['picture'], trial['category'], trial['question'])].append(trial['q1'])

new_pilot_exp = {}
new_pilot_exp['images'] = []

num_covered = 0

for (img, ctxt, q) in coverage_pair:
    pilot_exp_entry = {}
    
    for item in pilot_exp:
        if (item['filename'] == img and item['category'] == ctxt and item['question'] == q):
            pilot_exp_entry = item 

    if (len(coverage_pair[(img, ctxt, q)]) >= 3):
        print("Ratings for an answer fully covered!")
        print("image, ctxt, q: ", img, ctxt, q)
    else:
        new_pilot_exp['images'].append(pilot_exp_entry)

print("Number of answers covered: ", len(coverage_pair))
with open('new_pilot_exp.json', 'w') as f:
    f.write(json.dumps(new_pilot_exp, indent = 4))
        # Remove it from pilot_exp
# If an answer received more than 3 ratings, remove it from pilot_exp
# Then upload new_pilot_exp.json!
# 3 people seeing each answer