#/bin/bash
ps -x | grep "python3 trivial.py"
pkill -ef "python3 trivial.py"
python3 trivial.py&
echo LefèvreBot à bien redémarré