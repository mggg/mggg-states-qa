import sys
sys.path.insert(1, '../..')

from geodata.ExtractTable import ExtractTable

#########################################
# Regression Tests                      #
#########################################

def run_tests():
    print('et = ExtractTable()')
    et = ExtractTable()
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print()

    try:
        et.value = 'fail'
    except Exception as e:
        print('Expected failure:', e)
    
    try:
        et.column = 'fail'
    except Exception as e:
        print('Expected failure:', e)

    try:
        et.infile = "test/asdf"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        extracted = et.extract()
    except Exception as e:
        print('Expected failure.', e)
    print()

    et.infile = "test1.csv"

    try:
        et.value = "sdf"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.infile = "asdf/asdf"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.column = "col"
    except Exception as e:
        print('Expected failure.', e)

    print(et.extract())
    print()

    et.column = "col1"
    
    try:
        et.value = "fda"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.column = "col"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.value = "fda"
    except Exception as e:
        print('Expected failure.', e)

    print(et.extract())
    print()

    et.value = "c"
    print(et.extract())
    print()


def run_tests2():
    try:
        et = ExtractTable.read_file()
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et = ExtractTable.read_file("asdf/asdf")
    except Exception as e:
        print('Expected failure.', e)

    try:
        et = ExtractTable.read_file(column=2, value='asdf')
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et = ExtractTable.read_file("test1.csv", column="3")
    except Exception as e:
        print('Expected failure.', e) 

    try:
        et = ExtractTable.read_file("test1.csv", value="3")
    except Exception as e:
        print('Expected failure.', e) 

    try:
        et = ExtractTable.read_file("test1.csv", column="col1", value=3)
    except Exception as e:
        print('Expected failure.', e) 
    print()

    et = ExtractTable.read_file("test1.csv")
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print()


    et = ExtractTable.read_file("test1.csv", column="col1")
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print()

    et = ExtractTable.read_file("test1.csv", column="col1", value="c")
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print() 

    et = ExtractTable.read_file("test1.csv", column="col1", value=['a', 'c'])
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print()


def run_tests3():
    et = ExtractTable.read_file("test1.csv")
    print(type(et.list_columns()))
    print(et.list_columns())

    try:
        et.list_column_values()
    except Exception as e:
        print("Expected failure.", e)
    print()
    
    print(type(et.list_values('field_1')))
    print(et.list_values('field_1'))
    print(et.list_values('field_1', unique=True))
    print()

    et.column = 'col1'
    print(type(et.list_values()))
    print(et.list_values())
    print(et.list_values(unique=True))
    print()

    print(type(et.list_values('geometry')))
    print(et.list_values('geometry'))
    print(et.list_values('geometry', unique=True))
    print()


#########################################
# Function Calls                        #
#########################################
# run_tests()
# run_tests2()
run_tests3()
