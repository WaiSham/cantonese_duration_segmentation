import os
import argparse
import warnings


args = argparse.ArgumentParser()
args.add_argument("--mode", type=str, default=None, choices=["train", "adapt", "align"], help="Mode: train a new model or adapt an existing model")
args.add_argument("--pretrain_model_path", type=str, default=None, help="Path to the pretrained model for adaptation")

opts = args.parse_args()

if not opts.mode in ["train", "adapt", "align"]:
    raise ValueError("Invalid mode. Choose either 'train', 'adapt' or 'align'.")

if not os.path.exists(os.path.join("out", "aligned_corpus")):
    os.makedirs(os.path.join("out", "aligned_corpus"))

config_dir = os.path.join("conf", "mfa_config.yaml")
output_dir = os.path.join("out", "aligned_corpus")
output_model_path = os.path.join("out", "acoustic_model", "canto_acoustic_model.zip")
dict_path = os.path.join("dictionary", "lexicon.txt")
corpus_path = os.path.join("data", "corpus", "processed")

if opts.mode == "train":
    if opts.pretrain_model_path:
        warnings.warn("Pretrained model path will be ignored in training mode.")
    os.system(f"mfa train --clean --use_postgres -c {config_dir} --output_directory {output_dir} {corpus_path} {dict_path} {output_model_path}")
elif opts.mode == "adapt":
    if not opts.pretrain_model_path:
        raise ValueError("Pretrained model path must be provided for adaptation.")
    os.system(f"mfa train --clean --use_postgres -c {config_dir} --output_directory {output_dir} {corpus_path} {dict_path} {opts.pretrain_model_path} {output_model_path}")
else:  # align mode
    if not opts.pretrain_model_path:
        raise ValueError("Pretrained model path must be provided for alignment.")
    os.system(f"mfa align --clean --use_mp --use_postgres {corpus_path} {dict_path} {opts.pretrain_model_path} {output_dir}")