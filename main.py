# This is a sample Python script.

from optparse import Values
from flask import Flask, request, redirect, session, url_for,json, jsonify
from flask import render_template
#import simplejson
#import werkzeug
from werkzeug.datastructures import ImmutableMultiDict


from collections import OrderedDict


import requests

# setup global variables
nAgents = 0
nGoods = 0

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY' 


@app.route('/setupAuction', methods=['GET'])
def route_setupAuction():
    return render_template('setupAuction.html')

@app.route('/inputAgents', methods=['GET'])
def route_inputAgents():

    #if request.method == 'GET':
        args = request.args
        setupAuction_data = ImmutableMultiDict(args)
        

        session['setupAuction_data']=setupAuction_data
        print(session['setupAuction_data'])
        session['nAgents'] = int(args["nbAgents"])
        nAgents=session['nAgents']
        session['nGoods'] = int(args["nbGoods"])
        nGoods=session['nGoods']

        data={ 
            'nAgents' : nAgents,
            'nGoods' : nGoods
        }
        
        json_data=json.dumps(data, indent=4)
        print(json_data)
            

        return render_template('inputAgents.html', nAgents = nAgents,nGoods=nGoods,json_data=json_data)
    


@app.route('/inputGoods', methods=['GET'], endpoint='route_inputGoods')
#def route_inputGoods(arg, **kwargs):
def route_inputGoods():

    args = request.args
    print('args :', args)


    imd_Agent = ImmutableMultiDict(args)
    session['imd_Agent']=imd_Agent

    valu=list(imd_Agent.items())
    #print(valu[1])# GIVES out this ('agentURL[1]', 'url1')
    val=list(imd_Agent.values())
    #print(val[1]) #gives out url1
    NumberOfAgents=session['nAgents']
    print("session agent data print")
    print(NumberOfAgents)

    ListOfAgentsData=[] #a list to append the little dictionaries to
    for n in range(0,NumberOfAgents*2,2): 
        val=list(imd_Agent.values())
        #print(val[n])
        #print(val[n+1])
        data={
          'AgentName' : val[n],
            'AgentURL' : val[n+1]
                                    }
        #print(data)
        ListOfAgentsData.append(data)

        #json_dat=json.dumps(data, indent=4)
        #print(json_dat)

    #print(ListOfAgentsData)
    json_dat=json.dumps(ListOfAgentsData, indent=4)
    print(json_dat)
    nGoods=session['nGoods']

    session[json_dat]=json_dat

    return render_template('inputGoods.html', nGoods=nGoods,nAgents = nAgents,json_dat=json_dat)



@app.route('/inputValues', methods=['GET'], endpoint='route_inputValues')
def route_inputValues():

    args = request.args

    nGoods=int(session['nGoods'])
    nAgents=int(session['nAgents'])

    
    InputGood_Data = ImmutableMultiDict(args)
    session['InputGood_Data']=InputGood_Data #newly added
    print(session['InputGood_Data'])

    valu=list(InputGood_Data.items())
    print(valu[1])
    ListOfGoods=[] #a list to append the little dictionaries to
    for n in range(0,nGoods): 
        val=list(InputGood_Data.values())
        #print(val[n])
        
        Good_data={
          'Good_Name' : val[n]
                                    }
        #print(data)
        ListOfGoods.append(Good_data)

        #json_dat=json.dumps(data, indent=4)
        #print(json_dat)

    #print(ListOfGoods)
    Good_data=json.dumps(ListOfGoods, indent=4)
    print(Good_data)

    return render_template('inputValues.html', nGoods=nGoods,nAgents=nAgents,Good_data=Good_data)

@app.route('/inputSynergies', methods=['GET'], endpoint='route_inputSynergies')
def route_inputSynergies():

    nGoods=session['nGoods']
    nAgents=session['nAgents']
    

    args = request.args
    #args=request.form.get("bookid")
    print('args :', args)

    Synergy_data = ImmutableMultiDict(args)
    session['Synergy_data']=Synergy_data
    val=list(Synergy_data.values())
    #print(val[1])

    for v in range(len(Synergy_data)):
        val=list(Synergy_data.values())
        #print(val[v])



    ListOfGoodValuesData=[]
    for n in range(len(Synergy_data)): 

        for m in range(1,int(nAgents)+1): 
            for x in range(1,int(nGoods)+1): 
                    val=list(Synergy_data.values())
                    data={'agent'+ str(m):[
                        {
                            'name_good'+ str(x): 'Good'+ str(x),
                            'value_good'+ str(x): val[n]
                        }
                    ]}
                    ListOfGoodValuesData.append(data)

        #json_dat=json.dumps(data, indent=4)
        #print(json_dat)

    #print(ListOfGoodValuesData)
    Value_data=json.dumps(ListOfGoodValuesData, indent=4)
    #print(Value_data)

    return render_template('inputSynergies.html', nGoods=nGoods,nAgents=nAgents,Value_data=Value_data)
