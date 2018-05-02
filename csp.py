
class csp:
    def __init__(self, variables, domain, pots,confederation):
        self.variables=variables
        self.domains=domain
        self.neighbors=pots
        self.confederation=confederation
        self.curr_domains=None
        self.nassigns=0

    def mrv(self, assignment, csp):

        min= self.select_unassigned_variable( assignment, csp)
        for v in self.variables:
            if v not in assignment:
                if self.curr_domains:
                    r= len(self.curr_domains[v])
                    n= len(self.curr_domains[min])
                else:
                    count=0
                    for val in self.domains[v]:
                        if self.nconflicts(v, val, assignment) == 0:
                            count=count+1
                    n=count
                    count = 0
                    for val in self.domains[min]:
                        if self.nconflicts(min, val, assignment) == 0:
                            count = count + 1
                    r = count
                if r < n:
                    min = v
        return min


    def constraints(self,A, a,assignment):
        count=0
        l = list()
        for k, v in assignment.items():
            if a == v:
                l.append(k)

        for item in l:
          if ([k for k, v in self.confederation.iteritems() if str(item) in v][0] == ("UEFA")):
              count=count+1

        for item in l:

          if ([k for k, v in self.confederation.iteritems() if str(item) in v][0] == "UEFA"):
             if ([k for k, v in self.confederation.iteritems() if str(A) in v] == [k for k, v in self.confederation.iteritems() if str(item) in v]  and count>=2 ) :
                return True
          elif  ([k for k, v in self.confederation.iteritems() if str(item) in v][0] != "UEFA"):
             if ([k for k, v in self.confederation.iteritems() if str(A) in v] == [k for k, v in self.confederation.iteritems() if str(item) in v]):

              return  True


        for neigh in self.neighbors[A]:
            b = assignment.get(neigh, None)

            if(b != None and not (A == neigh or (a != b))):
                return True
        return False

    def nconflicts(self, var, val, assignment):

       if self.constraints(var, val,assignment):
            return 1
       return 0

    def assign(self, var, val, assignment):
        assignment[var] = val


    def select_unassigned_variable(self,assignment, csp):
        for v in self.variables:
            if v not in assignment:
                return v

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]


    def recursive_backtracking(self,assignment, csp):
        if len(assignment) == len(self.variables):
            return assignment
        var = self.mrv(assignment, csp)

        for value in self.lcv(var, assignment, csp):

            if 0 == self.nconflicts(var, value, assignment):
                self.assign(var, value, assignment)
                removals = self.start(var, value)
                if self.arc( var, value, assignment, removals):
                    result = self.recursive_backtracking(assignment,csp)
                    if result is not None:
                        return result
                self.undo_val(removals)
        self.unassign(var, assignment)
        return None


    def lcv(self,var, assignment, csp):

        return sorted(self.left_domain(var),
                      key=lambda val: self.numconflicts(var, val, assignment))

    def numconflicts(self, A, a, assignment):
        count = 0
        conflict = 0
        l = list()
        for k, v in assignment.items():
            if a == v:
                l.append(k)


        for item in l:
            if ([k for k, v in self.confederation.iteritems() if str(item) in v][0] == ("UEFA")):
                count = count + 1

        for item in l:

            if ([k for k, v in self.confederation.iteritems() if str(item) in v][0] == "UEFA"):
                if ([k for k, v in self.confederation.iteritems() if str(A) in v] == [k for k, v in
                                                                                      self.confederation.iteritems() if
                                                                                      str(item) in v] and count >= 2):

                    conflict = conflict + 1

            elif ([k for k, v in self.confederation.iteritems() if str(item) in v][0] != "UEFA"):
                if ([k for k, v in self.confederation.iteritems() if str(A) in v] == [k for k, v in
                                                                                      self.confederation.iteritems() if
                                                                                      str(item) in v]):

                    conflict = conflict + 1
        return conflict

    def arc(self, var, value, assignment, removals):
        return self.AC3( [(X, var) for X in self.neighbors[var]], removals)

    def AC3(self, queue=None, removals=None):
        if queue is None:
            queue = [(a, b) for a in self.variables for b in self.neighbors[a]]
        self.support_pruning()
        while queue:
            (Xi, Xj) = queue.pop()
            if self.changed( Xi, Xj, removals):

                if not self.curr_domains[Xi]:
                    return False
                for Xk in self.neighbors[Xi]:
                    if Xk != Xi:
                        queue.append((Xk, Xi))

        return True

    def changed(self, Xi, Xj, removals):
        revised = False
        for x in self.curr_domains[Xi][:]:
            all_good = True
            for y in self.curr_domains[Xj]:
                if self.diff_constraints(Xi, x, Xj, y):
                    all_good = False
                    break
            if all_good== True:
                 self.prune(Xi, x, removals)
                 revised = True
        return revised

    def backtracking_search(self,csp):
        return self.recursive_backtracking({}, csp)

    def diff_constraints(self,Xi, x, Xj, y):
       return x!=y

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = dict((v, list(self.domains[v]))
                                     for v in self.variables)

    def start(self, var, value):
        self.support_pruning()
        removals = [(var, d) for d in self.curr_domains[var] if d != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None: removals.append((var, value))

    def left_domain(self, var):
        return (self.curr_domains or self.domains)[var]

    def undo_val(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)


def get_details():
    f = open("input.txt", "r")
    input_given = []
    for line in f:
        input_given.append(line)
    input_given = map(lambda s: s.strip(), input_given)
    num_groups= input_given[0]
    num_pots= input_given[1]
    pot=[]
    for i in range(2 , 2+int(num_pots)):

        if input_given[i] != 'None':
            pot.append(input_given[i].split(","))

    dict = {}
    for i in range(2+int(num_pots), 2+int(num_pots)+ 6):
        x= input_given[i].split(":")
        dict[x[0]]= x[1].split(",")

    domain= {}
    variables = []
    list_d=  list(range(1,int(num_groups)+1))
    for i in pot:
        for c in i:
            variables.append(c)
            domain[c]= list_d
    neighbor={}
    for i in pot:
        for val in i:
            neighbor[val]= list(i)

    for k,v in dict.iteritems():

        if str(k)!= "UEFA":
            if (v[0])!= "None":
              for item in v:
                neighbor[str(item)].extend(v)



    for k, v in neighbor.iteritems():
        neighbor[k] = list(set(v))


    for k, v in neighbor.iteritems():
        if str(k) in v:
            v.remove(k)


    #check for pot count is less than group count
    flag= False
    for value in dict:
        value_list = dict[value]
        count = len(value_list)

        if value=="UEFA":
            if count> int(num_groups)*2:
              flag=True

        elif value!= "UEFA":
            if count > int (num_groups):
                flag= True


    for value in pot:
        count_pot=len(value)
        if count_pot > int(num_groups):
            flag = True


    if flag==True:
        f = open('output.txt', 'w')
        f.write("No")


    elif (flag==False):
      csp_obj= csp(variables,domain,neighbor,dict)
      assignment = csp_obj.backtracking_search(csp)

      if(assignment is not None):


            dd = {}

            for key, value in assignment.items():
                try:
                    dd[value].append(key)
                except KeyError:
                    dd[value] = [key]


            for groups in range(1,int(num_groups)+1):
                if groups not in dd:
                    dd[groups]= "None"


      f = open('output.txt', 'w')
      if assignment is not None:
            f.write("Yes")
            for i in range(1,int(num_groups)+1):
                    f.write("\n")
                    if ((dd[i])=="None"):
                        f.write(dd[i])
                    else:
                        f.write( ",".join(dd[i]))

      else:
            f.write("No")


get_details()
