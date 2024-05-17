import json 
import pandas as pd 

df = pd.read_csv('/Users/nanditanaik/Downloads/idefics_expanded_dataset_context_results.csv')

# Randomly select 200 rows from this

selected_rows = df.sample(n=200)

print(selected_rows)

pilot_exp = []

for idx, row in selected_rows.iterrows():
    pilot_exp.append({
        'filename': row['image'],
        'category': row['context'],
        'description': row['description'],
        'question': row['question'],
        'answer': row['generated_answer']
    })

with open('new_pilot_exp.json', 'w') as f:
    f.write(json.dumps(pilot_exp, indent = 4))