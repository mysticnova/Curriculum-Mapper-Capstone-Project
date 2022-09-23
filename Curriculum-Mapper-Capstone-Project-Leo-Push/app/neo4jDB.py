from py2neo import Graph,NodeMatcher,cypher,Node,Relationship
import json
from app import api
from config import NEO4j_URI, NEO4j_USER, NEO4j_PASSWORD

# connect to the Neo4j database
try:
    graphDB = Graph(NEO4j_URI, auth=(NEO4j_USER, NEO4j_PASSWORD))
except:
    print("\n****** Neo4j connect failed, please check the neo4j service ******\n")

def search_by_query(query):
    try:
        #using jolt API to get the data to the frontend
        data = api.joltAPI(query) 
        # data = {'links':'[{},{}]','nodes':'[{},{}]'} or data = {'status':'empty_data'}
        return data
    except:
        # return error message if the api call fails
        return {'status': 'joltAPI_error'}

def create_by_user(data):
    for item in data:
        #create a empty node object（source_node）
        source_node = Node()
        #get the data from the frontend (label,name)
        for (key,value) in zip(item['source'].keys(),item['source'].values()):
            if key == 'label':
                #assign a name to the previously created node object
                source_node.add_label(value)
            else:
                #add properties other than label(name, age, height, weight ...)
                source_node[key] = value
        #query whether the current node already exists in the database (check both label and name)
        source_match = NodeMatcher(graphDB).match(item['source']['label'],name=item['source']['name'])
        if source_match.__len__() == 0:
            #not exist: add the currently created node(source_node) to the database
            graphDB.create(source_node)
        else:
            #exist: directly copy the queried node to source_node
            source_node = source_match.first()

        #same as above, just processing the target node
        target_node = Node()
        for (key,value) in zip(item['target'].keys(),item['target'].values()):
            if key == 'label':
                target_node.add_label(value)
            else:
                target_node[key] = value
        target_match = NodeMatcher(graphDB).match(item['target']['label'], name=item['target']['name'])
        if target_match.__len__() == 0:
            graphDB.create(target_node)
        else:
            target_node = target_match.first()

        #handling the relationship
        rel_match = RelationshipMatcher(graphDB) #create a query object
        for (key,value) in zip(item['relationship'].keys(),item['relationship'].values()):
            if key == 'label':
                #relationship object :（‘startNode’, 'knows', 'endNode'）
                rel = Relationship(source_node,value,target_node)
                #any properties except label are added to the relationship object
                for (key1, value1) in zip(item['relationship'].keys(), item['relationship'].values()):
                    if key1 != 'label':
                        rel[key1] = value1
                #Use the previously created query object
                #query whether the current relationship already exists in the database(relationship between source_node and target_node)
                if len(rel_match.match([source_node,target_node],r_type=value)) == 0:
                    graphDB.create(rel)

# delete nodes and relationships by user
def deleteEntity(id, item):
    try:
        if item == 'node':
            # match the node by id
            node = graphDB.evaluate("MATCH (n) WHERE id(n) = {} RETURN n".format(id))
            graphDB.delete(node)
            return {'status':'update_node_success'}
        elif item == 'relationship':
            # match the relationship by id
            relationship = graphDB.evaluate("MATCH ()-[r]-() WHERE id(r) = {} DELETE r".format(id))
            return {'status':'update_relationship_success'}
    except:
        return {'status':'error'}

# create single node by user
def create_node(data):
    # create a empty node object
    source_node = Node()
    for (key, value) in zip(data.keys(), data.values()):
        if key == 'label':
            # add label to the node
            source_node.add_label(value)
        else:
            # add properties to the node
            source_node[key] = value
    # query whether the current node already exists in the database (check both label and name)
    source_match = NodeMatcher(graphDB).match(data['label'], name=data['name'])
    if source_match.__len__() == 0:
        graphDB.create(source_node)
        return {'status':'create_node_success'}
    else:
        source_node = source_match.first()
        return {'status':'node_already_exist'}

# update node attributes
def update_node(id, data):
    try:
        # match the node by id
        node = graphDB.evaluate("MATCH (n) WHERE id(n) = {} RETURN n".format(id))
        for (key, value) in zip(data.keys(), data.values()):
            # update attributes
            node[key] = value
        graphDB.push(node)
        return {'status':'success'}
    except:
        return {'status':'error'}

# update relationship attributes
def update_relationship(id, data):
    try:
        # match the relationship by id
        relationship = graphDB.evaluate("MATCH ()-[r]-() WHERE id(r) = {} RETURN r".format(id))
        for (key, value) in zip(data.keys(), data.values()):
            # update attributes
            relationship[key] = value
        graphDB.push(relationship)
        return {'status':'success'}
    except:
        return {'status':'error'}