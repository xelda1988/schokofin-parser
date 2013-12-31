#Program to parse a schokofin-protocol and export as CSV
#"Geld" as a function of time and with an ID as first entry

#author: Alexander Rietzler
#version: 0.1 - 17.12.2013
#contact: alexander.rietzler at gmail.com (at=@)

import os
import string
import csv

#input directory path, read directory name and save as ID-string:

parse_directory_path= "Beispieldaten/"
id_string_all = os.listdir(parse_directory_path)

def scale_trans(x, translcoeff, scalecoeff):
    y=(x - translcoeff)/scalecoeff
    return y
	
def database_from_dirpath(protocol_dir):
  
  #create list of saldofiles filedirectory  
    
  saldofiles_path =  os.listdir(protocol_dir)
  saldofiles_filtered_path = []
  filename_part = "Saldo"
  for x in saldofiles_path:
      if filename_part in x:
	  #print x
	  saldofiles_filtered_path.append(x)
	  
  #filter all files with Saldo in it and sort by creation time

  creation_time=[]
  timeinfo_list = []

  #get timeinfo of files
  for i in range(0,len(saldofiles_filtered_path)):
      fileinfo = os.stat(protocol_dir+'/'+saldofiles_filtered_path[i])
      #print fileinfo[8] # last access time
      timeinfo_list.append( fileinfo[8] )

  # creat list of list to sort by timeinfo
  data = [saldofiles_filtered_path, timeinfo_list]
  data = zip(*data)
  #print data
  data.sort(key=lambda tup: tup[1])  # sorts in place
  data = map(list, zip(*data))

  #print data[0]

  saldofiles_path_sorted = data[0]
  timelist_sorted = data[1]

  #time is in absolute time, translate by minimum (could be second??) = starttime and scale to minutes

      
  out = map (lambda x: scale_trans(x, min(timelist_sorted),60) , timelist_sorted)

  print "SORTED TIMES FOR CURRENT SUBDIRECTORY (MINUTES)"
  for x in out:
    print x
    
  

  #get money for each file and save to money list
  money_list=[]

  for path in saldofiles_path_sorted:
    f = open(protocol_dir+'/'+path)
    money_list.append( float(f.readlines()[7])/1000 ) #the 7.th line contains the "Geld"
    
  #print money_list

  #create database from csv
  
  print "SORTED 'KAPITAL' FOR CURRENT SUBDIRECTORY (TSD. EURO)"
  for x in money_list:
    print x
    
  money_strlist = []
  for item in money_list:
      money_strlist.append(str(item))


  database = list(money_strlist)
  database_time = list(out)
  database.insert(0, protocol_dir[len(parse_directory_path):]+'_money')
  database_time.insert(0, protocol_dir[len(parse_directory_path):]+'_time')
  database = [database, database_time]

  #print database
  
  return database

#write lists to csv


print "SUBDIRECTORY LIST:",id_string_all
with open('money_database.csv', 'wb') as csvfile:
      money_db = csv.writer(csvfile, delimiter=' ',
			      quotechar='|', quoting=csv.QUOTE_MINIMAL)
      for subdir_path in id_string_all:
	print "CURRENT SUBDIRECTORY PATH:",subdir_path
	database=(database_from_dirpath(parse_directory_path+subdir_path))
	#database = zip(*database)
	#print database
	for datarow in database:
	   money_db.writerow(datarow)

print "\nmoney_database.csv successfully created"   
print "DONE!"
