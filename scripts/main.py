from flask import Flask, render_template
from tkinter import *
import pandas as pd
from dbconnect import connect_tpch
from queryAPI import get_query
import numpy as np

class Application(Frame):
    def __init__(self):
        root = Tk()

        super().__init__(root)
        self.pack()
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
        self.matrix = []
        self.global_index = 0
        self.possible_chains = [
            ['r1','r2','r5','r6','r8'],
            ['r1','r2','r4','r8'],
            ['r3','r8'],
            ['r3','r7']
        ]
        self.master_array = []
        self.results = []
        self.lineitemcolumn = 4

    def create_widgets(self, root):       

        self.quit = Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(padx=5, pady=5)

        self.graph = Button(self)
        self.graph["text"] = "GENERATE GRAPH!"
        self.graph["command"] = self.generate_graph
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
        
    def region(self):
        return None

    def nation(self):
        return None

    def part(self):
        return None

    def supplier(self):
        return None

    def customer(self):
        return None

    def orders(self):
        return None

    def partsupp(self):
        return None

    def lineitem(self):
        return None


    def region_nation(self):
        self.align('r1','r2')
        self.query_array.append('SELECT * FROM ALIGNED_NATION LIMIT 0, 25')
        self.r1r2.config(state=DISABLED)
        self.create_matrix(1,2,25)

    def nation_supplier(self):  
        self.align('r2', 'r4')
        self.query_array.append('SELECT * FROM ALIGNED_SUPPLIER LIMIT 0, 100')
        self.r2r4.config(state=DISABLED)
        self.create_matrix(2,4,10000)

    def nation_customer(self):
        self.align('r2', 'r5')
        self.query_array.append('SELECT * FROM ALIGNED_CUSTOMER LIMIT 0, 100')
        self.r2r5.config(state=DISABLED)
        self.create_matrix(2,5,150000)

    def part_partsupp(self):
        self.align('r3', 'r7')
        self.query_array.append('SELECT * FROM ALIGNED_PARTSUPP LIMIT 0, 100')
        self.r3r7.config(state=DISABLED)
        self.create_matrix(3,7,800000)

    def part_lineitem(self):
        self.align('r3', 'r8')
        self.query_array.append('SELECT * FROM ALIGNED_LINEITEM LIMIT 0, 100')
        self.r3r8.config(state=DISABLED)
        self.create_matrix(3,8,6000000)

    def supplier_partsupp(self):
        self.align('r4', 'r7')
        self.query_array.append('SELECT * FROM ALIGNED_PARTSUPP LIMIT 0, 100')
        self.r4r7.config(state=DISABLED)
        self.create_matrix(4,7,800000)

    def supplier_lineitem(self):
        self.align('r4','r8')
        self.query_array.append('SELECT * FROM ALIGNED_LINEITEM LIMIT 0, 100')
        self.r4r8.config(state=DISABLED)
        self.create_matrix(4,8,6000000)

    def customer_orders(self):
        self.align('r5', 'r6')
        self.query_array.append('SELECT * FROM ALIGNED_ORDERS LIMIT 0, 100')
        self.r5r6.config(state=DISABLED)
        self.create_matrix(5,6,1500000)

    def orders_lineitem(self):
        self.align('r6','r8')
        self.query_array.append('SELECT * FROM ALIGNED_LINEITEM LIMIT 0, 100')
        self.lineitemcolumn = 5
        self.r6r8.config(state=DISABLED)
        self.create_matrix(6,8,6000000)

    def create_matrix(self, a, b, c):
        # Creates an array of array, where in the inside array contains 
        # details of all the nodes selected by user and the total 
        # number of rows the aligned table has 
        self.matrix.append([a,b,c])

    def create_nodes(self):
        # Node Dictionary, stores all the information about nodes, and its children
        node_dict = {}

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
            # Iterate through all the keys of the dictionary, it's values are children, if a node as more
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
        

        arr = []
        for n in node_array:
            # Checking if the array has another array, which means checking for diversions
            if(isinstance(n, list) == True):
                temp = arr[:] # Making temp empty by assigning blank array by doing Copy by value, temp = arr copies array by reference
                for j in n: # Iterate through the nested array
                    if(type(j))
                    elif(j != None):
                        temp.append(j)
                    else:
                        self.master_array.append(temp) # This means that you've hit the child node, store the whole path as an array in the master array
                        temp = [] # Empty temp to store a new tree path
            elif(isinstance(n, int) == True):
                arr.append(n)

        print(self.master_array)

        if(len(self.master_array) == 2):
            tree1 = self.master_array[0]
            treevalue1 = 0
            for i in range(1, len(self.master_array[0])):
                elem = self.master_array[0][i]
                ind = 0
                for j in self.matrix:
                    if(j[1] == elem):
                        ind = self.matrix.index(j)
                        break
                treevalue1 += self.matrix[ind][2]
    
            tree2 = self.master_array[1]
            treevalue2 = 0
            for i in range(1, len(self.master_array[1])):
                elem = self.master_array[1][i]
                ind = 0
                for j in self.matrix:
                    if(j[1] == elem):
                        ind = self.matrix.index(j)
                        break
                treevalue2 += self.matrix[ind][2]
            
            print(treevalue1, treevalue2)
        
        self.log_diverted_results()

    def align(self, first, second):
        if(first in self.alignment.keys()):
            self.alignment[first] = 2
        else:
            self.alignment[first] = 1

        if(second in self.alignment.keys()):
            self.alignment[second] = 2
        else:
            self.alignment[second] = 1

    def generate_graph(self):
        self.create_nodes()
        # if(2 not in self.alignment.values()):
        #     # self.log_values()
        #     if(len(self.alignment.values()) == 2):
        #         self.log_values("Linear")
        #         print("Success: Two pointed line")
        # else:
        #     if(list(self.alignment.values()).count(1) == 2):
        #         self.log_values("Linear")
        #         print("Success: Linear graph")
        #     elif(list(self.alignment.values()).count(1) == 3):
        #         self.log_values("Diverted")
        #         print("Success: Diverted graph")
        #     elif(list(self.alignment.values()).count(1) == 4):
        #         print("Failure: Graph is unconnected")
        #         # self.draw_graph()
                

    def draw_graph(self):
        w = Canvas(width=400, height=300)
        for i in self.alignment.keys():
            x = Label(w, text=self.relations_map[i], bg="cyan", fg="black")
            w.create_window(100, 100, window=x)
    
    def log_values(self, type):
        self.results = ["" for i in range(0, len(self.alignment.keys()) -1)]
        for i in range(0, len(self.query_array)):
            self.results[i] = connect_tpch(self.query_array[i], TRUE)
            if(not self.results[i]):
                print("Error: MySQL57 not running, please run it from the taskbar")
                break
            else:
                self.results[i] = sorted(self.results[i], key=lambda x: x[0])
        if(type == "Linear"):
            self.log_linear_results()
        elif(type == "Diverted"):
            self.log_diverted_results()


    def log_linear_results(self):
        if(len(self.results) == 4):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[4] > tuple2[0]):
                        continue
                    elif(tuple1[4] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[4] > tuple3[0]):
                            continue
                        elif(tuple2[4] < tuple3[0]):
                            break
                        for tuple4 in self.results[3]:
                            if(tuple3[4] > tuple4[0]):
                                continue
                            elif(tuple3[4] < tuple4[0]):
                                break    
                            elif(tuple1[4] == tuple2[0] and tuple2[4] == tuple3[0] and tuple3[4] == tuple4[0]):
                                print(tuple1[0], tuple1[4], tuple2[0], tuple2[4], tuple3[0], tuple3[4], tuple4[0], tuple4[self.lineitemcolumn])
        elif(len(self.results) == 3):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[4] > tuple2[0]):
                        continue
                    elif(tuple1[4] < tuple2[0]):
                        break
                    for tuple3 in self.results[2]:
                        if(tuple2[4] > tuple3[0]):
                            continue
                        elif(tuple2[4] < tuple3[0]):
                            break
                        elif(tuple1[4] == tuple2[0] and tuple2[4] == tuple3[0]):
                            print(tuple1[0], tuple1[4], tuple2[0], tuple2[4], tuple3[0], tuple3[self.lineitemcolumn])

        elif(len(self.results) == 2):
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[4] > tuple2[0]):
                        continue
                    elif(tuple1[4] < tuple2[0]):
                        break
                    else:
                        print(tuple1[0], tuple1[4], tuple2[0], tuple2[self.lineitemcolumn])
        elif(len(self.results) == 1):
            for tuple1 in self.results[0]:
                print(tuple1[0], tuple1[self.lineitemcolumn])
        else:
            print("Couldn't see any data")

    def log_diverted_results(self):
        results_lengths = [len(self.results[i]) for i in range(0, len(self.results))]
        if(len(results_lengths) == 3):
            inflection_array = [int() for i in range(0, len(self.results[0]))]
            index = 0
            temp = 0
            j = 0
            for i in range(index, len(self.results[2])):
                index+=1
                if(temp != self.results[2][i][0]):
                    temp = self.results[2][i][0]
                    inflection_array[j] = index
                    j+=1
            for tuple1 in self.results[0]:
                for tuple2 in self.results[1]:
                    if(tuple1[4] > tuple2[0]):
                        continue
                    elif(tuple1[4] < tuple2[0]):
                        break
                    else:
                        for i in range(0, len(inflection_array)-1):
                            for j in range(inflection_array[i], inflection_array[i+1]):
                                print(tuple1[0], tuple1[4], tuple2[0], tuple2[4], i, self.results[2][j][4])
        elif(len(results_lengths) > 3):
            query_dict = {}
            main_branch = []
            sub_branch = []
            for i in range(0, len(self.matrix)):
                query_dict[self.matrix[i][1]] = self.query_array[i]
            # print(query_dict)

            for key, value in query_dict.items():
                if(key in self.master_array[0] and key in self.master_array[1]):
                    main_branch.append(value)
                elif(key in self.master_array[0]):
                    main_branch.append(value)
                elif(key in self.master_array[1]):
                    sub_branch.append(value)
                else:
                    print("It shouldn't come here")
            print(main_branch, sub_branch)

            def return_linear_results(branch):
                join_result = []
                if(len(branch) == 4):
                    for tuple1 in branch[0]:
                        for tuple2 in branch[1]:
                            if(tuple1[4] > tuple2[0]):
                                continue
                            elif(tuple1[4] < tuple2[0]):
                                break
                            for tuple3 in branch[2]:
                                if(tuple2[4] > tuple3[0]):
                                    continue
                                elif(tuple2[4] < tuple3[0]):
                                    break
                                for tuple4 in branch[3]:
                                    if(tuple3[4] > tuple4[0]):
                                        continue
                                    elif(tuple3[4] < tuple4[0]):
                                        break    
                                    elif(tuple1[4] == tuple2[0] and tuple2[4] == tuple3[0] and tuple3[4] == tuple4[0]):
                                        join_result.append([tuple1[0], tuple1[4], tuple2[0], tuple2[4], tuple3[0], tuple3[4], tuple4[0], tuple4[self.lineitemcolumn]])
                elif(len(branch) == 3):
                    for tuple1 in branch[0]:
                        for tuple2 in branch[1]:
                            if(tuple1[4] > tuple2[0]):
                                continue
                            elif(tuple1[4] < tuple2[0]):
                                break
                            for tuple3 in branch[2]:
                                if(tuple2[4] > tuple3[0]):
                                    continue
                                elif(tuple2[4] < tuple3[0]):
                                    break
                                elif(tuple1[4] == tuple2[0] and tuple2[4] == tuple3[0]):
                                    join_result.append([tuple1[0], tuple1[4], tuple2[0], tuple2[4], tuple3[0], tuple3[self.lineitemcolumn]])

                elif(len(branch) == 2):
                    for tuple1 in branch[0]:
                        for tuple2 in branch[1]:
                            if(tuple1[4] > tuple2[0]):
                                continue
                            elif(tuple1[4] < tuple2[0]):
                                break
                            else:
                                join_result.append([tuple1[0], tuple1[4], tuple2[0], tuple2[self.lineitemcolumn]])
                elif(len(branch) == 1):
                    for tuple1 in branch[0]:
                        join_result.append([tuple1[0], tuple1[self.lineitemcolumn]])

                return join_result
            
            main_branch_result = []
            main_branch_result = ["" for i in range(0, len(main_branch))]
            main_joined = []
            for i in range(0, len(main_branch)):
                main_branch_result[i] = connect_tpch(main_branch[i], TRUE)
                if(not main_branch[i]):
                    print("Error: MySQL57 not running, please run it from the taskbar")
                    break
                else:
                    main_branch_result[i] = sorted(main_branch_result[i], key=lambda x: x[0])
                    main_joined = return_linear_results(main_branch_result)
                    

            sub_branch_result = []
            sub_branch_result = ["" for i in range(0, len(sub_branch))]
            sub_joined = []
            for i in range(0, len(sub_branch)):
                print("Heree")
                sub_branch_result[i] = connect_tpch(sub_branch[i], TRUE)
                if(not sub_branch[i]):
                    print("Error: MySQL57 not running, please run it from the taskbar")
                    break
                else:
                    sub_branch_result[i] = sorted(sub_branch_result[i], key=lambda x: x[0])
                    sub_joined = return_linear_results(sub_branch_result)

            inflection_array = [int() for i in range(0, len(sub_branch_result[0]))]
            index = 0
            temp = 0
            j = 0
            for i in range(index, len(sub_joined)):
                index+=1
                if(temp != sub_joined[i][0]):
                    temp = sub_joined[i][0]
                    inflection_array[j] = index
                    j+=1
            # print(inflection_array)
            inflection_array = np.trim_zeros(inflection_array)
            for tuple1 in main_joined:
                for tuple2 in sub_joined:
                    if(tuple1[1] > tuple2[0]):
                        continue
                    elif(tuple1[1] < tuple2[0]):
                        break
                    else:
                        print(tuple1[0], tuple1[1], tuple1[3], tuple2[1], tuple2[3])
                            
app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/')
def hello():
    main = Application()
    main.mainloop()
    return "Tkinter closed"

# @app.route('/table')
# def display_table():
#     # do something to create a pandas datatable
#     df = pd.DataFrame(data=[[1,2],[3,4]])
#     df_html = df.to_html()  # use pandas method to auto generate html
#     return render_template('page.html', table_html=df_html)




