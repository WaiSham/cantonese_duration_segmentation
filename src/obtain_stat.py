import os
import pandas as pd
import textgrid

TARGET_TIER = 0 # word tier

textgrid_dir = os.path.join("out", "aligned_corpus")
# textgrid_dir = "./alignment_samples" # ? for testing
stat_dir = os.path.join("out", "alignment_statistics")

word_num_table_dir = os.path.join("out", "word_num_pair", "grand_table.csv")
WORD_TABLE = pd.read_csv(word_num_table_dir)

def wordnum_strip(filename):
    """return wordnum from given filename"""
    wordnum = int(filename.split("-")[-1].replace(".TextGrid", ""))
    return wordnum

def get_word_from_wordnum(wordnum):
    try:
        return WORD_TABLE.query(f"Wordnum == {wordnum}")["Word"].values[0]
    except:
        print(f"Error in finding word with wordnum {wordnum}.")
        return None
    
def main():
    os.makedirs(stat_dir, exist_ok=True)

    for speaker in os.listdir(textgrid_dir):
        if not os.path.isdir(os.path.join(textgrid_dir, speaker)):
            continue

        df = pd.DataFrame(columns=["filename", "word", "wordnum", "syl 1 onset", "syl 1 offset", "syl 1 duration", "syl 2 onset", "syl 2 offset", "syl 2 duration", "word duration with pause", "word duration", "pause duration"])
        for file in os.listdir(os.path.join(textgrid_dir, speaker)):
    
            if not file.__contains__(".TextGrid"):
                continue

            audio_entry = []

            tg = textgrid.TextGrid()
            tg.read(os.path.join(textgrid_dir, speaker, file))
            target_tier = tg.tiers[TARGET_TIER]

            wordnum = wordnum_strip(file)
            word = get_word_from_wordnum(wordnum)
            
            audio_entry.append(file.replace("TextGrid", "wav"))
            audio_entry.append(wordnum)
            audio_entry.append(word)

            for i in range(len(target_tier)):
                interval = target_tier[i]
                if interval.mark == '':
                    continue
                audio_entry.append(interval.minTime)
                audio_entry.append(interval.maxTime)
                audio_entry.append(round(interval.maxTime - interval.minTime, 3))

            # calulate durations
            word_duration_with_pause = audio_entry[7] - audio_entry[3]
            pause_duration = (audio_entry[6] - audio_entry[4])
            word_duration = word_duration_with_pause - pause_duration

            audio_entry.append(round(word_duration_with_pause, 3))
            audio_entry.append(round(word_duration, 3))
            audio_entry.append(round(pause_duration, 3))

            df.loc[-1] = audio_entry
            df.index += 1
            df = df.sort_index()

        df = df.sort_values(by=["filename"])
        df.to_csv(f"{os.path.join(stat_dir, speaker + ".csv")}", index=False, encoding="utf-8")

if __name__ == "__main__":
    main()