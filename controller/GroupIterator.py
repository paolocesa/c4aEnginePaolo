from mini_planner.engine_one_miniplanner import launch_engine_one_Group
from planner.engine_three import launch_engine_three_Group

#iteration for the group intervention to make the Engine 1 work
def iterateOverTheGroup(group_json_req):
    #nella richiesta ho una lista di ids
    #todo: lo tratto come un json, verificare se deve essere una request e quindi cambiare con
    #todo: id_List = group_json_req.form['list_ids']
    id_List = group_json_req['list_ids']
    #uso una lista per memorizzare tutti  i miniplan
    group_list_miniplan = {}

    #per ogni id nella lista
    for id in id_List:
        #setto il profile uguale all'id
        #todo: stesso discorso di prima--> group_json_req.form['aged_id'] = id
        group_json_req['aged_id']= id
        #chiamo l'engine 1, che salva nel DB il miniplan (encodeResponse.postGeneratedMessage) e ritorna il json contenente la response
        #todo: uso Group per le prove, in definitiva usare laungh_engine_one_Pendulum
        response_json = launch_engine_one_Group(group_json_req)
        #memorizzo nella lista le informazioni, tenendo la corrispondenza id-miniplan
        group_list_miniplan[id] = response_json


    return group_list_miniplan

#iteration for the group intervention to make the Engine 3 work
def iterateOverTheIds(group_json_req):
    #nella richiesta ho una lista di ids
    # todo: lo tratto come un json, verificare se deve essere una request e quindi cambiare con
    # todo: id_List = group_json_req.form['list_ids']
    id_List = group_json_req['list_ids']
    # uso una lista per memorizzare tutti  i plans
    group_list_plans = {}

    #per ogni id nella lista
    for id in id_List:
        #setto il profile uguale all'id
        # todo: stesso discorso di prima--> group_json_req.form['aged_id'] = id
        group_json_req['aged_id'] = id
        #chiamo l'engine 3, che invia a madrid i miniplan e ritorna il json contenente il plan
        # todo: uso Group per le prove, in definitiva usare laungh_engine_three
        response_json = launch_engine_three_Group(group_json_req)
        #memorizzo nella lista le informazioni, tenendo la corrispondenza id-plan
        group_list_plans[id] = response_json

    return group_list_plans

#classe di test per verificare il funzionamento, non serve
class GroupIterator:
    def demo(self):

        myListIds = []
        #Erodiliana CARICATO
        myListIds.append("2")
        #Abbondanza DE PADOVA
        myListIds.append("3")

        my_req = {}
        my_req['list_ids'] = myListIds
        #to be changed in the iteration
        my_req['aged_id'] = ""
        my_req['pilot_id'] = "1"
        my_req['intervention_session_id'] = "1"
        #risorsa: Orti di guerra- Gruppo di lettura
        my_req['resource_id'] = "Op1"
        #template: proporre di iniziare un nuovo hobby
        my_req['template_id'] = "31"
        my_req['miniplan_local_id'] = "1"
        my_req['from_date'] = "01/01/2018"
        my_req['to_date'] = "25/01/2018"

        '''
        miniplanObtained = iterateOverTheGroup(my_req)
        for m in miniplanObtained:
            print m, miniplanObtained[m]
        '''
        plansObtained = iterateOverTheIds(my_req)
        for p in plansObtained:
            print p, plansObtained[p]

GroupIterator().demo()