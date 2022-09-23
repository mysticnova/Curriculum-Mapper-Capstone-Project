import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from config import JOLT_URL, NEO4j_USER, NEO4j_PASSWORD

header = {
    "content-type":'application/json'
}



def Aura(user_query):

    data = {   
        "statements" : [{
            "statement": user_query
        }]
    }
    # database authentication
    res = requests.post(url=AURA_URI, data=json.dumps(data), headers=header, auth=HTTPBasicAuth(NEO4j_USER,     AURA_PASSWORD))
    # load json data from response
    all_data = json.loads(res.text)['results']
    # initialize return data
    return_data = {}
    nodes = []
    links = []
    # iterate all data
    for item in all_data:
        if len(item['data']):
            for item1 in item['data']:
                #array mapping
                if len(item1['row']) > 0:
                    if type(item1['row'][0]).__name__ == 'list':
                        for row,meta in zip(item1['row'],item1['meta']):
                            link = {}
                            node = {}
                            #element mapping
                            for (rowItem,metaItem) in zip(row,meta):
                                if metaItem['type'] == 'node':
                                    # property merge
                                    node ={**rowItem,**metaItem}
                                if metaItem['type'] == 'relationship':
                                    rel_property = {**rowItem,**metaItem}
                                nodes.append(node)
                            if len(meta) > 1:
                                link['source'] = meta[0]['id']
                                link['target'] = meta[2]['id']
                                links.append(link)
                            link['property'] = rel_property
                    elif type(item1['row'][0]).__name__ == 'dict':
                        link = {}
                        node = {}
                        rel_property = {}
                        for row, meta in zip(item1['row'], item1['meta']):
                            if meta['type'] == 'node':
                                # property merge
                                node = {**row, **meta}
                            if meta['type'] == 'relationship':
                                rel_property = {**row, **meta}
                            nodes.append(node)
                        if len(item1['meta']) > 1:
                            link['source'] = item1['meta'][0]['id']
                            link['target'] = item1['meta'][2]['id']
                            links.append(link)
                        link['property'] = rel_property
    return_data['nodes'] = nodes
    return_data['links'] = links
    # empty data handling
    if len(nodes) == 0 and len(links) == 0:
        return {'status':'empty_data'}
    else:
        return return_data




def joltAPI(user_query):
    data = {   
        "statements" : [{
            "statement": user_query
        }]
    }
    # database authentication
    res = requests.post(url=JOLT_URL, data=json.dumps(data), headers=header, auth=HTTPBasicAuth(NEO4j_USER, NEO4j_PASSWORD))
    # load json data from response
    all_data = json.loads(res.text)['results']
    # initialize return data
    return_data = {}
    nodes = []
    links = []
    # iterate all data
    for item in all_data:
        if len(item['data']):
            for item1 in item['data']:
                #array mapping
                if len(item1['row']) > 0:
                    if type(item1['row'][0]).__name__ == 'list':
                        for row,meta in zip(item1['row'],item1['meta']):
                            link = {}
                            node = {}
                            #element mapping
                            for (rowItem,metaItem) in zip(row,meta):
                                if metaItem['type'] == 'node':
                                    # property merge
                                    node ={**rowItem,**metaItem}
                                if metaItem['type'] == 'relationship':
                                    rel_property = {**rowItem,**metaItem}
                                nodes.append(node)
                            if len(meta) > 1:
                                link['source'] = meta[0]['id']
                                link['target'] = meta[2]['id']
                                links.append(link)
                            link['property'] = rel_property
                    elif type(item1['row'][0]).__name__ == 'dict':
                        link = {}
                        node = {}
                        rel_property = {}
                        for row, meta in zip(item1['row'], item1['meta']):
                            if meta['type'] == 'node':
                                # property merge
                                node = {**row, **meta}
                            if meta['type'] == 'relationship':
                                rel_property = {**row, **meta}
                            nodes.append(node)
                        if len(item1['meta']) > 1:
                            link['source'] = item1['meta'][0]['id']
                            link['target'] = item1['meta'][2]['id']
                            links.append(link)
                        link['property'] = rel_property
    return_data['nodes'] = nodes
    return_data['links'] = links
    # empty data handling
    if len(nodes) == 0 and len(links) == 0:
        return {'status':'empty_data'}
    else:
        return return_data
