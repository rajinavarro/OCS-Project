# coding=utf-8
#Importação das bibliotecas para acessar o link do arquivo
import requests, csv
from html.parser import HTMLParser

#Importação da função de data
#from datetime import datetime, timezone, timedelta

#Salvamento do arquivo

class MyHTMLParser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        if not hasattr(self, 'params'):
            self.params = dict()
        
        if tag == 'input':
            a = dict(attrs)
            #print(a)
            if 'name' in a and 'value' in a:
                self.params[a['name']] = a['value']


ses = requests.session()
res = ses.get('http://10.50.11.16/ocsreports/')


parser = MyHTMLParser()
parser.feed(res.content.decode())
parser.params['LOGIN'] = 'admin'
parser.params['PASSWD'] = '@ti!2017'


res = ses.post('http://10.50.11.16/ocsreports/', data=parser.params)

res2 = ses.get('http://10.50.11.16/ocsreports/?function=visu_computers')

res3 = ses.get('http://10.50.11.16/ocsreports/index.php?function=export_csv&no_header=1&tablename=list_show_all&base=')

print(type(res3.text))

with open('export.csv', 'w') as csvfile:
    csvfile.writelines(res3.text)



#Variavel de controle
a = 0

#Leitura e importação de arquivos
arqold = open('data.csv','r')
linhasold = []
for linha in arqold:
    linhasold.append(linha)
arqnew = open('export.csv','r')
linhasnew = []
for linha in arqnew:
    linhasnew.append(linha)

#Comparação dos arquivos
if len(linhasnew) == len(linhasold):
    
    for x in range(len(linhasnew)):
        if linhasnew[x] != linhasold[x]:
            a = 1
            p = ("Há uma alteração na maquina {}".format(x))
            a = linhasnew[x].split(";")
            b = linhasold[x].split(";")
            for i in range(len(a)):
                if a[i] != b[i]:
                    #Geração de Relatório
                    p = (\nRelatorio: Componente Alterado: {} Componente Após a Alteração: {}\n.format(b[i],a[i]))

#Comparação Tamanho dos Arquivos(Adição/Remoção de Maquinas)
if len(linhasnew) > len(linhasold):
    p = ("\nUma nova maquina foi adicionada\n")
    a = 1
elif len(linhasnew) < len(linhasold):
    p = ("\nUma maquina foi removida\n")
    a = 1

#Fim da Interface
if a == 0:
    p = ("\nNão houveram alterações nas maquinas\n")

print (p)

#Fechamento Arquivos Leitura
arqold.close()
arqnew.close()

#Abrindo Arquivos Escrita
arqwold = open('data.csv', 'w')

arqrel = open('relatorio.txt','a')

#Data e Hora
diferenca = timedelta(hours = -3)
fuso_horario = timezone(diferenca)
horario = datetime.now()
hora_sp = horario.astimezone(fuso_horario)
horariof = hora_sp.strftime('%d/%m/%Y %H:%M')

#Escrevendo Relatorio no Arquivo
arqrel.write('''\nRelatorio {}
    {}'''.format(horariof,p))

#Escrevendo Arquivo novo no data
for linha in linhasnew:
    arqwold.write(linha)

#Fechando Arquivos de Escrita
arqwold.close()
arqrel.close()
