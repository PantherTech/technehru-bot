import pprint
import zulip
import sys
import re
import json
import httplib2
import os

from chatterbot import ChatBot
from translate import Translate
from hackernews import Hackernews
from movie import Movie
from lyrics import Lyrics
from holiday import Holiday
from currency import Currency
from cricket import Cricket
from github import GitHub


p = pprint.PrettyPrinter()
BOT_MAIL = "technehru-bot@technh.zulipchat.com"

class ZulipBot(object):
	def __init__(self):
		self.client = zulip.Client(site="https://technh.zulipchat.com/api/", api_key="vkEQgQYDPUgAGmXaTXdMPsMwlkkgMfM5", email="technehru-bot@technh.zulipchat.com")
		self.subscribe_all()
		self.hacknews = Hackernews()
		self.trans = Translate()
		self.movie= Movie()
		self.lyrics = Lyrics()
		self.holiday = Holiday()
		self.currency = Currency()
		self.cricket = Cricket()
		self.github = GitHub()
		self.chatbot = ChatBot(name="technehru")

		print("done init")
		self.subkeys = ["use", "help", "translate", "hackernews", "hn", "hotel", "HN", "cricnews", "cricketnews", "movie", "currency", "holiday", "lyrics", "github"]

	def subscribe_all(self):
		json = self.client.get_streams()["streams"]
		streams = [{"name": stream["name"]} for stream in json]
		self.client.add_subscriptions(streams)

	def process(self, msg):
		content = msg["content"].split()
		sender_email = msg["sender_email"]
		ttype = msg["type"]
		stream_name = msg['display_recipient']
		stream_topic = msg['subject']

		print(content)

		if sender_email == BOT_MAIL:
			return 

		print("Sucessfully heard.")

		if content[0].lower() == "technehru" or content[0] == "@**Technehru**":
			if content[1].lower() == "help" or content[1].lower() == "use":
				message = open("help.txt", "r")
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": message.read()
					})

			if content[1].lower() == "translate":
				ip = content[2:]
				ip = " ".join(ip)
				message = self.trans.translate(ip)
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})
			if content[1].lower() == "movie":
				ip = content[2:]
				ip = " +".join(ip)
				message = self.movie.about(ip)
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})

			if content[1].lower() == "lyrics":
				author = content[2]
				title = content[3:]
				title = " ".join(title)
				message = self.lyrics.about(author, title)
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})

			if content[1].lower() == 'holiday':
				quote_data = self.holiday.holiday()
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": quote_data
					})

			if content[1].lower() == 'currency':
				x = content[2]
				y = content[3]

				quote_data = self.currency.currency(x,y)
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": quote_data
					})

			if content[1].lower() == "cricnews" or content[1].lower() == "cricketnews":
				news = self.cricket.news()
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": news  
					})

			if content[1].lower() == 'hackernews' or content[1].lower() == 'hn':
				news = self.hacknews.get_hackernews()
				self.client.send_message({
					"type": "stream",
					"to": stream_name,
					"subject": stream_topic,
					"content": news
					})

			if content[1].lower() == 'github':
				if content[2].lower() == 'reopen' and content[3].lower() == 'issue':
					repo = content[4]
					num = int(content[5])
					result = self.github.reopen_issue(repo, num)
					self.client.send_message({
						"type": "stream",
						"to": stream_name,
						"subject": stream_topic,
						"content": result  
						})

				if content[2].lower() == 'comment' and content[3].lower() == 'issue':
					repo = content[4]
					num = int(content[5])
					comment = content[6:]
					comment = " ".join(comment)
					result = self.github.comment_issue(repo, num, comment)
					self.client.send_message({
						"type": "stream",
						"to": stream_name,
						"subject": stream_topic,
						"content": result  
						})

				if content[2].lower() == 'close' and content[3].lower() == 'issue':
					repo = content[4]
					num = int(content[5])
					result = self.github.close_issue(repo, num)
					self.client.send_message({
						"type": "stream",
						"to": stream_name,
						"subject": stream_topic,
						"content": result  
						})

				if content[2].lower() == 'assign' and content[3].lower() == 'issue':
					repo = content[4]
					num = int(content[5])
					assignee = content[6]
					result = self.github.assign_issue(repo, num, assignee)
					self.client.send_message({
						"type": "stream",
						"to": stream_name,
						"subject": stream_topic,
						"content": result  
						})


			if content[1] not in self.subkeys:
				ip = content[1:]
				ip = " ".join(ip)
				message = self.chatbot.get_response(ip).text
				self.client.send_message({
					"type": "stream",
					"subject": msg["subject"],
					"to": msg["display_recipient"],
					"content": message
					})

		
		elif "technehru" in content and content[0].lower() != "technehru":
			self.client.send_message({
				"type": "stream",
				"subject": msg["subject"],
				"to": msg["display_recipient"],
				"content": "Hey there! :blush:"
				})
		else:
			return

def main():
	bot = ZulipBot()
	bot.client.call_on_each_message(bot.process)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Thanks for using Technehru Bot. Bye!")
		sys.exit(0)
