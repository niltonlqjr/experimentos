#! /bin/bash

if [[ -d runtime-prediction ]]; then
    cd runtime-prediction
    git pull
    cd ..
else
    git clone https://github.com/garozipedro/runtime-prediction.git
fi

cd runtime-prediction/src
./build.sh $(pwd)/llvm-15.0.2
cd ../..
