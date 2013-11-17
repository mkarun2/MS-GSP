def ts_contains(transaction_sequence, candidate_sequence):
    t_str=""
    c_str=""
    for t in transaction_sequence:
        t_str = t_str+str(t).strip()
    for c in candidate_sequence:
        c_str = c_str+str(c).strip()
    return contains(t_str.replace(' ', ''), c_str.replace(' ', ''))
    
#=====================================================================================================================================#   
def contains(t_seq, c_seq):
    
    temp_c_seq=c_seq
    counter=0
    cseq=[]
    sorted_cseq=[]
    dseq=[]
    flag=[]

    #Splitting the candidate sequence into separate elements
    while temp_c_seq!="":
        cseq.append(temp_c_seq[temp_c_seq.find("[")+1:temp_c_seq.find("]")].split(","))
        #print("cseq:",cseq)
        temp_c_seq=temp_c_seq.replace("["+temp_c_seq[temp_c_seq.find("[")+1:temp_c_seq.find("]")]+"]","",1)
        #print("temp_c_seq:",temp_c_seq)
        counter=counter+1
        
    temp_c_seq=t_seq
    
    #Splitting the data sequence into separate elements
    while temp_c_seq!="":
        dseq.append(temp_c_seq[temp_c_seq.find("[")+1:temp_c_seq.find("]")].split(","))
        temp_c_seq=temp_c_seq.replace("["+temp_c_seq[temp_c_seq.find("[")+1:temp_c_seq.find("]")]+"]","",1)
    
    for i in range(0,len(dseq)):
        flag.append(0)

    for i in sorted(cseq,key=lambda i:len(i),reverse=True):
        sorted_cseq.append(i)
    
    #print sorted_cseq
    pattern=-1
    for can in cseq:
        for i in range(pattern+1,len(dseq)):
            if (set(can).issubset(set(dseq[i]))) and (flag[i]==0):
                pattern=i
                flag[i]=1
                break
    
    if sum(flag)==counter:
        return 1
    else:
        return 0

#=====================================================================================================================================#    
                  
#This function converts List of String to int
def convertStringToIntList(inputList):
    outputList = list(map(int,inputList))
    return outputList

#=====================================================================================================================================#   

#This function converts dictionary in String format to numerical format
def convert_string_to_int_dict(strDict):
    MISDict_int = dict((int(k),float(v) ) for k, v in strDict.items())
    return MISDict_int

#=====================================================================================================================================#   

# Method to get the first element alone in the set
def get_first_from_set(mySet):
    for item_id in mySet:
        break
    return item_id

#=====================================================================================================================================#      
# reverse a list of lists containing numbers
# def reverse_list_of_lists_numbers(inputList):
#     if inputList is not None and len(inputList) != 0:
#         # check if the len of each list is one in list of list
#         
# #         [x[::-1] for x in inputList]
#         return inputList
#     else:
#         return None

def reverse_list_of_lists_numbers(a):
    if a is not None and len(a) != 0:
        a.reverse()
        for i in a:
            if isinstance(i, list):
                reverse_list_of_lists_numbers(i)
        return a
    else:
        return None
    
#=====================================================================================================================================#   
def equals_list(list1,list2):    
    if (size_sequence(list1) == size_sequence(list2)):
        index_list1 = 0
        index_list2 = 0
#         import collections
#         compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
#         bool_list = list()
#             result = (compare(list1[index_list1],list2[index_list2]))
        
        while index_list1 < len(list1) and index_list2 < len(list2):
            if list1[index_list1] == list2[index_list2]:
                index_list1 = index_list1 + 1
                index_list2 = index_list2 + 1
                continue  
            else:
                return False

        return True
    else:
        return False

