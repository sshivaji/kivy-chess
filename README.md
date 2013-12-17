kivy-chess
==========

Work in progress Chess Application using Kivy.

To Build
   1. Download Kivy
   2. Install and test that kivy works
   3. If not running on Mac OS X, the libchess.so library needs to be built, go to https://github.com/sshivaji/python-chess, switch to the pgn branch.
   4. Then execute "python setup.py build". Copy libchess.so to root folder/chess.
   5. Install leveldb for database functionality, "sudo pip install leveldb"
   6. Finally, Execute "kivy main.py"
   7. To deploy to IOS/android, download the respective toolkits and use this project's rootdir.

To load large databases
   1. Go to the github.com/sshivaji/polyglot project and follow instructions to build databases.
   2. Rename polyglot leveldb folder to the name "polyglot_index.db"
   3. Copy/move polyglot leveldb index folder to kivy-chess/book/
   4. In the source code, search for .pgn and change "2400\_2013/\_47/\_classic.pgn" to your pgn file location (this hardcoding will be removed soon!) 

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
