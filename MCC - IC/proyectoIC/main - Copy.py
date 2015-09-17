#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import sys
import nltk
import random
import codecs

from StringIO import StringIO
from xml.dom import minidom
from xml.dom.minidom import Node
from random import shuffle
from lxml import etree
from settings import *



def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    print "Wordlist:"
    print wordlist
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    print "Features:"
    print features
    return features

def load_function():
    try:
        from lxml import etree
        print("running with lxml.etree")
    except ImportError:
        try:        
            import xml.etree.cElementTree as etree
            print("running with cElementTree on Python 2.5+")
        except ImportError:
            try:              
              import xml.etree.ElementTree as etree
              print("running with ElementTree on Python 2.5+")
            except ImportError:
                try:        
                    import cElementTree as etree
                    print("running with cElementTree")
                except ImportError:
                    try:          
                        import elementtree.ElementTree as etree
                        print("running with ElementTree")
                    except ImportError:
                        print("Failed to import ElementTree from any known place")
  
       
def parseBookXML():
    for x in os.listdir(data):        
        f = open(data+str(x))
        xml = f.read()
        f.close() 
        tree = etree.parse(StringIO(xml))
        #print tree.docinfo.doctype
        context = etree.iterparse(StringIO(xml))
        book_dict = {}
        books = []
        
        for action, elem in context:
            print action
            if not elem.text:
                text = "None"
            else:
                text = elem.text
            print elem.tag + " => " + text
            book_dict[elem.tag] = text
            if elem.tag == "tweet":
                books.append(book_dict)
                book_dict = {}
    return books

def read_xml_file_tweet():    
    for x in os.listdir(data):        
        f = open(data+str(x),"r")        
        lines = f.readlines()
        n_lineas = sum(1 for line in lines) #obtiene el número de líneas del archivo
        #print n_lineas
        f.close()
        tree = etree.parse(data+str(x))
        root = tree.getroot()        
        #for child in root:
        #    print(child.tag, child.attrib)
        #    for sentiment in child.iter('sentiment'):
        #        print sentiment.attrib
        #        for polarity in sentiment.attrib:
        #            print polarity
            #for neighbor in sentiment.findall(".//sentiment[1]"):
            #    print neighbor.get('polarity')
        for country in root.findall('tweet'):
            id_tweet = country.get('id')
            sentiment = country.find('sentiment').text
            #polarity = sentiment.get('polarity')
            print id_tweet, sentiment

def first_words(input, words):
    for i in range(0, len(input)):
        # Count spaces in the string.
        if input[i] == ' ':
            words -= 1
        if words == 0:
            # Return the slice up to this point.
            return input[0:i]
    return ""

def read_xml_tweet():    
    for x in os.listdir(data):
        #f = codecs.open(data+str(x),'r','utf-8')    
        #lines = f.readlines()        
        #n_lineas = sum(1 for line in lines) #obtiene el número de líneas del archivo        
        #f.close()
        #contador = 0
        #for line in lines:            
        #    if contador > 1:            
        #        description = line.replace("\n", "").lower()
        #        #print first_words(description,2)
        #        print description.split("<sentiment")
        #        #tweet = "<?xml version='1.0' encoding='UTF-8'?>" + description
        #    contador += 1
        file_result = open(path + "/sentiment_tweets.xml","wb")
        f = open(data+str(x),'r')
        lines = f.read()
        
        tweet = "<?xml version='1.0' encoding='UTF-8'?>\n<tweets>\n"
        contador = 1
        doc = minidom.parseString(lines)        
        for topic in doc.getElementsByTagName('tweet'):
            id_tweet = topic.getAttribute("id")            
            tweet = tweet + "<tweet id='" + str(id_tweet) + "'>"
            print topic.firstChild.nodeValue            
            #if topic.firstChild.nodeValue != None:
            #    tweet = topic.firstChild.nodeValue                            
            #title= topic.getElementsByTagName('sentiment')[i].firstChild.nodeValue            
            for subnode in topic.childNodes:
                if subnode.nodeType == Node.ELEMENT_NODE and subnode.tagName == "sentiment":
                    print subnode.firstChild.nodeValue
                    tweet = tweet + "<sentiment contador='" + str(contador) + "'>" + str(subnode.firstChild.nodeValue.encode("utf-8")) + "</sentiment>"                    
                    topic.removeChild(subnode)
                    contador += 1
            contador = 1
            tweet = tweet + "</tweet>\n"
        tweet = tweet + "</tweets>\n"
        file_result.write(tweet)
            #for sentiment in topic.getElementsByTagName('sentiment'):
            #    polarity = sentiment.getAttribute("polarity")
            #    print sentiment.firstChild.nodeValue                           
        file_result.close()    
        #tweet = "asadadadsa tt sla tt lkjdakjsakdjaskld"
        #print tweet.split("tt")

