import os
import json
import time
import sys
import re
from neo4j import GraphDatabase


class Example(object):
    print("Starting")
    print(object)
    # start a timer

    """ generated source for class Example """
    @classmethod
    def main(cls, args):
        start_time = time.time()
        """ generated source for method main """
        jsonPath = os.getenv("JSON_FILE")
        print("Path to JSON file is " + jsonPath)
        # get the maximum value of two variables
        nbArticles = int(max(int(os.getenv("MAX_NODES")), 1000))
        print("Number of articles to consider is " + str(nbArticles))
        neo4jIP = os.getenv("NEO4J_IP")
        print("IP addresss of neo4j server is " + neo4jIP)

        pattern = r'NumberInt\((\d+)\)'
        count = 0

        with open('file.json', 'r') as f:
            for line in f:
                if line.startswith('},'):
                    count += 1
                line = re.sub(pattern, r'\1', line)
                # print to a new file
                if count >= nbArticles:
                    print('}]', file=open('test.json', 'a'))
                    break
                print(line, file=open('test.json', 'a'))

        print('File created')

        # load json read test.json file and store it in a variable data
        with open('test.json', 'r') as f:
            json_string = f.read()
            print('file read')

        # Parse the escaped JSON string
        data = json.loads(json_string)

        uri = "bolt://" + neo4jIP + ":7687"
        driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

        i = 0

        while i < nbArticles:
            item = data[i]
            # Create a node for the article
            with driver.session() as session:
                session.run(
                    "MERGE (a:Article {_id: $id, title: $title})", id=item['_id'], title=item.get('title', ''))
            # Create a node for each article that has author and a relationship between the author and the article
            if 'authors' in item:
                for author in item['authors']:
                    # if there is no name, we don't create the node
                    if 'name' in author and '_id' in author:
                        with driver.session() as session:
                            session.run(
                        "MATCH (n:Article {_id: $article_id})"
                        "MERGE (a:Author {_id: $id, name: $name})"
                        "MERGE (a)-[:AUTHORED]->(n)",
                        id=author['_id'],
                        name=author['name'],
                        article_id=item['_id'])
            i += 1
        print(i)
        i = 0
        session.close()

        while i < nbArticles:
            item = data[i]
            if 'references' in item:
                for reference in item['references']:
                    # create a relationship between the article and the reference
                    with driver.session() as session:
                        for item in data:
                            if 'references' in item:
                                query = """
                                    MATCH (a:Article {_id: $id}) FOREACH (citationid in $citationids |MERGE (a)-[:CITES]->(:Article {_id: citationid}))
                                """
                                params = { "id": item['_id'], 'citationids': item['references'] }
                                session.run(query, params)
            i += 1

        elapsedTime = time.time() - start_time

        print('{“number_of_articles”=', nbArticles,
              ', “memoryMB”=”3000”, “seconds”=”', elapsedTime, '”}')

if __name__ == '__main__':
    print(sys.argv)
    Example.main(sys.argv)