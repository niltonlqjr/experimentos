#! /bin/python

import argparse
import os
import yaml as yl
import csv

def read_sequences(data):
    return data['sequences']


def run_gprof(bench_dir, compiler, sequence, workset, IR_filename, relpath):
    cur_dir = os.getcwd()
    outpath = cur_dir + "/" + relpath
    os.chdir(bench_dir + '/src')
    cmd = f'./compile.sh {compiler} "{sequence}" {workset} 1'
    print(cmd)
    os.system(cmd)
#    os.system(f'clang++ -pg {IR_filename} -o a.gprof.out')
    os.system(f'./get_gprof_data.sh program_o.bc test {outpath}')
    os.system(f'make -f Makefile.{compiler} cleanup')
    os.chdir(cur_dir)
    gfile = open(outpath, "r")
    gprof_analysis = list(csv.reader(gfile, delimiter="/"))
    gfile.close()
#    print(gprof_analysis)
    analysis_dict = {}
    for line in gprof_analysis:
        analysis_dict[line[3]] = {}
        analysis_dict[line[3]]['% time'] = line[0]
        analysis_dict[line[3]]['cumulative seconds'] = line[1]
        analysis_dict[line[3]]['self seconds'] = line[2]
    return analysis_dict


parser=argparse.ArgumentParser(description='extract ir2vec vectors and store in a yaml file')
parser.add_argument('bench_dir',
                    type=str,
                    help='benchmark directory (must contain src/compile.sh)')
parser.add_argument('sequences_file',
                    type=str,
                    help='file contaning optimization sequences')
parser.add_argument('--output-file', '-o',
                    dest='output_file',
                    default='output.yaml',
                    help='output filename')
parser.add_argument('--compiler','-c',
                    dest='compiler',
                    default='opt',
                    help='compiler used')
parser.add_argument('--workset',
                    dest='workset',
                    default='0',
                    help='workset used from benchmarks that determine workset on compile time')
parser.add_argument('--IR-filename',
                    dest='IR_filename',
                    default='program_o.bc',
                    help='filename of the full prgram llvm IR (used as argument to ir2vec)')
parser.add_argument('--runs',
                    dest='runs',
                    default=10,
                    type=int,
                    help='how many times to run each with each sequence')
args=parser.parse_args()

bench_dir = args.bench_dir
sequences_file = args.sequences_file
output_file = args.output_file
compiler = args.compiler
workset = args.workset
IR_filename = args.IR_filename
runs = args.runs

try:
    with open(sequences_file) as f:
        sequences_data = yl.safe_load(f)
    #read sequences from the file
    sequences=read_sequences(sequences_data)
except:
    print('Error opening sequences file\Running gprof with default optimization levels')
    sequences={0:['-O0'],
               1:['-O1'],
               2:['-O2'],
               3:['-O3'],
               4:['-Os'],
               5:['-Oz']}
    #definir um formato para as sequencias
output = {}
#print(bench_dir) # ../benchmarks/cpu2006/astar
#print(sequences_file) # ../results/sequences/spec2006/astar.yaml
#print(output_file) # ../results/gprof/spec2006/astar.yaml

outdir = output_file + '.dir'
os.system(f'mkdir {outdir}')
for s in sequences:
    output[s] = {}
    output[s]['sequence'] = sequences[s]
    for run in range(runs):
        print(s)
        analysis_filename=f'{s}_{run}.csv'
        seq_str=' '.join(sequences[s])
        output[s][run] = {}
        outpath = os.path.join(outdir, analysis_filename)
        output[s][run]['gprof data'] = run_gprof(bench_dir, compiler, seq_str, workset, IR_filename, outpath)
os.system(f'rm -r {outdir}')

data = {}
data['metodology'] = {}
data['metodology']['compiler']=compiler
data['metodology']['workset']=workset
data['metodology']['runs']=runs
data['data'] = output

with open(output_file,'w') as f:
    yl.dump(data,f)
