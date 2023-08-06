#coding: utf-8

from pyahooapis.service import Service, BaseObject


class FuriganaService(Service):
    
    def __init__(self, appid):
        Service.__init__(self, appid, 'http://jlp.yahooapis.jp/FuriganaService/V1/furigana')
    
    def get_words(self, sentence, grade=None, json=False):
        '''
        詳しくは
        http://developer.yahoo.co.jp/webapi/jlp/furigana/v1/furigana.html
        
        Args:
            sentence: ルビ振りする文章
            grade: 学年(0~7)
            json: JSON形式で返すかどうか
        Returns:
            そのうち
        '''
        params = {}
        params['sentence'] = sentence
        if grade is not None:
            params['grade'] = grade
        
        dom = self._getDOM(params)
        
        words = []
        
        for w in dom.getElementsByTagName('Word'):
            words.append(Word(self._getText(w, 'Surface'),
                                  self._getText(w, 'Furigana'),
                                  self._getText(w, 'Roman'),
                                  [
                                   SubWord(self._getText(sw, 'Surface'),
                                           self._getText(sw, 'Furigana'),
                                           self._getText(sw, 'Roman'))
                                   for sw in w.getElementsByTagName('SubWord')
                                  ]))
        
        return self.parseJSON(words) if json else words
    

class Word(BaseObject):
    
    def __init__(self,
                 surface,
                 furigana,
                 roman,
                 subwords=None):
        self.surface = surface
        self.furigana = furigana
        self.roman = roman
        self.subwords = subwords
    
    def __str__(self):
        return self.surface


class SubWord(BaseObject):
    
    def __init__(self,
                 surface,
                 furigana,
                 roman):
        self.surface = surface
        self.furigana = furigana
        self.roman = roman
    
    def __str__(self):
        return self.surface
    
