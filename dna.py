from sys import argv
import csv
import time

def get_crime_data(file):
  """
  With the file name passed via ARGV, this function will return a dictionary of crime record data.
  """
  with open(file,newline='') as original:
    csvOriginal = csv.DictReader(original, dialect = 'excel')
    return(list(csvOriginal))


def get_sus_data(file):
  """
  With the file name passed via ARGV, this function will return a dictionary of suspect data.
  """
  with open(file,newline='') as original:
    csvOriginal = csv.DictReader(original, dialect = 'excel')
    return(list(csvOriginal))


def get_str(crime):
  """ 
  Given a single crime dictionary, the function will return the list of all the required STR to be checked.
  """
  a=list(crime.keys())
  return a[1:]

def check_crime(crime_data,suspect):
  """
  Given a dictionary containing crime STR information and a suspect's STR count in a list, function will return true if it matches
  """
  temp= list(crime_data.values()) # Holds the value from the dictionary temporarily
  crime_str_count = []
  
  for i in temp[1:]:
    crime_str_count.append(int(i))

  if crime_str_count==suspect:
    crime_ID = crime_data['CrimeID'] 
    return crime_ID
  return ''

def process_suspect(crime,g_seq):
  """
  Given a list of dictionaries containing crime data and a list of STR count for a particular suspect, function will return a string of matching crimes.
  """
  crime_list = ''
  matched_crimeID=''  
  for i in crime:
    matched_crimeID = check_crime(i,g_seq)
    if len(matched_crimeID)>0:
      if len(crime_list)>0:
        crime_list = crime_list + ',' + matched_crimeID
      else:
        crime_list = crime_list + matched_crimeID
  return crime_list




def get_count(suspect,str):
  """
  Given the Genetic sequence of a suspect and the list of STR, this function will return a list of count of each STR that has the longest occurnace in a continous chain.
  """
  count = 0
  temp_count = 0
  start_p = 0 # This variable stores the location of the starting point of the test substring that will be sliced from the original sequence string
  str_count = []
  
  for s in str:
    str_l = len(s) #Holds the lenght of the STR
    while (len(suspect)-start_p)>= str_l:
      if suspect[start_p:start_p+str_l]==s:
        temp_count += 1
        start_p += str_l
      else:
        if count < temp_count:
          count = temp_count
        temp_count=0
        start_p += 1
    str_count.append(count)
    count = 0
    temp_count = 0
    start_p = 0
  return str_count

def handle_suspects(crime,suspects):
  """
  Given the Crime and Suspects data base, both passed as a list of dictionary, the function will return a list of dictionary, where each dictionary contains the name of the suspect and the Crime ID for which their DNC STR count matched.
  """
  fnl_list = []
  str_count = []
  guilty_cases = []

  strs = get_str(crime[0])

  for i in suspects:
    str_count = get_count(i['Sequence'],strs)
    guilty_cases = process_suspect(crime,str_count)
    fnl_list.append({'Suspect':i['Suspect'],'Crimes':guilty_cases})
  return fnl_list
    
def end_writer(file,final_crimes):
  """
  Given a file passed via ARGV and a list of dictionaries containing suspects with a string of crimes where DNA matched, this function will write a file as the output for the final program.
  """

  header_key_words = list(final_crimes[0].keys()) #This variable holds the header key words for the file to be written.
  with open(file, 'w', newline='') as newFile:
    csvNew = csv.DictWriter(newFile, header_key_words , dialect = 'excel')
    csvNew.writeheader()
    csvNew.writerows(final_crimes)


def run():
  """
  This function joins all the helper functions together to produce the required output csv file.
  """
  #This function call reads the crime database CSV file
  crime_cases = get_crime_data(argv[1])

  #This function call reads the suspect database CSV file
  genetic_data_of_suspects = get_sus_data(argv[2])
  
  #This function call processes the two lists of dictionaries to produce a final list of dictionaries to be sent for writting
  processed_suspects_data = handle_suspects(crime_cases,genetic_data_of_suspects)

  #This function call writes the output list of dictionaries to a CSV file
  end_writer(argv[3],processed_suspects_data)






if __name__ == "__main__":
  start = time.perf_counter()
  run()
  end = time.perf_counter()
  print(f"Time used: {end-start} seconds")
