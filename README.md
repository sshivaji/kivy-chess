kivy-chess
==========

Work in progress Chess Application using Kivy.

To Build
   1. Download Kivy
   2. Install and test that kivy works
   3. If not running on Mac OS X, the libchess.so library needs to be built, go to https://github.com/sshivaji/python-chess, switch to the pgn branch.
   4. Then execute "python setup.py build". Copy libchess.so to root folder/chess
   3. Finally, Execute "kivy main.py"
   4. To deploy to IOS/android, download the respective toolkits and use this project's rootdir.

Features
   1. Ability to play over human input moves.
   2. Observe engine output on positions.
   3. Take back and move forward, with variation support.
   4. Opening book support
   5. Database support with position index.
   6. DGT board support

Screenshots
  1. Main Screen ![Main Screen](/doc/screenshots/kivy-chess-main-shot.png "Main Screen")
  1. DGT Options ![DGT](/doc/screenshots/kivy-chess-dgt.png "DGT")
