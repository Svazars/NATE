export TARGET="bots/a.out" 
export TARGET="bots/run-java.sh" 

rm -rf TMP
mkdir TMP

export noHead=''

for file in inputs/*.stocks; do
  export name=$(basename "$file" .stocks)  
  python3.4 emulator.py $noHead $file  $TARGET 10000 "TMP/$name" 
  noHead='-no-header'
done







