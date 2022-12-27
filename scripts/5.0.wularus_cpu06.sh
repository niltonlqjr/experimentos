#!/bin/bash

benchmarks=('astar' 'dealII' 'gobmk' 'hmmer' 'libquantum' 'milc' 'omnetpp' 'povray' 'bzip2' 'gcc' 'h264ref' 'lbm' 'mcf' 'namd' 'sjeng')

benchmarks_dir=../benchmarks/cpu2006
script_dir=../wularus-analysis
sequences_dir=../results/sequences/spec2006
output_dir=../results/wularus/spec2006
log_dir=../logs/wularus/spec2006

mkdir -p ${output_dir}
mkdir -p ${log_dir}

for b in ${benchmarks[@]}
do
    echo $b
    python3 ${script_dir}/wularus-analysis.py ${benchmarks_dir}/${b} \
            ${sequences_dir}/${b}.yaml \
            ../llvm-15.0.2/bin \
            ../runtime-prediction/src/build/libprediction_pass.so \
            -o=${output_dir}/${b}.yaml > ${log_dir}/${b}.out 2> ${log_dir}/${b}.err
done
# ./wularus-analysis.py ../benchmarks/cpu2006/astar ../results/sequences/spec2006/astar.yaml ../llvm-15.0.2/bin ../runtime-prediction/src/build/libprediction_pass.so -o=astar.yaml
