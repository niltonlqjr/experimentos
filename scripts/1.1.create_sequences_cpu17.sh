benchmarks=('blender' 'deepsjeng' 'gcc' 'imagick' 'lbm' 'leela' 'mcf' 'nab' 'namd' 'omnetpp' 'parest' 'perlbench' 'povray' 'x264' 'xalancbmk' 'xz')
benchmarks_dir=../benchmarks/cpu2017

script_dir=../generate_sequences
flags_file=../flags_opt12/yamls/set_flags_O0+O1+O2+O3+Os+Oz.yaml
output_dir=../results/sequences/spec2017
log_dir=../logs/sequences/spec2017

min_len=5
max_len=294
total_seq=100

mkdir -p ${output_dir}
mkdir -p ${log_dir}

for b in ${benchmarks[@]}
do
    echo $b
    python3 ${script_dir}/generate_sequences.py --min=${min_len} --max=${max_len} \
            --total=${total_seq} --flags-file=${flags_file} -o=${output_dir}/${b}.yaml \
            --prog ${benchmarks_dir}/${b}/src > ${log_dir}/create_sequences_${b}.out \
            2> ${log_dir}/create_sequences_${b}.err
done