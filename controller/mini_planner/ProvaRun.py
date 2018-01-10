from controller.mini_planner.Logica import readXML, evaluateRules

import json
import re

#todo: versione nuova da testare, parlarne con Diego
def calcoloFiltri(profileData, resourceData, contextData):
    RULES_DOCUMENT = "rules.json"
    profile = readXML(profileData)
    resource = readXML(resourceData)
    context = readXML(contextData)
    data = {}
    data.update(profile)
    data.update(resource)
    if context is not None:
        data.update(context)
    closesResults = evaluateRules(RULES_DOCUMENT, data)
    filtri_True = []
    filtri_False = []
    for r in closesResults:
        if closesResults[r]:
            filtri_True.append(r)
        else:
            filtri_False.append(r)
    return filtri_True, filtri_False

def composeFormulations(closes_results, formulations, open_text):
    word_pieces = {}
    for w in formulations:
        close = formulations[w]['precondition']
        splitted_close = close.split(",")
        numCloses = len(splitted_close)
        results_multiplePrec = {}
        if numCloses > 1:
            for i in range(0, numCloses):
                results_multiplePrec[splitted_close[i]] = closes_results[splitted_close[i]]
            flagBrokenLoop = False
            for e in results_multiplePrec:
                if results_multiplePrec[e]== False:
                    flagBrokenLoop = True
                    break
            if flagBrokenLoop:
                hypotesis = False
            else:
                hypotesis = True
        else:
            hypotesis = closes_results[close]

        if hypotesis:
            word_pieces[w] = formulations[w]['consequence']
        else:
            if 'alternative' in formulations[w]:
                word_pieces[w] = formulations[w]['alternative']
    for t in open_text:
        for piece in word_pieces:
            if t == word_pieces[piece]:
                word_pieces[piece] = open_text[t]
    return word_pieces
def orderMessage(sentences):
    order = sentences['order']
    max_index = len(order)
    start_index = 1
    message_ordered = ""
    while start_index <= max_index:
        str_index = str(start_index)
        message_ordered = message_ordered + "{*"+order[str_index].encode('ascii','ignore')+"*}"
        start_index = start_index + 1
    return message_ordered
def replacePlaceHolders(message_text,data,word_data, order):
    #replace the body_placeholder of the message with the actual body
    final_msg = order.replace("{*body*}", message_text['body'])
    for w_var in word_data:
        if w_var != 'order':
            final_msg = final_msg.replace("{*" + w_var + "*}", str(word_data[w_var]))
    # once the message is ready, all the msg variables have to be filled with the right value
    for var in data:
        final_msg = final_msg.replace("[*" + var + "*]", str(data[var]))
    #check if there is still some {*w*} in the text and, in case, remove them
    p = re.compile('{\*\w+\*}')
    final_mex = p.sub('', final_msg)
    return final_mex
def composeMessage(profileData, resourceData, contextData, messageData):
    RULES_DOCUMENT = "rules.json"
    #get the information from all the xml needed
    profile = readXML(profileData)
    #print "profile-->", type(profile), profile
    resource = readXML(resourceData)
    context = readXML(contextData)
    #merge everything together as 'data'
    data = {}
    data.update(profile)
    data.update(resource)
    if context is not None:
        data.update(context)
    #analyze how the message has to be built
    with open(messageData) as json_mex:
        message = json.load(json_mex)
        json_mex.close()
    #take the closes to be used
    closes_used = message['closes']
    #the text to be composed togethere
    text = message['open_text']
    #the formulations that specify the structure of the message
    forms = message['verbal_formulations']
    #evaluate the rules
    closesResults = evaluateRules(RULES_DOCUMENT, data)
    #form all the results, take only the one needed for this message
    neededResults = {}
    for c in closesResults:
        if c in closes_used:
            neededResults[c] = closesResults[c]
    #analyze the formulations and compose the peices of message
    msg_pieces = composeFormulations(neededResults, forms, text)
    #compose the message following the order defined in json
    order = orderMessage(msg_pieces)
    #replace all the placeholders to make the message more personal
    personal_msg = replacePlaceHolders(text, data, msg_pieces, order)
    return personal_msg



from model.Aged import Aged
from model.Resource import Resource
from controller.mini_planner.generalize_data import generateXMLDoc, createMessageJson, createMessageJsonV2

class ProvaRun:
    def demografic(self):
        u = Aged(0001)
        u.name = "Paolo"
        u.email = "3"
        u.topics = ["sports", "movies"]
        r = Resource(02, "Evento & sportivo")


#inserire da qui negli engines di c4a
        utente = generateXMLDoc(u)
        #print utente
        risorsa = generateXMLDoc(r)
        #risorsa = "resource.xml"
        #print risorsa

        #todo: dopo la demo pensare a come rendere anche questo generico
        provaTemplate={}
        provaTemplate['tags'] = "greetings,body,motivate"
        provaTemplate['tone'] = "High"

        filtri = calcoloFiltri(utente, risorsa, None)
        vere = filtri[0]
        false = filtri[1]
        vere_str = ""
        false_str = ""
        for v in vere:
            vere_str = vere_str+","+v
        vere_str = vere_str.replace(",","",1)
        for f in false:
            false_str = false_str+","+f
        false_str = false_str.replace(",","",1)
        print vere_str
        print false_str

        splittedFalse = false_str.split(",")
        print splittedFalse
        print false



        m = createMessageJson("body del messaggio, preso dalla risorsa",provaTemplate)
        m2 = createMessageJsonV2("body del messaggio, preso dalla risorsa",provaTemplate, vere, false)
        #m = "messageGenerated.json"
        '''mex_to_be_written = composeMessage(utente, risorsa, None, m)

        with open("PersonalizedMessageGenerated.txt", "w") as text_file:
            text_file.write("{}".format(mex_to_be_written))
        print mex_to_be_written
        '''





ProvaRun().demografic()