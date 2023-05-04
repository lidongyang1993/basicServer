CURRENT_DIR=$(cd $(dirname $0); pwd)
echo $CURRENT_DIR
cd $CURRENT_DIR
source ./venv/bin/activate
nohup python job_run.py -u $1 -m $2 -n $3 -d $4
