# TP2 AdvDB, Brede Swann, Zerika Karim
##  Approach for loading the graph

To load the graph in the Neo4j container, an app container is created to process everything.

In this container, the volume is created with the "dblpv13.json" datas.

In "Dockerfile", it is declared that python is used, a library "Neo4j" is added and the file "tp2.py" is copied to the container.

Reading the whole file containing the datas is not possible since it is too big. Then, the file is processed line by line and here is the logic :
    - Count each line that starts with '},' to know how many items are processed
    - Use a RegEx 'NumberInt\((\d+)\)' to correct the syntax of the json file
    - If the count of the number of item is equal to the number of articles defined in the docker-compose file, break the loop and 

The printed file in json respect the syntax and can now be read by the library "json" of python

Create the driver with the Neo4j library with the right authentification and url

In a while loop, push one item at a time creating the Article node, Author node and their relationship AUTHORED.

When everything is created, another while loop tries to create the CITES relationship between articles. I didn't get why it didn't work. I tried in the first loop, and by doing a second one.

If I do it directly on the neo4j browser, it works. Would you have an idea of why it is not working for me ?

## Parameter values

    - JSON_FILE=/file.json
    - MAX_NODES=10000
    - Memory = 4 gb

## Result of a performance test.

{“number_of_articles”= 10000 , “memoryMB”=”4000”, “seconds”=” 247.80165815353394 ”}
