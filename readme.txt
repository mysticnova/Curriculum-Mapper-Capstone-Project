This is a temporary fix until a more elegant solution can be found that rids the need for neo4j browser functioning as a middle man. 

Instructions: 

2)


First of all install neo4j browser (not neo4j desktop). 

The installation instructions to do so can be found here:

Mac - https://neo4j.com/docs/operations-manual/current/installation/osx/

Windows - https://neo4j.com/docs/operations-manual/current/installation/windows/

3) Launch the flask app:

flask run

It will say that neo4j failed to connect. Ignore that notification in the terminal and proceed to the next step.


3) Launch your neo4j browser instance

- <NEO4J_HOME>/bin/neo4j start

4) Visit http://localhost:7474 and enter the following credentials

NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=5LzX5uDDm6ZlI-Y2s02QzV3HqcDVu1dNUE0KJ0Hh36A

5) Open the flask server browser and navigate to http://127.0.0.1:5000/textbox.html
You should now have the functionality of AuraDB integrated in your work flow. 








