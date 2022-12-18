events=$1 #'instructions:u,ref-cycles:u'
workset=$2 #'1000'
report_name=$3 #'performance_counters.csv'
 
case ${workset} in 
'test')
    args=1000
    input=/dev/null
    output='output.txt'
    ;;
*)
    echo "invalid workset"
    exit
    ;;
esac

perf stat -e ${events} -x, -o ${report_name} ./a.out ${args} < ${input} > ${output}