from controller.mini_planner.Logica import readXML, evaluateRules

import json
import re

#todo: versione nuova da testare, parlarne con Diego
def performRulesOnData(profileData, resourceData, contextData):
    RULES_DOCUMENT = "rules.json"
    profile = readXML(profileData)
    resource = readXML(resourceData)
    context = readXML(contextData)
    data = {}
    if profile is not None:
        data.update(profile)
    if resource is not None:
        data.update(resource)
    if context is not None:
        data.update(context)
    closesResults = evaluateRules(RULES_DOCUMENT, data)
    rules_True = []
    rules_False = []
    for r in closesResults:
        if closesResults[r]:
            rules_True.append(r)
        else:
            rules_False.append(r)
    return rules_True, rules_False, data

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

def replacePlaceHolders(message_text, data, word_data, order):
    #replace the body_placeholder of the message with the actual body
    final_msg = order.replace("{*body*}", message_text['body'])
    for w_var in word_data:
        if w_var != 'order':
            #todo: passare a Diego questo errore,
            #UnicodeEncodeError: 'ascii' codec can't encode character u'\u2019' in position 18: ordinal not in range(128)
            #viene lanciato ogni tanto, capire cosa recupera da db quando si verifica
            final_msg = final_msg.replace("{*" + w_var + "*}", str(word_data[w_var]))
    # once the message is ready, all the msg variables have to be filled with the right value
    for var in data:
        final_msg = final_msg.replace("[*" + var + "*]", str(data[var]))
    #check if there is still some {*w*} in the text and, in case, remove them
    formulationPattern = re.compile('{\*\w+\*}')
    final_mex = formulationPattern.sub('', final_msg)
    # Todo: added a control if there is still some placeholder not found
    final_mex = final_mex.replace('[*', '{*')
    final_mex = final_mex.replace('*]', '*}')
    varPattern = re.compile('({\*\w+\*})')
    varFound = varPattern.search(final_mex)
    if varFound is not None:
        # Todo: stabilire come comunicare che e' stato trovato un campo non valido (ora inserisco "DATA-NOT-FOUND")
        final_mex = varPattern.sub('[*ERROR: DATA-NOT-FOUND*]', final_mex)

    return final_mex

def composeMessageV2(parametersData, messageData, closesVerified):

    #analyze how the message has to be built
    with open(messageData) as json_mex:
        message = json.load(json_mex)
        json_mex.close()
    #take the closes to be used
    closes_used = message['closes']
    #the text to be composed together
    text = message['open_text']
    #the formulations that specify the structure of the message
    forms = message['verbal_formulations']

    #from all the results, keep the ones needed for this message
    neededResults = {}
    for c in closes_used:
        if c in closesVerified:
            #set the value to True, used in case there is an alternative
            neededResults[c] = True

    #analyze the formulations and compose the peices of message
    msg_pieces = composeFormulations(neededResults, forms, text)
    #compose the message following the order defined in json
    order = orderMessage(msg_pieces)
    #replace all the placeholders to make the message more personal
    personal_msg = replacePlaceHolders(text, parametersData, msg_pieces, order)
    return personal_msg

from model.Aged import Aged
from model.Resource import Resource
from controller.mini_planner.generalize_data import generateXMLDoc, createMessageJsonV2

class ProvaRun:
    def demografic(self):
        u = Aged(0001)
        u.name = "Paolo"
        u.email = "3"
        u.topics = ["sports", "movies"]
        r = Resource(02, "Evento & sportivo")


#inserire da qui negli engines di c4a
        utente = generateXMLDoc(u)
        risorsa = generateXMLDoc(r)

        #todo: verificare come bisogna cambiare tutta la struttura del Template
        provaTemplate={}
        provaTemplate['tags'] = "greetings,body,motivate"
        provaTemplate['tone'] = "Neutral"

        vere, false, data = performRulesOnData(utente, risorsa, None)
        message_json = createMessageJsonV2("body del messaggio, preso dalla risorsa",provaTemplate, false)
        msg_to_be_written = composeMessageV2(data, message_json, vere)

        with open("PersonalizedMsgV2.txt", "w") as text_file:
            text_file.write("{}".format(msg_to_be_written))

        print "regole vere: ", vere
        print "regole false: ", false
        print "data salvata: ", data
        print msg_to_be_written

    def provaReplaceFineControllo(self):
        mex = "prima[*hello *]dopo"
        print "mex iniziale : ", mex
        mex = mex.replace('[*','{*')
        mex = mex.replace('*]', '*}')
        print "mex dopo replace : ", mex
        varPattern = re.compile('({\*\w+\*})')
        varFound = varPattern.search(mex)
        if varFound is not None:
            print "sono nell'if: ", type(varFound)
            # Todo: stabilire come comunicare che e' stato trovato un campo non valido (ora inserisco "DATA-NOT-FOUND")
            mex = varPattern.sub('[*ERROR: DATA-NOT-FOUND*]', mex)

        print "finale: ", mex







ProvaRun().demografic()
#ProvaRun().provaReplaceFineControllo()