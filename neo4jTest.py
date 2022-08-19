from py2neo import Graph,NodeMatcher,cypher
#graph - Connect the neo4j database
#neo4j is runing on localhhost and port 7687 
#auth(username,password) name(the name of the database)
graph = Graph("http://localhost:7474", auth=("neo4j","test"),name="neo4j")

def search_by_label(label):
    #query = neo4j cypher query
    # query = f'match (n:{label}) return n'
    query = f'MATCH (n:CBoK) RETURN n'
    #query1Result - store the result of the query
    #run() - build-in function of py2neo to execute cypher query 
    query1Result = graph.run(query)
    #fomart the result using to_data_frame() function (pandas)
    data = query1Result.to_data_frame()
    #convert the data to json format
    json_data = data.to_json(orient="records",force_ascii=False)
    return json_data