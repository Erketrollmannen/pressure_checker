#!/usr/bin/python3
import tagreader
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import threading

class Lop:
	def __init__(self, tags, client, start, end):
		self.start = start
		self.end = end
		self.tags = tags # {tag: "desc"}
		self.has_df = False
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

	def get_df(self):
		self.temp_df = self.client.read(self.tags, self.start, self.end)
		for col in self.temp_df.columns:
			self.temp_df[col][self.temp_df[col] < 0] = np.nan
		self.temp_df.dropna(inplace=True)
		self.temp_df["diff"] = self.temp_df[self.A] - self.temp_df[self.B]
		self.temp_df["min"] = -0.07
		self.temp_df["max"] = 0.07
		self.has_df = True

	def get_flow_df(self):
		if not self.has_df or self.prover:
			return None
		return self.temp_df[self.flow_meter]
		
	def plot(self, flow_list):
		self.main_ax = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
		self.main_ax.set_title(f"pressure differanse {self.A}, {self.B}")
		self.main_ax.set_ylim([-0.1, 0.1])
		self.flow_ax = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=self.main_ax)
		self.main_ax.plot(self.temp_df["diff"])
		self.main_ax.plot(self.temp_df["min"], linestyle="dotted")
		self.main_ax.plot(self.temp_df["max"], linestyle="dotted")
		if not self.prover:
			self.flow_ax.plot(self.temp_df[self.flow_meter])
			self.flow_ax.set_title(f"{self.flow_meter} {self.tags[self.flow_meter]}")
		if self.prover:
			for i in flow_list:
				if i is None:
					continue
				self.flow_ax.plot(i)
		plt.subplots_adjust(left=0.033, bottom=0.026, right=0.98, top=0.95, wspace=0.2, hspace=0.49)
		plt.get_current_fig_manager().window.state("zoomed")
		plt.show()

def search_tag(tags):
	res = dict()
	for tag in tags:
		print(tag)
		search_results = client.search(tag)
		if not search_results:
			continue
		res[search_results[0][0]] = search_results[0][1]
	lop = Lop(res, client, start, end)	
	return lop

def get_start_end():
    end = datetime.date.today()
    start = end + datetime.timedelta(days=-30)
    return str(start), str(end)

def connect_to_aspen():
	print("Venter på svar frå aspen")
	API = "aspenone"
	sources = tagreader.list_sources(API)
	if "MO-IP21Y" not in sources:
		print("Kunne ikkje koble til MO-IP21Y")
		os._exit(0)
	else:
		source = "MO-IP21Y"
	client = tagreader.IMSClient(source, API)
	client.cache = None
	client.connect()
	return client

def yeet(tags):
	data = list()
	print("Søker etter tag...")
	for i in tags:
		data.append(search_tag(i))

	flow_list = list()
	data[0].get_df()
	flow_list.append(data[0].get_flow_df())
	if len(data) >= 2:
		for i, lop in enumerate(data):
			if i < len(data) - 1:
				thread = threading.Thread(target=data[i+1].get_df)
				thread.start()
			flow_list.append(lop.get_flow_df())
			lop.plot(flow_list)
			thread.join()
	else:
		data[0].plot(flow_list)

def get_tag_list():
	os.system("cls")
	print("Arbeidspunktkontroll trykk sjekk")
	inn = input("1. MSA\n2. MSB\nEnter for alle tag\nc for å avslutte\n")

	MSA_TAGS = [["80-PI-316A", "80-PI-316B", "80-FI-312N"], ["80-PI-326A", "80-PI-326B", "80-FI-322N"],
				["80-PI-336A", "80-PI-336B", "80-FI-332N"], ["80-PI-346A", "80-PI-346B", "80-FI-342N"],
				["80-PI-356A", "80-PI-356B", "80-FI-352N"], ["80-PI-366A", "80-PI-366B", "80-FI-362N"],
				["80-PI-376A", "80-PI-376B", "80-FI-372N"], ["80-PI-386A", "80-PI-386B", "80-FI-382N"],
				["80-PI-396A", "80-PI-396B", "80-FI-392N"], ["80-PI-406A", "80-PI-406B", "80-FI-402N"],
				["80-PI-416A", "80-PI-416B", "80-FI-412N"], ["80-PI-455A", "80-PI-455B"],
				["80-PI-456A", "80-PI-456B"]]

	MSB_TAGS = [["80-PI-516A", "80-PI-516B", "80-FI-512N"], ["80-PI-526A", "80-PI-526B", "80-FI-522N"],
				["80-PI-536A", "80-PI-536B", "80-FI-532N"], ["80-PI-546A", "80-PI-546B", "80-FI-542N"],
				["80-PI-556A", "80-PI-556B", "80-FI-552N"], ["80-PI-566A", "80-PI-566B", "80-FI-562N"],
				["80-PI-576A", "80-PI-576B", "80-FI-572N"], ["80-PI-586A", "80-PI-586B", "80-FI-582N"],
				["80-PI-596A", "80-PI-596B", "80-FI-592N"], ["80-PI-606A", "80-PI-606B", "80-FI-602N"],
				["80-PI-616A", "80-PI-616B", "80-FI-612N"], ["80-PI-655A", "80-PI-655B"],
				["80-PI-656A", "80-PI-656B"]]
		

	if inn.lower() == "c":
		os._exit(0)
	elif inn == "1":
		while True:
			os.system("cls")
			print("Velg løp MSA.")
			print("b for å gå tilbake.")
			print("c for å avslutte.")
			print("Enter for alle.")
			print("12. Prover innløp.")
			print("13. Prover utløp.")

			inn = input("Skriv tall for ønsket løp på MSA. (separer tall med mellomrom for fleire løp.) \n\tf.eks \"1 2 3\" for å plotte løp 1, 2 og 3\n")
			if inn == "":
				return MSA_TAGS, None
			elif inn.lower() == "b":
				msa, msb = get_tag_list()
			elif inn.lower() == "c":
				os._exit(0)
			split = inn.split()
			try:
				index = [int(i)-1 for i in split]
			except IndexError:
				print("Du må skrive eit tall, eller tall separert med mellomrom")
				continue
			try:
				t = [MSA_TAGS[i] for i in index]
			except IndexError:
				print("Godtar ikkje høgere tall enn 13.\n")
				continue
			return t, None
		
	elif inn == "2":
		while True:
			os.system("cls")
			print("Velg løp MSB.")
			print("Enter for alle")
			print("b for å gå tilbake")
			print("c for på avslutte")
			inn = input("Skriv tall for ønsket løp på MSB. (separer tall med mellomrom for fleire løp.)\n\tf.eks \"1 2 3\" for å plotte løp 1, 2 og 3\n")
			if inn == "":
				return MSB_TAGS, None
			elif inn.lower() == "b":
				msa, msb = get_tag_list()
				return msa, msb
			elif inn.lower() == "c":
				os._exit(0)
			split = inn.split()
			try:
				index = [int(i)-1 for i in split]
			except IndexError:
				print("Du må skrive eit tall, eller tall separert med mellomrom")
			try:
				t = [MSB_TAGS[i] for i in index]
			except IndexError:
				print("Godtar ikkje høgere tall enn 13.\n")
				continue
			return t, None
	else:
		return MSA_TAGS, MSB_TAGS

if __name__ == "__main__":

	style.use("ggplot")
	client = connect_to_aspen()
	start, end = get_start_end()

	msa, msb = get_tag_list()
	if msa is not None:
		yeet(msa)
	if msb is not None:
		yeet(msb)
