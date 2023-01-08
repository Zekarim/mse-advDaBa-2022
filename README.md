# TP2 AdvDB, Brede Swann, Zerika Karim
##  Approach for loading the graph

To load the graph in the Neo4j container, an app container is created to process everything.

In this container, the volume is created with the "dblpv13.json" datas.

In "Dockerfile", it is declared that python is used, a library "Neo4j" is added and the file "tp2.py" is copied to the container.

We have done two differents python file. One with a multi-threads method and one without multi-thread in order to compare the performance.

Initially, the "build.sh" will run the code without the multi-thread. If you want to run the code with the multi-thread, in "DockerFile" change the name "tp2.py" by "tp2mt.py".

The Username and the password are: neo4j/test. They are also written in "docker-compose.yaml".

Reading the whole file containing the datas is not possible since it is too big. Then, the file is processed line by line and here is the logic :
    - Count each line that starts with '},' to know how many items are processed.
    - Use a RegEx 'NumberInt\((\d+)\)' to correct the syntax of the json file.
    - If the count of the number of item is equal to the number of articles defined in the docker-compose file, break the loop.

The printed file in json respect the syntax and can now be read by the library "json" of python.

Create the driver with the Neo4j library with the right authentification and url.

In a while loop, push one item at a time creating the Article node, Author node and their relationship AUTHORED.

When everything is created, another while loop create the CITES relationship between articles.


## Parameter values

    - JSON_FILE=/file.json
    - MAX_NODES=10000
    - Memory = 4 gb

## Result of a performance test.

Without multi-thread:
{“number_of_articles”= 10000 , “memoryMB”=”3000”, “seconds”=” 753.1971309185028 ”}

With multi-thread:
{“number_of_articles”= 10000 , “memoryMB”=”3000”, “seconds”=” 252.9682822227478 ”}

