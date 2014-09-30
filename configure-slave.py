#!/usr/bin/python
import os
import sys
import random, string

import MySQLdb

def getenv(name, default=None, required=True):
   """Get an envaironment variable.

      Args:
      name: Name of the variable
      default: default value if the variable is not set
      required: True to report an error if the variable is not set
   """
   res = os.getenv(name, default)
   if required and not res:
      print "Required envaironment variable not found: %s" % name
      sys.exit(-1)
   return res

def randomword(length):
   """Generate a random string with the specified length"""
   return ''.join(random.choice(string.lowercase) for i in range(length))

def databaseConnection(host, user, passwd):
   """Connect to a mysql databas and returns the connection"""
   try:
      return MySQLdb.connect(host=host, 
                     user=user, 
                      passwd=passwd, 
                      db="mysql") 
   except Exception as inst:
      print "Unable to connect to host '%s' with user '%s': %s" % (host, user, inst)
      sys.exit(-1)

def userExists(db, username):
   """Check if a mysql user exists

      Args:  
      db: database connection
      username: username to Check
      returns: True if the user exists
   """
   cur = db.cursor()
   cur.execute('SELECT count(*) c from user where User = %s', [username])
   res = cur.fetchall()
   cur.close()
   return res[0][0] > 0

def sanitize(string):
   """Exit if the given string contains any special character"""
   scaped_str = filter(str.isalnum, string)
   if scaped_str != string:
      print "Use only alnum characters: '%s'" % string
      sys.exit(-1)


def createReplicationUser(db, username, password):
   """Create a mysql user for replication purposes"""
   if userExists(db, username):
      print "User already exists: '%s'" % username
      sys.exit(-1)
   try:
      db.query("CREATE USER '%s'@'%%' IDENTIFIED BY '%s'" % (username, password))
   except Exception as inst:
      print "Unable to create user '%s': %s" %(username, inst)
      sys.exit(-1)
   repl_password = randomword(10)
   try:
      db.query("GRANT REPLICATION SLAVE ON *.* TO '%s'@'%%' IDENTIFIED BY '%s'" % (username, repl_password))
   except Exception as inst:
      print "Unable setting privileges to user '%s': %s" %(username, inst)
      sys.exit(-1)
   return repl_password

def dumpDb(host, username, password, database, output):
   """Dump a database to a file"""
   exitCode = os.system("mysqldump -u %s -p%s -h %s --skip-lock-tables --single-transaction --flush-logs --hex-blob --master-data=1 %s > %s" %
      (username, password, host, database, output))
   if exitCode != 0:
      print "Unable to export master database: %s" % exitCode
      sys.exit(-1)

slave_id = getenv("SLAVE_ID")
database = getenv("DATABASE")

master_ip = getenv('MASTER_IP')
master_user = getenv('MASTER_USER')
master_password = getenv('MASTER_PASSWORD')
#db = databaseConnection(master_ip, master_user, master_password)

#createReplicationUser(db, sanitize("user_1"), sanitize("pass1"))
dumpFile = "/tmp/dump_%s.sql" % slave_id
dumpDb(master_ip, master_user, master_password, database, dumpFile)
