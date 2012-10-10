#!/usr/bin/env python
import random
import json
from urllib2 import urlopen

def get_questions():
	return json.loads(urlopen('http://localhost:8080/questions').read())['results']
	
questions = get_questions()
rnd = random.randint(0, len(questions) - 1)

answer = None
try:
	answer = raw_input('\n# ' + questions[rnd]['question'] + '\n> ')
except KeyboardInterrupt:
	print

if answer == questions[rnd]['answer']:
	print
	print "That's right!"
	print
else:
	print
	print "# The answer is:"
	print "> " + questions[rnd]['answer']
	print