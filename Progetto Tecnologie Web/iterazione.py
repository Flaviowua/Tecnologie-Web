import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

app.config['DEBUG'] = True

#utilizzo la funzione render_template di Flask che permette di ritornare al client un html presente nella
#cartella templates in sostituendo cosi' la parte di codice Python con del codice html

#utilizzo l'oggetto request di Flask per gestire la richesta da parte del client e prendere i parametri passati in input



@app.route('/',methods=['GET'])
#funzione homePage mi permette di gestire le richieste di tipo GET , mettendo l'elemento da ricercare nel form della pagina index.html
def homePage():
    return render_template('index.html')


#funzione ricerca mi permette di gestire le richieste di tipo POST , prendo l'input immesso dell'utente , contatto il web server , ottengo le iformazioni,
# le converto e le utilizzo per l'output a schermo (mi servo dell'id per effettuare una nuova richiesta di informazioni per i personaggi dell'i-esimo programma televisivo ottenuto in risposta.
@app.route('/',methods=['POST'])
def ricerca():
    
     #dalla request http prendo il form (l'input immesso dall'utente).
    nome_programma_televisivo = request.form.get('programma_televisivo')
    
    url = 'https://api.tvmaze.com/search/shows?q={}'
    url_con_nome = url.format(nome_programma_televisivo) #compilo il placeholder
    
    risposta = requests.get(url_con_nome) #ottengo il jason di tipo str
    text = risposta.text
    data = json.loads(text) #converto le informazioni per l'estrapolazione in tipo list
    if len(data) == 0:
        return render_template('nessun_risultato.html')
    else:
        print("esco con 1")
        print(type(data))
        #effettuo questo controllo in quanto potrei ottenere una lista con un elemento che risulta essere vuoto
        try:
            print(data)
        except:
            return render_template('risultato_troppo_generale.html')
        
        #lista che conterra' i programmi televisivi risultanti con tutte le informazioni estratte
        lista_programmi = []
        
        #per singolo programma estraggo le informazioni
        for programma in data:
            
            #parte di codice che mi permette di estrarre l'id e di ottenere i personaggi di quel programma televisivo.
            id_show = programma['show']['id']
            url_personaggi = 'https://api.tvmaze.com/shows/{}/cast'
            url_con_nome_programma = url_personaggi.format(id_show)
            url_completo_programma = requests.get(url_con_nome_programma)
            text_personaggi = url_completo_programma.text

            data_personaggi = json.loads(text_personaggi)
            
            # lista che conterra' i veri personaggi con ognuno di essi le varie informazioni che mi servono.
            lista_personaggi = []
            
            if len(data_personaggi) == 0:
                
                #lascio la lista dei personaggi vuota.
                print("passo a oggetto programma_televisivo la lista dei personaggi vuota")
            else:
                count = 0
                
                for personaggio in data_personaggi:
                    
                    #uso un contatore per fare il controllo solo una volta in quanto se ci sta gia' il primo personaggio vuol dire che i successivi esistono.
                    if count == 0: # se la lista risultaten dei personaggi contiene un elemento ma questo elemento e' vuoto , salta il procedimento successivo (ciclo for con dentro questo if) e lascia la lista dei personaggi vuota.
                        try:
                            print(data_personaggi)
                        except:
                            break
                        
                    
                    personaggio_trovato = {
                        'nome' : personaggio['person']['name'],
                        'luogo_nascita' : (personaggio['person']['country']['name'] if personaggio['person']['country'] else "None"),
                        'nato' : personaggio['person']['birthday'],
                        'morto' : personaggio['person']['deathday'],
                        'genere' : personaggio['person']['gender'],
                        'foto_attore' : (personaggio['person']['image']['medium'] if personaggio['person']['image'] else "None"),
                        'foto_attore_originale' : (personaggio['person']['image']['original'] if personaggio['person']['image'] else "None"),
                        'nome_personaggio' : personaggio['character']['name'],
                        'foto_personaggio' : (personaggio['character']['image']['medium'] if personaggio['character']['image'] else "None"),
                        'foto_personaggio_originale' : (personaggio['character']['image']['original'] if personaggio['character']['image'] else "None"),
                        
                    }
                    
                    lista_personaggi.append(personaggio_trovato)
                    count = count + 1
                    
                    
                    
                
            #estrarre info che mi servono
            programma_televisivo = {
                'nome_programma' : programma['show']['name'],
                'tipo' : programma['show']['type'],
                'lingua' : programma['show']['language'],
                'generi' : programma['show']['genres'],
                'stato' : programma['show']['status'],
                'debutto' : programma['show']['premiered'],
                'conclusione' : programma['show']['ended'],
                'durata_episodo' : programma['show']['runtime'],
                'numero_episodi' : programma['show']['weight'],
                'descrizione' : programma['show']['summary'],
                'luogo_produzione' : (programma['show']['network']['country']['name'] if programma['show']['network'] else "None"),
                'foto_media' : (programma['show']['image']['medium'] if programma['show']['image'] else "None"),
                'foto_originale' : (programma['show']['image']['original'] if programma['show']['image'] else "None"),
                'valutazione' : programma['show']['rating']['average'],
                'personaggi' : lista_personaggi,
                    
                
                
                
                
                
                
            }
            
            lista_programmi.append(programma_televisivo)
            
        return render_template('risultati_ricerca.html',lista_programmi=lista_programmi)
        
    

if __name__=="__main__":
    app.run()