import splitfolders

input_folder = 'synth_dataset'
output_folder = 'synth_dataset_split'

splitfolders.ratio(input_folder, output=output_folder, seed=1337, ratio=(0.8, 0.1, 0.1))