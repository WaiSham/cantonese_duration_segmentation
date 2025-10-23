import os

target_dir = os.path.join("data", "corpus", "processed")
lexicon_path = os.path.join("out", "dictionary", "lexicon.txt")
config_path = os.path.join("conf", "mfa_config.yaml")

path = os.listdir(target_dir)

for speaker in path:
    os.system(f"mfa validate --single_speaker --clean {os.path.join(target_dir, speaker)} {lexicon_path} --config_path {config_path}")