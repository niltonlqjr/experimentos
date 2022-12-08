import yaml as yl
import argparse


parser = argparse.ArgumentParser(description='do the union yaml passes files')
parser.add_argument('input_files',
                    nargs='+',
                    help='files that will be merged')
parser.add_argument('--output','-o',
                    default='passes_merged.yaml',
                    help='output')

args=parser.parse_args()

input_files = args.input_files
output = args.output


full_passes_set = set()

for filename in input_files:
    with open(filename) as f:
        passes = yl.safe_load(f)
    full_passes_set = full_passes_set | set(passes) # full_passes = full_passes U passes


full_passes = list(full_passes_set)

with open(output,'w') as f:
    yl.dump(full_passes,f)
