import random
import collections
from collections import Counter
class Technology(object):    
    def __init__(self, label, color):
        self.label=label
        self.color=color
        
    def __str__(self):
        return(str(self.label)+"&"+str(self.color))
    
    

class User(object):
    def __init__(self,user_id):
        self.user_id=user_id
        self.tech=None
        self.tech_list=[]
        self.temp_tech=None
        self.friends_list=[]

    def __lt__(self, other):
        if self.prv < other.prv:
            return True
        else:
            return False
    
    def get_friends(self):
        return self.friends_list

    def is_friend(self, other):
        if other in self.friends_list:
            return True
        else:
            False

    def get_id(self):
        return self.user_id

    def get_tech(self):
        return self.tech

    def __repr__(self):
        return (str(self.user_id)+": "+str(self.tech))



class Graph(object):
    def __init__(self, population):
        self.population=population
        self.users_list=[]
        self.tmp_node_set=set()
        for i in range(self.population):
            self.users_list.append(User(i))

    def circle_connect(self, n):
        i=0
        while i < self.population:
            j=1
            while j<=n:
                self.users_list[i].friends_list.append(self.users_list[(i+j)%self.population])
                self.users_list[(i+j)%self.population].friends_list.append(self.users_list[i])
                j+=1
            i+=1
            
    def random_connections(self, num_connections):
        while num_connections > 0:
            a=random.choice(self.users_list)
            b=random.choice(self.users_list)
            if a==b:
                continue
            elif a.is_friend(b) or b.is_friend(a):
                continue 
            else :
                a.friends_list.append(b)
                b.friends_list.append(a)
                num_connections-=1

    def is_connected(self, seed_user, threshold):
        ## judge whether the undirected graph is connected
        ## threshold is the depth of the recursion
        if threshold < 0:
            return
        else:
            for friend in seed_user.get_friends():
                threshold-=1
                self.tmp_node_set.add(friend)
                self.is_connected(friend,threshold)    
        return (len(self.tmp_node_set)==len(self.get_users()))
#         return (len(self.tmp_node_set), len(self.get_users())

        ## second method: using for loop(ugly)
#         self.tmp_node_set=set()
#         for a in user.get_friends():
#             for b in a.get_friends():
#                 for c in b.get_friends():
#                     for d in c.get_friends():
#                         for e in d.get_friends():
#                             for f in e.get_friends():
#                                 for g in f.get_friends():
#                                     for h in g.get_friends():
#                                         for i in h.get_friends():
#                                             for j in i.get_friends():
#                                                 for k in j.get_friends():
#                                                     for l in k.get_friends():
#                                                         for m in l.get_friends():
#                                                             self.tmp_node_set.add(m)
#         return (len(self.tmp_node_set)), len(self.get_users())
            
        
    def time_step(self):
        for user in self.users_list:
            for friend in user.get_friends():
                user.tech_list.append(friend.get_tech())
            user.temp_tech = self.get_next_tech(user)
        for user in self.users_list:
            user.tech=user.temp_tech
    
    def get_next_tech(self, user):
        friends_tech_list = []
        for friend in user.get_friends():
            friends_tech_list.append(friend.get_tech())
        friends_tech_list.append(user.get_tech())
        friends_tech_list=list(filter((None).__ne__, friends_tech_list))
        c = collections.Counter(friends_tech_list)
        tmp_key_list=[]
        for key in c:
            if c[key] == max(c.values()):
                tmp_key_list.append(key)
        if len(tmp_key_list) == 0:
            result = None
        else:
            result = random.choice(tmp_key_list)
#         print("result"+str(result))
        return result
            
    def get_users(self):
        """returns a list containing the users in the graph, in
        order of their IDs"""
        return self.users_list
    
    def __repr__(self):
        result=""
        for user in self.users_list:
            result = result + str(user.get_id()) + ": "
            for friend in user.get_friends():
                result = result + str(friend.get_id()) + " "
            result += "\n"
        return result


    
