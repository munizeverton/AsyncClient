import asyncio
import aiohttp
import requests
import json
import math
import time
import sys

global urls
global total
global processado
global start_time_inicio

total = 0
processado = 0

if len(sys.argv) < 3:
    sys.exit('Parametros invalidos')

urlMain                  = sys.argv[2]

try:
    requestsSimultaneous = int(sys.argv[1])
except ValueError:
    sys.exit('Numero invalido de requisicoes simultaneas')

def writeSuccessLog(url):
    text_file = open("succes_log.txt", "a+")
    text_file.write("========================== \n Url: %s \n========================== \n \n" % url)
    text_file.close()


def writeErrorLog(url,content):
                text_file = open("error_log.txt", "a+")
                text_file.write("========================== \n Url: %s \n %s \n========================== \n \n" % (url, content))
                text_file.close()

                text_file = open("error_url.txt", "a+")
                text_file.write("%s \n" % url)
                text_file.close()

@asyncio.coroutine
def fetch_page():
    global total
    global urls
    global processado
    global start_time_inicio
    local = total
    total += 1
    start_time_pacote = time.time()
    print("Carregando: "+str(local+1)+" - "+str(urls[local]))
    response = yield from aiohttp.request('GET', urls[local])
    processado = processado+1
    tempo_medio_unitario = ((time.time() - start_time_inicio)/processado)
    
    print("%s Processados: %ss"% (processado,str(tempo_medio_unitario*(len(urls) - processado))))
    if response.status == 200:
        result = yield from response.read()
        print("===========================================================================================")
        print("Resultado 200:"+str(local+1)+"-"+response.url)
        print(result)
        print("Pacote %s processado em %s \n" % (local+1, time.time() - start_time_pacote))
        print("===========================================================================================")
        writeSuccessLog(response.url)
    else:
        result = yield from response.read()
        print("===========================================================================================")
        print("Resultado Erro:"+str(local+1)+"-"+response.url)
        print(result)
        print("Pacote %s processado em %s \n" % (local+1, time.time() - start_time_pacote))
        print("===========================================================================================")
        writeErrorLog(response.url,result)

    if total < len(urls):
        yield from fetch_page()
        return "Foi"

def main():
    coros = []
    for x in range(0,requestsSimultaneous):
        coros.append(asyncio.Task(fetch_page()))

    yield from asyncio.gather(*coros)
    return "Fim"


print ('Iniciando... \n')
print ('Pegando urls na API... \n')
r = requests.get(urlMain)

jsonString = r.text

dictJson = json.loads(jsonString)

start_time_inicio = time.time()

urls = []
for id in dictJson['ids']:
    urls.append(dictJson['url'] + str(id))

content = asyncio.get_event_loop().run_until_complete(main())
print(content)