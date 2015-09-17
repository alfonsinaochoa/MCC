#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import sys
import nltk
import random
import codecs
import xml.etree.ElementTree as ET

from StringIO import StringIO
from xml.dom import minidom
from xml.dom.minidom import Node

from random import shuffle
from lxml import etree
from settings import *
from funtwokenize import *
from django.utils.encoding import smart_unicode, smart_str


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
    polarity = 'NONE'
    xml_lines = ''
    for x in os.listdir(data):        
        f = codecs.open(data+str(x),'r','utf-8')    
        lines = f.readlines()        
        n_lineas = sum(1 for line in lines) #obtiene el número de líneas del archivo
        print n_lineas
        f.close()
        for line in lines:
            xml_lines = xml_lines + line
        tree = ET.parse(data+str(x))
        tree = ET.fromstring(xml_lines)
        root = tree.getroot()
        #f = open(data+str(x),'r')
        #lines = f.read()                
        #contador = 1
        #flag = True
        for tweet in root.findall('tweet'):
            #content = tweet.find('content').text.encode('utf-8').decode('utf-8')
            #print unicode(tweet.find('content').text)
            print tweet.find('content').text
            #print unicode(tweet.find('content').text)
        
def get_xml_tweet2():
    #dic_tweet.clear()
    polarity = 'NONE'
    for x in os.listdir(data):        
        #file_result = open(path + "/sentiment_tweets.xml","wb")
        f = open(data+str(x),'r')
        lines = f.read()                
        contador = 1
        flag = True
        doc = minidom.parseString(lines)        
        for topic in doc.getElementsByTagName('tweet'):
            #id_tweet = topic.getAttribute("tweetid")                        
            print topic.getElementsByTagName('tweetid')                          
            for subnode in topic.childNodes:
                #print subnode.tagName
                if subnode.nodeType == Node.ELEMENT_NODE and subnode.tagName == "polarity":
                    #print u'abcdé'.encode('utf-8').decode('utf-8')
                    #polarity = subnode.firstChild.nodeValue.encode('utf-8').decode('utf-8')
                    
                    print unicode(subnode.firstChild.nodeValue, 'utf-8')
                    #out = subnode.firstChild.nodeValue.replace('-', '').encode("utf-8")
                    #out = out.replace( u'\u201c', u'"') #.replace( u'\xed', u',').replace( u'\u201c', u'"')                    
                    #print out                   
                    #print out.encode('ascii')
                    #print subnode.firstChild.nodeValue #.encode("utf-8")
                    
                    #tweet = tweet + "<sentiment polarity='" + str(subnode.getAttribute("polarity")) + "' contador='" + str(contador) + "'>" + str(subnode.firstChild.nodeValue.encode("utf-8")) + "</sentiment>"                                        
                    #hnode = doc.createElement("analysis_sentiment")
                    #hnode.setAttribute("contador", str(contador))
                    #htext = doc.createTextNode('')
                    #hnode.appendChild(htext)
                    #topic.insertBefore(hnode,subnode)
                    #topic.removeChild(subnode)
                    contador += 1
            contador = 1
      
            
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
    
    print 'Pre processing data'       
    get_xml_tweet()
   
    
    