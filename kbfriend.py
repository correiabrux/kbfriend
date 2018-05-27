from slackclient import SlackClient
from kanboard import Kanboard
import time
import os

slacktoken = os.environ['SLACKTOKEN']
kbtoken = os.environ['KBTOKEN']
kburl = os.environ['KBURL']

slack_client = SlackClient(slacktoken)
kb = Kanboard(kburl, "jsonrpc", kbtoken)

def opentask(description, projectname, channel):
    try:
        project = kb.getProjectByName(name=projectname)
        project_id = project.get('id')
        task_id = kb.create_task(project_id=project_id, title=description)
        message =  "Task Opened"
        sendmessage(channel, message)
    except:
        message = "Unknow Project"
        sendmessage(channel, message)

def sendmessage(channel, message):
    slack_client.api_call(
        'chat.postMessage',
        channel=channel,
        text=message,
        as_user='true:'
        )

def closetask(channel, taskid):
    try:
        kb.closeTask(task_id=taskid)
        message = "Task Closed"
        sendmessage(channel, message)
    except:
        message = "Unknow Task"
        sendmessage(channel, message)

def listprojects(channel):
    try: 
        list = kb.getAllProjects()
        allprojects = ""
        for i in list:
            project_name = i['name']
            project_id = i['id']
            allprojects = allprojects + " " + project_id + " " + project_name + "\n"
        sendmessage(channel, allprojects)
    except:
        message = "Unknow Project"
        sendmessage(channel, message)       

def getcolumnname(column_id):
    try:
        getname = kb.getColumn(column_id=column_id)
        columnname = getname['title']
        return columnname
    except:
        pass

def listtasks(channel, projectname):
    try: 
        alltasks = ""
        project = kb.getProjectByName(name=projectname)
        project_id = project.get('id')
        tasks = kb.getAllTasks(project_id=project_id)
        for i in tasks:
            column_id = i['column_id']
            column_task = getcolumnname(column_id)
            title_task = i['title']
            id_task = i['id']
            alltasks = alltasks + " " + id_task + " - " + title_task + " - " + column_task + "\n"
        sendmessage(channel, alltasks)
    except:
        message = "Unknow Tasks"
        sendmessage(channel, message)    

def listcolumns(channel, projectname):
    try:
        allcolumns = ""
        project = kb.getProjectByName(name=projectname)
        project_id = project.get('id')
        columns = kb.getColumns(project_id=project_id)
        for i in columns:
            column_name = i['title']
            column_id = i['id']
            allcolumns = allcolumns + " " + column_id + " - " + column_name + "\n"
        sendmessage(channel, allcolumns)
    except:
        message = "Unknow Project"
        sendmessage(channel, message)


def openproject(channel, projectname):
    try:
        project = kb.createProject(name=projectname)
        message = "Project Created"
        sendmessage(channel, message)
    except:
        message = "Unknow Command"
        sendmessage(channel, message)


def movetask(channel, projectid, idtask, idcolumn):
    try: 
        swimlane = kb.getTask(task_id=idtask)['swimlane_id']
        kb.moveTaskPosition(project_id=projectid,task_id=idtask,column_id=idcolumn,position=1,swimlane_id=swimlane)
        message = "Task Moved"
        sendmessage(channel, message)
    except: 
        message = "Failed, try again"
        sendmessage(channel, message)

def parser(text, channel):
    try: 
        splittext = text.split(' ')
        getlast = splittext[3:]
        description = ' '.join(getlast)
        return description
    except: 
        message = "Parse Failed"
        sendmessage(channel, message)

def main():
    if slack_client.rtm_connect():
        while True:
            events = slack_client.rtm_read()
            for event in events:
                if (
                    'channel' in event and
                    'text' in event and
                    event.get('type') == 'message'
                ):
                    channel = event['channel']
                    text = event['text']
                    if 'kb' == text.split()[0]:
                        if 'opentask' == text.split()[1]:
                            projectname = text.split()[2]
                            description = parser(text, channel)
                            opentask(description, projectname, channel)
                        elif 'closetask' == text.split()[1]:
                            taskid = text.split()[2]
                            closetask(channel, taskid)
                        elif 'listcolumns' == text.split()[1]:
                            projectname = text.split()[2]
                            listcolumns(channel, projectname)
                        elif 'listtasks' == text.split()[1]:
                            projectname = text.split()[2]
                            listtasks(channel, projectname)
                        elif 'openproject' == text.split()[1]:
                            projectname = text.split()[2]
                            openproject(channel, projectname)
                        elif 'listprojects' == text.split()[1]:
                            listprojects(channel)
                        elif 'movetask' == text.split()[1]:
                            projectid = text.split()[2]
                            idtask = text.split()[3]
                            idcolumn = text.split()[4]
                            movetask(channel,projectid,idtask,idcolumn)
                        elif 'help' == text.split()[1]:
                            message = "```\
$kb listprojects                          #Lista Projetos\n\
$kb listtasks project                     #Lista Taks\n\
$kb listcolumns project                   #Lista colulnas\n\
$kb openproject projectname               #Cria Projeto\n\
$kb opentask project description          #Abre Task\n\
$kb closetask taskid                      #Fecha Task\n\
$kb movetask projectid taskid columnid    #Move Task```"
                            sendmessage(channel, message)
                        else:
                            message = "Unknow Command"
                            sendmessage(channel, message)
                        
            time.sleep(1)
    else:
        print('Connection failed, invalid token?')

if __name__ == "__main__":
    main()
