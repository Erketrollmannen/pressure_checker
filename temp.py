#!/usr/bin/python3

import tagreader
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import threading
import time

class Lop:
	def __init__(self, tags, client, start, end):
		self.start = start
		self.end = end
		self.tags = tags # {tag: "desc"}
		self.running = False
		if len(self.tags) == 2:
			self.prover = True
		else:
			self.prover = False
		for key in tags.keys():
			if "A" in key:
				self.A = key
			elif "B" in key:
				self.B = key
			elif "N" in key:
				self.flow_meter = key
		self.client = client

	def find_times_with_flow(self):
		pass

	def get_df(self):
		print("tread started")
		self.running = True
		self.temp_df = self.client.read(self.tags, self.start, self.end)
		for col in self.temp_df.columns:
			self.temp_df[col][self.temp_df[col] < 0] = np.nan
		self.temp_df.dropna(inplace=True)

		self.temp_df["diff"] = self.temp_df[self.A] - self.temp_df[self.B]
		self.temp_df["min"] = -0.2
		self.temp_df["max"] = 0.2
		print(self.temp_df)
		self.running = False
		
	def plot(self):
		print(self.running)
		self.main_ax = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
		self.main_ax.set_title(f"temperatur differanse {self.A}, {self.B}")
		self.main_ax.set_ylim([-0.5, 0.5])
		self.flow_ax = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=self.main_ax)
		self.main_ax.plot(self.temp_df["diff"])
		self.main_ax.plot(self.temp_df["min"], linestyle="dotted")
		self.main_ax.plot(self.temp_df["max"], linestyle="dotted")
		if not self.prover:
			self.flow_ax.plot(self.temp_df[self.flow_meter])
			self.flow_ax.set_title(f"{self.flow_meter} {self.tags[self.flow_meter]}")

		plt.subplots_adjust(left=0.033, bottom=0.026, right=0.98, top=0.95, wspace=0.2, hspace=0.49)
		plt.get_current_fig_manager().window.state("zoomed")
		plt.show()
		

def search_tag(tags):
	res = dict()
	for tag in tags:
		search_results = client.search(tag)
		print(search_results)
		if not search_results:
			continue
		res[search_results[0][0]] = search_results[0][1]
	lop = Lop(res, client, start, end)	
	return lop

def get_start_end():
	end = str(datetime.datetime.now())
	end = end.split(" ")[0]
	end_split = end.split("-")
	tmp = "0" + str(int(end_split[1]) - 1) if end_split[1] != "12" else "1"
	start = f"{end_split[0]}-{tmp}-{end_split[2]}"
	return start, end


if __name__ == "__main__":
	style.use("ggplot")
	MSA_TAGS = [["80-TI-312A", "80-TI-312B", "80-FI-312N"], ["80-TI-322A", "80-TI-322B", "80-FI-322N"],
				["80-TI-332A", "80-TI-332B", "80-FI-332N"], ["80-TI-342A", "80-TI-342B", "80-FI-342N"],
				["80-TI-352A", "80-TI-352B", "80-FI-352N"], ["80-TI-362A", "80-TI-362B", "80-FI-362N"],
				["80-TI-372A", "80-TI-372B", "80-FI-372N"], ["80-TI-382A", "80-TI-382B", "80-FI-382N"],
				["80-TI-392A", "80-TI-392B", "80-FI-392N"], ["80-TI-402A", "80-TI-402B", "80-FI-402N"],
				["80-TI-412A", "80-TI-412B", "80-FI-412N"], ["80-TI-451A", "80-TI-451B"],
				["80-TI-452A", "80-TI-452B"]]

	MSB_TAGS = [["80-TI-512A", "80-TI-512B", "80-FI-512N"], ["80-TI-522A", "80-TI-522B", "80-FI-522N"],
				["80-TI-532A", "80-TI-532B", "80-FI-532N"], ["80-TI-542A", "80-TI-542B", "80-FI-542N"],
				["80-TI-552A", "80-TI-552B", "80-FI-552N"], ["80-TI-562A", "80-TI-562A", "80-FI-562N"],
				["80-TI-572A", "80-TI-572B", "80-FI-572N"], ["80-TI-582A", "80-TI-582B", "80-FI-582N"],
				["80-TI-592A", "80-TI-592B", "80-FI-592N"], ["80-TI-602A", "80-TI-602B", "80-FI-602N"],
				["80-TI-612A", "80-TI-612B", "80-FI-612N"], ["80-TI-651A", "80-TI-651B"],
				["80-TI-652A", "80-TI-652B"]]
	data = dict()

	start, end = get_start_end()
	API = "aspenone"
	sources = tagreader.list_sources(API)
	if "MO-IP21Y" not in sources:
		os._exit(0)
	else:
		source = "MO-IP21Y"
	client = tagreader.IMSClient(source, API)
	client.connect()

	data["MSA"] = list()
	data["MSB"] = list()
	for i in MSA_TAGS:
		data["MSA"].append(search_tag(i))

	for i in MSB_TAGS:
		data["MSB"].append(search_tag(i))

	data["MSA"][0].get_df()
	for i, lop in enumerate(data["MSA"]):
		thread = threading.Thread(target=data["MSA"][i+1].get_df)
		thread.start()
		lop.plot()
		thread.join()
		
	data["MSB"][0].get_df()
	for i, lop in enumerate(data["MSB"]):
		if i < len(data["MSA"]):
			thread = threading.Thread(target=data["MSB"][i+1].get_df)
			thread.start()
		while lop.running:
			print("busy")
			time.sleep(0.5)
		lop.plot()
	