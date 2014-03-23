kivy-chess
==========

Work in progress Chess Application using Kivy.

To Build
   1. Download Kivy
   2. Install and test that kivy works
   3. If not running on Mac OS X, the libchess.so library needs to be built, go to https://github.com/sshivaji/python-chess, switch to the pgn branch.
   4. Then execute "sudo python setup.py install".
   5. Go to the pyfish tree at https://github.com/jromang/Stockfish/tree/pyfish (switch to branch pyfish), execute "sudo python setup.py install". Eventually pyfish will replace libchess entirely.
   6. Install leveldb for database functionality, "sudo pip install leveldb"
   7. Finally, Execute "kivy main.py"

To load large databases
   
   1. Open via the UI in settings and select open reference database
   
To save large database location

   1. Go to the github.com/sshivaji/polyglot project.
   2. Execute ``sudo make install``
   3. Copy/move polyglot leveldb index folder to kivy-chess/book/
 
    

   
To use DGT support
   1. Go to the DGT folder.
   2. Follow instructions under https://github.com/sshivaji/kivy-chess/tree/master/dgt
   3. Then go to the setup button and configure your DGT board.

Features
   1. Ability to play over human input moves.
   2. Observe engine output on positions.
   3. Take back and move forward, with variation support.
   4. Opening book support
   5. Database support with position index.
   6. DGT board support

Screenshots
  1. Main Screen ![Main Screen](/doc/screenshots/kivy-chess-main.jpg "Main Screen")
  1. DGT Options ![DGT](/doc/screenshots/kivy-chess-dgt.png "DGT")
