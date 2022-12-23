#bin=$1 #'a.gprof.out'
ir_filename=$1 #'program_o.bc'
workset=$2 #'test'
report_name=$3 #'gprof-analysis.txt'
#ir_filename=$4 #'program_o.bc'

case ${workset} in
'test')
    args="omnetpp.ini"
    output='../omnetpp.out'
    err='../omnetpp.err'
    work_dir="../data/test/input/"
    ;;
*)
    echo "invalid workset"
    exit
    ;;
esac

bin='a.gprof.out'

compile_gmon="clang++ -pg ${ir_filename} -o ${bin}"
echo $compile_gmon && $compile_gmon

mv ${bin} ${work_dir}
cur_dir=`pwd`

cd ${work_dir}
./${bin} ${args} > ${output} 2> ${err}
gprof -b ${bin} gmon.out | tail -n +6 | awk '{ printf "%s/%s/%s/",$1,$2,$3; $1=$2=$3=""; gsub(/^[ \t]+/,"",$0);; print $0 }' > ${report_name}

rm ${output}
rm ${err}
rm gmon.out
rm ${bin}

cd ${cur_dir}
