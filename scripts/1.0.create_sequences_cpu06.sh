benchmarks=('astar' 'dealII' 'gobmk' 'hmmer' 'libquantum' 'milc' 'omnetpp' 'povray' 'bzip2' 'gcc' 'h264ref' 'lbm' 'mcf' 'namd' 'sjeng')
benchmarks_dir=../benchmarks/cpu2006

script_dir=../generate_sequences
flags_file=../flags_opt12/yamls/set_flags_O0+O1+O2+O3+Os+Oz.yaml
output_dir=../results/sequences
min_len=1
max_len=294
total_seq=100

mkdir -p $output_dir

for b in ${benchmarks[@]}
do
    echo $b
    python3 ${script_dir}/generate_sequences.py --min=${min_len} --max=${max_len} \
            --total=${total_seq} --flags-file=${flags_file} -o=${output_dir}/${b}.yaml \
            --prog ${benchmarks_dir}/${b}/src
done