import os
import pandas as pd

target_dir = os.path.join("data", "corpus", "processed")

subjects = os.listdir(target_dir)

word_num_pair = pd.read_csv(os.path.join("out", "word_num_pair", "grand_table.csv"))

for subject in subjects:
    for file in os.listdir(os.path.join(target_dir, subject)):
        if not file.endswith("wav"):
            continue
        os.rename(os.path.join(target_dir, subject, file), os.path.join(target_dir, subject, file.replace(" ", "")))
        word_num = int(file.split('-')[-1].removesuffix(".wav"))
        search_result = word_num_pair.loc[word_num_pair["Wordnum"] == word_num]
        if search_result.empty:
            continue
        Word = search_result["Word"].iloc[0]
        with open(os.path.join(target_dir, subject, file.replace("wav", "lab")), mode='w', encoding="utf-8") as lab:
            lab.writelines(' '.join(Word))
