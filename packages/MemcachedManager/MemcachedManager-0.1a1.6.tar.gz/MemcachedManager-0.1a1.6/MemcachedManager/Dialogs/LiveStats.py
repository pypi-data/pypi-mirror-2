import matplotlib
from matplotlib import pyplot

from PyQt4 import QtGui
from PyQt4 import QtCore
from MemcachedManager.Dialogs.ui_LiveStats import Ui_liveStatsDialog
import time
import threading
import MemcachedManager.Settings
import os
import datetime
import gc

class Dialog(QtGui.QDialog, Ui_liveStatsDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		self.currentCluster = None
		self.monitor = False
		self.thread = None
		self.threadInterupt = False
		self.stats = []
		
		self.settings = MemcachedManager.Settings.Settings()
		
		self.lblConnectionsGraph.clear()
		self.lblGetsGraph.clear()
		self.lblHitsMissesGraph.clear()
		self.lblMemoryGraph.clear()
		
		self.connect(self, QtCore.SIGNAL('finished(int)'), self.stopMonitor)
		
	def show(self):
		QtGui.QDialog.show(self)
		self.startMonitor()
		self.stats = []
		
	def setCluster(self, cluster):
		self.currentCluster = cluster
		
	def startMonitor(self):
		self.monitor = True
		self.threadInterupt = False
		if self.thread is None:
			self.thread = Monitor(self)
			self.connect(self.thread, QtCore.SIGNAL('refresh'), self.updateGraphs)
			self.thread.start()
	
	def stopMonitor(self):
		self.monitor = False
		self.threadInterupt = True
		self.stats = []
		self.lblConnectionsGraph.clear()
		self.lblGetsGraph.clear()
		self.lblHitsMissesGraph.clear()
		self.lblMemoryGraph.clear()
		
	def toggleMonitor(self):
		if self.monitor:
			self.stopMonitor()
		else:
			self.startMonitor()
			
	def updateGraphs(self):
		self.graphConnections()
		#self.graphGetsSets()
		#self.graphHistMisses()
		#self.graphMemory()
		gc.collect()
			
	def graphConnections(self):
		figure = pyplot.figure(figsize=(5.5,2.51), linewidth=2)
		matplotlib.rc('lines', linewidth=2)
		matplotlib.rc('font', size=10)
		
		y = []
		legend = ['Total']
		for s in self.stats[0]['stats'].getServers():
			legend.append(s.getName())
			
		for s in self.stats:
			values = []
			values.append(s['stats'].getConnections())
			for server in s['stats'].getServers():
				values.append(server.getConnections())
			y.append(values)
			
		ax = figure.add_subplot(111)
		#TODO: Added Preference Values for Colors
		#ax.set_color_cycle(['c', 'm', 'y', 'k'])
		ax.plot(y)
		
		def format_date(x, pos=None):
			if int(x) >= len(self.stats):
				return ''
			else:
				return self.stats[int(x)]['date'].strftime('%I:%M:%S')
			
		ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_date))
		ax.legend(legend, prop=matplotlib.font_manager.FontProperties(size=8))
		figure.autofmt_xdate()
		path = os.path.join(MemcachedManager.Settings.getSaveLocation(), 'ActiveConnections.png')
		figure.savefig(path)
		figure.clear()
		#self.lblConnectionsGraph.setPixmap(QtGui.QPixmap(path))
	
	def graphGetsSets(self):
		figure = pyplot.figure(figsize=(5.5,2.51), linewidth=2)
		matplotlib.rc('lines', linewidth=2)
		matplotlib.rc('font', size=10)
		
		y = []
		legend = ['Gets', 'Sets']
		for s in self.stats:
			total = s['stats'].getGets() + s['stats'].getSets()
			sets = (float(s['stats'].getSets())/total)*100
			gets = (float(s['stats'].getGets())/total)*100
			y.append((gets, sets))
			
		ax = figure.add_subplot(111)
		ax.plot(y)
		
		def format_date(x, pos=None):
			if int(x) >= len(self.stats):
				return ''
			else:
				return self.stats[int(x)]['date'].strftime('%I:%M:%S')
			
		ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_date))
		ax.legend(legend, prop=matplotlib.font_manager.FontProperties(size=8))
		figure.autofmt_xdate()
		
		path = os.path.join(MemcachedManager.Settings.getSaveLocation(), 'ActiveGetsSets.png')
		figure.savefig(path)
		figure.clear()
		self.lblGetsGraph.setPixmap(QtGui.QPixmap(path))
	
	def graphHistMisses(self):
		figure = pyplot.figure(figsize=(5.5,2.51), linewidth=2)
		matplotlib.rc('lines', linewidth=2)
		matplotlib.rc('font', size=10)
		
		y = []
		legend = ['Hits', 'Misses']
		for s in self.stats:
			total = s['stats'].getHits() + s['stats'].getMisses()
			hits = (float(s['stats'].getHits())/total)*100
			misses = (float(s['stats'].getMisses())/total)*100
			y.append((hits, misses))
			
		ax = figure.add_subplot(111)
		ax.plot(y)
		
		def format_date(x, pos=None):
			if int(x) >= len(self.stats):
				return ''
			else:
				return self.stats[int(x)]['date'].strftime('%I:%M:%S')
		ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_date))
		ax.legend(legend, prop=matplotlib.font_manager.FontProperties(size=8))
		figure.autofmt_xdate()
		
		path = os.path.join(MemcachedManager.Settings.getSaveLocation(), 'ActiveHitsMisses.png')
		figure.savefig(path)
		figure.clear()
		self.lblHitsMissesGraph.setPixmap(QtGui.QPixmap(path))
	
	def graphMemory(self):
		figure = pyplot.figure(figsize=(5.5,2.51), linewidth=2)
		matplotlib.rc('lines', linewidth=2)
		matplotlib.rc('font', size=10)
		
		y = []
		legend = ['Free', 'Used']
		for s in self.stats:
			total = s['stats'].getTotalSpace()
			free = (float(s['stats'].getFreeSpace())/total)*100
			used = (float(s['stats'].getUsedSpace())/total)*100
			y.append((free, used))
			
		ax = figure.add_subplot(111)
		ax.plot(y)
		
		def format_date(x, pos=None):
			if int(x) >= len(self.stats):
				return ''
			else:
				return self.stats[int(x)]['date'].strftime('%I:%M:%S')
		
		ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_date))
		ax.legend(legend, prop=matplotlib.font_manager.FontProperties(size=8))
		figure.autofmt_xdate()
		
		path = os.path.join(MemcachedManager.Settings.getSaveLocation(), 'ActiveMemory.png')
		figure.savefig(path)
		figure.clear()
		self.lblMemoryGraph.setPixmap(QtGui.QPixmap(path))
		
			
#class Monitor(threading.Thread):
class Monitor(QtCore.QThread):
	def __init__(self, dialog):
		#threading.Thread.__init__(self)
		QtCore.QThread.__init__(self)
		self.dialog = dialog
		
	def run(self):
		while not self.dialog.threadInterupt:
                        try:
        			stats = self.dialog.currentCluster.getStats()
        		except Exception, e:
                                try:
                                        stats = self.dialog.currentCluster.getStats()
                                except Exception, e:
                                        stats = None
                        if stats is not None:
                                self.dialog.stats.append({'date':datetime.datetime.today().time(), 'stats':stats})
                                if len(self.dialog.stats) > 20:
                                        self.dialog.stats.pop(0)
				
                                self.emit(QtCore.SIGNAL('refresh'), None)
                                time.sleep(int(self.dialog.settings.settings.config['Stats']['RefreshInterval']))
