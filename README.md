# A-Star-PathFinding
A-Star Path Finding Program

Description:
This program creates a 30 by 30 grid in pygame where the user can place two nodes (orange as start and blue as end)
with barriers in bewteen. The route with the least amount of nodes is found using the A-Star algorithm.

Algorithm:
A-Star path finding is an informed search algorithm which means we cconsider the endpoint location but we do not 
know intially where the barriers / walls are. In the search we will check the nearest neighbors on the 2D plane which
means the nodes adjacent to the start node. Then we use the prioroty score of each node to determine the quickest route 
searching. The equation of this function is f(n) = g(n) + h(n) where f(n) is the priority score of n (node), g(n) is the
current shortest distance and h(n) is the estimate distance from n to the end. For this 2D plane, we assume that each node
has an edge of score 1.

This program was written along with the youtube video linked below
https://www.youtube.com/watch?v=JtiK0DOeI4A

Some changes were made to this program including
 - usage of pygame grid derivered from my "Drawing with Pygame" github 
 - complete comment of algorithm and code
 - reconstructed main function
 - added print statement in terminal to check how many nodes it took to get from end to start