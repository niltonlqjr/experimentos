import argparse
import os
import csv
import yaml as yl


def read_perf_csv(filename,PCs):
    try:
        ret={}
        print(filename)
        with open(filename) as f:
            data=csv.reader(f)
            for row in data:
                if len(row) > 3:
                    PC_name=row[2]
                    if PC_name in PCs:
                        try:
                            ret[PC_name] = float(row[0])
                        except:
                            ret[PC_name] = None
    except:
        ret = {}
    return ret


def read_PCs(bench_dir, compiler, sequence,
             PCs_lists, workset_compile, workset_run,
             perf_csv,runs):
    cur_dir=os.getcwd()
    str_seq=' '.join(sequence)
    os.chdir(bench_dir)
    compile_cmd = f'./compile.sh {compiler} "{str_seq}" {workset_compile} 1'
    print(compile_cmd)
    os.system(compile_cmd)
    ret=[]
    for i in range(runs):
        PCs={}
        for PCs_list in PCs_lists:
            PCs_string = ','.join(PCs_list)
            run_cmd=f'./get_performance_counters.sh "{PCs_string}" {workset_run} {perf_csv}'
            print(run_cmd)
            os.system(run_cmd)
            PC=read_perf_csv(perf_csv,PCs_list)
            PCs.update(PC)
        ret.append(PCs)
        

    os.system(f'rm {perf_csv}')
    os.system(f'make -f Makefile.{compiler} cleanup')
    os.chdir(cur_dir)

    return ret


parser=argparse.ArgumentParser(description='extract performace counters and store in a yaml file')
parser.add_argument('bench_dir',
                    type=str,
                    help='benchmark direcotry (must contain compile.sh and get_performance_counters.sh)')
parser.add_argument('sequences_file',
                    type=str,
                    help='file contaning optimization sequences')
parser.add_argument('--PC-files', '-f',
                    dest='PC_files',
                    default='',
                    type=str,
                    nargs='+',
                    help='yaml files containig performance counters to extract'
                    +'(each file will do their own runs)')
parser.add_argument('--runs', '-r',
                    dest='runs',
                    default=10,
                    type=int,
                    help='number of executions for each sequence')
parser.add_argument('--output-file', '-o',
                    dest='output_file',
                    default='output.yaml',
                    help='output filename')
parser.add_argument('--compiler','-c',
                    dest='compiler',
                    default='opt',
                    help='compiler used')
parser.add_argument('--workset-run',
                    dest='workset_run',
                    default='test',
                    help='workset used from benchmarks that determine workset on run time')
parser.add_argument('--workset-compile',
                    dest='workset_compile',
                    default='0',
                    help='workset used from benchmarks that determine workset on compile time')
parser.add_argument('--perf-output',
                    dest='perf_output',
                    default='output.perf.tmp.csv',
                    help='filename of output for perf (this is a temporary file and will be deleted after its use)')
args=parser.parse_args()

bench_dir = args.bench_dir
sequences_file = args.sequences_file
PC_files = args.PC_files
output_file = args.output_file
compiler = args.compiler
workset_run = args.workset_run
workset_compile = args.workset_compile
perf_output = args.perf_output
runs = args.runs


try:
    with open(sequences_file) as f:
        sequences_data = yl.safe_load(f)
    sequences = sequences_data['sequences']
except:
    print('Error opening sequences file\nExtracting with default optimization levels')
    sequences={0:['-O0'],
               1:['-O1'],
               2:['-O2'],
               3:['-O3'],
               4:['-Os'],
               5:['-Oz']}

try:
    PCs_lists=[]
    for PC_file in PC_files:
        with open(PC_file) as f:
            PCs=yl.safe_load(f)
            PCs_lists.append(PCs)
except:
    print('Error opening performance counters file\n Extracting only instructions:u')
    PCs_lists = [['instructions:u']]

output={}

for s in sequences:
    output[s]={}
    output[s]['sequence'] = sequences[s]
    output[s]['PCs'] = read_PCs(bench_dir,compiler,sequences[s],PCs_lists,
                    workset_compile,workset_run,perf_output,runs)

data = {}
data['metodology']={}
data['metodology']['compiler'] = compiler
data['metodology']['run workset'] = workset_run
data['metodology']['compile workset'] = workset_compile
data['metodology']['PCs list'] = PCs_lists
data['metodology']['number of runs'] = runs

data['PCs'] = output

with open(output_file,'w') as f:
    yl.dump(data,f)