virtualenv -p python2 --system-site-packages chesspython
chesspython/bin/pip install setuptools --no-use-wheel --upgrade
chesspython/bin/pip install six
chesspython/bin/pip install cython==0.20.2
chesspython/bin/pip install hg+http://bitbucket.org/pygame/pygame
chesspython/bin/pip install kivy==1.9.1
chesspython/bin/pip install git+https://github.com/kivy/buildozer.git@master
chesspython/bin/pip install git+https://github.com/kivy/plyer.git@master
chesspython/bin/pip install -U pygments docutils
chesspython/bin/pip install pillow
#chesspython/bin/pip install python-chess==0.12.5
chesspython/bin/pip install -r requirements.txt
git clone https://github.com/jromang/Stockfish
cd Stockfish
git checkout pyfish
cd src
../../chesspython/bin/python setup.py install
cd ../..
git clone https://github.com/sshivaji/polyglot
cd polyglot
git checkout leveldb
cd src
sudo make install
cd ../..
git clone https://github.com/sshivaji/ctgreader
cd ctgreader
sudo make install
cd ..
git clone https://github.com/mcostalba/chess_db
cd chess_db/parser
make build ARCH=x86-64
sudo make install
cd ../..
cp chess_db/parser/parser utils
cp chess_db/parser/chess_db.py utils

#../chesspython/bin/python setup.py install
