#! /bin/python

import argparse
import os, subprocess
import yaml as yl
import csv

def read_sequences(data):
    return data['sequences']


def run_wularus(bench_dir, compiler, sequence, workset, IR_filename, outpath, cost_kind, path_to_llvm_bin, path_to_wularus_lib):
    cur_dir = os.getcwd()
    os.chdir(bench_dir + '/src')
    cmd = f'./compile.sh {compiler} "{sequence}" {workset} 1'
    print(cmd)
    os.system(cmd)
    # Make paths absolute, since we changed dir.
    if not os.path.isabs(path_to_wularus_lib):
        path_to_wularus_lib = os.path.join(cur_dir, path_to_wularus_lib)
    if not os.path.isabs(path_to_llvm_bin):
        path_to_llvm_bin = os.path.join(cur_dir, path_to_llvm_bin)
    if not os.path.isabs(outpath):
        outpath = os.path.join(cur_dir, outpath)
    os.system(f'{path_to_llvm_bin}/opt -load-pass-plugin {path_to_wularus_lib} -passes=prediction_pass -disable-output {IR_filename} --prediction-cost-kind {cost_kind} 2> {outpath}')
    os.system(f'make -f Makefile.{compiler} cleanup')
    os.chdir(cur_dir)
    outfile = open(outpath, "r")
    analysis_list = list(csv.reader(outfile, delimiter=":"))
    outfile.close()
    analysis_dict = {}
    analysis_dict[analysis_list[0][0]] = analysis_list[0][1].strip() # Cost kind.
    analysis_dict[analysis_list[1][0]] = float(analysis_list[1][1]) # Total cost.
    # Demangle function names with 'llvm-cxxfilt'.
    for line in analysis_list[2:]:
        p = subprocess.Popen(f'{path_to_llvm_bin}/llvm-cxxfilt {line[0]}',
                             stdout=subprocess.PIPE, shell=True)
        demangled_fname = p.communicate()[0][:-1].decode('utf-8').strip()
        analysis_dict[demangled_fname] = float(line[1])
    return analysis_dict


parser=argparse.ArgumentParser(description='extract ir2vec vectors and store in a yaml file')
parser.add_argument('bench_dir',
                    type=str,
                    help='benchmark directory (must contain src/compile.sh)')
parser.add_argument('sequences_file',
                    type=str,
                    help='file contaning optimization sequences')
parser.add_argument('path_to_llvm_bin',
                    type=str,
                    help='absolute path to llvm/bin (version 15 required)')
parser.add_argument('path_to_wularus_lib',
                    type=str,
                    help='absolute path to wularus llvm plugin (libpredictionpass.so)')
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
args=parser.parse_args()

bench_dir = args.bench_dir
sequences_file = args.sequences_file
path_to_llvm_bin = args.path_to_llvm_bin
path_to_wularus_lib = args.path_to_wularus_lib
output_file = args.output_file
compiler = args.compiler
workset = args.workset
IR_filename = args.IR_filename

try:
    with open(sequences_file) as f:
        sequences_data = yl.safe_load(f)
    #read sequences from the file
    sequences=read_sequences(sequences_data)
except:
    print('Error opening sequences file\Running wularus with default optimization levels')
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
#print(output_file) # ../results/wularus/spec2006/astar.yaml

outdir = output_file + '.dir'
os.system(f'mkdir {outdir}')
for s in sequences:
    output[s] = {}
    output[s]['sequence'] = sequences[s]
    seq_str=' '.join(sequences[s])
    for cost_kind in ['latency', 'recipthroughput', 'codesize']:
        analysis_filename=f'{cost_kind}_{s}.csv'
        outpath = os.path.join(outdir, analysis_filename)
#        output[s][cost_kind] = run_wularus(bench_dir, compiler, seq_str, workset, IR_filename, outpath, cost_kind, path_to_llvm_bin, path_to_wularus_lib)
        output[s][cost_kind] = run_wularus(bench_dir, compiler, seq_str, workset, IR_filename, outpath, cost_kind, path_to_llvm_bin, path_to_wularus_lib)
os.system(f'rm -r {outdir}')

data = {}
data['metodology'] = {}
data['metodology']['compiler']=compiler
data['metodology']['workset']=workset
data['data'] = output

with open(output_file,'w') as f:
    yl.dump(data,f)