# check equality of two list of lists (subsequence check)
def dropItemOperationsInSequences(list1,list2):
    if (list1 is not None and list2 is not None) \
        and (length_sequence(list1) > 1 and length_sequence(list2) > 0):
        
        # for dropping the second item from list1, check the elements 1 and 2 in list1
        element_count = 1
        for i in range(2):
            # if the size of the 1st element is 1
            if element_count == 1 and len(list1[i]) == 1: # first element
                element_count = element_count + 1
                continue
            # 1st element , size 2, remove 2nd item 
            if element_count == 1 and len(list1[i]) > 1: 
                # drop the 2nd item
                item2 = list1[i].pop(1)
                #print(item2)
                break
            # 2nd element is size == 1, get first item and delete list
            elif element_count == 2 and (len(list1[i]) == 1):
                item2 = list1[i].pop(0)
                del list1[i]
                #print("2nd item ",item2)
                break
            # 2nd element is size > 1, get first item
            elif element_count == 2 and (len(list1[i]) > 1):
                item2 = list1[i].pop(0)
                #print("2nd item ",item2)
                break
           
        
        #print("list1 : ",list1 )
    
        # drop the last item from list2
        last_element_list2 = list2[len(list2)-1] 
        last_item_list2 = last_element_list2.pop(len(last_element_list2)-1)
        if len(list2[len(list2)-1]) == 0:
            del list2[len(list2)-1]

        return list1,list2,item2,last_item_list2
    else:
        return None,None,None,None
    
def dropItemOperationsInSequencesNormalJoin(list1,list2):
    if (list1 is not None and list2 is not None) \
        and (length_sequence(list1) > 1  and length_sequence(list2) > 1):
        item1 = list1[0].pop(0)
        if len(list1[0]) == 0:
            del list1[0]
        last_item_list2 = list2[len(list2)-1].pop()
        if len(list2[len(list2)-1]) == 0:
            del list2[len(list2)-1]
        return list1,list2,item1,last_item_list2
    else:
        return None,None,None,None

#=====================================================================================================================================#   
    
# convert list of sets to one single list
def convert_list_of_lists_to_one_list(list_of_lists):
    temp_list = list()
    # union all the sets and make a temporary final list
    for s1 in list_of_lists:
        temp_list.extend(s1)        
    return temp_list   # convert set to list

#=====================================================================================================================================#   
    
# check if key is last item in the given set and also separate element
def check_last_item_separate_element(inpListSets,key):
    if (len(inpListSets)-1) >= 0:
        s = inpListSets[len(inpListSets)-1]     # last set in the list
        # check if this is a single element set and check if that element is the key
        if s is not None and len(s) == 1:
            if s.__contains__(key):
                return True
            else:
                return False
        else:
            return False

#=====================================================================================================================================#   
        
# get the length of the sequence
def length_sequence(sequence): # list of sets
    temp_list = list()
    # union all the sets and make a temporary final list
    for s1 in sequence:
        temp_list.extend(s1)        
    return len(temp_list)   # return the number of items in the list as length

#=====================================================================================================================================#   

# get the size of the sequence
def size_sequence(sequence): # list of sets
    if sequence is not None:
        return len(sequence)
    
#=====================================================================================================================================#
def check_presence_of_min_item(mylist, min_item):
    return (min_item in [j for i in mylist for j in i])   


def find_k_1_subsets(F_k):
    import copy
    temp_list=list()
    myList=[]
    F_k_temp = list(copy.deepcopy(F_k))
    
    for i in range(0,len(F_k_temp)):
        for j in F_k_temp[i]:
            myList.append(j)
    
    for item in myList:        
        F_k_temp=delete(item,F_k_temp)
        #print(F_k_temp)
        temp_list.append(F_k_temp)
        F_k_temp = copy.deepcopy(F_k)
    return temp_list
           
           
def delete(item, F_k):
    item_set=[]
    for item_set in F_k:
        try:
            item_set.remove(item)
            if(len(item_set)==0):
                F_k.remove(item_set)
        except ValueError:
            pass
    return F_k


# # Call the main method
# # if __name__ == '__main__':  print("Inga:",reverse_list_of_lists_numbers([[5],[4],[3]]))
# #if __name__ == '__main__': print(ts_contains( [[10,20], [30], [10,40, 60, 70]], [[60,70]] ) )
# if __name__ == '__main__':  print("Inga:",dropItemOperationsInSequences(  [[80,70,30]], [[30],[70,40]]     ))
