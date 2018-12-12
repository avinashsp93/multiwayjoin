from flask import Flask, render_template
from tkinter import *
import pandas as pd
from dbconnect import connect_tpch
from queryAPI import get_query
import numpy as np
import time

class Application(Frame):
    def __init__(self):
        root = Tk()
        # variables to measure time throughout the program
        self.start_time = ""
        self.elapsed_time = ""
        self.response_time = ""
        super().__init__(root)
        self.pack()
        self.counter = 0
        self.create_widgets(root)
        self.alignment = {}
        self.relations_map = {
            'r1': 'region',
            'r2': 'nation',
            'r3': 'part',
            'r4': 'supplier',
            'r5': 'customer',
            'r6': 'orders',
            'r7': 'partsupp',
            'r8': 'lineitem'
        }
        self.query_array = []
        self.query_dict = {
            1: "SELECT * FROM ALIGNED_REGION",
            2: "SELECT * FROM ALIGNED_REGION_NATION",
            4: "SELECT * FROM ALIGNED_NATION_SUPPLIER",
            5: "SELECT * FROM ALIGNED_NATION_CUSTOMER",
            6: "SELECT * FROM ALIGNED_CUSTOMER_ORDERS",
            7: "SELECT * FROM ALIGNED_SUPPLIER_PARTSUPP",
            8: "SELECT * FROM ALIGNED_ORDERS_LINEITEM"
        }
        self.matrix = []
        self.master_array = []
        self.results = []
        self.lineitemcolumn = 4
        self.return_results = []
        self.depth = 0
        self.logfile = open('.\logfile.txt', 'w')


    def create_widgets(self, root):       

        self.quit = Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(padx=5, pady=5)

        self.graph = Button(self)
        self.graph["text"] = "GENERATE RESULT!"
        self.graph["command"] = self.generate_result
        self.graph.pack(padx=5, pady=5)

        self.r1r2 = Button(self)
        self.r1r2["text"] = "Region -> Nation"
        self.r1r2["command"] = self.region_nation
        self.r1r2.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r2r4 = Button(self)
        self.r2r4["text"] = "Nation -> Supplier"
        self.r2r4["command"] = self.nation_supplier
        self.r2r4.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r2r5 = Button(self)
        self.r2r5["text"] = "Nation -> Customer"
        self.r2r5["command"] = self.nation_customer
        self.r2r5.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r3r7 = Button(self)
        self.r3r7["text"] = "Part -> Partsupp"
        self.r3r7["command"] = self.part_partsupp
        self.r3r7.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r3r8 = Button(self)
        self.r3r8["text"] = "Part -> Lineitem"
        self.r3r8["command"] = self.part_lineitem
        self.r3r8.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r4r7 = Button(self)
        self.r4r7["text"] = "Supplier -> Partsupp"
        self.r4r7["command"] = self.supplier_partsupp
        self.r4r7.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r4r8 = Button(self)
        self.r4r8["text"] = "Supplier -> Lineitem"
        self.r4r8["command"] = self.supplier_lineitem
        self.r4r8.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r5r6 = Button(self)
        self.r5r6["text"] = "Customer -> Orders"
        self.r5r6["command"] = self.customer_orders
        self.r5r6.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
        self.r6r8 = Button(self)
        self.r6r8["text"] = "Orders -> Lineitem"
        self.r6r8["command"] = self.orders_lineitem
        self.r6r8.pack(padx=5, pady=5, side=LEFT, anchor="n")
        
    def region_nation(self):
        self.align('r1','r2')
        self.r1r2.config(state=DISABLED)
        self.r1r2.config(bg="cyan")
        self.create_matrix(1,2,25)

    def nation_supplier(self):  
        self.align('r2', 'r4')
        self.r2r4.config(state=DISABLED)
        self.r2r4.config(bg="cyan")
        self.create_matrix(2,4,10000)

    def nation_customer(self):
        self.align('r2', 'r5')
        self.r2r5.config(state=DISABLED)
        self.r2r5.config(bg="cyan")
        self.create_matrix(2,5,150000)

    def part_partsupp(self):
        self.align('r3', 'r7')
        self.r3r7.config(state=DISABLED)
        self.r3r7.config(bg="cyan")
        self.create_matrix(3,7,800000)

    def part_lineitem(self):
        self.align('r3', 'r8')
        self.lineitemcolumn = 5
        self.r3r8.config(state=DISABLED)
        self.r3r8.config(bg="cyan")
        self.create_matrix(3,8,6000000)

    def supplier_partsupp(self):
        self.align('r4', 'r7')
        self.r4r7.config(state=DISABLED)
        self.r4r7.config(bg="cyan")
        self.create_matrix(4,7,800000)

    def supplier_lineitem(self):
        self.align('r4','r8')
        self.lineitemcolumn = 5
        self.r4r8.config(state=DISABLED)
        self.r4r8.config(bg="cyan")
        self.create_matrix(4,8,6000000)

    def customer_orders(self):
        self.align('r5', 'r6')
        self.r5r6.config(state=DISABLED)
        self.r5r6.config(bg="cyan")
        self.create_matrix(5,6,1500000)

    def orders_lineitem(self):
        self.align('r6','r8')
        self.lineitemcolumn = 5
        self.r6r8.config(state=DISABLED)
        self.r6r8.config(bg="cyan")
        self.create_matrix(6,8,6000000)

    def create_matrix(self, a, b, c):
        # Creates an array of array, where in the inside array contains 
        # details of all the nodes selected by user and the total 
        # number of rows the aligned table has 
        self.matrix.append([a,b,c])

    def store_linear_results(self): 
        self.return_results = []
        if(len(self.results) == 5):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[1] > tuple3[0]):
                            continue
                        elif(tuple2[1] < tuple3[0]):
                            break
                        for tuple4 in self.results[3]:
                            if(tuple3[1] > tuple4[0]):
                                continue
                            elif(tuple3[1] < tuple4[0]):
                                break
                            for tuple5 in self.results[4]:
                                if(tuple4[1] > tuple5[0]):
                                    continue
                                elif(tuple4[1] < tuple5[0]):
                                    break
                                elif(tuple1[1] == tuple2[0] and tuple2[1] == tuple3[0] and tuple3[1] == tuple4[0] and tuple4[1] == tuple5[0]):
                                    # print(tuple1, tuple2, tuple3, tuple4, tuple5)
                                    self.return_results.append([tuple1, tuple2, tuple3, tuple4, tuple5])
        elif(len(self.results) == 4):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[1] > tuple3[0]):
                            continue
                        elif(tuple2[1] < tuple3[0]):
                            break
                        for tuple4 in self.results[3]:
                            if(tuple3[1] > tuple4[0]):
                                continue
                            elif(tuple3[1] < tuple4[0]):
                                break    
                            elif(tuple1[1] == tuple2[0] and tuple2[1] == tuple3[0] and tuple3[1] == tuple4[0]):
                                # print(tuple1, tuple2, tuple3, tuple4)
                                self.return_results.append([tuple1, tuple2, tuple3, tuple4])
        elif(len(self.results) == 3):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[1] > tuple3[0]):
                            continue
                        elif(tuple2[1] < tuple3[0]):
                            break
                        elif(tuple1[1] == tuple2[0] and tuple2[1] == tuple3[0]):
                            # print(tuple1, tuple2, tuple3)
                            self.return_results.append([tuple1, tuple2, tuple3])
        elif(len(self.results) == 2):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    else:
                        # print(tuple1, tuple2)
                        self.return_results.append([tuple1, tuple2])
        else:
            print("Couldn't see any data")

    def create_nodes(self):
        # Node Dictionary, stores all the information about nodes, and its children
        node_dict = {}
        divert_flag = 0
        for i in self.matrix:
            if(i[0] not in node_dict.keys()):
                node_dict[i[0]] = [i[1]]
            else:
                node_dict[i[0]].append(i[1])
        # Deciding the starting point of the node, set the start element to the lowest key in the dictionary
        start = sorted(list(node_dict.keys()))[0]

        # Recursive function, to produce node array using the dictionary we have
        def dict_recur(node):
            temp_array = []
            # Iterate through all the keys of the dictionary, it's values are children, if a node has more
            # than one child, Put them in another array and append the array, end all the arrays with None
            while(node in list(node_dict.keys())):
                temp_array.append(node)
                if(len(node_dict.get(node)) == 1): # Graph goes linear so far
                    node = node_dict.get(node)[0]
                elif(len(node_dict.get(node)) > 1): # Graph diverts here
                    for i in node_dict.get(node):
                        temp_array.append(dict_recur(i))
                    node = None
            temp_array.append(node)
            temp_array.append(None)
            return temp_array
            
        node_array = dict_recur(start)
        # print(node_array)

        arr = []
        for n in node_array:
            # Checking if the array has another array, which means checking for diversions
            if(isinstance(n, list) == True):
                divert_flag = 1
                temp = arr[:] # Making temp empty by assigning blank array by doing Copy by value, temp = arr copies array by reference
                for j in n: # Iterate through the nested array
                    if(isinstance(j, type([]))):
                        temp2 = temp[:] # If the nested array has another nesting in it
                        for k in j:
                            if(k != None):
                                temp2.append(k)
                            else:
                                self.master_array.append(temp2) # Array of arrays that are trees till end node
                                temp2 = []
                    elif(j != None):
                        temp.append(j)
                    else:
                        self.master_array.append(temp) # This means that you've hit the child node, store the whole path as an array in the master array
                        temp = [] # Empty temp to store a new tree path
            elif(isinstance(n, int) == True):
                arr.append(n)

        # Removing empty array from master array
        if([] in self.master_array):
            self.master_array.remove([])

        # Removing unwanted trees
        temp_array = []
        for i in self.master_array:
            le = i[len(i)-1]
            if(le not in node_dict.keys()):
                temp_array.append(i)
        
        self.master_array = temp_array[:]
        
        if(not divert_flag):
            # Linear Graph
            self.master_array = node_array[:-1] # Copy the tree sequence to the master array
            self.depth = len(self.master_array)
            self.results = [[] for i in range(0, self.depth)] # Having array of arrays to store results of first depth pass


            # Get the first aligned table always
            query = self.query_dict[self.master_array[0]]
            self.results[0] = connect_tpch(query, TRUE)
            range_array = [1, 1]

            for i in self.results[0]:
                self.depth = len(self.master_array)
                index = 0
                range_array[0] = range_array[1] = i[1]
                while(self.depth != 0):
                    query = self.query_dict[self.master_array[index]]
                    if(index):
                        sid_string = "R"+str(self.master_array[index-1])+"_SID"
                        query += " WHERE "+sid_string+" >= "+str(range_array[0])+ " AND "+sid_string+ " <= "+str(range_array[1])+" ORDER BY R"+str(self.master_array[index])+"_SID"
                        self.results[index] = connect_tpch(query, TRUE)
                        # print(query)
                        range_array[0] = self.results[index][0][1]
                        range_array[1] = self.results[index][len(self.results[index])-1][1]
                    index+=1
                    self.depth-=1
                if(self.results[0].index(i) == 0):
                    self.response_time = time.time() - self.start_time
                self.log_linear_results()
            self.process_time = time.time() - self.start_time
            print("Process time : ", "{:.4f}".format(self.process_time))
            print("Response time: ", "{:.4f}".format(self.response_time))
            print("Number of rows", self.counter)
            # print(len(self.results[0]), len(self.results[1]), len(self.results[2]))
            
        else:
            # Diverted Graph
            self.query_array = []
            # Diverted Graph with 2 branches
            if(len(self.master_array) == 2):
                # Finding treeweight of tree 1
                tree1 = self.master_array[0]
                treeweights = []
                elem = self.master_array[0][len(self.master_array[0])-1]
                ind = 0
                for j in self.matrix:
                    if(j[1] == elem):
                        ind = self.matrix.index(j)
                        break
                treeweights.append(self.matrix[ind][2])
        
                # Finding treeweight of tree 2
                tree2 = self.master_array[1]
                elem = self.master_array[1][len(self.master_array[1])-1]
                ind = 0
                for j in self.matrix:
                    if(j[1] == elem):
                        ind = self.matrix.index(j)
                        break
                treeweights.append(self.matrix[ind][2])

                # Swap short and long if treeweight1 is greater than treeweight 2, to carry out the same logic
                if(treeweights[0] > treeweights[1]):
                    temp = self.master_array[0]
                    self.master_array[0] = self.master_array[1]
                    self.master_array[1] = temp

                self.query_array = []
                main_result = []

                print(self.query_array, treeweights)

                # Traverse linearly on the shorter branch
                for i in range(0, len(self.master_array[0])):
                    # Make results big enough to store the results of the subtree
                    self.results = [[] for j in range(0, len(self.master_array[0]))]
                    if((self.master_array[0][i]) in self.query_dict.keys()):
                        self.query_array.append(self.query_dict[self.master_array[0][i]])




                query = self.query_array[0]
                self.results[0] = connect_tpch(query, TRUE)
                
                range_array = [1, 1]

                for i in self.results[0]:
                    self.depth = len(self.master_array[0])
                    index = 0
                    range_array[0] = range_array[1] = i[1]
                    while(self.depth != 0):
                        query = self.query_dict[self.master_array[0][index]]
                        if(index):
                            sid_string = "R"+str(self.master_array[0][index-1])+"_SID"
                            query += " WHERE "+sid_string+" >= "+str(range_array[0])+ " AND "+sid_string+ " <= "+str(range_array[1])+" ORDER BY R"+str(self.master_array[0][index])+"_SID"
                            self.results[index] = connect_tpch(query, TRUE)
                            print(query)
                            range_array[0] = self.results[index][0][1]
                            range_array[1] = self.results[index][len(self.results[index])-1][1]
                        index+=1
                        self.depth-=1
                    self.store_linear_results()


                main_result = self.return_results[:]
                
                print(len(main_result))

                # Identify the intersection point for the branch and traverse linearly from that intersection point
                # in another branch
                sub_branch = []
                sub_result = []
                for j in self.master_array[1][::-1]:
                    if(j not in self.master_array[0]):
                        sub_branch.append(j)
                    else:
                        sub_branch.append(j)
                        break
                sub_branch = sub_branch[::-1]
                
                self.query_array = []
                for i in range(0, len(sub_branch)):
                    # Make results big enough to store the results of the subtree
                    self.results = ["" for j in range(0, len(sub_branch))]

                    if((sub_branch[i]) in self.query_dict.keys()):
                        self.query_array.append(self.query_dict[sub_branch[i]])
                
                query = self.query_array[0]
                self.results[0] = connect_tpch(query, TRUE)
                range_array = [1, 1]

                for i in self.results[0]:
                    self.depth = len(sub_branch)
                    index = 0
                    range_array[0] = range_array[1] = i[1]
                    while(self.depth != 0):
                        query = self.query_dict[sub_branch[index]]
                        if(index):
                            sid_string = "R"+str(sub_branch[index-1])+"_SID"
                            query += " WHERE "+sid_string+" >= "+str(range_array[0])+ " AND "+sid_string+ " <= "+str(range_array[1])+" ORDER BY R"+str(sub_branch[index])+"_SID"
                            print(query)
                            self.results[index] = connect_tpch(query, TRUE)
                            range_array[0] = self.results[index][0][1]
                            range_array[1] = self.results[index][len(self.results[index])-1][1]
                        index+=1
                        self.depth-=1
                    self.store_linear_results()
               
                sub_result = self.return_results[:]
                print(len(sub_result))
                
                # print(sub_result)
                # self.log_diverted_results(main_result, sub_result, sub_branch[0])

        # print(self.master_array)
                
        # self.elapsed_time = time.time() - self.start_time
        # print("{:.4f}".format(self.elapsed_time))

    


    def log_linear_results(self): 
        if(len(self.results) == 5):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[1] > tuple3[0]):
                            continue
                        elif(tuple2[1] < tuple3[0]):
                            break
                        for tuple4 in self.results[3]:
                            if(tuple3[1] > tuple4[0]):
                                continue
                            elif(tuple3[1] < tuple4[0]):
                                break
                            for tuple5 in self.results[4]:
                                if(tuple4[1] > tuple5[0]):
                                    continue
                                elif(tuple4[1] < tuple5[0]):
                                    break
                                elif(tuple1[1] == tuple2[0] and tuple2[1] == tuple3[0] and tuple3[1] == tuple4[0] and tuple4[1] == tuple5[0]):
                                    self.counter+=1
                                    # self.logfile.write('|'.join('%s' % x for x in tuple1))
                                    # self.logfile.write('|'.join('%s' % x for x in tuple2))
                                    # self.logfile.write('|'.join('%s' % x for x in tuple3))
                                    # self.logfile.write('|'.join('%s' % x for x in tuple4))
                                    # self.logfile.write('|'.join('%s' % x for x in tuple5))
                                    # self.logfile.write('\n')
        elif(len(self.results) == 4):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[1] > tuple3[0]):
                            continue
                        elif(tuple2[1] < tuple3[0]):
                            break
                        for tuple4 in self.results[3]:
                            if(tuple3[1] > tuple4[0]):
                                continue
                            elif(tuple3[1] < tuple4[0]):
                                break    
                            elif(tuple1[1] == tuple2[0] and tuple2[1] == tuple3[0] and tuple3[1] == tuple4[0]):
                                self.counter+=1
                                # self.logfile.write('|'.join('%s' % x for x in tuple1))
                                # self.logfile.write('|'.join('%s' % x for x in tuple2))
                                # self.logfile.write('|'.join('%s' % x for x in tuple3))
                                # self.logfile.write('|'.join('%s' % x for x in tuple4))
                                # self.logfile.write('\n')
        elif(len(self.results) == 3):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[1] > tuple3[0]):
                            continue
                        elif(tuple2[1] < tuple3[0]):
                            break
                        elif(tuple1[1] == tuple2[0] and tuple2[1] == tuple3[0]):
                            self.counter+=1
                            # self.logfile.write('|'.join('%s' % x for x in tuple1))
                            # self.logfile.write('|'.join('%s' % x for x in tuple2))
                            # self.logfile.write('|'.join('%s' % x for x in tuple3))
                            # self.logfile.write('\n')
        elif(len(self.results) == 2):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    else:
                        self.counter+=1
                        # self.logfile.write('|'.join('%s' % x for x in tuple1))
                        # self.logfile.write('|'.join('%s' % x for x in tuple2))
                        # self.logfile.write('\n')
        elif(len(self.results) == 1):
            for tuple1 in self.results[0]:
                #logging to a file
                # self.logfile.write('|'.join('%s' % x for x in tuple1))
                # self.logfile.write('\n')
                self.counter+=1
        else:
            print("Couldn't see any data")
        



    def align(self, first, second):
        if(first in self.alignment.keys()):
            self.alignment[first] = 2
        else:
            self.alignment[first] = 1

        if(second in self.alignment.keys()):
            self.alignment[second] = 2
        else:
            self.alignment[second] = 1

    def generate_result(self):
        self.start_time = time.time()
        self.create_nodes()
        self.logfile.close()
                   
app = Flask(__name__)


@app.route('/')
def hello():
    main = Application()
    main.mainloop()
    return "Tkinter closed"




