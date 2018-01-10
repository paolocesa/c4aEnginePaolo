import jsonpickle
import json
import re
from random import randint

import controller.get_data as gData

#convert a json to an xml
from model.Close import Close


def json2xml(json_obj, obj_name):
    result_list = list()
    #start creating the list of xml elements
    result_list.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    #name of the xml
    result_list.append("<%s" % (obj_name))
    for tag_name in json_obj:
        #each element has to become an attribute of the xml
        #todo: verificare se gestisce tutte le eccezioni
        sub_obj = json_obj[tag_name]
        if isinstance(sub_obj, unicode):
            #print "**********sono dentro all'if"
            sub_obj=sub_obj.replace('"',"&quot;")
            sub_obj =sub_obj.replace("'","&apos;")
            sub_obj =sub_obj.replace("<","&lt;")
            sub_obj =sub_obj.replace(">","&gt;")
            sub_obj =sub_obj.replace("&","&amp;")

        result_list.append("%s =\"%s\" " % (tag_name, sub_obj))
    #close the tag at the end
    result_list.append("/>")
    return "\n".join(result_list)

def generateXMLDoc(class_instance):
    json_element = jsonpickle.encode(class_instance)
    json_dict = json.loads(json_element)
    #class name is saved as key, need to be removed
    class_name = json_dict.pop("py/object").encode('utf-8')
    #rename it using only tha class name
    class_name = "<"+class_name
    #remove the path
    class_name = class_name.replace(".","testo",class_name.count(".")-1)
    class_name = class_name.replace(".", ">")
    #set to lowercase
    class_name = re.sub(r"<.*>","",class_name).lower()
    string_unicode = json2xml(json_dict, class_name)
    # save as xml file all the data retrieved
    final_str = (string_unicode.encode('utf8'))
    #print final_str
    #create the xml file
    with open("%s.xml" % (class_name), "w") as xml_file:
        xml_file.write("{}".format(final_str))
    #aggiunta 25 novembre
    return xml_file.name

def createMessageJson(resourceMessageText, template_mex_structure):

    # struttura iniziale del message, solo con body, closes vuote e dentro alle formulations solo l'ordine
    mexJson = {
        "closes": ["regolaOrdine"],
        "open_text": {"body": resourceMessageText + "\n"},
        "verbal_formulations": {
            "order": {"precondition": "regolaOrdine"}
        }
    }
    # recupero le frasi che compongono il messaggio
    mex_struct = template_mex_structure['tags'].split(",")
    # uso mex_struct per ricavare l'ordine
    dim = len(mex_struct)
    conseq = {}
    for i in range(dim):
        conseq[str(i + 1)] = mex_struct[i]
    mexJson['verbal_formulations']['order']['consequence'] = conseq
    # dal template recupero le informazioni relative alla struttura del messaggio
    pieces_to_have = mex_struct
    # escludo body, serve solo per l'ordine
    pieces_to_have.remove('body')
    tone_to_take = template_mex_structure['tone']
    # uso mex_struct per ricavare l'ordine

    # usato per salvare le frasi che vengono chieste a DB
    sentences = {}

    # recupero tutte le frasi necessarie
    for piece in pieces_to_have:
        #print "piece----> ", piece, type(piece)
        # chiamo DB
        closesFound = gData.getClauses(piece, tone_to_take)
        #print type(closesFound)
        flagNoPieceFound = False
        if closesFound == None:
            flagNoPieceFound = True

        if flagNoPieceFound:
            closeEmpty = Close("00")
            closeEmpty.text = ""
            closeEmpty.preconditions = ""
            sentences[piece] = closeEmpty
            #print "sentences-------->", sentences
        else:
            numFound = len(closesFound)
            # controllo se ne ho piu' di uno e, nel caso, filtro random per averne una sola
            if numFound > 1:
                sentences[piece] = closesFound[randint(0, numFound - 1)]
            else:
                sentences[piece] = closesFound[0]
    closes_to_be_added = []
    # inserisco tutti i pezzi di frase nel json
    for s in sentences:
        # setto variabile per lavorare meglio
        frase = sentences[s]
        # aggiungo in open text la frase
        mexJson['open_text'][s] = frase.text + "\n"
        # splitto il testo libero dentro a preconditions, dividendo ad ogni virgola
        preconditions_splitted = frase.preconditions.split(",")
        # setto a prescindere la consequence da usare
        mexJson['verbal_formulations'][s] = {}
        mexJson['verbal_formulations'][s]['consequence'] = s
        # se non ci sono preconditions, introduco quella fittizia
        if len(frase.preconditions) == 0:
            # regola fittizia sempre vera
            closes_to_be_added.append('regolaNoPreconditions')
            mexJson['verbal_formulations'][s]['precondition'] = 'regolaNoPreconditions'
        else:
            # aggiungo le preconditions trovate dentro ad una lista a parte (controllo dopo se ci sono ripetizioni)
            closes_to_be_added.extend(preconditions_splitted)
            # aggiungo la verbal formulation per la sentence
            # mexJson['verbal_formulations'][s] = {}
            mexJson['verbal_formulations'][s]['precondition'] = frase.preconditions
            # mexJson['verbal_formulations'][s]['consequence'] = s
    # salvo dentro a closes le closes trovate, dopo aver rimosso i duplicati
    closes = []
    for i in closes_to_be_added:
        if i not in closes:
            closes.append(i)
    mexJson['closes'].extend(closes)

    with open('messageGenerated.json', 'w') as json_file:
        json.dump(mexJson, json_file)

    return json_file.name


