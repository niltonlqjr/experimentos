#benchmarks=('astar' 'dealII' 'gobmk' 'hmmer' 'libquantum' 'milc' 'omnetpp' 'povray' 'bzip2' 'gcc' 'h264ref' 'lbm' 'mcf' 'namd' 'sjeng')
benchmarks=('astar' 'gobmk' 'hmmer' 'milc' 'omnetpp' 'povray' 'bzip2' 'gcc' 'h264ref' 'lbm' 'mcf' 'namd' 'sjeng')
benchmarks_dir=../benchmarks/cpu2006

script_dir=../extract-performance-counters
sequences_dir=../results/sequences/spec2006
output_dir=../results/PCs/spec2006
log_dir=../logs/PCs/spec2006

PCs_files='../'$script_dir'/PCs_26.yaml'

mkdir -p ${output_dir}
mkdir -p ${log_dir}

for b in ${benchmarks[@]}
do
    echo $b
    python3 ${script_dir}/extract_pcs.py ${benchmarks_dir}/${b}/src \
            ${sequences_dir}/${b}.yaml -f $PCs_files -r 10 \
            -o=${output_dir}/${b}.yaml > ${log_dir}/${b}.out \
            2> ${log_dir}/${b}.err
done