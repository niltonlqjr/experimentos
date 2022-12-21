import argparse
import os
import yaml as yl


def read_sequences(data):
    return data['sequences']
    

def read_embedding_from_file(file):
    try:
        with open(file) as f:
            data = f.read()
        ret = [float(x) for x in data.split()]
        if len(ret) != 300:
            print('error reading output file, vector dimension different from 300')
            exit(0)
    except:
        ret = []
    return ret

def read_ir2vec_embeeding(bench_dir, compiler, sequence, 
                          workset, ir2vec_cmd_line, 
                          ir2vec_output, IR_filename):
    cur_dir = os.getcwd()
    os.chdir(bench_dir)
    cmd = f'./compile.sh {compiler} "{sequence}" {workset} 1'
    print(cmd)
    os.system(cmd)
    ir2vec_cmd_line += f' -o={ir2vec_output} {IR_filename}'
    os.system(ir2vec_cmd_line)
    emb = read_embedding_from_file(ir2vec_output)
    os.system(f'rm {ir2vec_output}')
    os.system(f'make -f Makefile.{compiler} cleanup')
    os.chdir(cur_dir)
    return emb


parser=argparse.ArgumentParser(description='extract ir2vec vectors and store in a yaml file')
parser.add_argument('bench_dir',
                    type=str,
                    help='benchmark direcotry (must contain compile.sh)')
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
parser.add_argument('--ir2vec-cmd',
                    dest='ir2vec_cmd',
                    default='ir2vec',
                    type=str,
                    help='command to run ir2vec')
parser.add_argument('--ir2vec-vocab',
                    dest='ir2vec_vocab',
                    default='/IR2Vec/vocabulary/seedEmbeddingVocab-300-llvm12.txt',
                    type=str,
                    help='ir2vec vocabulary file fullpath')
parser.add_argument('--ir2vec-flags',
                    dest='ir2vec_flags',
                    default='--fa --level=p',
                    type=str,
                    help='ir2vec additional flags')
parser.add_argument('--ir2vec-output',
                    dest='ir2vec_output',
                    default='output.ir2vec.tmp',
                    help='filename of output for ir2vec (this is a temporary file and will be deleted after its use)')
args=parser.parse_args()

bench_dir = args.bench_dir
sequences_file = args.sequences_file
output_file = args.output_file
compiler = args.compiler
workset = args.workset
IR_filename = args.IR_filename
ir2vec_cmd = args.ir2vec_cmd
ir2vec_vocab = args.ir2vec_vocab
ir2vec_flags = args.ir2vec_flags
ir2vec_output = args.ir2vec_output

try:
    with open(sequences_file) as f:
        sequences_data = yl.safe_load(f)
    #read sequences from the file
    sequences=read_sequences(sequences_data)
except:
    print('Error opening sequences file\nExtracting IR2Vec with default optimization levels')
    sequences={0:['-O0'],
               1:['-O1'],
               2:['-O2'],
               3:['-O3'],
               4:['-Os'],
               5:['-Oz']}
    #definir um formato para as sequencias
print(sequences)
ir2vec_line = f'{ir2vec_cmd} {ir2vec_flags} --vocab={ir2vec_vocab}'
output={}
for s in sequences:
    seq_str=' '.join(sequences[s])
    output[s] = {}
    output[s]['sequence'] = sequences[s]
    output[s]['embedding'] = read_ir2vec_embeeding(bench_dir,compiler,seq_str,
                                workset,ir2vec_line,ir2vec_output,IR_filename)

data = {}
data['metodology'] = {}
data['metodology']['compiler']=compiler
data['metodology']['workset']=workset
data['metodology']['ir2vec flags']=ir2vec_flags

data['embeddings'] = output

with open(output_file,'w') as f:
    yl.dump(data,f)
