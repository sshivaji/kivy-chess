from uci import UCIEngine

uci_engine = UCIEngine("/Users/shiv/chess/engines/komodo-3-mac")
uci_engine.start()
uci_engine.configure({})

while not uci_engine.ready:
    uci_engine.registerIncomingData()
# opts = uci_engine.get_options()
for k,v in uci_engine.get_options().iteritems():
    print k
    print v
# print uci_engine.engine_info

# uci_engine.set_option('Threads','2')
# print uci_engine.get_options()


uci_engine.startGame()
