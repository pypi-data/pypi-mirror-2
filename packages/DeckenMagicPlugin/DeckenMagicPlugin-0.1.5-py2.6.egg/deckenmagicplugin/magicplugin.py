from urllib import urlretrieve
import urlparse
import sqlite3
import os
import conjunto

formatos = ['', 'Standard', 'Block', 'Extended', 'Legacy', 'Vintage']

standard  = ['', 'roe','wwk','zen','m10','arb','cfx','ala' ]

extended = standard + ['9e','eve','shm',
 	'mt','lw','fut','pc','ts','tsts','cs','ai','ia','di','gp','rav','sok','bok',
	'chk','5dn','ds','mi']
	
others = ['sc','le','on','ju','tr','od','ap','ps','in','pr','ne','mm','ud','ui','us',
	'ex','sh','tp','wl','vi','mr','hl','fe','dk','lg','aq','an','8e','7e','6e','5e',
	'4e','rv','un','be','al']
	
legacy = extended + others

vintage = legacy

sets_por_formato = { 
	'Standard' : standard,
	'Block': ['roe','wwk','zen'],
	'Extended': extended,
	'Legacy': legacy,
	'Vintage': vintage,
	 }
	
palavras_tipos = {
	'' : '',
	'Creature' : r" (tipo like '%Creature%' and tipo not like '%Enchant Creature%') ",
 	'Artifact' : r" (tipo like '%Artifact%' and tipo not like '%Creature%' )",
	'Planeswalker' : r" tipo like '%Planeswalker%' ", 
	'Enchantment' : r" tipo like '%Enchant%' ",
 	'Sorcery' : r" tipo = 'Sorcery' ", 
	'Instant' : r" tipo like '%Instant%' ", 
	'Land' : r" (tipo like '%Land%' and tipo not like '%Enchant Land%')  " }

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
	
def montar_filtros(filtros):
	clausules = []
	for filtro in filtros:
		combo = filtros[filtro]
		model = combo.get_model()
		active = combo.get_active()
		if active < 0:
			continue
		else:
			valor = model[active][0]
			if not valor: continue
			if filtro == 'Card Type':
				clausules.append( palavras_tipos[ model[active][0] ] )
			elif filtro == 'Card Format':
				lista = [ "'%s'" % x for x in sets_por_formato[valor] if x ]
				clausules.append( " sigla in (%s) " % ','.join(lista) )
			else:
				clausules.append( " sigla = '%s' " % valor )
	print ' and '.join( clausules )
	return ' and '.join( clausules )

class Query:
	
	def __init__(self, conn):
		self.conn = conn
		self.c = self.conn.cursor()
		self.select = "select nome, sigla, numero, tipo, mana, raridade, texto from card"
		
	def all_cards(self, filtros):
		if filtros:
			self.c.execute(self.select + r" where %s order by nome" % filtros)
		else:
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
		
	def find_by_name(self, name, filtros):
		if filtros:
			query = "%s where upper(nome) like '%s%%' and ( " % (self.select, name.upper()) + filtros +  ") order by nome"
		else:
			query = "%s where upper(nome) like '%s%%' order by nome" % (self.select, name.upper())
		print query
		self.c.execute(query)
		return query_to_cards(self.c.fetchall())
		
		
class MagicPlugin:
	
	number_columns = 2
	number_columns_invisibles = 3
	columns_names = [ 'Card', 'Set' ]
	attributes_card_columns = [ 'name', 'sigla', 'numero' ]
	select_filters = ['Card Format','Card Set','Card Type']
	
	def get_select_filter_values(self, name):
		filter_values = { 
			'Card Format' : formatos, 
			'Card Set' : legacy,
			'Card Type' : palavras_tipos.keys(),
		}
		return filter_values[name]
	
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
		
	def find_by_name(self, conn, name, filtros):
		query = Query(conn)
		return query.find_by_name(name, montar_filtros(filtros))
		
	def all_cards(self, conn, filtros):
		query = Query(conn)
		return query.all_cards( montar_filtros(filtros) )
		
	def update_sets(self, conn):
		return conjunto.update_sets(conn)
		
	def load_sets(self, conn):
		conjunto.load_sets(conn)
		
	def create_tables(self, conn):
		conjunto.create_tables(conn)
		
	def teste(self):
		conjunto.teste()