import json 

data = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-evaluate-answers-study-export (15).json'))
pilot_exp = json.load(open('pilot_exp.json'))

all_original_answers = json.load(open('all_answers.json'))

coverage_pair = {}

for participant in data:
    for trial in data[participant]:
        include = True 

        for trial in data[participant]:
            if (trial['picture'] == 'house.jpeg') and (trial['question'] == 'What is behind the cottage?'):
                if (trial['q1'] != 'correct' and trial['q2'] != 'image_required'):
                    include = False 
        
            if (trial['picture'] == 'hummingbird.jpeg' and 'answer' not in trial):
                if (trial['q1'] != 'correct' and trial['q2'] != 'image_required'):
                    include = False 

            if (trial['picture'] == 'hummingbird.jpeg' and 'answer' in trial):
                if (trial['q1'] != 'wrong' and trial['q2'] != 'image_required'):
                    include = False

        if (not include):
            print("Excluding based on attention checks")
            continue 

        if ((trial['picture'], trial['category'], trial['question']) not in coverage_pair):
            coverage_pair[(trial['picture'], trial['category'], trial['question'])] = []
        coverage_pair[(trial['picture'], trial['category'], trial['question'])].append([trial['q1'], trial['q1OtherValue'], trial['q2'], trial['q2OtherValue']])

        if (trial['comments'] != ''):
            print(trial['comments'])

        if (trial['glb_comments'] != ''):
            print(trial['glb_comments'])
    
new_pilot_exp = {}
new_pilot_exp['images'] = []

num_covered = 0

collected_datapoints = []

coverage_number = 5

for (img, ctxt, q) in coverage_pair:
    pilot_exp_entry = {}
    
    ans = ""

#    print("Number covered: ", len(coverage_pair[(img, ctxt, q)]))
    
    for answer in all_original_answers:
        if (answer['filename'] == img and answer['category'] == ctxt and answer['question'] == q):
            ans = answer['answer'] 

    for item in pilot_exp['images']:
        if (item['filename'] == img and item['category'] == ctxt and item['question'] == q):
            pilot_exp_entry = item 

    print("Coverage pair: ", len(coverage_pair[(img, ctxt, q)]))
    print("Pilot exp entry: ", pilot_exp_entry)

    if (len(coverage_pair[(img, ctxt, q)]) >= 5):
        num_covered += 1

        q1_answers = []
        q1_other = []
        q2_answers = []
        q2_other = []

        for i in range(0, len(coverage_pair[(img, ctxt, q)])):
            q1_answers.append(coverage_pair[(img, ctxt, q)][i][0])
            q1_other.append(coverage_pair[(img, ctxt, q)][i][1])
            q2_answers.append(coverage_pair[(img, ctxt, q)][i][2])
            q2_other.append(coverage_pair[(img, ctxt, q)][i][3])

        collected_datapoints.append({
                'image': img,
                'context': ctxt,
                'question': q,
                'answer': ans,
                'q1': q1_answers,
                'q1_other': q1_other,
                'q2': q2_answers,
                'q2_other': q2_other
        })
    else:
        new_pilot_exp['images'].append(pilot_exp_entry)

for entry in pilot_exp['images']:
    found = False 

    for (img, ctxt, q) in coverage_pair:
        print("Entry: ", entry)
        print("Img: ", img)
        print("Ctxt: ", ctxt)
        print("Question: ", q)
        if (entry['filename'] == img and entry['category'] == ctxt and entry['question'] == q):
            found = True 
    if (not found):
        new_pilot_exp['images'].append(pilot_exp_entry)

with open('new_pilot_exp.json', 'w') as f:
    f.write(json.dumps(new_pilot_exp, indent = 4))

for answer in all_original_answers:
    found = False 

    print("Length of coverage pair: ", len(coverage_pair[(img, ctxt, q)]))
    for (img, ctxt, q) in coverage_pair:
        if (answer['filename'] == img and answer['category'] == ctxt and answer['question'] == q):
            found = True 

    if (found and len(coverage_pair[(img, ctxt, q)])):
        print("Length of coverage pair: ", len(coverage_pair[((img, ctxt, q))]))
        if (len(coverage_pair[(img, ctxt, q)]) < 5):
            new_pilot_exp['images'].append(answer)
    if (found):
        new_pilot_exp['images'].append(answer)        
#    elif (not found):
 #           new_pilot_exp['images'].append(answer)

print("Number fully covered: ", num_covered)

with open('collected_datapoints_new.json', 'w') as f:
    f.write(json.dumps(collected_datapoints, indent = 4))

with open('new_pilot_exp.json', 'w') as f:
    f.write(json.dumps(new_pilot_exp, indent = 4))