
# General utilities module for this algorithm 
# all the functions are being used, hence the *
from MSGSPUtilities import *

class MSGSP:

    # Global Variables #
    ####################
    L = list()                   #Set containing valid items based on MIS
    MISDict = dict()            #This is dictionary containing ITEM_ID as Keys and MIS as Values in int : float format
    SortedMISList = list()          #This is a LIST containing ITEM_IDs sorted based on their MIS values in int format
    support_count_dict=dict()       #Support count Dictionary of each item int : int
    transaction_count = None      #Total number of Transactions
    SDC = None
    CANDIDATE_COUNT_DICT = dict()
    FREQUENT_ITEMSET_DICT = dict()
    FILE_PATH = 'C:/Users/Ravi/Desktop/CS_583_Data Mining/Project_1/'
    
    #write output to intermediate files
    def write_to_file(self, itemSetList,File_name):
        file_path = self.FILE_PATH+str(File_name)+'.txt'
        f = open (file_path, 'w')
        for line in itemSetList:
            f.write(str(line)+"\n")
        f.close()
    
    # Method to read and return file contents
    def generateListFromInputFile(self,location):
        global SDC
        sequenceList = list()
        try:
            fHandler = open(location,'r')
            for line in fHandler:
                sequenceList.append(line.strip())
                if line.strip().__contains__('SDC'):
                    list_sdc = line.strip().rsplit(' ');
                    self.SDC = float(list_sdc[2])
            return sequenceList
        except IOError as e:
            print("File not found " , e) 
    #=====================================================================================================================================#   
    
    # Method to convert list to dictionary
    def convertMISListToDict(self, MISInputList):
        # extract the item and its MIS value    
        for st in MISInputList:
            try:
                if "(" and ")" in st:            
                    start_index = st.index("(") + 1
                    end_index = st.index(")")
                    item = st[start_index:end_index]      #item substring     
                    if "=" in st:       
                        start_index = st.index("=")+1
                        value = st[start_index :]          # MIS value substring
                        self.MISDict[item] = value.strip();
            except ValueError as e:
                print("error in obtaining MIS substring", e)
        return self.MISDict
    
    #=====================================================================================================================================#   
    
          
    # given a sequence list, return a list of sets of sequences of transactions
    def createListOfSets(self,sequenceList):
        
            # initialize support_count_dictionary
            global support_count_dictionary
            for i in SortedMISList:
                self.support_count_dict[i] = 0
        
            import re
            finalList = list()
            for s in sequenceList:
                m = re.findall('{[0-9, ]*}',s)
                listOfSets = [list(list(map(int,st.replace('{','').replace('}','').split(',')))) for st in m]  # convert to list of sets of sequences
                finalList.append(listOfSets)
                
                # support_count_dictionary calculation
                # frozen set of list of sets containing the set of items in a transaction
                itemSets = frozenset().union(*listOfSets)
                for item_id in itemSets:
                    self.support_count_dict[item_id] = self.support_count_dict[item_id] + 1
                    
            return finalList
    #=====================================================================================================================================#     
            
    # init-pass() method in the algorithm
    
    def initPass(self,sequenceList):
        global L,support_count_dict,transaction_count
