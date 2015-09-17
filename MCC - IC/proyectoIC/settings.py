import os

#Importar librerias para coneccion de la base de datos
import psycopg2
import sys

#global algorithms_selected
#global slices
#global traces
#global results
#global cache_hitrate_gnu
#global name_cache_hitrate_gnu
#global cache_request_gnu
#global name_cache_request_gnu
#global num_lines
#global shuffle_array


if not os.path.exists('results'):
    os.makedirs('results')

if not os.path.exists('graphics'):
    os.makedirs('graphics')
  
data = os.getcwd()+'/data/'
results = os.getcwd()+'/results/'
graphics = os.getcwd()+'/graphics/'

path = os.getcwd()
#algorithms_selected = ["LRU", "RANDOM", "RANDOM_LRU_3", "S4LRU"]
#slices = [1]
#cache_hitrate_gnu = graphics+'/cache_hitrate.gnu'
#name_cache_hitrate_gnu = 'cache_hitrate.gnu'
#
#cache_request_gnu = graphics+'/cache_request.gnu'
#name_cache_request_gnu = 'cache_request.gnu'
#cache_hitrate_slices_gnu = graphics+'cache_hitrate_slices_'
#
#num_lines = 0
#shuffle_array = []
#dic_temporality = dict()

##Define our connection string
#conn_string = "host='200.126.23.101' dbname='SOA' user='postgres' password='postgrados@db'"
## print the connection string we will use to connect
#print "Connecting to database\n	->%s" % (conn_string)
## get a connection, if a connect cannot be made an exception will be raised here
#conn = psycopg2.connect(conn_string)
## conn.cursor will return a cursor object, you can use this cursor to perform queries
#cursor = conn.cursor()
#print "Connected!\n"
