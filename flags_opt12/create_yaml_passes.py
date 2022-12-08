import yaml as yl
import argparse

parser = argparse.ArgumentParser(description='receives a text file with opt -debug-pass=Arguments and convert it into a yaml containing all passes there')

parser.add_argument('input_file',
                    help='output from opt -debug-pass=Arguments')
parser.add_argument('--output','-o',
                    default='passes.yaml',
                    help='output file')

args = parser.parse_args()
input_file = args.input_file
output=args.output

with open(input_file) as f:
    opt_text = f.read()

only_passes=opt_text.replace('Pass Arguments:', '') 
lines=only_passes.split('\n')
all_passes_str = ' '.join(lines)
all_passes_list = all_passes_str.split()

with open(output,'w') as f:
    yl.dump(all_passes_list,f)
