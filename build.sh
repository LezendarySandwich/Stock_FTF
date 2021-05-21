ENVIRONMENT_DIR=env
if [[ -d $ENVIRONMENT_DIR ]]
then
    echo "Environment ($ENVIRONMENT_DIR) already exists"
else
    python3 -m venv $ENVIRONMENT_DIR
fi
source env/bin/activate
pip3 install -r requirements.txt