# Background
- the audio data should be separated into different speakers, each audio data should contain 2 chinese characters.
- the structure are as follow:
	- speaker (number)
		- session (if exists, only matters in copying stage)
			- audio datas with (wordnum) attached in the filename
- also provided .xlsx file storing wordnum and session respectively

## Steps to process the data
**Assumed working dir is outermost one (i.e. cantonese_duration_segmentation)**

0. assumed that you have conda (a virtual environment management tool), and python installed already
	- environment are stored in `env`. run `conda env create -f {your_path_to_the_environment}`
	- `base` environment might be needed for other code that does not have a required environment
	- run `conda activate base_roger` if needed

1. run `python src/read_xlsx.py` to obtain word_num to word pair csv.
	- requirement: please follow the format in `data/Stimuli_v2_23 Jan 2020.xlsx`

2. run `cp data/corpus/raw/Subject\ ${subject_number}/\*/\*.wav data/corpus/processed/Subject_${subject_number}` for all the Subjects
	- i.e. for each speaker, copy all the audio files under `processed/${your_speaker}`
	- rename the subject folder to remove space, this will helpful for the scripts afterwards

3. run `python src/create_lab.py` to make .lab speech script files containing space-separated string of words

4. run `python src/prepare_word_list.py` to generate **dictionary/words.txt** with unique characters and words

5. call `conda activate canto-cv-align` to run `python src/canto_g2p.py`
	- this will genereate all pronunciation in IPA form
	- the requirements are stored in **env** (a directory)
	- the code may run in relatively long time (couple of hours, 37h for ~29k words)
	- to save time, it is possible to manually append words and IPA in `dictionary/yue.tsv` to skip generation
	- use `screen` or `tmux` to run this in background to prevent interruption

6. call `conda activate aligner` to run `python src/valid_all.py` (if you wish to train a new model for alignment)
	- change training config: subset size to more than num of utterance per speaker if needed, defaults set to 20000

7. (optional) train a new model OR adapt to new data, and then align automatically
	- run `conda activate aligner`
	- then run `python train.py --mode {["train", "adapt"]} --pretrain_model_path {path_to_your_model}`
	- give pretrain acoustic model path in *adapt* mode
	- modify `conf/mfa_config.yaml` if needed in train/align mode
	- trained new model will be saved to `out/acoustic_model`
	- output alignment will be saved to `out/aligned_corpus`

8. align manually with given path (skip if you have done step 7)
	- run `conda activate aligner` to run `python src/train.py --mode align --pretrain_model_path {path_to_your_model}`
	- resolution is 5 ms per frame
	- output alignment will save to `out/aligned_corpus`

9. (optional) sampling
	- run `python src/alignment_sampling.py` to take sample from aligned results
	- use *praat* to read sampled files and see if there's anything unusual

10. get statistics
	- run `python src/obtain_stat.py` to get csv file of alignment
	- the code only works for 2 characters word only, let me know if needed to scale up