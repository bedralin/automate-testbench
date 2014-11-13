#!/usr/bin/env python
'''
This script is a database utility for IDLab.
'''

import datetime
import time
import os
import psycopg2
import logging
import csv

__author__ = "Bronson Edralin"
__copyright__ = "Copyright 2014 Instrumentation Development Laboratory (IDLab), Department of Physics, University of Hawaii at Manoa"
__credits__ = ["Christian A. Damo", "Reed Shinsato"]
__version__ = "0.01"
__maintainer__ = "Bronson Edralin"
__email__ = "bedralin@hawaii.edu"
__status__ = "Prototype"

DEBUG=False # NOT NECESSARY because error is printed in HVB_ASSEMBLY_log file
	   # setting DEBUG=True will print error to screen.

if DEBUG:
    print "Entering DEBUG Mode...\n"

logging.basicConfig(filename='HVB_ASSEMBLY_log',level=logging.DEBUG,format='%(asctime)s %(message)s')

class DatabaseUtility:
    '''
    This is a package for interfacing with the postgres database
    through the python. This is basically an API that controls actions
    done to the database utilizing the psycopg2 package.
    '''
    def __init__(self,host='192.168.153.108',dbname='mydb',user='bronson',password='pass123'):

	#ssh bronson@193.168.153.108 -L 5432:localhost:5432 -p hunt123
	
	DatabaseInfo = 'host='+'127.0.0.1'+ ' port=5000'+' dbname='+dbname+' user='+user+' password='+password
	print "Connecting to database\n ->%s\n"%(DatabaseInfo)
	self.conn = psycopg2.connect(DatabaseInfo)
	self.cur = self.conn.cursor()

    def insert_data_into_database(self, insertFilename, tableName):
	'''
	given: a file name of a csv file and a table name in string form
	return: nothing, but inputs the dta into a psql database on the
	        local comuter into the specified table name
	'''
	#setup the csv reader object
	insertFile = open(insertFilename,'r')
	reader = csv.reader(insertFile)
	#start a counter to keep track of how many errors occurred
	error = 0
	print "Inserting data into the "+tableName+" now ..."
	
	#this block of code feeds into the database one entry at a time
	#if there is an error during insertion eg, violates primary key
	#constraints, then it counts the error and outputs it to the 
	#user.
	for row in reader:
	    if (row[0]!="Purpose"):
		try:
		    #keeps a savepoint so that in the event there
		    #is an error, then it will roll back in the 
		    #exception block of code
		    self.cur.execute("BEGIN;")
		    self.cur.execute("SAVEPOINT my_savepoint;")
		    #create the command name here
		    sql = "INSERT INTO "+tableName+" (DateTime,BoardID,"+\
		    "BoardName,Channel,ISEG_V,LoadRelay1,LoadRelay2,K,"+\
		    "MCPAT,MCPAB,MCPBT,MCPBB,Result_V) VALUES ('"+row[1]\
		    +"','"+row[2]+"','"+row[3]+"',"+row[4]+","+row[5]+\
		    ","+row[6]+","+row[7]+","+row[8]+","+row[9]+\
		    ","+row[10]+","+row[11]+","+row[12]+","+row[13]+\
		    ");"
		    #this executes the command stored in sql
		    #it acts like you just typed the command line
		    #at the psql prompt
		    self.cur.execute(sql)
		    #this commits the command in the psql
		    #similar to hitting enter
		    self.conn.commit()
		    #time.sleep(0.2)
		except Exception, e:
		    self.cur.execute("ROLLBACK TO SAVEPOINT my_savepoint;")
		    logging.warning('Did not insert data into table "'+tableName+\
		    '"\n'+'\tError occured: '+str(e)+'\t'+str(row[1])+","+\
		    str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+\
		    ","+str(row[6])+","+str(row[7])+","+str(row[8])+","+str(row[9])\
		    +","+str(row[10])+","+str(row[11])+","+str(row[12])+","+\
		    str(row[13])+"\n")
		    if DEBUG:
			print 'Did not insert data into table "'+tableName+\
			'"\n'+'\tError occured: %s',e
		    #keeps record of how many errors occured
		    error = error + 1
	#output to the user stating at what time the insertion
	#finished and how many errors there were
        print "\nAt "+str(datetime.datetime.now())+", "+str(error)+" error(s) occured."
        print "\t-> Please refer to 'HVB_ASSEMBLY_log' file for more information.\n"
	insertFile.close()

    def create_table(self,tableName):
	'''
	given: a string
	return: nothing but creates a table in the psql database with
	       the string as the name
	'''
	#this checks to see if the table already exists in the database
	#if the specified table name exists then it ends the method
	#with a return of 1
	error=0
	if self.check_table_exists(tableName) == True:
	    return 1
	    
	try:
	    #otherwise the program creates the command string
	    sql = 'CREATE TABLE '+tableName+'( DateTime timestamp with '+\
		'time zone NOT NULL, BoardID character varying NOT NULL, BoardName '+\
		'character varying NOT NULL, Channel integer NOT NULL, ISEG_V '\
		'integer NOT NULL, LoadRelay1 integer NOT NULL, LoadRelay2 integer '\
		'NOT NULL, K integer NOT NULL, MCPAT integer NOT NULL, MCPAB '+\
		'integer NOT NULL, MCPBT integer NOT NULL, MCPBB integer NOT NULL, '\
		+'Result_V double precision, CONSTRAINT '+tableName+'_prim_key '+\
		'PRIMARY KEY (DateTime, BoardID, BoardName, Channel,ISEG_V,LoadRelay1'+\
		',LoadRelay2,K,MCPAT,MCPAB,MCPBT,MCPBB,Result_V)) WITH( OIDS=FALSE);'	    
	    #types it out at the psql prompt
	    self.cur.execute(sql)
	    #then hits enter to commit the command
	    self.conn.commit()
	    #We then change the owner of the table to postgres
	    #for security purposes, most likely it defaults to
	    #postgres, but this is just to make sure
	    sql = 'ALTER TABLE '+tableName+' OWNER TO postgres;'
	    #again execute is as if you're typing thte command at
	    #the psql prompt
	    self.cur.execute(sql)
	    #commits it as if you're hitting enter at the end of
	    #the command
	    self.conn.commit()
	    print 'Successfully inserted table '+tableName
	except Exception, e:
	    #in the event there's some error with the above code
	    #the software will notify the user that it failed
            logging.warning('Did not create table "'+tableName+'"\n'+'\tError occured: %s',e)
	    if DEBUG:
		print 'Did not create table "'+tableName+'"\n'+'\tError occured: %s',e 
	    error+=1
	
	print "\nAt "+str(datetime.datetime.now())+", "+str(error)+" error(s) occured."
	print "\t-> Please refer to 'HVB_ASSEMBLY_log' file for more information.\n"

    def close_conn(self):
	'''
	given: nothing
	return: nothing but closes the connection, this is just for good
	house keeping practice
	'''
	self.conn.close()

    def check_table_exists(self,tableName):
	'''
	given: a string of the name of the table desired
	return: a True or False to say if the specified table name
	       does indeed exist
	'''
	#queries the database to see if the table is within the list
	#of tables that's in the database's schema
	self.cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (tableName,))
	#return True or False if the specified table name exists or not
	true_or_false=False
	if self.cur.fetchone()[0]==1:
	    self.cur.close()
	    true_or_false=True
	if true_or_false==True:
	    print 'Table "'+tableName+'" already exists...'
	return true_or_false

