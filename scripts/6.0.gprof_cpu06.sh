benchmarks=('astar' 'dealII' 'gobmk' 'hmmer' 'libquantum' 'milc' 'omnetpp' 'povray' 'bzip2' 'gcc' 'h264ref' 'lbm' 'mcf' 'namd' 'sjeng')
benchmarks_dir=../benchmarks/cpu2006

script_dir=../gprof-analysis
sequences_dir=../results/sequences/spec2006
output_dir=../results/gprof/spec2006
log_dir=../logs/gprof/spec2006

mkdir -p ${output_dir}
mkdir -p ${log_dir}

for b in ${benchmarks[@]}
do
    echo $b
    if [[ ! -e ${benchmarks_dir}/${b}/src/get_gprof_data.sh ]]; then
        echo 'gprof script for ['$b'] not found'
        continue
    fi
    python3 ${script_dir}/gprof-analysis.py ${benchmarks_dir}/${b} \
            ${sequences_dir}/${b}.yaml -o=${output_dir}/${b}.yaml > ${log_dir}/${b}.out \
            2> ${log_dir}/${b}.err
done

# ./gprof-analysis.py ../benchmarks/cpu2006/astar ../example-bench/fib/exemplo/sequences_fib.yaml -o=../results/gprof/spec2006/astar.yaml
