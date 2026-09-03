from typing import List, Optional,Tuple
from api import AbstractConcept, AbstractSense, AbstractLexeme, POS, AbstractAnnotatedString
import queries


class Concept(AbstractConcept):   
    """
    Implementation of the object Concept
    """
    def __init__(self, data):              
        self.integer= data[0]
        self.gram_cat = data[1]
        self.identifier= data[2]
       
       
    def __repr__(self):
        return "Concept(id="+ str(self.integer)+')'

    def index(self) -> str:
        return self.identifier

    def pos(self) -> POS:
        return self.gram_cat
    
    def definition(self, lang: str) -> Optional[AbstractAnnotatedString]:
       row = queries.fetch_definition(self.integer, lang)
       if row is None:
            return None       
       else:            
            return AnnotatedString_Temp(row)

    def senses(self, lang: Optional[str] = None) -> List[AbstractSense]:
        rows= queries.fetch_senses_by_concept(self.integer,lang)
        return [Sense(row) for row in rows]

    def lexemes(self, lang: Optional[str] = None) -> List[AbstractLexeme]:
       rows= queries.fetch_lexemes_by_concept(self.integer,lang)
       return [Lexeme(row) for row in rows]

    def hypernyms(self) -> List[AbstractConcept]:
        rel_hyper= queries.fetch_related_synsets(self.integer,"5")
        return [Concept(row) for row in rel_hyper]
    
    def hyponyms(self) -> List[AbstractConcept]: 
        rel_hypo= queries.fetch_related_synsets(self.integer,"6")
        return [Concept(row) for row in rel_hypo]
    
    def meronyms(self) -> List[AbstractConcept]:  
       rel_mero=queries.fetch_related_synsets(self.integer,"7")
       return [Concept(row) for row in rel_mero]
    
    def holonyms(self) -> List[AbstractConcept]: 
        rel_holo=queries.fetch_related_synsets(self.integer,"8")
        return [Concept(row) for row in rel_holo]
    


    

class Lexeme(AbstractLexeme): 
    """
    Implementation of the object Lexeme
    """
    
    def __init__(self, data):              
        self.integer= data[0]

    
    def __repr__(self):
        return "Lexeme(id="+ str(self.integer)+")"
    
    def index(self) -> str:
         return str(self.integer)
    
    def lang(self) -> str:   
       row = queries.find_language_lexeme (self.integer)
       return (row[0])  
  
    def lemma(self) -> str:
        row = queries.find_lemma (self.integer)
        return (row[0])  
   
    def all_forms(self) -> List[str]:
        rows = queries.fetch_forms_by_lexeme(self.integer)
        results =[]
        for row in rows:
            results.append(row[0])
        return results  
   
    def senses(self) -> List[AbstractSense]:       
        rows = queries.fetch_senses_by_lexeme(self.integer)
        return [Sense(row) for row in rows]     


    def concepts(self) -> List[AbstractConcept]:
        rows = queries.fetch_concepts_by_lexeme(self.integer)
        return [Concept(row) for row in rows] 





class Sense(AbstractSense): 
    """
    Implementation of the object Sense
    """
    def __init__(self, data):                
        self.integer= data[0]
        self.linked_concept = data[1]
        self.linked_entry = data[2]
     

    def __repr__(self):
        return "Sense(id="+ str(self.integer)+")"

    def index(self) -> str:
        return str(self.integer)
    
 
    def examples(self) -> List[AbstractAnnotatedString]:   
        row = queries.fetch_examples(self.integer)
        if row is None:
            return None       
        else:                   
            return AnnotatedString(row)

        
    def concept(self) -> AbstractConcept:   
        row = queries.fetch_concept_by_sense(self.linked_concept)
        return Concept(row) 
      

    def lexeme(self) -> AbstractLexeme:      
        return Lexeme([self.linked_entry])

  
    def lang(self) -> str:    
       row = queries.find_language_lexeme (self.linked_entry)
       return (row[0])  
    



class AnnotatedString_Temp(AbstractAnnotatedString):    
    """
    Temporary class to deal with definitions
    """ 
    def __init__(self, data):           
        self._text = data[0]
        self._lang = data[1]


    def text(self) -> str:
        return self._text

    def lang(self) -> str:
        return self._lang
    
    def sense_offsets(self) -> List[Tuple[AbstractSense, int, int]]:
        pass


class AnnotatedString(AbstractAnnotatedString):
    """
    Print examples and definitions as well as their annotations
    """
   
    def __init__(self, data):     
        
        self._text=[]
        self._lang=[] 
        self._dic={}   
        for elem in data:                 
            self._lang = elem[1]
            self._text.append(elem[0])
            if  (elem[2], elem[3], elem[4]) not in self._dic:
                self._dic[(elem[2], elem[3], elem[4])]=[[elem[-2], elem[-1]]]     
            else:
                 self._dic[(elem[2], elem[3], elem[4])].append([elem[-2], elem[-1]])
                
             

    def text(self) -> str:
        return self._text

    def lang(self) -> str:
        return self._lang

    def sense_offsets(self) -> List[Tuple[AbstractSense, int, int]]:    
    
        list_offsets=[]
        for sense_index in self._dic:
            for list_numbers in self._dic[sense_index]:
                list_offsets.append(tuple([Sense(sense_index), list_numbers[0],  list_numbers[1]]))

        return list_offsets
        
     


