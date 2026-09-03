from typing import List, Optional
import queries
from api import AbstractConcept, AbstractSense, AbstractLexeme, POS
from subclasses import*


class Cygnet:
    """
    main class of the module
    """
    def __init__(self):
       pass

    def concepts(self,
                 form: Optional[str] = None,
                 langs=None,
                 pos: Optional[POS] = None
                 ) -> List[AbstractConcept]:
        rows = queries.fetch_concepts(form=form, langs=langs, pos=pos)
        return [Concept(row) for row in rows]

    def concept(self, ili: str) -> Optional[AbstractConcept]:
        row = queries.fetch_concept_by_ili(ili)
        if row is None:
            return None
        else:
            return Concept(row)
        
    def senses(self,
               form: Optional[str] = None,
               langs=None
               ) -> List[AbstractSense]:
        rows = queries.fetch_senses(form=form, langs=langs)
        return [Sense(row) for row in rows]

    def lexemes(self,
                form: Optional[str] = None,
                langs=None
                ) -> List[AbstractLexeme]:
        rows = queries.fetch_lexemes(form=form, langs=langs)
        return [Lexeme(row) for row in rows]
    

    def langs(self) -> List[str]:
        languages = queries.print_all_languages()
        return [l[0] for l in languages]
    
