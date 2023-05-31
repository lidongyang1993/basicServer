CURRENT_DIR=$(cd $(dirname $0); pwd)
echo $CURRENT_DIR
cd $CURRENT_DIR
source ./venv/bin/activate
nohup python job_run.py -u $1 -m $2 -n $3 -d $4 -r $5  > case_log.out 2>&1 &
