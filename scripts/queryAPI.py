from dbconnect import connect_tpch

def get_query(first, second):

    if(first == 'region' and second == 'nation'):
        # R1 -> R2
        # REGION -> NATION
        table_drop = 'DROP TABLE ALIGNED_NATION; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_NATION ' +
        'SELECT ALIGNED_REGION.R1_SID, NATION.* ' +
        'FROM ALIGNED_REGION ' +
        'RIGHT JOIN NATION ON ALIGNED_REGION.R_REGIONKEY = NATION.N_REGIONKEY ' +
        'ORDER BY ALIGNED_REGION.R1_SID; ' +
        'ALTER TABLE ALIGNED_NATION ADD R2_SID INTEGER; ' +
        'UPDATE ALIGNED_NATION ' +
        'SET R2_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_NATION ADD PRIMARY KEY(N_NATION); ' +
        'ALTER TABLE ALIGNED_NATION ADD KEY(R1_SID); ' +
        'ALTER TABLE ALIGNED_NATION ADD UNIQUE KEY(R2_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_nation';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'nation' and second == 'supplier'):
        # R2 -> R4
        # NATION -> SUPPLIER
        table_drop = 'DROP TABLE ALIGNED_SUPPLIER; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_SUPPLIER '
        'SELECT ALIGNED_NATION.R2_SID, SUPPLIER.* ' +
        'FROM ALIGNED_NATION '
        'RIGHT JOIN SUPPLIER ON ALIGNED_NATION.N_NATIONKEY = SUPPLIER.S_NATIONKEY ' +
        'ORDER BY ALIGNED_NATION.R2_SID; ' +
        'ALTER TABLE ALIGNED_SUPPLIER ADD R4_SID INTEGER; ' +
        'UPDATE ALIGNED_SUPPLIER ' +
        'SET R4_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_SUPPLIER ADD PRIMARY KEY(S_SUPPKEY); ' +
        'ALTER TABLE ALIGNED_SUPPLIER  ADD KEY(R2_SID); ' +
        'ALTER TABLE ALIGNED_SUPPLIER ADD UNIQUE KEY(R4_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_supplier';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'nation' and second == 'customer'):
        # R2 -> R5
        # NATION -> CUSTOMER
        table_drop = 'DROP TABLE ALIGNED_CUSTOMER; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_CUSTOMER '
        'SELECT ALIGNED_NATION.R2_SID, CUSTOMER.* ' +
        'FROM ALIGNED_NATION '
        'RIGHT JOIN CUSTOMER ON ALIGNED_NATION.N_NATIONKEY = CUSTOMER.C_NATIONKEY ' +
        'ORDER BY ALIGNED_NATION.R2_SID; ' +
        'ALTER TABLE ALIGNED_CUSTOMER ADD R5_SID INTEGER; ' +
        'UPDATE ALIGNED_CUSTOMER ' +
        'SET R5_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_CUSTOMER ADD PRIMARY KEY(C_CUSTKEY); ' +
        'ALTER TABLE ALIGNED_CUSTOMER  ADD KEY(R2_SID); ' +
        'ALTER TABLE ALIGNED_CUSTOMER ADD UNIQUE KEY(R5_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_customer';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'part' and second == 'partsupp'):
        # R3 -> R7
        # PART -> PARTSUPP
        table_drop = 'DROP TABLE ALIGNED_PARTSUPP; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_PARTSUPP '
        'SELECT ALIGNED_PART.R3_SID, PARTSUPP.* ' +
        'FROM ALIGNED_PART '
        'RIGHT JOIN PARTSUPP ON ALIGNED_PART.P_PARTKEY = PARTSUPP.PS_PARTKEY ' +
        'ORDER BY ALIGNED_PART.R3_SID; ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD R7_SID INTEGER; ' +
        'UPDATE ALIGNED_PARTSUPP ' +
        'SET R7_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD PRIMARY KEY(PS_PARTKEY, PS_SUPPKEY); ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD KEY(R3_SID); ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD UNIQUE KEY(R7_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_partsupp';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'part' and second == 'lineitem'):
        # R3 -> R8
        # PART -> LINEITEM
        table_drop = 'DROP TABLE ALIGNED_LINEITEM; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_LINEITEM '
        'SELECT ALIGNED_PART.R3_SID, LINEITEM.* ' +
        'FROM ALIGNED_PART '
        'RIGHT JOIN LINEITEM ON ALIGNED_PART.P_PARTKEY = LINEITEM.L_PARTKEY ' +
        'ORDER BY ALIGNED_PART.R3_SID; ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD R8_SID INTEGER; ' +
        'UPDATE ALIGNED_LINEITEM ' +
        'SET R8_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD PRIMARY KEY(L_ORDERKEY, L_LINENUMBER); ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD KEY(R3_SID); ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD UNIQUE KEY(R8_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_lineitem';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'supplier' and second == 'partsupp'):
        # R4 -> R7
        # SUPPLIER -> PARTSUPP
        table_drop = 'DROP TABLE ALIGNED_PARTSUPP; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_PARTSUPP '
        'SELECT ALIGNED_SUPPLIER.R4_SID, PARTSUPP.* ' +
        'FROM ALIGNED_SUPPLIER '
        'RIGHT JOIN PARTSUPP ON ALIGNED_SUPPLIER.P_PARTKEY = PARTSUPP.PS_PARTKEY ' +
        'ORDER BY ALIGNED_SUPPLIER.R4_SID; ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD R7_SID INTEGER; ' +
        'UPDATE ALIGNED_PARTSUPP ' +
        'SET R7_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD PRIMARY KEY(PS_PARTKEY, PS_SUPPKEY); ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD KEY(R4_SID); ' +
        'ALTER TABLE ALIGNED_PARTSUPP ADD UNIQUE KEY(R7_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_partsupp';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'supplier' and second == 'lineitem'):
        # R4 -> R8
        # SUPPLIER -> LINEITEM
        table_drop = 'DROP TABLE ALIGNED_LINEITEM; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_LINEITEM '
        'SELECT ALIGNED_SUPPLIER.R4_SID, LINEITEM.* ' +
        'FROM ALIGNED_SUPPLIER '
        'RIGHT JOIN LINEITEM ON ALIGNED_SUPPLIER.P_PARTKEY = LINEITEM.L_PARTKEY ' +
        'ORDER BY ALIGNED_SUPPLIER.R4_SID; ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD R8_SID INTEGER; ' +
        'UPDATE ALIGNED_LINEITEM ' +
        'SET R8_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD PRIMARY KEY(L_ORDERKEY, L_LINENUMBER); ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD KEY(R4_SID); ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD UNIQUE KEY(R8_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_lineitem';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'customer' and second == 'orders'):
        # R5 -> R6
        # CUSTOMER -> ORDERS
        table_drop = 'DROP TABLE ALIGNED_ORDERS; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_ORDERS '
        'SELECT ALIGNED_CUSTOMER.R5_SID, ORDERS.* ' +
        'FROM ALIGNED_CUSTOMER '
        'RIGHT JOIN ORDERS ON ALIGNED_CUSTOMER.C_CUSTKEY = ORDERS.O_CUSTKEY ' +
        'ORDER BY ALIGNED_CUSTOMER.R5_SID; ' +
        'ALTER TABLE ALIGNED_ORDERS ADD R6_SID INTEGER; ' +
        'UPDATE ALIGNED_ORDERS ' +
        'SET R6_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_ORDERS ADD PRIMARY KEY(O_ORDERKEY); ' +
        'ALTER TABLE ALIGNED_ORDERS ADD KEY(R5_SID); ' +
        'ALTER TABLE ALIGNED_ORDERS ADD UNIQUE KEY(R6_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_orders';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    elif(first == 'orders' and second == 'lineitem'):
        # R6 -> R8
        # ORDERS -> LINEITEM
        table_drop = 'DROP TABLE ALIGNED_LINEITEM; '
        operation = ('SELECT @n:=0; ' +
        'CREATE TABLE ALIGNED_LINEITEM '
        'SELECT ALIGNED_ORDERS.R6_SID, LINEITEM.* ' +
        'FROM ALIGNED_ORDERS '
        'RIGHT JOIN LINEITEM ON ALIGNED_ORDERS.O_ORDERKEY = LINEITEM.L_ORDERKEY ' +
        'ORDER BY ALIGNED_ORDERS.R6_SID; ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD R8_SID INTEGER; ' +
        'UPDATE ALIGNED_LINEITEM ' +
        'SET R8_SID = @n := @n + 1; ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD PRIMARY KEY(L_ORDERKEY, L_LINENUMBER); ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD KEY(R6_SID); ' +
        'ALTER TABLE ALIGNED_LINEITEM ADD UNIQUE KEY(R8_SID); ')

        table_exists = "SELECT count(*) FROM information_schema.tables where table_schema='tpch' and table_name='aligned_lineitem';"
        table_flag = connect_tpch(table_exists, True)[0][0]
        print(table_flag)
        if(table_flag == 1):
            operation = table_drop + operation
        print(operation)
        return operation
    else:
        print("something wrong")