def get_xml_tweet():    
    for x in os.listdir(data):        
        file_result = open(path + "/sentiment_tweets.xml","wb")
        f = open(data+str(x),'r')
        lines = f.read()        
        tweet = "<?xml version='1.0' encoding='UTF-8'?>\n<tweets>\n"
        contador = 1
        doc = minidom.parseString(lines)        
        for topic in doc.getElementsByTagName('tweet'):
            id_tweet = topic.getAttribute("id")            
            tweet = tweet + "<tweet id='" + str(id_tweet) + "'>"
            print topic.firstChild.nodeValue                           
            for subnode in topic.childNodes:
                if subnode.nodeType == Node.ELEMENT_NODE and subnode.tagName == "sentiment":
                    out = subnode.firstChild.nodeValue.replace( '-', '').encode("utf-8")
                    #out = out.replace( u'\u201c', u'"') #.replace( u'\xed', u',').replace( u'\u201c', u'"')                    
                    print out
                    #print out.encode('ascii')
                    #print subnode.firstChild.nodeValue 
                    #tweet = tweet + "<sentiment polarity='" + str(subnode.getAttribute("polarity")) + "' contador='" + str(contador) + "'>" + str(subnode.firstChild.nodeValue.encode("utf-8")) + "</sentiment>"                                        
                    #hnode = doc.createElement("analysis_sentiment")
                    #hnode.setAttribute("contador", str(contador))
                    #htext = doc.createTextNode('')
                    #hnode.appendChild(htext)
                    #topic.insertBefore(hnode,subnode)
                    #topic.removeChild(subnode)
                    #contador += 1
            contador = 1         
            tweet = tweet + "</tweet>\n"
        #print doc.toprettyxml()
        tweet = tweet + "</tweets>\n"
        file_result.write(tweet)
        file_result.close()    
            
def load_xml_file_tweet():    
    for x in os.listdir(data):        
        f = open(data+str(x),"r")        
        lines = f.readlines()
        n_lineas = sum(1 for line in lines) #obtiene el número de líneas del archivo
        #print n_lineas
        f.close()
        tree = etree.parse(data+str(x))
        root = tree.getroot()
        print root
        for child in root:
            print(child.tag, child.attrib, child.text)
 

if __name__ == "__main__":    
    
    print 'Preprocesamiento de datos'       
    get_xml_tweet()
    print '\201c'
    print '\xed'
    
    #pos_tweets = [('Yo amo este carro', 'positivo'),
    #              ('Esta vista es increíble', 'positivo'),
    #              ('Me siento bien esta mañana', 'positivo'),
    #              ('Estoy tan emocionada sobre el concierto', 'positivo'),
    #              ('El es mi mejor amigo', 'positivo')]
    #
    #                          
    #neg_tweets = [('No me gusta este carro', 'negativo'),
    #              ('El paisaje es horrible', 'negativo'),
    #              ('Amanecí cansada el día de hoy', 'negativo'),
    #              ('No estoy emocionada sobre el concierto', 'negativo'),
    #              ('El es mi enemigo', 'negativo')]
    #
    #tweets = []
    #for (words, sentiment) in pos_tweets + neg_tweets:
    #    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    #    tweets.append((words_filtered, sentiment))
    #
    ##print tweets
    #word_features = get_word_features(get_words_in_tweets(tweets))
    #print "word_features: "
    #print word_features
    #
    #training_set = nltk.classify.apply_features(extract_features, tweets)
    #print "training_set: "
    #print training_set
    
    
