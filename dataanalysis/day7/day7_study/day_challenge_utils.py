import csv


def save_sample_csv(scores):
    with open('sample.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

# def load_scores_csv(path):