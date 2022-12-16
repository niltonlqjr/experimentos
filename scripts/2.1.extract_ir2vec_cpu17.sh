benchmarks=('blender' 'deepsjeng' 'gcc' 'imagick' 'lbm' 'leela' 'mcf' 'nab' 'namd' 'omnetpp' 'parest' 'perlbench' 'povray' 'x264' 'xalancbmk' 'xz')
benchmarks_dir=../benchmarks/cpu2017

script_dir=../extract-ir2vec
sequences_dir=../results/sequences/spec2017
output_dir=../results/ir2vec/spec2017
log_dir=../logs/ir2vec/spec2017

mkdir -p ${output_dir}
mkdir -p ${log_dir}

for b in ${benchmarks[@]}
do
    echo $b
    python3 ${script_dir}/extract_ir2vec.py ${benchmarks_dir}/${b}/src \
            ${sequences_dir}/${b}.yaml -o=${output_dir}/${b}.yaml > ${log_dir}/${b}.out \
            2> ${log_dir}/${b}.err
done