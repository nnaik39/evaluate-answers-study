import scipy.stats
import json 
from statsmodels.stats.inter_rater import fleiss_kappa
import random 
import numpy as np

collected_datapoints = json.load(open('collected_datapoints.json'))
all_original_answers = json.load(open('all_answers.json'))
#pilot_exp = json.load(open('pilot_exp.json'))

all_q1_kappas = []
all_q2_kappas = []

num_covered = 0

random.seed(42)
data = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-evaluate-answers-study-export (11).json'))
coverage_number = 5

coverage_pair = {}

majority_count = {}

def most_common(lst):
    return max(set(lst), key=lst.count)

datapoint_vote = []

print("Number of collected datapoints: ", len(collected_datapoints))
num_points = 0

for point in collected_datapoints:
    if (point['image'] == 'images/house.jpeg' or point['image'] == 'images/hummingbird.jpeg'):
        continue

    if (len(point['q1']) < coverage_number):
        continue 

    print("Current point: ", point)

    num_points += 1

    print("Randomly sampling this point: ", point['q1'])

    print("Length: ", len(point['q1']))
    print("Coverage number: ", coverage_number)

    point['q1'] = random.sample(point['q1'], coverage_number)

    print("Point: ", point['q1'])

    counts = np.array([
    [point['q1'].count('correct'), point['q1'].count('idk'), point['q1'].count('wrong')]
    ])

    q1_kappa = fleiss_kappa(counts, method='uniform')

    point['q2'] = random.sample(point['q2'], coverage_number)

    print("Point[q2] ", point['q2'])
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

print("number of points covered: ", num_points)

print("Number of total points covered: ", len(all_q1_kappas))

print("Mean Fleiss Kappa: ", np.mean(np.array(all_q1_kappas)))
print("Mean Fleiss Kappa: ", np.mean(np.array(all_q2_kappas)))
print("Majority Count: ", majority_count)