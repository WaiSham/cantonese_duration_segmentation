import pandas as pd
import os

word_num_pair = pd.read_csv(os.path.join("out", "word_num_pair", "grand_table.csv"))
word_list = word_num_pair["Word"].to_list()

concat_words = "".join(word_list)
unique_chara = "".join(dict.fromkeys(concat_words))

print(f"length of characters in all words: {len(concat_words)}")
print(f"length of unique characters: {len(unique_chara)}")

os.makedirs(os.path.join("out", "dictionary"), exist_ok=True)

with open(os.path.join("out", "dictionary", "words.txt"), mode='w') as f:
    for char in unique_chara:
        f.writelines(char+'\n')
    for word in word_list:
        f.writelines(word+'\n')