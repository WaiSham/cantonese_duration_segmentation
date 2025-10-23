import pandas as pd
import argparse
import os

pd.options.mode.copy_on_write = True

TOTAL_SESSIONS = 3
SETS_PER_SESSION = 9

# add argument to specify input excel file
parser = argparse.ArgumentParser(description="Process excel file to generate word-num pairs.")
parser.add_argument("--input", type=str, default="data/Stimuli_v2_23 Jan 2020.xlsx", help="Path to the input excel file.")
args = parser.parse_args()

excel = pd.read_excel(args.input, sheet_name=0)

os.makedirs(os.path.join("out", "word_num_pair"), exist_ok=True)

big_df = pd.DataFrame()

for session_num in range(1, 1 + TOTAL_SESSIONS):
    for set_num in range(1, 1 + SETS_PER_SESSION):

        session = excel[excel["Session"] == session_num]
        set_name = f"Set {set_num}"

        target_col = session.columns.get_loc(set_name)

        word_num_pair = session.iloc[ : , [target_col, target_col+1]]
        word_num_pair[set_name] = word_num_pair[set_name].astype(int)

        sorted = word_num_pair.sort_values(by=set_name)
        sorted.columns = ["Wordnum", "Word"]

        sorted["Session"] = session_num
        sorted["Set"] = set_num

        sorted.to_csv(os.path.join("out", "word_num_pair", f"session{session_num}_set{set_num}.csv"), index=None)

        big_df = pd.concat([big_df, sorted], ignore_index=True)
    

big_sorted = big_df.sort_values(by=["Wordnum"])
big_sorted.to_csv(os.path.join("out", "word_num_pair", "grand_table.csv"), index=None)