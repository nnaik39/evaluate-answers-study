import scipy.stats
import json 
from statsmodels.stats.inter_rater import fleiss_kappa
import random 
import numpy as np

data = json.load(open('collected_datapoints.json'))
all_original_answers = json.load(open('all_answers.json'))
pilot_exp = json.load(open('pilot_exp.json'))

all_q1_kappas = []

all_q2_kappas = []

num_covered = 0

# house, "What is behind the cottage?"
# hummingbird, "Is the hummingbird drinking from the flower?"
# hummingbird, "Is there a flower in the image?"

# TODO: Perform exclusions based on the attention checks
# Check based on which hummingbird question it was

random.seed(42)
data = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-evaluate-answers-study-export (8).json'))

coverage_pair = {}

included_participants = []

for participant in data:
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

    if (include):
        included_participants.append(participant)

for participant in data:
    if (participant in included_participants):
        for trial in data[participant]:
            if ((trial['picture'], trial['category'], trial['question']) not in coverage_pair):
                coverage_pair[(trial['picture'], trial['category'], trial['question'])] = []
            coverage_pair[(trial['picture'], trial['category'], trial['question'])].append([trial['q1'], trial['q1OtherValue'], trial['q2'], trial['q2OtherValue']])

            if (trial['comments'] != ''):
                print(trial['comments'])

            if (trial['glb_comments'] != ''):
                print(trial['glb_comments'])

collected_datapoints = []

for (img, ctxt, q) in coverage_pair:
    pilot_exp_entry = {}
    
    ans = ""
    
    for answer in all_original_answers:
        if (answer['filename'] == img and answer['category'] == ctxt and answer['question'] == q):
            ans = answer['answer'] 

    for item in pilot_exp['images']:
        if (item['filename'] == img and item['category'] == ctxt and item['question'] == q):
            pilot_exp_entry = item 

    if (len(coverage_pair[(img, ctxt, q)]) >= 3):
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

#print("Number fully covered: ", num_covered)
#print("Length of collected datapoints: ", len(collected_datapoints))

# number where the majority voted it correct
# number where the majority voted it wrong
# number where the majority voted 'idk'

majority_count = {}

def most_common(lst):
    return max(set(lst), key=lst.count)

for point in collected_datapoints:
    if (point['image'] == 'hummingbird.jpeg' or point['image'] == 'house.jpeg'):
        continue

    if (len(point['q1']) < 7):
        continue 

    point['q1'] = random.sample(point['q1'], 3)

    print("Point: ", point['q1'])

    counts = np.array([
    [point['q1'].count('correct'), point['q1'].count('idk'), point['q1'].count('wrong')]
    ])

#    print("Counts: ", counts)

    q1_kappa = fleiss_kappa(counts, method='uniform')

    point['q2'] = random.sample(point['q2'], 3)

    counts = np.array([
    [point['q2'].count('image_required'), point['q2'].count('image_not_required')]
    ])

    q2_kappa = fleiss_kappa(counts, method='uniform')

    maj_rating = most_common(point['q1'])

    if (maj_rating not in majority_count):
        majority_count[maj_rating] = 0
    majority_count[maj_rating] += 1
#    print("Q1 kappa: ", q1_kappa)

    maj_rating = most_common(point['q2'])

    if (maj_rating not in majority_count):
        majority_count[maj_rating] = 0
    majority_count[maj_rating] += 1

    if (q1_kappa != q1_kappa):
        continue 

    if (q2_kappa != q2_kappa):
        print("Excluding because NaN")
        continue 

    all_q2_kappas.append(q2_kappa)
    all_q1_kappas.append(q1_kappa)

print("Mean Fleiss Kappa: ", np.mean(np.array(all_q1_kappas)))
print("Mean Fleiss Kappa: ", np.mean(np.array(all_q2_kappas)))
print("Majority Count: ", majority_count)