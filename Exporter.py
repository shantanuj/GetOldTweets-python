# -*- coding: utf-8 -*-

import sys,getopt,got,datetime,codecs
users=[]
pre_processed=[]
def main(argv):
	
	
	if len(argv) == 0:
		print 'You must pass some parameters. Use \"-h\" to help.'
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print """\nTo use this jar, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-aa)
       until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Exporter.py --username "barackobama" --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n
 
 # Example 4 - Get the last 10 top tweets by username
 python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n"""
		return
 
	try:
		opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets="))
		
		tweetCriteria = got.manager.TweetCriteria()
		
		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
				
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
				
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
				
		
		outputFile = codecs.open("pre_processing.csv", "w+", "utf-8")
		
		outputFile.write('username;date;text;mentions;hashtags;id')
		
		print 'Searching...\n'
		
		def receiveBuffer(tweets):
			
			for t in tweets:
				
				mentions=t.mentions.split(' ')
				username=t.username
				pre_processed.append([t.username,t.date.strftime("%Y-%m-%d %H:%M"),t.text,mentions,t.hashtags,t.id])
				if(mentions and (username=="TataPower" )):  #or username=="tatapower_ddl"
					for m in mentions:
						if(not (m in users)):
							users.append(m[1:])


				outputFile.write(('\n%s;%s;"%s";%s;%s;"%s"' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.text, t.mentions, t.hashtags, t.id)))
			outputFile.flush();
			
			print 'More %d saved on file...\n' % len(tweets)
		
		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		
		


	except arg:
		print 'Arguments parser error, try -h' + arg
	finally:
		outputFile.close()     
		print 'Done. Output file generated "output_got.csv".'
		processTweets()                             
		


def processTweets():
	#file handling code first try catch finally
	#1) Extract all tweets which mention user or are made by user 
	#2) Store tweets into file which 
	#3) Optional later--> Label as question and answer
	#user is a list of users mentioned by tata
	# pre_processed structure--> [[username(str),date(str),text(str),mentions(list),hashtags(str),id(str)],[.......]]
	


	try:			
		outputFileT = codecs.open("post_processing.csv", "w+", "utf-8")
		
		outputFileT.write('username,date,text')
		post_processed=[]
		if(len(users)):
			users.pop(0)
		#print(users)

		for us in users:

			for tw in pre_processed:
				print(tw[3])
				print("-------------"+us)
				if(us==tw[0] or ((('@'+us) in tw[3]) and (tw[0]=='TataPower' ) )): # or tw[0]=='tatapower_ddl' comparing whether user is mentioned or has made a tweet
					post_processed.append(tw)
					#possible to have a better storage representation here
					outputFileT.write(('\n%s,%s,"%s"' % (tw[0], tw[1], tw[2]))) #outputFileT.write(('\n%s;%s;"%s";%s;%s;"%s"' % (tw[0], tw[1], tw[2], tw[3], tw[4], tw[5])))
		#print(post_processed)
	except Exception as e:
		print e
	finally:
		outputFileT.close()     
		print 'Done. Output file generated "post_processing.csv".'
	
if __name__ == '__main__':
	main(sys.argv[1:])
