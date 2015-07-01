kivy-chess
==========

Chess Database/Analysis and playing program.

Features
   1. Ability to analyze positions remotely on powerful computers (more information coming soon).
   2. Instant Database position searches.
   3. Play vs the computer with levels that can work for strong and weak players (from club players to GMs).
   4. Opening book support. Ability to find holes in your repertoire (more information coming).
   5. DGT board support.

Screenshots
  1. Main Screen ![Main Screen](/doc/screenshots/kivy-chess-main.png "Main Screen")
  1. DGT Options ![DGT](/doc/screenshots/kivy-chess-dgt.png "DGT")

Techical Information:

To Build
   1. Run ./install.sh
   2. Execute ./chesspython/bin/python main.py

To load large databases
   
   1. Open via the UI in settings and select open reference database
   
To save large database location

   1. Go to the github.com/sshivaji/polyglot project. Switch to the leveldb branch
   2. Execute ``sudo make install``
   3. Copy/move polyglot leveldb index folder to kivy-chess/book/
 
To use DGT support
   1. Go to the DGT folder.
   2. Follow instructions under https://github.com/sshivaji/kivy-chess/tree/master/dgt
   3. Then go to the setup button and configure your DGT board.
