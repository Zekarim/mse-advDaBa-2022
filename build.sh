#  #!/usr/bin/sh
#  # Build the docker image and run the docker-compose
docker build . -t neo4jtp
docker-compose up -d --build