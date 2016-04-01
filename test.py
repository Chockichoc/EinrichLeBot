#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot
import os
import time
import codecs

class BotModeration(ircbot.SingleServerIRCBot):
	def __init__(self):
        	ircbot.SingleServerIRCBot.__init__(self, [("irc.chockichoc.fr", 6667)],
                                           "Einrich_le_bot", "histobot")
		self.availableCmd = ["!histo"]        

	def on_welcome(self, serv, ev):
		serv.join("#Canal2000")

    	def on_kick(self, serv, ev):
        	serv.join("#Canal2000")

	def on_pubmsg(self, serv, ev):
	
		self.auteur = irclib.nm_to_n(ev.source())
        	self.canal = ev.target()
        	self.message = ev.arguments()[0].decode('utf-8', errors='replace')
		self.serv = serv
		self.find_cmd_on_string(self.message)
		info = '<'+time.strftime('%H:%M',time.localtime()) +"> "+self.auteur + ' : ' + self.message + '\n'
      		self.write_file("/var/www/html","histo.txt", info)


	def on_privmsg(self, serv, ev):
        	self.auteur = irclib.nm_to_n(ev.source())
        	self.canal = ev.target()
        	self.message = ev.arguments()[0].decode('utf-8', errors='replace')
        	self.serv = serv
       		self.find_cmd_on_string(self.message)

	def find_cmd_on_string(self, string_with_cmd):
        	for cmd in self.availableCmd:
            		if cmd in string_with_cmd:
                		self.execute_cmd(cmd)
                		return True
        	return False

	def execute_cmd(self, cmd):
        	if cmd=="!histo":
            		self.serv.privmsg(self.auteur, "irc.chockichoc.fr/index.php")

	def write_file(self, folder, file, info):
        	with codecs.open(folder+'/'+file, 'r','utf-8',errors="replace") as fin:
            		data = fin.read().splitlines(True)
        	if len(data) >= 5000:
            		with codecs.open(folder+'/'+file, 'w', 'utf-8',errors="replace") as fout:
                		fout.writelines(data[1:])
                		fout.writelines(info)
        	else:
            		with codecs.open(folder+'/'+file, 'w', 'utf-8',errors="replace") as fout:
                		fout.writelines(data)
                		fout.writelines(info)		

if __name__ == "__main__":
    BotModeration().start()



