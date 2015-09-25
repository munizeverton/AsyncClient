import grequests, requests, json, math, time, sys

def writeSuccessLog(response):
	text_file = open("succes_log.txt", "a+")
	text_file.write("========================== \n Url: %s \n========================== \n \n" % response.url)
	text_file.close()


def writeErrorLog(response):
	text_file = open("error_log.txt", "a+")
	text_file.write("========================== \n Status: %s - Url: %s \n %s \n========================== \n \n" % (response.status_code, response.url, response.content))
	text_file.close()

	text_file = open("error_url.txt", "a+")
	text_file.write("%s \n" % response.url)
	text_file.close()

start_time = time.time()

if len(sys.argv) < 3:
    sys.exit('Parametros invalidos')

urlMain                  = sys.argv[2]

try:
    requestsSimultaneous = int(sys.argv[1])
except ValueError:
    sys.exit('Numero invalido de requisicoes simultaneas')

print 'Iniciando... \n'
print 'Pegando urls na API... \n'
r = requests.get(urlMain)

jsonString = r.text

dictJson = json.loads(jsonString)

urls = []

for id in dictJson['ids']:
	urls.append(dictJson['url'] + str(id))

tamanhoArray = len(urls)
print 'Iniciando requisicoes... \n'
for x in range(0, int(math.ceil( float(tamanhoArray) / float(requisicoesSimultaneas))) ):
	print 'Pacote %s de %s...' % (x + 1, int(math.ceil( float(tamanhoArray) / float(requisicoesSimultaneas))) + 1)
	start_time_pacote = time.time()
	rs = (grequests.get(u) for u in urls[x * requisicoesSimultaneas : x * requisicoesSimultaneas + requisicoesSimultaneas])
	for response in grequests.map(rs):
		if response.status_code == 200:
			writeSuccessLog(response)
		else:
			writeErrorLog(response)
	print("Pacote %s processado em %s \n" % (x + 1, time.time() - start_time_pacote))


print("Processo executado em %s " % (time.time() - start_time))
print 'Fim \n'