#         print("SortedMISList:",SortedMISList)
        #self.SortedMISList = [20, 60, 70, 80, 90, 10, 30, 40, 50]
        # Find the first i item that meets MIS(i)
        for item_id in SortedMISList:
            if(float(self.support_count_dict[item_id])/transaction_count >=  float(self.MISDict[item_id])):
                if self.L.__contains__(item_id):
                    continue
                else:
                    self.L.append(item_id)
                    break
        
        # get the first item from L to compare MIS of other items, to add to set L 
        first_item = get_first_from_set(self.L)
        
        # Move in the sorted order to retrieve the first j item where j.count/n >= MIS(first_item)
        for item_id in SortedMISList:
            if(float(self.support_count_dict[item_id])/transaction_count >= float(self.MISDict[first_item])):
                if self.L.__contains__(item_id):
                    continue
                else:
                    self.L.append(item_id)         
            else:
                continue    
        return self.L
      
    #=====================================================================================================================================#    
    
    # pre-process input files for the algorithm
    def preprocessInputFile(self,sequenceInputFile, MISInputFile):
        MISList = self.generateListFromInputFile(MISInputFile)
        MISDict_string = self.convertMISListToDict(MISList)  # complete string version
        global MISDict,transaction_count,SortedMISList 
        self.MISDict = convert_string_to_int_dict(MISDict_string) # Converts String dictionary to float
        SortedMISList_String = sorted(self.MISDict, key = self.MISDict.get)#This contains sorted list of items based on MIS values
        SortedMISList = convertStringToIntList(SortedMISList_String)   # store a list of item_id (int) sorted on MIS values
        sequenceList = self.generateListFromInputFile(sequenceInputFile)    #This line reads Transactions into a list
        transaction_count = len(self.createListOfSets(sequenceList))
        return sequenceList
    
    #=====================================================================================================================================#   
    
    #This function generates F1 set
    def generate_F1(self,L):
        F1=[]
        for item_id in L:
            if(self.support_count_dict[item_id]/ transaction_count >= self.MISDict[item_id]):
                item_1_set = {item_id}
                F1_temp_list = list()       # create a list of 1 item set in it
                F1_temp_list.append(item_1_set)     # add the set to the list
                F1.append(F1_temp_list)             # add to final list to return
        return F1  
    
    #=====================================================================================================================================#   
    
    # Method to calculate level 2 candidate generation    
    def level2_candidate_gen(self,L):