##Elimina las direcciones de los traces de wikipedia, asignándoles un id único a cada una.
##Esta función sólo debe ejecutarse una vez.
#def transform_wikipedia_traces(character, position):
#    dic_temporality.clear() 
#    contador = 1    
#    n_lineas = 0    
#    trace_complete = []    
#    
#    for x in os.listdir(traces):  #recorre la lista de los archivos de traces
#        numero_archivo = 1
#        f = open(traces+x, "r")
#        lines = f.readlines()
#        n_lineas = sum(1 for line in lines) #obtiene el número de líneas del archivo
#        f.close()
#        file_result = open(traces+x, "w")
#       
#        for line in lines:        
#            if character != None:
#                key = line.replace("\n", "").lstrip().split(" ")[position].split(character)[1]
#            else:
#                key = line.replace("\n", "").lstrip().split(" ")[position]
#                   
#            if not(dic_temporality.has_key(key)):
#                dic_temporality[key] = {'valor':contador, 'columna_uno': line.replace("\n", "").lstrip().split(" ")[0] , 'columna_dos':line.replace("\n", "").lstrip().split(" ")[1]}
#                if (numero_archivo == n_lineas):
#                    file_result.write(str(line.replace("\n", "").lstrip().split(" ")[0]) + " " + str(line.replace("\n", "").lstrip().split(" ")[1]) + " " + str(contador))
#                else:
#                    file_result.write(str(line.replace("\n", "").lstrip().split(" ")[0]) + " " + str(line.replace("\n", "").lstrip().split(" ")[1]) + " " + str(contador) + "\n")
#                contador +=1
#            else:
#                if (numero_archivo == n_lineas):
#                    file_result.write(str(dic_temporality.get(key)['columna_uno']) + " " + str(dic_temporality.get(key)['columna_dos']) + " " + str(dic_temporality.get(key)['valor']))
#                else:
#                    file_result.write(str(dic_temporality.get(key)['columna_uno']) + " " + str(dic_temporality.get(key)['columna_dos']) + " " + str(dic_temporality.get(key)['valor']) + "\n")
#            numero_archivo += 1
#        file_result.close()
#        print " proceso archivo:" + str(traces+x)
#        
#    
#       
#
##Permite leer cualquier trace, recibe la posición donde está el id y un caracter en caso de que el id esté
##compuesto por uno, caso contrario recibe None
#def inicialize_traces(character, position):
#    dic_temporality.clear() 
#    contador = 0
#    n_lineas = 0
#    trace_complete = []    
#    for x in os.listdir(traces):  #recorre la lista de los archivos de traces
#        f = open(traces+x, "r")
#        lines = f.readlines()
#        n_lineas = n_lineas + sum(1 for line in lines) #obtiene el número de líneas del archivo        
#        f.close()        
#        for line in lines:        
#            if character != None:
#                key = line.replace("\n", "").lstrip().split(" ")[position].split(character)[0]
#            else:
#                key = line.replace("\n", "").lstrip().split(" ")[position]
#            #print key
#            trace_complete.append(key)
#            if not(dic_temporality.has_key(key)):
#                dic_temporality[key] = {'first_position':contador, 'last_position':contador, 'amount':1}
#            else:
#                dic_temporality.get(key)['amount'] += 1
#                dic_temporality.get(key)['last_position'] = contador
#                if (dic_temporality.get(key)['amount'] > 2):
#                    shuffle_array.append(key)
#            contador +=1
#    random.shuffle(shuffle_array)
#    num_lines = n_lineas
#    
#    return trace_complete,num_lines
#

