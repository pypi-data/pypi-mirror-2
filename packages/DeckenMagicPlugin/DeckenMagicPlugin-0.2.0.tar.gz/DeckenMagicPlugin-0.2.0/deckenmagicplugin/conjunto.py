#-*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup as bs

import urllib2
import csv
import sqlite3
import re
import os

def create_tables(conn):
	c = conn.cursor()
	c.execute('create table colecao (descricao text, sigla text, total text, bloco text)')
	c.execute("create table card (nome text, sigla text, numero text, tipo text, mana text, raridade text, texto text)")
	conn.commit()
	c.close()
	conn.close()

def load_sets(conn):
	c = conn.cursor()
	
	reader = csv.reader(open(os.path.join(os.path.dirname(__file__), 'magic_sets.csv')), delimiter='\t')
	for carta in reader:
		c.execute("insert into colecao (descricao, sigla, total, bloco) values (?,?,?,?)", (
			carta[0], carta[1], carta[2], carta[3])
			)
	conn.commit()
	c.close()
	conn.close()
	
def teste():
	print 'OK'
	
def names_sets(conn, siglas):
	c = conn.cursor()
	lista = [ "'%s'" % x for x in siglas if x ]
	c.execute("select descricao from colecao where sigla in (%s)" % ','.join(lista))
	resultado = [ x[0] for x in c.fetchall() ]
	return resultado
	
	
def update_sets(conn):
	c = conn.cursor()

	reader = csv.reader(open(os.path.join(os.path.dirname(__file__), 'magic_sets.csv')), delimiter='\t')

	conjuntos_arquivo = []

	for i in reader:
		conjuntos_arquivo.append(i)

	c.execute("select count(*) from colecao")

	total_banco = int( c.fetchone()[0] )
	total_arquivo = len(conjuntos_arquivo)

	print total_banco
	print total_arquivo

	# verifica se ha um novo set verificando o total no banco e no csv
	# se houve diferenca, descobre quais sao os sets novos e cadastra no banco
	if total_banco < total_arquivo:
		# quais sao os conjuntos novos?
		c.execute("select descricao from colecao")
		conjuntos = []
		for i in c.fetchall():
			conjuntos.append(i[0])
		for i in conjuntos_arquivo:
			if i[0] not in conjuntos:
				# cadastra set no banco
				c.execute("insert into colecao (descricao, sigla, total, bloco) values (?,?,?,?)", i)
				conn.commit()
				yield "Cadastrando %s no banco de dados." % i[0]

	# para cada set verifica se ha diferenca do total de cards informado pelo set
	# e o total de cards para aquele set cadastrado
	c.execute("select sigla, total from colecao")
	colecoes = c.fetchall()
	#print colecoes
	localizadas = []
	for i in colecoes:
		c.execute("select count(*) from card where sigla = ?", [ i[0] ])
		total = c.fetchone()
		if int( i[1] ) <> int(total[0] ):
			print i[1], total[0]
			localizadas.append( i[0] )

	print len(localizadas), 'colecoes para pesquisar'

	for sigla in localizadas:
		print 'Colecao', sigla
		c.execute("select numero from card where sigla = ? ", [ sigla ])
		cards_existentes = []
		for card in c.fetchall():
			cards_existentes.append( card[0])
		conjunto_existents = set(cards_existentes)
		c.execute("select total, descricao from colecao where sigla = ? ", [sigla])
		resposta = c.fetchone()
		total, colecao = resposta
		total = int(total)
		conjunto_total = set( map( str, range(1, total + 1)) )
		conjunto_busca = conjunto_total - conjunto_existents
		print conjunto_existents
		print conjunto_busca
		quantos = 0
		porcentagem = lambda x, y : (x / float(len(y)) ) * 100
		yield "Cadastrando os cards do set %s. ( %2.2f )" % (sigla, porcentagem(quantos, conjunto_busca))
		for numero in conjunto_busca:
			print "http://www.magiccards.info/%s/en/%s.html" % (sigla, numero)
			page = urllib2.urlopen("http://www.magiccards.info/%s/en/%s.html" % (sigla, numero))
			texto = page.read()
			page.close()
			soup = bs(texto)
			carta = soup.find('a',href="/%s/en/%s.html" % (sigla, numero))
			if not carta:
				continue
			nome = soup.find('a',href="/%s/en/%s.html" % (sigla, numero)).contents[0]
			ctext = soup.find('p',{'class':'ctext'})
			tipo_e_mana = ctext.previousSibling.previousSibling.contents[0]
			print tipo_e_mana
			try:
				tipo, mana = tipo_e_mana.split(',')
				mana.replace('\n','')
				mana = mana.split()[0]
			except ValueError:
				tipo, mana = tipo_e_mana, ''
			print colecao
			b = soup.findAll('b',text=re.compile(colecao))
			print b
			encontrou = False
			contador = 1
			while not encontrou:
				try:
					raridade = b[-contador]			
					raridade = raridade[ raridade.index('(') + 1 : raridade.index(')') ]
					encontrou = True
				except IndexError:
					raridade = b
					encontrou = True
				except ValueError:
					contador += 1
			try:
				tamanho = len(ctext.contents[0].contents)
				if tamanho > 1:
					posicoes = range(0, tamanho, 3)
					texto_da_carta = ""
					for i in posicoes:
						texto_da_carta += "%s\n" % ctext.contents[0].contents[i]
					print texto_da_carta
				else:
					texto_da_carta = ctext.contents[0].contents[0]
			except IndexError:
				texto_da_carta = ""
			tupla = nome, sigla, numero, tipo, mana, raridade, texto_da_carta
			print tupla
			if u"Missing!" in unicode(tupla[3]):
				tupla = nome, sigla, numero, '', mana, raridade, texto_da_carta
			print 'cadastrando'
			c.execute("insert into card (nome, sigla, numero, tipo, mana, raridade, texto) values (?,?,?,?,?,?,?)", tupla)
			conn.commit()
			quantos += 1
			yield "Cadastrando os cards do set %s. ( %2.2f )" % (sigla, porcentagem(quantos, conjunto_busca))
	c.close()
	conn.close()
	yield "Atualização concluída."