@app.route('/synergydisplay', methods=['GET'], endpoint='route_synergydisplay')
def route_synergydisplay():


#Getting data that we extracted from all of the other routes to build the final CompDesc 
    nGoods=int(session['nGoods'])
    nAgents=int(session['nAgents'])
    setupAuction_data=session['setupAuction_data']

    InputGood_Data=session['InputGood_Data']

    Synergy_data=session['Synergy_data']

    imd_Agent=session['imd_Agent']



    ListOfGoods=[] #a list to append the little dictionaries's values to
    for n in range(0,nGoods): 
        val=list(InputGood_Data.values())
        Good_data= val[n]
        ListOfGoods.append(Good_data)


##### To organize the agents data anmchiw chwiya b chwiya 
    #print("Synergy data")
    #print(session['Synergy_data'])
    #print("\nGood's data")
    #print(InputGood_Data)
    

    ChildNodes=[]

    for y in range(1,nAgents+1):
        AgentChildNodes=[]
        for x in range(1,nGoods+1):
            Nodes={ 
                "node": "leaf", 
                "value" : Synergy_data["Value of Good "+str(x)+" to agent "+str(y)], 
                "units": Synergy_data["Units of Good "+str(x)+" to agent "+str(y)], 
                "good": InputGood_Data["GoodName["+str(x)+"]"]
                }
            #AgentChildNodes=["agent "+str(y) :  Nodes]
            AgentChildNodes.append(Nodes) #assemble all the child nodes of a single agent
        
        ChildNodes.append(AgentChildNodes) #assemble all the child nodes into one list
   
    Nodes_dat=json.dumps(ChildNodes, indent=4)
    #print(Nodes_dat)

#######

    allocation=[]
    for y in range(1,nAgents+1):
        #GoodAllocationPerAgent=[]
        dicts={}
        for x in range(1,nGoods+1):

            dicts[InputGood_Data["GoodName["+str(x)+"]"]]=Synergy_data["Allocation of Good "+str(x)+" to agent "+str(y)]

        allocation.append(dicts)

    allocation_data=json.dumps(allocation, indent=4)
    #print("allocation data")
    #print(allocation_data)
    



####### Building a list containing agent informations 
    imd_Agent=session['imd_Agent']
    AgentData=[]
    for n in range(1,nAgents+1): 

            data={
                'id' : imd_Agent['agentName['+str(n)+']'],
                'url' : imd_Agent['agentURL['+str(n)+']'],
                "valuation":{
                    'node':"ic",
                    'value': 0, 
                    'min':1,
                    'max': 1, 
                    'child_nodes': ChildNodes[(n-1)]
                    },
                'allocation':allocation[(n-1)],
                'budget':imd_Agent['agentBudget['+str(n)+']']
                
                }
    
            AgentData.append(data)
   
    json_dat=json.dumps(AgentData, indent=4)
    #print(json_dat)

#####


    for n in range(1,nGoods+1): 
        data={  'competition_id' : setupAuction_data['competition_id'],
                'title' : setupAuction_data['title'],
                'description' : setupAuction_data['description'],
                'starts': setupAuction_data['starts'],
                'response_clock': setupAuction_data['response_clock'],
                'bid_clock': setupAuction_data['bid_clock'],
                'mechanism': setupAuction_data['mechanism'],
                'goods': ListOfGoods, 
                'agents': [ AgentData

                ]
        }
    

    json_data=json.dumps(data, indent=4)
    print(json_data)

    
    #data = json.dumps(json_data)
    with open('data.json','w') as f:
        json.dump(json_data, f,indent = 4)
        #f.write(data)


    return render_template('synergydisplay.html', nGoods=nGoods,nAgents=nAgents,json_data=json_data)


if __name__ == '__main__':



    app.run(host='127.0.0.1',port=5000)

