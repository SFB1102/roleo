#-*- coding:utf-8 -*-

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from view2D.views import index, query
from view2D.dataProcess import process
import view2D.errorCode as errorCode

class IndexTest(TestCase):
    def test_view2D_URL_ResolvesTo_IndexView(self):
        found = resolve('/view2D/')
        self.assertEqual(found.func, index)

    # TODO add other test

class QueryTest(TestCase):
    def test_VERB_FORMAT_ERROR(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['verb'] = '你好'.decode('utf8')
        request.POST['role'] = 'A0'
        request.POST['noun'] = 'apple'
        request.POST['group1'] = 'verb'
        response = query(request)
        realResult = response.content

        result = '{"errCode": ' + str(errorCode.VERB_FORMAT_ERROR) + '}'
        self.assertEqual(result, realResult)

    def test_NOUN_FORMAT_ERROR(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['verb'] = 'eat'
        request.POST['role'] = 'A0'
        request.POST['noun'] = '你好'.decode('utf8')
        request.POST['group1'] = 'verb'
        response = query(request)
        realResult = response.content

        result = '{"errCode": ' + str(errorCode.NOUN_FORMAT_ERROR) + '}'
        self.assertEqual(result, realResult)
        
    def test_group_notExist(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['verb'] = '你好'.decode('utf8')
        request.POST['role'] = 'A0'
        request.POST['noun'] = 'apple'
        request.POST['group1'] = 'asdf'
        response = query(request)
        realResult = response.content

        result = '{"errCode": ' + str(errorCode.INTERNAL_ERROR) + '}'
        self.assertEqual(result, realResult)


class DataProcessorTest(TestCase):
    def test_process(self):
        realResult = process('eat', 'apple', 'A0', 'verb')
        queryDict = {
            'y': 0.7788627028935319, 
            'x': 0.45877782991981186, 
            'cos': 0.096960180200616961, 
            'word': 'apple-n'
        }
        wordList = ['announce-v', 'release-v', 'launch-v', 'unveil-v', 'have-v', 'make-v', 'say-v', 'introduce-v', 'sell-v', 'add-v', 'do-v', 'recommend-v', 'admit-v', 'claim-v', 'listen-v', 'offer-v', 'recall-v', 'dominate-v', 'slice-v', 'decide-v']
        self.assertEqual('apple-n', realResult['queried']['word'])

    def test_process_exception_INTERNAL_ERROR(self):
        result = {'errCode' : errorCode.INTERNAL_ERROR}
        self.assertEqual(result, process('', '', '', 'error'))

    def test_process_exception_NOUN_EMPTY(self):
        result = {'errCode' : errorCode.NOUN_EMPTY}
        self.assertEqual(result, process('eat', '', 'A0', 'noun'))
    
    def test_process_exception_VERB_EMPTY(self):
        result = {'errCode' : errorCode.VERB_EMPTY}
        self.assertEqual(result, process('', 'apple', 'A0', 'verb'))

    def test_process_exception_MBR_VEC_EMPTY(self):
        result = {'errCode' : errorCode.MBR_VEC_EMPTY}
        self.assertEqual(result, process('asdf', 'apple', 'A0', 'verb'))

    def test_process_exception_QUERY_EMPTY(self):
        result = {'errCode' : errorCode.QUERY_EMPTY}
        self.assertEqual(result, process('eat', 'asdf', 'A0', 'verb'))

    def test_process_exception_SMT_ROLE_EMPTY(self):
        result = {'errCode' : errorCode.SMT_ROLE_EMPTY}
        self.assertEqual(result, process('eat', 'apple', 'AM-MOD', 'verb'))

# TODO add other test