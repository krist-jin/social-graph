import random
import collections
class Technology(object):    
    def __init__(self, label, color):
        """Each technology should be constructed with
        a text label and a color for display purposes"""
        self.label=label
        self.color=color



class User(object):
    def __init__(self,user_id):
        self.user_id=user_id
        self.tech=None
        self.tech_list=[]
        self.temp_tech=None
        self.friends_list=[]

    def __lt__(self, other):
        """this is a built in comparison function, so that
        user1 < user2 always returns False.  You may not need
        this method at all, but it can sometimes be handy
        for sorting lists that contain users without throwing
        errors"""
        return False
    
    def get_friends(self):
        """returns a list of the user's friends,
        which are also users"""
        return self.friends_list
    

    def is_friend(self, other):
        """returns True if this User and other are friends.
            returns False otherwise"""
        if other.user_id in self.friends_list:
            return True
        else:
            False
    

    def get_id(self):
        """Returns this User's id"""
        return self.user_id
    

    def get_tech(self):
        """Returns the Technology used by the User, or None if
        the User has no Technlology"""
        return self.tech

    def __repr__(self):
        return (str(self.user_id)+str(self.tech)+str(self.friends_list))


class Graph(object):

    def __init__(self, population):
        """create a new graph with population users and no connections.
        no users in the new graph should have any technology"""
        self.population=population
        self.users_list=[]
        for i in range(self.population):
            self.users_list.append(User(i))
    


    def circle_connect(self, n):
        """connect each user i to the next n users, that is
        users (i+1)%population, (i+2)%population,...,
        (i+n)%population."""
        i=0
        while  i < self.population:
##            if i < n:
##                z=0
##                while z+i<n:
##                    self.users_list[i].friends_list.append(self.users_list[self.population-n+i+z].user_id)
##                    z+=1
            j=1
            while j<=n:
                self.users_list[i%self.population].friends_list.append(self.users_list[(i%self.population+j)%self.population].user_id)
                self.users_list[(i%self.population+j)%self.population].friends_list.append(self.users_list[i%self.population].user_id)
                j+=1
##            print(self.users_list[i%self.population].friends_list)               #### USED FOR TEST
            i+=1
       

                
        
            
    def random_connections(self, num_connections):
        """add num_connections new connections randomly to the graph"""
        while num_connections > 0:
            a=random.choice(self.users_list)
            b=random.choice(self.users_list)
            if a==b:
                continue
            else :
                a.friends_list.append(b.user_id)
                b.friends_list.append(a.user_id)
                num_connections-=1


    def is_connected(self):
        """returns True if there is a path from every graph User to
        every other user"""
        ## judge whether the undirected graph is connected
        connected_user=set()
        for i in range(self.population):
            for j in range(len(self.users_list[i].friends_list)):
                connected_user.add(self.users_list[i].friends_list[j])
        if len(connected_user)==self.population:
            return True
        else:
            return False
        
    

    def time_step(self):
        """move the simulation forward by one time period.
        Each user adopts the most popular technology among
        themselves and their friends.  If there are multiple
        technologies that are tied for most popular, the user
        selects one at random."""
        # To find the most common tech in a subset of users,
        # you cannot build a frequency table using a
        # dictionary since Technologies are mutable objects.
        # If you want to follow a similar strategy, you can
        # import the collections package and use a Counter
        # object, which works like a (slow) dictionary for
        # mutable objects.  However, there are many other
        # strategies that you could use to do the same thing.
        
####        while any(self.users_list[i].label == None for i in range(self.population)):
        for i in range(self.population):
            for j in range(len(self.users_list[i].get_friends())):
                self.users_list[i].tech_list.append(self.users_list[self.users_list[i].get_friends()[j]].get_tech())
####                for n,s in enumerate(self.users_list[i].tech_list):
####                    if s==None:
####                        self.users_list[i].tech_list[n]=0       
####            print(self.users_list[i].tech_list)
            if all(x == None for x in self.users_list[i].tech_list):
                self.users_list[i].temp_tech=self.users_list[i].tech
####                print(self.users_list[0].temp_tech)
####            elif((self.users_list[i].tech_list).count(k for k in self.users_list[i].tech_list)==1):
####                self.users_list[i].temp_tech=self.users_list[i].tech
            else:
                self.users_list[i].tech_list=list(filter((None).__ne__, self.users_list[i].tech_list))
                counter=collections.Counter(self.users_list[i].tech_list)
                if (counter.most_common(1)[0][1]==1 and self.users_list[i].tech !=None):
                    self.users_list[i].temp_tech=self.users_list[i].tech
                else:
####                    print((self.users_list[i].tech_list).count(k))
                    self.users_list[i].temp_tech=counter.most_common(1)[0][0]
####                    self.users_list[i].temp_tech=max(k for k in self.users_list[i].tech_list if (self.users_list[i].tech_list).count(k)>1)           
        for i in range(self.population):
            self.users_list[i].tech=self.users_list[i].temp_tech
            
            ##USED FOR TEST(OUTPUT)
##        for i in range(self.population):
##            print(i,self.users_list[i].tech)
            
        
        
    def get_users(self):
        """returns a list containing the users in the graph, in
        order of their IDs"""
        return self.users_list
    
    def __repr__(self):
        return str(self.users_list)



    
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
        self.counter = 0

    def choose_user(self):
        """returns a user that does not currently have
        a technology, to serve as a first-adopter for 
        this analyzer's technology"""
        if self.first_time_flag == True:
            self.pagerank()
            self.plan_list = self.get_untouched(self.user_list)
            self.first_adopter_list.append(self.get_best_from_plan())
            self.first_time_flag = False
            return self.first_adopter_list[self.counter]
        else:
            self.counter+=1
            self.plan_list = self.get_connected()
            self.plan_list = self.get_untouched(self.plan_list)
            self.first_adopter_list.append(self.get_best_from_plan())
            return self.first_adopter_list[self.counter]

    def pagerank(self, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
        """
        Compute and return the PageRank in an directed graph.    
         
        @type  graph: digraph
        @param graph: Digraph.
         
        @type  damping_factor: number
        @param damping_factor: PageRank dumping factor.
         
        @type  max_iterations: number 
        @param max_iterations: Maximum number of iterations.
         
        @type  min_delta: number
        @param min_delta: Smallest variation required for a new iteration.
         
        @rtype:  Dict
        @return: Dict containing all the nodes PageRank.
        """
         
        graph_size = 500

        # value for nodes without inbound links
        min_value = (1.0-damping_factor)/graph_size 
         
        # itialize the page rank dict with 1/N for all nodes
        #pagerank = dict.fromkeys(nodes, 1.0/graph_size)
##        pagerank = dict.fromkeys(nodes, 1.0)
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
             
            print ('This is NO.%s iteration') % (i+1)
##            print (pagerank)
            print ('')
     
            #stop if PageRank has converged
            if diff < min_delta:
                break
         
        for user in self.user_list:
            print(user.get_id()+"\t"+user.prv)

            
     
    def get_untouched(self, user_list):
        untouched_list=[]
        for user in user_list:
            if user.get_tech() == None:
                # insert some filter function in this line
                untouched_list.append(user)
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
        return plan_list




##TEST CODE
gp=Graph(40)
gp.circle_connect(2)
gp.random_connections(4)
gp.users_list[0].tech="fuji"
gp.users_list[3].tech="canon"
gp.users_list[7].tech="nikon"
