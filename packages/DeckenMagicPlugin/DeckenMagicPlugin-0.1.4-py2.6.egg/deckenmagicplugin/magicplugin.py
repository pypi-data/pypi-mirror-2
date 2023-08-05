from urllib import urlretrieve
import urlparse
import sqlite3
import os
import conjunto

class Card(dict):
	
	def __init__(self, **attributes):
		for i in attributes:
			self[i] = attributes[i]
			
def query_to_cards(scroll):
	cards = []
	for i in scroll:
		card = Card(nome=i[0], sigla=i[1], numero=i[2], tipo=i[3], mana=i[4], raridade=i[5], texto=i[6])
		cards.append(card)
	return cards

class Query:
	
	def __init__(self, conn):
		self.conn = conn
		self.c = self.conn.cursor()
		self.select = "select nome, sigla, numero, tipo, mana, raridade, texto from card"
		
	def all_cards(self):
		self.c.execute(self.select + " order by nome")
		return query_to_cards(self.c.fetchall())
		
	def find_by(self, **criteria):
		scroll = []
		for i in criteria:
			scroll.append("%s=?" % i)
		clause = " and ".join(scroll)
		query = "%s where %s order by nome" % (self.select, clause)
		print 'QUERY', query
		print 'CRITERIOS', criteria
		self.c.execute(query, criteria.values())
		return query_to_cards(self.c.fetchall())
		
	def find_by_name(self, name):
		query = "%s where upper(nome) like '%s%%' order by nome" % (self.select, name.upper())
		print query
		self.c.execute(query)
		return query_to_cards(self.c.fetchall())
		
		
class MagicPlugin:
	
	number_columns = 2
	number_columns_invisibles = 3
	columns_names = [ 'Card', 'Set' ]
	attributes_card_columns = [ 'name', 'sigla', 'numero' ]
	
	def get_image_back(self):
		return os.path.join(os.path.dirname(__file__), 'images', 'back.jpg')
		
	def value_columns_by_card(self, card):
		return [ card['nome'], card['sigla'], card['numero'] ]
		
	def download_image(self, card, path):
		url = "http://magiccards.info/scans/en/%s/%s.jpg" % (card['sigla'], card['numero'])
		parsed = list(urlparse.urlparse(url))
		print 'Baixando ', parsed
		urlretrieve(urlparse.urlunparse(parsed), path)
		
	def find_card(self, conn, column_values):
		query = Query(conn)
		posicao_sigla = column_values[self.attributes_card_columns.index('sigla')]
		posicao_numero = column_values[self.attributes_card_columns.index('numero')]
		result = query.find_by(sigla = posicao_sigla, numero= posicao_numero)
		print result
		return result
		
	def description_card(self, card):
		return "%s - %s" % (card['nome'], card['sigla'])
		
	def detail_card(self, card):
		texto = '%s\t\t%s\n\n%s\t\t%s - %s\n\n%s\n\n%s' % (card['nome'], card['mana'], 
			card['tipo'], card['sigla'], card['raridade'],
			card['texto'],
			card['numero']
		)	
		return texto
		
	def find_or_create_path(self, local, card):
		if card['sigla'] not in os.listdir(local):
			os.mkdir(os.path.join(local,card['sigla']))
		caminho = "%s/%s/%s.jpg" % (local, card[ 'sigla'], card['numero'])
		return caminho
		
	def find_by_name(self, conn, name):
		query = Query(conn)
		return query.find_by_name(name)
		
	def all_cards(self, conn):
		query = Query(conn)
		return query.all_cards()
		
	def update_sets(self, conn):
		return conjunto.update_sets(conn)
		
	def load_sets(self, conn):
		conjunto.load_sets(conn)
		
	def create_tables(self, conn):
		conjunto.create_tables(conn)
		
	def teste(self):
		conjunto.teste()