#def do_originals(trace_complete):
#    for algn in algorithms_selected:
#        k = None
#        if algn.find("RANDOM_LRU") >= 0:
#            algm = kRANDOM_LRU
#            k = int(algn.replace("RANDOM_LRU_", ""))
#        elif algn[0] == "S" and algn.find("LRU") > 0:
#            algm = SkLRU
#            k = int(algn[1:].replace("LRU", ""))
#        elif algn not in l:
#            print "Algorithm: %s does not exist" % algn
#            exit()
#        else:
#            algm =  l[algn]
#
#        folder = results+ str(algn)
#        if not os.path.exists(folder):
#            os.makedirs(folder)
#
#        fo = open(folder+'/'+str(algn) + "_ORIGINAL.res","wb")
#
#        
#        for c in array_cache:
#            
#            alg = algm.alg(c, k=k)
#            
#            time1 = time.time()
#            lc = 0
#
#            print trace_complete
#
#            for line in trace_complete:
#                
#                lc += 1
#                ret = alg.get(line)
#                if not ret:
#                    alg.put(line, 1)
#                #print 'stored: '
#                #print alg.stored
#
#            time2 = time.time()
#            diff = time2-time1
#            tp = lc / (0.0 + diff)
#            hr = alg.hitcount / (0.0 + alg.count)
#            fo.write( "%s %d %.4f %.2f\n" % (str(alg), c, 100.0*hr, tp));
#        fo.close()
#
#def range_hitrate_request():
#    maxhit = 0
#    maxtp = 0
#    i = 0
#    mimhit = 0
#    mimtp = 0
#    
#    for fn in os.listdir(results):
#        f = open(results+fn)
#        lines= f.readlines()
#        f.close()
#
#        for line in lines:
#            a, cache_size, val, time = line.replace("\n", "").split(" ")
#            maxhit = max(maxhit, float(val))
#            maxtp = max(maxtp, float(time))
#            if i==0:
#                minhit = float(val)
#                mintp = float(time)
#                i+=1
#            minhit = min(minhit, float(val))
#            mintp = min(mintp, float(time))
#
#
#    maxhit += maxhit if minhit == 0 else minhit
#    maxtp += maxtp if mintp == 0 else mintp
#    minhit -= 20
#    mintp -= 20
#
#    return maxhit, maxtp, minhit, mintp
#
#def range_cache():
#    min_cache, max_cache = [array_cache[0], array_cache[-1]]
#    return min_cache, max_cache
#
#       
#def create_new_trace():
#    real_traces = []
#    sqlProceso = ""
#    contador = 1
#    cursor.execute('BEGIN TRANSACTION;'"DELETE FROM temporality_trace;"';COMMIT;')    
#    print "Termina delete de la tabla temporality_trace"
#    time1 = time.time()
#    #Ingreso de los datos del diccionario
#    update_bitacora("temporality_trace_dictionary")
#    for k,v in dic_temporality.items():        
#        sqlProceso = "INSERT INTO temporality_trace(key, first_position, last_position, amount, real_position,id,tipo) VALUES ('"+k+"','"+str(v['first_position'])+"','"+str(v['last_position'])+"','"+str(v['amount'])+"','"+str(v['first_position'])+"','"+str(contador)+"',1);"
#        contador += 1
#        if v['last_position'] != v['first_position']:
#            sqlProceso = sqlProceso + "INSERT INTO temporality_trace(key, first_position, last_position, amount, real_position,id,tipo) VALUES ('"+k+"','"+str(v['first_position'])+"','"+str(v['last_position'])+"','"+str(v['amount'])+"','"+str(v['last_position'])+"','"+str(contador)+"',1);"
#            contador += 1   
#        cursor.execute('BEGIN TRANSACTION;'+sqlProceso+';COMMIT;')
#    update_bitacora("temporality_trace_dictionary")
#    time2 = time.time()
#    diff = time2-time1
#    print "El tiempo en insertar los datos del diccionario es de: " + str(diff)
#    
#    #Ingreso de los datos del shuffle_array
#    sqlProceso = ""
#    time1 = time.time()
#    update_bitacora("temporality_trace_shuffle_array")
#    for key in shuffle_array:                
#        sqlProceso = "INSERT INTO temporality_trace(key, first_position, last_position, amount, real_position,id,tipo) VALUES ('"+key+"',0,0,1,null,'"+str(contador)+"',null);"
#        contador += 1        
#        cursor.execute('BEGIN TRANSACTION;'+sqlProceso+';COMMIT;')
#    update_bitacora("temporality_trace_shuffle_array")
#    time2 = time.time()
#    diff = time2-time1
#    print "El tiempo en insertar los datos del shuffle array es de: " + str(diff)
#    
#    time1 = time.time()
#    update_bitacora("func_create_trace")
#    sqlProceso = "select * from func_create_trace();"
#    cursor.execute(sqlProceso)
#    update_bitacora("func_create_trace")
#    time2 = time.time()
#    diff = time2-time1
#    print " El tiempo en generar el nuevo trace es de: " + str(diff)    
#    
#    time1 = time.time()
#    update_bitacora("temporality_trace_order")
#    sqlProceso = "select key from temporality_trace order by real_position asc;"
#    cursor.execute(sqlProceso)    
#    try:        
#        real_traces = cursor.fetchall()                    
#    except:
#        real_traces = []
#    update_bitacora("temporality_trace_order")
#    time2 = time.time()
#    diff = time2-time1
#    print " El tiempo en retornar el nuevo trace es de: " + str(diff)    
#    #print real_traces
#    return real_traces  
#
#def do_shuffle(trace_complete, num_lines):    
#        
#    for algn in algorithms_selected:    #recorre lista de algoritmos        
#        k = None
#        if algn.find("RANDOM_LRU") >= 0:
#            algm = kRANDOM_LRU
#            k = int(algn.replace("RANDOM_LRU_", ""))
#        elif algn[0] == "S" and algn.find("LRU") > 0:
#            algm = SkLRU
#            k = int(algn[1:].replace("LRU", ""))
#        elif algn not in l:
#            print "Algorithm: %s does not exist" % algn
#            exit()
#        else:
#            algm =  l[algn]
#            
#        for j in xrange(len(slices)): #recorre arreglo de slices  
#            n_slice = slices[j]
#
#            folder = results+ str(algn)
#            if not os.path.exists(folder):
#                os.makedirs(folder)
#
#            file_result = open(folder+'/'+str(algn) + "_K_" + str(slices[j])+".res","wb")
#
#            for i in xrange(len(array_cache)):    #recorre lista de tamaños de cache
#                c = int(array_cache[i])
#                alg = algm.alg(c, k=k)        
#                time1 = time.time()
#                lc = 0
#
#                if (num_lines < slices[j]):                                        
#                    n_slice = 1
#                contador = 0
#                
#                for q in xrange(n_slice): #divide el archivo en n partes
#                    
#                    if ((n_slice > 0) and (n_slice < num_lines)) :
#                        if(contador == 0):                            
#                            num = int(round(num_lines / n_slice,0))                            
#                            max_num = num
#                        else:                            
#                            max_num = max_num + num 
#                            if (q == n_slice - 1):
#                                max_num = num_lines                        
#
#                        arreglo_lineas = random.sample(range(contador, max_num), max_num-contador)
#                        lista = range(contador, max_num)
#                        random.shuffle(lista)
#                        contador = max_num
#                        for m in xrange(len(arreglo_lineas)):
#                            #line = lines[arreglo_lineas[m]]
#                            line = trace_complete[arreglo_lineas[m]]
#                            lc += 1
#                            ret = alg.get(line)
#                            if not ret:
#                                alg.put(line, 1)
#            
#                time2 = time.time()
#                diff = time2-time1
#                tp = 0
#                if (diff > 0):
#                    tp = lc / (0.0 + diff)
#                hr = 0
#                if(alg.count > 0):
#                    hr = alg.hitcount / (0.0 + alg.count)            
#                file_result.write(str(alg) + " " + str(c) + " " + str(100.0*hr) + " " + str(tp) + "\n")
#                
#        file_result.close()
#
# 
##Función que genera un nuevo arreglo para calcular el temporality
#def calculate_temporality(num_lines):    
#    real_traces = []          
#    indice = 0
#    
#    for q in xrange(num_lines):
#        id = next((key for key, value in dic_temporality.items() if (value['first_position'] == q or value['last_position'] == q)), None)        
#        if (id != None):            
#            real_traces.append(id)
#        else:
#            indice = random.randint(0, len(shuffle_array)-1)
#            real_traces.append(shuffle_array.__getitem__(indice))
#            shuffle_array.__delitem__(indice)                         
#            #id = next((key for key, value in dic_temporality.items() if value['last_position'] == q), None)            
#            #if (id != None):
#            #    real_traces.append(id)
#            #else:                
#            #    indice = random.randint(0, len(shuffle_array)-1)
#            #    real_traces.append(shuffle_array.__getitem__(indice))
#            #    shuffle_array.__delitem__(indice)                         
#    return real_traces  
#
#def do_temporality(trace_complete):
#    for algn in algorithms_selected:
#        k = None
#        if algn.find("RANDOM_LRU") >= 0:
#            algm = kRANDOM_LRU
#            k = int(algn.replace("RANDOM_LRU_", ""))
#        elif algn[0] == "S" and algn.find("LRU") > 0:
#            algm = SkLRU
#            k = int(algn[1:].replace("LRU", ""))
#        elif algn not in l:
#            print "Algorithm: %s does not exist" % algn
#            exit()
#        else:
#            algm =  l[algn]
#
#        folder = results+ str(algn)
#        if not os.path.exists(folder):
#            os.makedirs(folder)
#
#        fo = open(folder+'/'+str(algn) + "_TEMPORAL.res","wb")
#
#        for c in array_cache:
#            
#            alg = algm.alg(c, k=k)
#            
#            time1 = time.time()
#            lc = 0
#            
#            #print trace_complete
#            for line in trace_complete:
#                print line[0]
#                lc += 1
#                ret = alg.get(line[0])
#                if not ret:
#                    alg.put(line[0], 1)
#                    #print 'stored: '
#                    #print alg.stored
#
#            time2 = time.time()
#            diff = time2-time1
#            tp = lc / (0.0 + diff)
#            hr = alg.hitcount / (0.0 + alg.count)
#            fo.write( "%s %d %.4f %.2f\n" % (str(alg), c, 100.0*hr, tp));
#        fo.close()
#
#def range_hitrate_request_algorithm(algorithm):
#    folder = results+algorithm+'/'
#    maxhit = 0
#    maxtp = 0
#    i = 0
#    mimhit = 0
#    mimtp = 0
#    
#    for fn in os.listdir(folder):
#        f = open(folder+fn)
#        lines= f.readlines()
#        f.close()
#
#        for line in lines:
#            a, cache_size, val, time = line.replace("\n", "").split(" ")
#            maxhit = max(maxhit, float(val))
#            maxtp = max(maxtp, float(time))
#            if i==0:
#                minhit = float(val)
#                mintp = float(time)
#                i+=1
#            minhit = min(minhit, float(val))
#            mintp = min(mintp, float(time))
#
#
#    maxhit += maxhit if minhit == 0 else minhit
#    maxtp += maxtp if mintp == 0 else mintp
#    minhit -= 20
#    mintp -= 20
#
#    return maxhit, maxtp, minhit, mintp


    