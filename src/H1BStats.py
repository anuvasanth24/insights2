
import sys
import csv
import itertools
from operator import itemgetter
import collections


def OpenFile(filename):

    try:
        csv_file = open(filename)
        # Using csv.DictReader to return a list of OrderedDicts, one OrderedDict per row
        reader = csv.DictReader(csv_file, delimiter=';')
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
        
    return csv_file, reader


def CloseFile(file_handle):
    if file_handle is not None:
        file_handle.close()


def WriteToFile(final_sorted_list, output_file,fieldnames):
    
    try:
        with open(output_file, 'w') as csv_file:
            #final_sorted_list is also in the form of a list of OrderedDicts and hence using
            #csv.DictWriter to write output list to file
            writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
    
            for row in final_sorted_list:
                writer.writerow(row)
    except IOError as e:
        print(e)

#Making sure fieldnames passed from the argsv list are indeed present in file
def CheckIfFieldPresent(file_handle, fieldname):

    present = True
    if file_handle is not None:
        for row in file_handle:
            if fieldname not in row.keys():
                print(f'{fieldname} not present in file')
                present = False

            return present
                

def CreateCertifiedList(file_handle, fieldname):
    certified_list = []

    if file_handle is not None:
        for row in file_handle:
            if(row[fieldname] == 'CERTIFIED'):
                certified_list.append(row)
    
    return certified_list
        

def GetTop10List(cert_list, fieldname, key_list):
    
    final_list = []
    final_sorted_list = []

    certified_list_length = len(cert_list)
    if certified_list_length == 0:
        print("No certified Applications in file")
        return final_sorted_list
        
    # sort the certified list first so it can be grouped by the values of the field
    sorted_cert_list = sorted(cert_list, key=itemgetter(fieldname))
          
    # List of steps:
    # 1. group the sorted list by the different values of the field
    # 2. get length of each group
    # 3. Create an OrderedDict per group with the following keys (therefore each row corresponds to a group)
    #           (occupation/state name, application count, percentage)
    # 4. Sort the final list in descending order by application count
    # 5. If more than 10 groups present in the list, return top 10. If not return whole list
    
    for key, group_name in itertools.groupby(sorted_cert_list, key=lambda x:x[fieldname]):
        count = len(list(group_name))
        percent = round(float((count/certified_list_length)*100),1)
        value_list = [key,count,percent]
        d = collections.OrderedDict(zip(key_list,value_list))
        final_list.append(d)
    
        final_sorted_list = sorted(final_list, key=itemgetter(key_list[1]),reverse=True)
    
        if(len(final_sorted_list) > 10):
            final_sorted_list = final_sorted_list[:10]

    return final_sorted_list


def main(argv):

    fields_present = True

    # Format: H1bStats.py <input_file_name> <cert_fieldname> <occupation_fieldname> <state_fieldname>

    if len(argv) < 4:
        print("Usage: H1bStats.py <input_file_name> <cert_fieldname> <occupation_fieldname> <state_fieldname>")
        return

    print("Aggregating ...")
    
    input_file = sys.argv[1]
    cert_fieldname = sys.argv[2]
    occ_fieldname = sys.argv[3]
    state_fieldname = sys.argv[4]
    
    occ_output_filename = './output/top_10_occupations.txt'
    state_output_filename = './output/top-10_states.txt'

    occ_key_list = ['TOP_OCCUPATIONS','NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']
    state_key_list = ['TOP_STATES','NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']
    
    csv_file, reader = OpenFile(input_file)
    
    #Make sure fields provided by user are indeed present in the file. If not, bail.
    fields_present &= CheckIfFieldPresent(reader, cert_fieldname)
    fields_present &= CheckIfFieldPresent(reader, occ_fieldname)
    fields_present &= CheckIfFieldPresent(reader, state_fieldname)

    if fields_present == False:
        CloseFile(csv_file)
        return;

    import time
    start = time.time()
    
    # Filtering all rows to get just the rows where the application has been CERTIFIED
    certified_list = CreateCertifiedList(reader, cert_fieldname)

  
    # Getting the top 10 List of certified applications by occupation
    final_occ_sorted_list = GetTop10List(certified_list,occ_fieldname,occ_key_list)
    WriteToFile(final_occ_sorted_list, occ_output_filename, occ_key_list)
    
    # Getting the top 10 List of certified applications by occupation
    final_state_sorted_list = GetTop10List(certified_list,state_fieldname,state_key_list)
    WriteToFile(final_state_sorted_list,state_output_filename,state_key_list)
    end = time.time()
    print(end-start)


    CloseFile(csv_file)
    


if __name__ == '__main__':
    main(sys.argv[1:])

