from django.shortcuts import render
from . import models
from datetime import datetime
from django.utils import timezone
# import csv

from django.db.utils import IntegrityError
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction

import nltk, re
import pandas as pd


def removeStopwords(example_sent):  
  from nltk.corpus import stopwords  
  from nltk.tokenize import word_tokenize  
    
  # example_sent = """This is a sample sentence, 
  #                   showing off the stop words filtration."""
    
  stop_words = set(stopwords.words('english'))  
    
  word_tokens = word_tokenize(example_sent)  
    
  filtered_sentence = [w for w in word_tokens if not w in stop_words]  
    
  filtered_sentence = []  
    
  for w in word_tokens:  
      if w not in stop_words:  
          filtered_sentence.append(w)  
    
  # print(word_tokens)  
  return filtered_sentence  



def prePro(s1, s2):
  import nltk, re
  s1  = re.sub('[^a-zA-Z0-9\s]', '', s1)
  s2  = re.sub('[^a-zA-Z0-9\s]', '', s2)
  s1 = s1.lower()
  s2 = s2.lower()
  s1 = removeStopwords(s1)
  s2 = removeStopwords(s2)
  return s1, s2


# e.sub('[^a-zA-Z0-9\s]', '', answer)



def testView(request, id):
    obj = models.Test.objects.get(id=id)
    model = pd.read_csv(f"./media/{obj.questions.name}")
    # import os
    _id = model['Index']
    ques=  model['Question']
    request.session['test'] = obj.id

    return render(request, 'test.html', context={'objects': dict(zip(_id, ques)).items(), 'time': obj.end_time, 'test_id': obj.id})

def availableTestView(request):
    objects = list(models.Test.objects.all())
    availableObjects = []
    for i in objects:
        if i.start_time >= timezone.now():
            availableObjects.append(i)
    return render(request, 'available.html', context={'objects': availableObjects})


import matplotlib.pyplot as plt


def evaluateView(request):
    
    import tensorflow_hub as hub
    import numpy as np

    import tensorflow as tf

    module_url = "https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed"

    embed = hub.Module(module_url)


    test = models.Test.objects.get(id=request.session['test'])

    questions = pd.read_csv(f"./media/{test.questions.name}")
    indexes = questions['Index']
    marks = []
    for i in indexes:
        answer = questions[questions['Index']==i]['Answer']
        print(str(answer[i-1]))
        givenAnswer = request.POST.get(str(i))

        answer  = re.sub('[^a-zA-Z0-9\s]', '', str(answer[i-1]))
        givenAnswser = re.sub('[^a-zA-Z0-9\s]', '', str(givenAnswer))

        answer = answer.lower()

        givenAnswser = givenAnswser.lower()

        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')
        answer = removeStopwords(answer)
        newGiven = removeStopwords(givenAnswser)
        answer = ' '.join(answer)
        givenAnswser = ' '.join(newGiven)

        
        
        sentences=[answer, givenAnswser]
        print(sentences)
        similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        similarity_message_encodings = embed(similarity_input_placeholder)
        with tf.Session() as session:
            session.run(tf.global_variables_initializer())
            session.run(tf.tables_initializer())
            message_embeddings_ = session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: sentences})

            corr = np.inner(message_embeddings_, message_embeddings_)
            print(corr)
            marks.append(corr[0][1])

    # marks=[.5, .9]

    marksF = [round(float(i)*100, 2) for i in marks]
    print(marks)
    print(marksF)

    return render(request, 'result.html', context={'marks': zip(indexes, marksF), 'total': len(marks)*100, 'score': sum(marksF)} )
