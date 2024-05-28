import json 

data = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-evaluate-answers-study-export (10).json'))
pilot_exp = json.load(open('pilot_exp.json'))

all_original_answers = json.load(open('all_answers.json'))

coverage_pair = {}

for participant in data:
    for trial in data[participant]:
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

for (img, ctxt, q) in coverage_pair:
    pilot_exp_entry = {}
    
    ans = ""
    
    for answer in all_original_answers:
        if (answer['filename'] == img and answer['category'] == ctxt and answer['question'] == q):
            ans = answer['answer'] 

    for item in pilot_exp['images']:
        print("Item: ", item)
        if (item['filename'] == img and item['category'] == ctxt and item['question'] == q):
            pilot_exp_entry = item 

    if (len(coverage_pair[(img, ctxt, q)]) >= 5):
        num_covered += 1

#        print("Coverage pair: ", coverage_pair)

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

#for answer in all_original_answers:
 #   found = False 

#    for (img, ctxt, q) in coverage_pair:
 #       if (answer['filename'] == img and answer['category'] == ctxt and answer['question'] == q):
  #          found = True 

#    if (not found):
 #       new_pilot_exp['images'].append(answer)

print("Number fully covered: ", num_covered)

with open('collected_datapoints.json', 'w') as f:
    f.write(json.dumps(collected_datapoints, indent = 4))

with open('new_pilot_exp.json', 'w') as f:
    f.write(json.dumps(new_pilot_exp, indent = 4))