def createMessageJsonV2(resourceMessageText, template_mex_structure, prec_vere, prec_false):
    # struttura iniziale del message, solo con body, closes vuote e dentro alle formulations solo l'ordine
    mexJson = {
        "closes": ["regolaOrdine"],
        "open_text": {"body": resourceMessageText + "\n"},
        "verbal_formulations": {
            "order": {"precondition": "regolaOrdine"}
        }
    }
    # recupero le frasi che compongono il messaggio
    mex_struct = template_mex_structure['tags'].split(",")
    # uso mex_struct per ricavare l'ordine
    dim = len(mex_struct)
    conseq = {}
    for i in range(dim):
        conseq[str(i + 1)] = mex_struct[i]
    mexJson['verbal_formulations']['order']['consequence'] = conseq
    # dal template recupero le informazioni relative alla struttura del messaggio
    pieces_to_have = mex_struct
    # escludo body, serve solo per l'ordine
    pieces_to_have.remove('body')
    tone_to_take = template_mex_structure['tone']
    # uso mex_struct per ricavare l'ordine

    # usato per salvare le frasi che vengono chieste a DB
    sentences = {}

    # recupero tutte le frasi necessarie
    for piece in pieces_to_have:
        # print "piece----> ", piece, type(piece)
        # chiamo DB
        closesFound = gData.getClauses(piece, tone_to_take)
        # print type(closesFound)
        flagNoPieceFound = False
        if closesFound == None:
            flagNoPieceFound = True

        if flagNoPieceFound:
            closeEmpty = Close("00")
            closeEmpty.text = ""
            closeEmpty.preconditions = ""
            sentences[piece] = closeEmpty
            # print "sentences-------->", sentences
        else:
            numFound = len(closesFound)
            # controllo se ne ho piu' di uno e, nel caso, filtro random per averne una sola
            if numFound > 1:
                #todo: invece che filtrare random, scelgo prima quelle in cui so gia' che le regole sono vere
                #todo: a questo punto non ha piu' senso la struttura json con preconditions
                # per ogni clause con preconditions
                closesNotValid = []
                for c in closesFound:
                    prec = c.preconditions
                    # controllo e tengo solo quelle che hanno regole non false
                    prec_splitted = prec.split(",")
                    isFalse = False
                    for el in prec_splitted:
                        if el in prec_false:
                            # rimuovi c perche' ha una precondition falsa
                            isFalse = True
                    if isFalse:
                        closesNotValid.append(c)
                # all the closes found have been evaluated, remove the not valid
                for c in closesFound:
                    if c in closesNotValid:
                        closesFound.remove(c)
                #from the remaining closes, check if more than one are still present
                newNumFound = len(closesFound)
                if newNumFound >= 1:
                    #select one at random from the new group
                    sentences[piece] = closesFound[randint(0, newNumFound - 1)]
                else:
                    closeEmpty = Close("00")
                    closeEmpty.text = ""
                    closeEmpty.preconditions = ""
                    sentences[piece] = closeEmpty
            else:
                sentences[piece] = closesFound[0]
    closes_to_be_added = []
    # inserisco tutti i pezzi di frase nel json
    for s in sentences:
        # setto variabile per lavorare meglio
        frase = sentences[s]
        # aggiungo in open text la frase
        mexJson['open_text'][s] = frase.text + "\n"
        # splitto il testo libero dentro a preconditions, dividendo ad ogni virgola
        preconditions_splitted = frase.preconditions.split(",")
        # setto a prescindere la consequence da usare
        mexJson['verbal_formulations'][s] = {}
        mexJson['verbal_formulations'][s]['consequence'] = s
        # se non ci sono preconditions, introduco quella fittizia
        if len(frase.preconditions) == 0:
            # regola fittizia sempre vera
            closes_to_be_added.append('regolaNoPreconditions')
            mexJson['verbal_formulations'][s]['precondition'] = 'regolaNoPreconditions'
        else:
            # aggiungo le preconditions trovate dentro ad una lista a parte (controllo dopo se ci sono ripetizioni)
            closes_to_be_added.extend(preconditions_splitted)
            # aggiungo la verbal formulation per la sentence
            # mexJson['verbal_formulations'][s] = {}
            mexJson['verbal_formulations'][s]['precondition'] = frase.preconditions
            # mexJson['verbal_formulations'][s]['consequence'] = s
    # salvo dentro a closes le closes trovate, dopo aver rimosso i duplicati
    closes = []
    for i in closes_to_be_added:
        if i not in closes:
            closes.append(i)
    mexJson['closes'].extend(closes)

    with open('messageGenerated.json', 'w') as json_file:
        json.dump(mexJson, json_file)

    return json_file.name