class GraphAnalyzer(object):
    def __init__(self, graph, my_tech):
        """Contruct a new analyzer to study a provided graph,
        where my_tech represents the given company's technology"""
        self.graph = graph
        self.my_tech = my_tech
        self.user_list = self.graph.get_users()
        self.first_time_flag = True
        self.plan_list = []
        self.first_adopter_list = []

    def choose_user(self):
        """returns a user that does not currently have
        a technology, to serve as a first-adopter for 
        this analyzer's technology"""
        if self.first_time_flag == True:
            self.pagerank()
            self.plan_list = self.get_untouched(self.user_list)
            best = self.get_best_from_plan()
            self.first_adopter_list.append(best)
            best.tech = self.my_tech
            self.first_time_flag = False
            return best
        else:
            self.plan_list = self.get_connected()
            self.plan_list = self.get_untouched(self.plan_list)
            best = self.get_best_from_plan()
            self.first_adopter_list.append(best)
            return best

    def pagerank(self, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
         
        graph_size = 500

        # value for nodes without inbound links
        min_value = (1.0-damping_factor)/graph_size 
         
        # itialize the page rank for all nodes
        for user in self.user_list:
            user.prv = 1.0
             
        for i in range(max_iterations):
            diff = 0 #total difference compared to last iteraction
            # computes each node PageRank based on inbound links
            for user in self.user_list:
                tmp_prv = min_value
                for friend in user.get_friends():
                    tmp_prv += damping_factor * friend.prv / len(friend.get_friends())
                diff += abs(user.prv - tmp_prv)
                user.prv = tmp_prv
     
            #stop if PageRank has converged
            if diff < min_delta:
                break
        
        # print out each user's page rank value 
#         for user in self.user_list:
#             print(str(user.get_id())+"\t"+str(user.prv))

    def get_untouched(self, user_list):
        untouched_list=[]
        for user in user_list:
            if user.get_tech() == None:
                # insert some filter function in this line
                untouched_list.append(user)
        if len(untouched_list) == 0:
            print("there is no untouched user now...")
            untouched_list.append(self.get_best_from_plan())
        return untouched_list

    def get_best_from_plan(self):
        best = self.plan_list[0]
        for i in range(len(self.plan_list)):
            if self.plan_list[i].prv > best.prv:
                best = self.plan_list[i]
        return best

    def get_connected(self):
        plan_list=self.first_adopter_list[0].get_friends()
        for user in self.first_adopter_list:
            plan_list = list(set(plan_list) & set(user.get_friends()))
        if len(plan_list) == 0:
            print("there is no connected user now...")
            plan_list = list(set(plan_list) | set(user.get_friends()))
        return plan_list
    
    
    
    

##TEST CODE
gp=Graph(500)
gp.circle_connect(3)
gp.random_connections(50)
my_tech = Technology("krist","green")
team_list=[]
for i in range(12):
    team = Technology(i, i)
    team_list.append(team)
team_list.append(my_tech)
random.shuffle(team_list)
my_pos = team_list.index(my_tech)
print("my pos is: "+str(my_pos))
for i in range(3):
    for team in team_list[:my_pos]:
        random.choice(GraphAnalyzer(gp, team).get_untouched(gp.users_list)).tech = team
    ga = GraphAnalyzer(gp, my_tech)
    ga.choose_user().tech = my_tech
    for team in team_list[my_pos+1:]:
        random.choice(GraphAnalyzer(gp, team).get_untouched(gp.users_list)).tech = team
print("The first adopter result: ")
for user in gp.users_list:
    if user.tech is not None:
        print(str(user.get_id())+": "+str(user.get_tech().label))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
for i in range(100):
    gp.time_step()
result=[]
for user in gp.users_list:
    result.append(str(user.get_tech().label))
print("final result: ")
print(Counter(result).most_common(13))
