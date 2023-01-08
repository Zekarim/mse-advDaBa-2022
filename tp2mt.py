import os
import json
import time
import sys
import re
import threading
from neo4j import GraphDatabase


class Example(object):
    print("Starting")
    print(object)
    # start a timer
    start_time = time.time()

    def process_data(self, data):
        
        nbArticles = int(max(int(os.getenv("MAX_NODES")), 1000))
        neo4jIP = os.getenv("NEO4J_IP")
        uri = "bolt://" + neo4jIP + ":7687"
        driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

        i = 0

        while i < len(data):
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

        session.close()

        i = 0

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

        session.close()

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

        # Split the data into two equal parts
        quart = len(data) // 8

        # Create two threads to process the data in parallel
        ex = Example()
        thread1 = threading.Thread(target=ex.process_data, args=(data[:quart],))
        thread2 = threading.Thread(target=ex.process_data, args=(data[quart:quart*2],))
        thread3 = threading.Thread(target=ex.process_data, args=(data[quart*2:quart*3],))
        thread4 = threading.Thread(target=ex.process_data, args=(data[quart*3:quart*4],))
        thread5 = threading.Thread(target=ex.process_data, args=(data[quart*4:quart*5],))
        thread6 = threading.Thread(target=ex.process_data, args=(data[quart*5:quart*6],))
        thread7 = threading.Thread(target=ex.process_data, args=(data[quart*6:quart*7],))
        thread8 = threading.Thread(target=ex.process_data, args=(data[quart*7:],))

        

        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()
        thread8.start()

        # Wait for the threads to complete
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        thread8.join()
        
        elapsedTime = time.time() - start_time

        print('{“number_of_articles”=', nbArticles,
              ', “memoryMB”=”3000”, “seconds”=”', elapsedTime, '”}')
        

if __name__ == '__main__':
    print(sys.argv)
    Example.main(sys.argv)