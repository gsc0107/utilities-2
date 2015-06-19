#!/bin/bash

this_dir="/Users/donnahenderson/github/my_fork/smcsmc/tests/utility/test_lag"
smc2_cmd=/Users/donnahenderson/github/my_fork/smcsmc/smcsmc
lag_dir="${this_dir}/lag_test1"
seg_file=/Users/donnahenderson/github/my_fork/smcsmc/tests/utility/sim-1Samples2msdata1.seg

cp $this_dir/test_lag.sh $lag_dir/

for epoch in 3 7
do

epoch_dir="${lag_dir}/epoch${epoch}_inference"
mkdir ${epoch_dir}

for lag in 100000 200000
do

out_dir="${epoch_dir}/lag${lag}"
mkdir ${out_dir}

for test in 1 2
do

output="${out_dir}/epoch${epoch}_lag${lag}_test${test}.txt"
$smc2_cmd -seed ${test} -seg ${seg_file} -p "1*3+15*4+1" -tmax 4 -Np 10 -EM 20\
 -xc $[$epoch+1]-17 -xc 1-$[$epoch-1] -xr 1-17 -lag $lag > $output

done

echo "done with lag ${lag} for epoch ${epoch}"

done

echo "done with epoch ${epoch}"

done
