def getListMessages(messages, nmsg, resource, channels):
    '''
    Check the messages to send for the resource -> id_resource, compose the list based on importance of a message
    :param messages: dict of messages like sent by the api
    :param nmsg: number of messages to send
    :return: list with the messages to send
    '''
    comp_msgs = []
    msgs = []
    list_messages = []
    for m in messages:
        if m['Resource_ID'] == resource.resource_id:
            if m['Compulsory'] == 'Yes' and m['Channel'] in channels:
                comp_msgs.append(m)
            elif m['Channel'] in channels:
                msgs.append(m)

    if len(comp_msgs) + len(msgs) < nmsg:
        for c in comp_msgs:
            list_messages.append(c)
        for m in msgs:
            list_messages.append(m)
        return list_messages

    else:
        for i in range(0, nmsg):
            if i < len(comp_msgs):
                list_messages.insert(int(comp_msgs[i]['Message_ID'][-2:]), comp_msgs[i])
            elif len(msgs) != 0:
                list_messages.insert(int(msgs[i - len(comp_msgs)]['Message_ID'][-2:]) - 1, msgs[i - len(comp_msgs)])

        return list_messages


# TODO fix
def selectMessages(messages, nmsg, channels):
    comp_msgs = []
    msgs = []
    list_messages = []
    for m in messages:
        if m.is_compulsory == 'Yes' and m.channels[0]['channel_name'] in channels:
            comp_msgs.append(m)
        elif m.channels[0]['channel_name'] in channels:
            msgs.append(m)

    if len(comp_msgs) + len(msgs) < nmsg:
        for c in comp_msgs:
            list_messages.append(c)
        for m in msgs:
            list_messages.append(m)
        return list_messages

    else:
        for i in range(0, nmsg):
            if i < len(comp_msgs):
                list_messages.insert(int(comp_msgs[i].message_id[-2:]), comp_msgs[i])
            elif len(msgs) != 0:
                list_messages.insert(int(msgs[i - len(comp_msgs)].message_id[-2:]) - 1, msgs[i - len(comp_msgs)])

        return list_messages