#         print(L)
        C2 = list()              # candidate 2 sequence set
        for l in self.L:
            #print("l:",l)        
            if float(self.support_count_dict[l]/transaction_count) >= float(self.MISDict[l]):            
                indx = L.index(l)        # item h after l   
                while indx < len(L):               
                    h = L[indx]
                    #print("h:",h)
                    if (float(self.support_count_dict[h]/transaction_count)  >= float(self.MISDict[l])) \
                        and (abs( self.supportOfItem(h) - self.supportOfItem(l) ) <= self.SDC):                   
                        # meaning [x,y] not using sets here though because of the hashing problem
                        
                        if l!=h:
                        
                            if self.MISDict[h] == self.MISDict[l]:
                                if l > h:
                                    s1 = [h,l] 
                                elif l < h:
                                    s1 = [l,h] 
                            else:
                                s1 = [l,h] 
                                
                            list1 = list()
                            list1.append(s1)
                            C2.append(list1)
                                
                            ls1 = [l] # {x}
                            ls2 = [h] # {y}
                            list2 = list()
                            list2.append(ls1) 
                            list2.append(ls2) 
                            C2.append(list2)
                    
                        ls3 = [h] # {y}
                        ls4 = [l] # {x}
                        list3 = list()
                        list3.append(ls3) 
                        list3.append(ls4) 
                        C2.append(list3)                 
                    indx = indx + 1
                    #print()
        return C2
    
    #=====================================================================================================================================#   
    # Join step for MSCandidateGen method         
    def special_join_step(self,s1,s2,candidate_sequence_list):   
        import copy     
        
        s1_list = convert_list_of_lists_to_one_list(s1)
        
        # have to deep copy because have to remove items from list 
        tmp_s1_list = copy.deepcopy(s1)
        tmp_s2_list = copy.deepcopy(s2)
                
        c1 = copy.deepcopy(s1)
        c2 = copy.deepcopy(s1)

        tmp_s1_list,tmp_s2_list,second_item_s1,last_item_s2 = dropItemOperationsInSequences(tmp_s1_list,tmp_s2_list)
        
        # get the last item from original list without pop for later use
        if len(s1_list) > 0:
            last_item_s1 = copy.deepcopy(s1_list[len(s1_list)-1])    
            first_item_s1 = copy.deepcopy(s1_list[0])
        
        if tmp_s1_list is not None and tmp_s2_list is not None and second_item_s1 is not None and \
            last_item_s2 is not None:

            # subsequence obtained by dropping are equal and MIS last s2 > MIS 2nd of s1
        
            if equals_list(tmp_s1_list,tmp_s2_list) and self.MISDict[last_item_s2] > self.MISDict[first_item_s1]\
                and (abs( self.supportOfItem(second_item_s1) - self.supportOfItem(last_item_s2) ) <= self.SDC):
                
                # last_item_s2 is separate element
                if check_last_item_separate_element(s2,last_item_s2):
                    
                    #candidate_list = list()
                    #candidate_list = list(s1)
                    c1.append([last_item_s2])
    
                    candidate_sequence_list.append(c1)
                    
                    # if length and size of s1 and s2 == 2 and MIS last item of s2 > last item s1
                    if length_sequence(s1) == 2 and size_sequence(s1) == 2 and last_item_s2 > last_item_s1:
                        #and self.MISDict[last_item_s2] > self.MISDict[last_item_s1]:
                        
                        # add last_item_s2 to last element of S1
                        #candidate_list = list()
                        last_element_s1 = copy.deepcopy(s1[len(s1) - 1])       #last set       
                        
                        if not last_element_s1.__contains__(last_item_s2):
                            last_element_s1.append(last_item_s2)
                            
                        c2 = s1[:len(s1)-1]                       
                        c2.append(last_element_s1)

                        # add to the final list of all candidates
                        candidate_sequence_list.append(c2)
                
                elif (((length_sequence(s1) == 2 and size_sequence(s1) == 1) and (last_item_s2 > last_item_s1)) or (length_sequence(s1) > 2)):
                    #and (abs( self.supportOfItem(last_item_s2) - self.supportOfItem(second_item_s1) ) <= self.SDC):

                    #candidate_list = list()
                    # get the last element of S1 and add last item of S2 to it to for a candidate sequence
                    last_element_s1 = copy.deepcopy(s1[len(s1) - 1])
                    
                    if not last_element_s1.__contains__(last_item_s2):
                        last_element_s1.append(last_item_s2)

                    c1 = s1[:len(s1)-1]                       
                    c1.append(last_element_s1)
                    
                    # add to the final list of all candidates
                    candidate_sequence_list.append(c1)
        
        #print("C LIST", candidate_sequence_list)        
        return candidate_sequence_list
    
    #=====================================================================================================================================# 
        
    # reverse Join step for MSCandidateGen method         
    def special_join_step_reverse(self,s1,s2,candidate_sequence_list):   
        import copy     
        
        s1_list = convert_list_of_lists_to_one_list(s1)
        
        # have to deep copy because have to remove items from list 
        tmp_s1_list = copy.deepcopy(s1)
        tmp_s2_list = copy.deepcopy(s2)
                
        newSS1 = copy.deepcopy(s1)

        tmp_s1_list,tmp_s2_list,second_item_s1,last_item_s2 = dropItemOperationsInSequences(tmp_s1_list,tmp_s2_list)
        
        # get the last item from original list without pop for later use
        if len(s1_list) > 0:
            last_item_s1 = copy.deepcopy(s1_list[len(s1_list)-1])    
            first_item_s1 = copy.deepcopy(s1_list[0])
        
        if tmp_s1_list is not None and tmp_s2_list is not None and second_item_s1 is not None and \
            last_item_s2 is not None:

            # subsequence obtained by dropping are equal and MIS last s2 > MIS 2nd of s1
            
            if equals_list(tmp_s1_list,tmp_s2_list) and self.MISDict[last_item_s2] > self.MISDict[first_item_s1]\
                and (abs( self.supportOfItem(second_item_s1) - self.supportOfItem(last_item_s2) ) <= self.SDC):

                # last_item_s2 is separate element
                if check_last_item_separate_element(s2,last_item_s2):
                    newSS1.append([last_item_s2])    
                    candidate_sequence_list.append(reverse_list_of_lists_numbers(newSS1))
                    
                    # if length and size of s1 and s2 == 2 and MIS last item of s2 > last item s1
                    if length_sequence(s1) == 2 and size_sequence(s1) == 2 and last_item_s2 < last_item_s1:
                        # add last_item_s2 to last element of S1
                        last_element_s1 = copy.deepcopy(s1[len(s1) - 1])       #last set       
                        
                        if not last_element_s1.__contains__(last_item_s2):
                            last_element_s1.append(last_item_s2)
                            
                        candidate_list = copy.deepcopy(s1[:len(s1)-1])                       
                        candidate_list.append(last_element_s1)

                        # add to the final list of all candidates
                        candidate_sequence_list.append(reverse_list_of_lists_numbers(candidate_list))
                
                elif (((length_sequence(s1) == 2 and size_sequence(s1) == 1) and (last_item_s2 < last_item_s1)) or (length_sequence(s1) > 2)):
                    # get the last element of S1 and add last item of S2 to it to for a candidate sequence
                    last_element_s1 = copy.deepcopy(s1[len(s1) - 1])
                    
                    if not last_element_s1.__contains__(last_item_s2):
                        last_element_s1.append(last_item_s2)

                    c1 = copy.deepcopy(s1[:len(s1)-1])                       
                    c1.append(last_element_s1)
                    
                    # add to the final list of all candidates
                    candidate_sequence_list.append(reverse_list_of_lists_numbers(c1))
      
        return candidate_sequence_list    
    #=====================================================================================================================================#                    

    def check_first_item_s1_min_mis(self,tmp_s1):
        if(len(tmp_s1) > 0):
            temp_list = list()
            # create a temp list with union of all lists including duplicates
            for s1 in tmp_s1:
                temp_list.extend(s1) 
        # get the first item in S1
        first_item = temp_list[0]
        first_item_index = 0
        
        # check if first item in S1 strictly less than every other item in S1
        # if yes return true else return false
        for current_item in temp_list:
            if first_item_index == 0:
                first_item_index = first_item_index + 1
                continue
            else:
                if self.MISDict[first_item] < self.MISDict[current_item]:
                    continue
                else:
                    return False
        # this line is executed only when the loop didn't return false
        return True
    
    def check_last_item_s2_min_mis(self,tmp_s2):
        if(len(tmp_s2) > 0):
            temp_list = list()
            # create a temp list with union of all lists including duplicates
            for s1 in tmp_s2:
                temp_list.extend(s1) 
                
        # get the first item in S1
        last_item = temp_list[len(temp_list)-1]
        current_index = len(temp_list) - 2
        # check if last item in S2 strictly less than every other item in S2
        # if yes return true else return false
        while (current_index >= 0):
            if self.MISDict[last_item] < self.MISDict[temp_list[current_index]]:    
                current_index = current_index - 1
                continue
            else:
                return False
            
        # this line is executed only when the loop didn't return false
        return True


    # MSCandidate generation function
    def MSCandidateGen(self,F): # F = list of list of sets

        candidate_sequence_list = list()
        for s1 in F:
            for s2 in F:
