CURRENT_DIR=$(cd $(dirname $0); pwd)
echo $CURRENT_DIR
cd $CURRENT_DIR
source ./venv/bin/activate
nohup python job_run_from_db.py -u "$1" -r "$2"   > case_log.out 2>&1 &
