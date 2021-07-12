#!/usr/bin/python3

import tagreader
import os
import datetime
import scipy.stats

class Lop:
	def __init__(self, tags, client):
		self.tags = tags # {tag: "desc"}
		if len(self.tags) == 2:
			self.prover = True
		else:
			self.prover = False
		for key in tags.keys():
			if "A" in key:
				self.A = key
			elif "B" in key:
				self.B = key
		self.client = client

	def find_times_with_flow(self):
		pass

	def get_df(self):
		if self.prover:
			self.temp_a
		
	def statistics(self, start, end):
		print(self.tags)
		self.temp_df = client.read(self.tags, start, end)
		self.temp_df["diff"] = self.temp_df[self.A] - self.temp_df[self.B]
		res = scipy.stats.ttest_ind(self.temp_df[self.A], self.temp_df[self.B], equal_var=True)
		print(self.temp_df)
		print(self.temp_df)
		print(res)
		

def search_tag(tags):
	res = dict()
	for tag in tags:
		search_results = client.search(tag)
		print(search_results)
		if not search_results:
			continue
		res[search_results[0][0]] = search_results[0][1]
	lop = Lop(res, client)	
	return lop

def get_start_end():
	end = str(datetime.datetime.now())
	end = end.split(" ")[0]
	end_split = end.split("-")
	tmp = "0" + str(int(end_split[1]) - 1) if end_split[1] != "12" else "1"
	start = f"{end_split[0]}-{tmp}-{end_split[2]}"
	return start, end


if __name__ == "__main__":
	MSA_TAGS = [["80-TI-312A", "80-TI-312B", "80-FI-312G"], ["80-TI-322A", "80-TI-322B", "80-FI-322G"]]
				#"["80-TI-332A", "80-TI-332B", "80-FI-332G"], ["80-TI-342A", "80-TI-342B", "80-FI-342G"],
				#"["80-TI-352A", "80-TI-352B", "80-FI-352G"], ["80-TI-362A", "80-TI-362A", "80-FI-362G"],
				#"["80-TI-372A", "80-TI-372B", "80-FI-372G"], ["80-TI-382A", "80-TI-382B", "80-FI-382G"],
				#"["80-TI-392A", "80-TI-392B", "80-FI-392G"], ["80-TI-402A", "80-TI-402B", "80-FI-402G"],
				#"["80-TI-412A", "80-TI-412B", "80-FI-412G"], ["80-TI-451A", "80-TI-451B"],
				#"["80-TI-452A", "80-TI-452B"]]

	MSB_TAGS = [["80-TI-512A", "80-TI-512B", "80-FI-512G"], ["80-TI-522A", "80-TI-522B", "80-FI-522G"]]
				#["80-TI-532A", "80-TI-532B", "80-FI-532G"], ["80-TI-542A", "80-TI-542B", "80-FI-542G"],
				#["80-TI-552A", "80-TI-552B", "80-FI-552G"], ["80-TI-562A", "80-TI-562A", "80-FI-562G"],
				#["80-TI-572A", "80-TI-572B", "80-FI-572G"], ["80-TI-582A", "80-TI-582B", "80-FI-582G"],
				#["80-TI-592A", "80-TI-592B", "80-FI-592G"], ["80-TI-602A", "80-TI-602B", "80-FI-610G"],
				#["80-TI-612A", "80-TI-612B", "80-FI-612G"], ["80-TI-651A", "80-TI-651B"],
				#["80-TI-652A", "80-TI-652B"]]
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
	for i in MSA_TAGS:
		data["MSA"].append(search_tag(i))

	for i in MSB_TAGS:
		data["MSA"].append(search_tag(i))

	print(data["MSA"])
	for i in data["MSA"]:
		print(i)
		input()
		i.statistics(start, end)