#                 print("s1:",s1)
#                 print("s2:",s2)
                #min_item_s1,min_item_s1_index = self.getIndex_Min_MISValue(s1)
                #min_item_s2,min_item_s2_index = self.getIndex_Min_MISValue(s2)
    
                # case: min item in S1 is in 1st index
                if self.check_first_item_s1_min_mis(s1):
#                     print("case-1")
                    candidate_sequence_list = self.special_join_step(s1,s2,candidate_sequence_list)
                
                # case: min item in S2 is in last index
                elif self.check_last_item_s2_min_mis(s2):
#                     print("case-2")
                    candidate_sequence_list = self.special_join_step_reverse(reverse_list_of_lists_numbers(s2),reverse_list_of_lists_numbers(s1),candidate_sequence_list)
                    reverse_list_of_lists_numbers(s1)
                    
                # case: normal join step
                else:
#                     print("normal join")
                    candidate_sequence_list = self.normal_join_step(s1,s2,candidate_sequence_list)
#                 print()
        # remove empty lists if present
        candidate_sequence_list = [x for x in candidate_sequence_list if x != []]

        #prune step
        for c_k in candidate_sequence_list:
            #print("c_k:",c_k)
            self.prune(c_k,F)
                
        return candidate_sequence_list
    
    #=====================================================================================================================================#   
    
    # Normal sequence join step
    # subsequence obtained by dropping the 2nd item of S1 and last item of S2 are same 
    def normal_join_step(self,s1,s2,candidate_sequence_list):
        import copy     

        # have to deep copy because have to remove items from list 
        tmp_s1_list = copy.deepcopy(s1)
        tmp_s2_list = copy.deepcopy(s2)
        
        tmp_s1_list,tmp_s2_list,first_item_s1,last_item_s2 = dropItemOperationsInSequencesNormalJoin(tmp_s1_list,tmp_s2_list)

        if tmp_s1_list is not None and tmp_s2_list  is not None and equals_list(tmp_s1_list,tmp_s2_list) \
            and (abs( self.supportOfItem(first_item_s1) - self.supportOfItem(last_item_s2) ) <= self.SDC):
            # s1 extended with last item of s2 as separate element
            candidate = list()
            if check_last_item_separate_element(s2, last_item_s2):
                candidate = copy.deepcopy(s1)
                candidate.append([last_item_s2])
                candidate_sequence_list.append(candidate)
            # s1 extended with last item of s2 as part of the last element of s1
            else:
                last_element_s1 = copy.deepcopy(s1[len(s1) - 1]) 
                if not last_element_s1.__contains__(last_item_s2):
                    last_element_s1.append(copy.deepcopy(last_item_s2))     
                candidate_list = copy.deepcopy(s1[:len(s1)-1])                       
                candidate_list.append(last_element_s1)
                candidate_sequence_list.append(candidate_list)

        return candidate_sequence_list
    #=====================================================================================================================================#   
    
    # Method to compute item support using support_count_dicitonary
    def supportOfItem(self,item):
        return (self.support_count_dict[item]/transaction_count)
    
    #=====================================================================================================================================#   
    def prune(self,C_k,FkMinus1):
        item_with_min_MIS, index = self.getIndex_Min_MISValue(C_k)
        subsets = find_k_1_subsets(C_k)
        finalCandidateSequenceList = list()
        for subset in subsets:
            #print("subset:",subset)
            if( check_presence_of_min_item(subset,item_with_min_MIS) == True):
                #Need to check if this subset has a support >= support of min item      
                # check if subset is present in FkMinus1
                tmp_ret_list = [x for x in subset if FkMinus1.__contains__(x)]
                if len(tmp_ret_list) == 0:
                    continue
                else:
                    finalCandidateSequenceList.append(subset)
            else:
                pass

    # Given a list, return the index of item with min MIS value
    def getIndex_Min_MISValue(self,itemList):
        if(len(itemList) > 0):
            temp_list = list()
            # create a temp list with union of all lists including duplicates
            for s1 in itemList:
                temp_list.extend(s1)        
    
            min_mis_item = temp_list[0]  # first item in list
            for item in temp_list :
                mis = self.MISDict[item]
                if mis < self.MISDict[min_mis_item]:
                    min_mis_item = item
            return min_mis_item,temp_list.index(min_mis_item)   # return item with min MIS and its index
                
    #=====================================================================================================================================#          
    
    # MS-GSP algorithm    
    def MSGSP(self,sequenceInputFile,MISInputFile):
        import time
        start_time = time.time()
        
        #Process input files
        global L,CANDIDATE_COUNT_DICT, transaction_count
        file_path = self.FILE_PATH + 'Final_Output.txt'
        f1 = open (file_path, 'w')
        
        import copy
        sequenceList = self.preprocessInputFile(sequenceInputFile, MISInputFile)
        print("Pre-processing input files completed...")
        input_sequence = self.createListOfSets(sequenceList)
        L = self.initPass(sequenceList)
        print("L:",L)
        self.write_to_file(L, "L")
        print("Init Pass completed...")
        F1 = self.generate_F1(L)
        self.write_to_file(F1, "Frequent-1-Itemset")
        print("Frequent-1-Itemset generated...")             
        self.FREQUENT_ITEMSET_DICT[1] = F1
        F = F1

        # writing Frequent 1 itemset details to file
        f1.write("The number of length {0} sequential patterns is {1}".format(1,len(F)))
        f1.write("\n")
        for tmp in F:
            tmp_F = [list(x) for x in tmp]
            for itm in tmp_F:
                f1.write("Pattern: {0} Count: {1}".format(str(itm),self.support_count_dict[itm[0]]))
                f1.write("\n")
        f1.write("\n")
        
        k = 2
        frequent_itemset_count = 2
        while(F != None and len(F)>0):
            if k == 2:
                C = self.level2_candidate_gen(L)
                self.write_to_file(C, "Candidate_List_C2")
            else:
                C = self.MSCandidateGen(F)
                self.write_to_file(C, "Candidate_List_C"+str(frequent_itemset_count))
                  
            for c in C:
                str_candidate = repr(c).strip()    
                self.CANDIDATE_COUNT_DICT[str_candidate] = 0
                  
            for transaction_sequence in input_sequence:
                tmp_transaction_sequence = copy.deepcopy(transaction_sequence)
                for candidate in C:
                    tmp_candidate_sequence = copy.deepcopy(candidate)
                    str_candidate = repr(candidate).strip()                             # convert candidate (list of sets) to string
                    if ts_contains(tmp_transaction_sequence, tmp_candidate_sequence):
                        self.CANDIDATE_COUNT_DICT[str_candidate] = self.CANDIDATE_COUNT_DICT[str_candidate] + 1   # increment candidate count
                    tmp_transaction_sequence = copy.deepcopy(transaction_sequence)
                    tmp_candidate_sequence = copy.deepcopy(candidate)
            Fk = list()
            for candidate in C:
                str_candidate = repr(candidate)
                #print("candidate:",candidate)
                min_item_candidate,min_item_index = self.getIndex_Min_MISValue(candidate)
                #print("min candidate and its position:",min_item_candidate,min_item_index)
                #print("transaction count:",transaction_count)
                #print("CANDIDATE_COUNT_DICT for str_candidate:",self.CANDIDATE_COUNT_DICT[str_candidate])
                #print("MISDict[min_item_candidate]:",self.MISDict[min_item_candidate])
                #print()
                if float(self.CANDIDATE_COUNT_DICT[str_candidate]/transaction_count) >= float(self.MISDict[min_item_candidate]):
                    Fk.append(candidate)
            
            # writing Frequent k itemset details to file
            f1.write("The number of length {0} sequential patterns is {1}".format(frequent_itemset_count,len(Fk)))
            f1.write("\n")
            for itm in Fk:      
                f1.write("Pattern: {0} Count: {1}".format(itm,self.CANDIDATE_COUNT_DICT[repr(itm)]))
                f1.write("\n")
            f1.write("\n")
                    
            print("F{0} - {1}".format(frequent_itemset_count,Fk))
            if len(Fk) > 0:
                self.FREQUENT_ITEMSET_DICT[frequent_itemset_count] = Fk
            print("Frequent-{0}-Itemset generated...".format(frequent_itemset_count))  
            self.write_to_file(Fk, "Frequent-"+str(frequent_itemset_count)+"-Itemset")
            k = k + 1
            frequent_itemset_count = frequent_itemset_count + 1
            F = Fk
            
        print("\nFINAL FREQUENT ITEMSETS")
        print(self.FREQUENT_ITEMSET_DICT)

        f1.close()
        
        print ("Execution time : {0} seconds".format(time.time() - start_time))
          
#=====================================================================================================================================#           

# Call the main method
# if __name__ == '__main__':  MSGSP().MSGSP("test-data/large-data-2/data2.txt", "test-data/large-data-2/para2-1.txt")
# if __name__ == '__main__':  MSGSP().MSGSP("test-data/large-data-2/data2.txt", "test-data/large-data-2/para2-2.txt")
# if __name__ == '__main__':  MSGSP().MSGSP("test-data/small-data-1/data-1.txt", "test-data/small-data-1/para1-1.txt")
if __name__ == '__main__':  MSGSP().MSGSP("test-data/data-1.txt", "test-data/para1-1.txt")