cd `dirname $0`

if [ ! -e env3 ]
then
    python3 -m virtualenv env3
fi
source ./env3/bin/activate

mkdir -p py3
cd py3
cp ../protlib.py ../unit_tests.py .
2to3 --write protlib.py unit_tests.py
python unit_tests.py
