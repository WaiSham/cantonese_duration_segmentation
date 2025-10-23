import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

def cleanup_directory(dir_path):
    """Clean up the target directory if it exists"""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)

def get_subject_files(aligned_corpus_path):
    """Get files grouped by subject"""
    subject_files = defaultdict(list)
    
    # Walk through all Subject directories
    for subject_dir in Path(aligned_corpus_path).glob('Subject_*'):
        textgrid_files = list(subject_dir.glob('*.TextGrid'))
        subject_files[subject_dir.name] = textgrid_files
        
    return subject_files

def get_corresponding_wav(textgrid_file, processed_dir):
    """Get corresponding .wav file path from processed directory"""
    subject_name = textgrid_file.parent.name
    wav_name = textgrid_file.stem + '.wav'
    return Path(processed_dir) / subject_name / wav_name

def sample_and_copy_files(n_samples):
    """Sample n pairs of files from each subject and copy to alignment_samples"""

    #! path config
    aligned_corpus_path = os.path.join("out", "aligned_corpus")
    processed_dir = os.path.join("data", "corpus", "processed")
    sample_dir = os.path.join("out", "alignment_samples")

    os.makedirs(sample_dir, exist_ok=True)
    
    # Clean up sample directory
    cleanup_directory(sample_dir)
    
    # Get files grouped by subject
    subject_files = get_subject_files(aligned_corpus_path)
    
    # Create directories for samples
    for subject in subject_files.keys():
        os.makedirs(os.path.join(sample_dir, subject), exist_ok=True)
    
    # Sample and copy files for each subject
    for subject, textgrid_files in subject_files.items():
        if len(textgrid_files) < n_samples:
            print(f"Warning: Subject {subject} has fewer than {n_samples} files. Skipping.")
            continue
            
        # Randomly sample files
        selected_textgrids = random.sample(textgrid_files, n_samples)
        
        for textgrid_file in selected_textgrids:
            # Get corresponding wav file
            wav_file = get_corresponding_wav(textgrid_file, processed_dir)
            
            if not wav_file.exists():
                print(f"Warning: No matching WAV file for {textgrid_file.name}")
                continue
                
            # Copy files to sample directory
            shutil.copy2(
                textgrid_file, 
                os.path.join(sample_dir, subject, textgrid_file.name)
            )
            shutil.copy2(
                wav_file, 
                os.path.join(sample_dir, subject, wav_file.name)
            )
            # print(f"Copied pair: {textgrid_file.name} and {wav_file.name}")

def main():
    while True:
        try:
            n_samples = int(input("Enter number of samples to take from each subject: "))
            if n_samples <= 0:
                print("Please enter a positive number")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    sample_and_copy_files(n_samples)
    print("Sampling completed!")

if __name__ == "__main__":
    main()