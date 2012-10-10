# SQL Alchemy
from sqlalchemy import create_engine, \
	Table, Column, Integer, String, MetaData
from sqlalchemy.sql import select

class LTModel(object):

	def __init__(self):
		self.engine = create_engine('sqlite:///:memory:', echo=False, connect_args={'check_same_thread': False})
		self.metadata = MetaData()

		# Entries definition
		self.entries = Table('entries', self.metadata, 
			Column('id', Integer, primary_key=True),
			Column('category', String(64)),
			Column('topic', String(64)),
			Column('question', String(255)),
			Column('answer', String(255))
		)

		self.metadata.create_all(self.engine)
		self.conn = self.engine.connect()
		self._create_dummy_data()

	def _create_dummy_data(self):
		self.conn.execute(self.entries.insert(), [
			{
				'category': 'programming', 
				'topic': 'git', 
				'question': 'How do you pull from repo?', 
				'answer': 'git pull'
			},
			{
				'category': 'programming', 
				'topic': 'git', 
				'question': 'How do you push to repo?', 
				'answer': 'git push'
			},
			{
				'category': 'random', 
				'topic': 'family', 
				'question': 'What\'s your mother\'s name?', 
				'answer': 'Rosica'
			},
		])

	def get_entries(self, format='json'):
		select_query = select([self.entries])
		return self.conn.execute(select_query)

ltm = LTModel()


# API in Flask
from flask import Flask
import json

app = Flask(__name__)
app.debug = True

@app.route('/questions')
def get_questions():
	results = []
	for entry in ltm.get_entries():
		results.append(dict(entry))
	return json.dumps({'results': results})

if __name__ == "__main__":
	app.run(port=8080)