from typing import Optional
from db import Database


#-------- queries related to cygnet.py

def fetch_concepts(form: Optional[str] = None,
                   langs=None,
                   pos: Optional[str] = None):
    """
    Retrieve all concepts optionally filtered by form, languages and/or POS
    """
    sql_concept = """SELECT DISTINCT synsets.rowid, LOWER(synsets.pos), ili FROM synsets
                    JOIN senses ON synsets.rowid = senses.synset_rowid
                    JOIN entries ON entries.rowid = senses.entry_rowid
                    JOIN forms ON entries.rowid = forms.entry_rowid
                    JOIN languages ON languages.rowid = entries.language_rowid"""
    params: list = []
    conditions = []
    if form:
        conditions.append(" form=?")
        params += [form]
    if langs:
        lang_list = [langs] if isinstance(langs, str) else langs
        placeholders = ",".join("?" * len(lang_list))
        conditions.append(f" languages.code IN ({placeholders})")
        params += lang_list
    if pos:
        conditions.append(" LOWER(synsets.pos)=?")
        params.append(pos)

    if len(conditions)==1:
        sql_concept=  sql_concept + "\n WHERE  " + conditions[0] + "\n ORDER BY synsets.rowid ASC"
     
    elif len(conditions)>1:
        condition = "\n WHERE " + " AND ".join(conditions)
        sql_concept +=f""" {condition}
                    ORDER BY synsets.rowid ASC"""  
    
    return Database.execute(sql_concept, tuple(params)).fetchall()





def fetch_concept_by_ili ( ili: str):
    """
    Retrieve the specific concept related to an ILI
    """
    return Database.execute(
        """SELECT rowid, LOWER(pos), ili FROM synsets        
      WHERE ili=?""", (ili,)
    ).fetchone()


def fetch_senses(form: Optional[str] = None, langs=None):
    """
    Retrieve all concepts optionnally filtered by form and/or languages
    """
    sql_sense= "SELECT DISTINCT senses.rowid, senses.synset_rowid, senses.entry_rowid FROM senses"
    params: list = []
    conditions = []
    if form:
        conditions.append(" form=?")
        params += [form]
    if langs:
        lang_list = [langs] if isinstance(langs, str) else langs
        placeholders = ",".join("?" * len(lang_list))
        conditions.append(f" languages.code IN ({placeholders})")
        params += lang_list
    
    if len(conditions)==1:
        sql_sense +=  """ \n JOIN entries ON entries.rowid = senses.entry_rowid
                    JOIN forms ON entries.rowid = forms.entry_rowid
                    JOIN languages ON languages.rowid = entries.language_rowid""" + "\n WHERE  " + conditions[0] + """\n ORDER BY senses.sense_index, senses.rowid"""
     
    elif len(conditions)>1:
        condition = "\n WHERE " + " AND ".join(conditions)
        sql_sense +=f""" \n JOIN entries ON entries.rowid = senses.entry_rowid
                    JOIN forms ON entries.rowid = forms.entry_rowid
                    JOIN languages ON languages.rowid = entries.language_rowid
                    {condition}
                    ORDER BY senses.sense_index, senses.rowid"""
  
    
    return Database.execute(sql_sense, tuple(params)).fetchall()




def fetch_lexemes(form: Optional[str] = None, langs=None):
    """
    Retrieve all lexemes optionnally filtered by form and/or languages
    """
    sql_lexeme= "SELECT DISTINCT entries.rowid from entries"
    params: list = []
    conditions = []
    if form:
        conditions.append(" form=?")
        params += [form]
    if langs:
        lang_list = [langs] if isinstance(langs, str) else langs
        placeholders = ",".join("?" * len(lang_list))
        conditions.append(f" languages.code IN ({placeholders})")
        params += lang_list
    
    if len(conditions)==1:
        sql_lexeme +=  """ \n JOIN senses ON entries.rowid = senses.entry_rowid
                                JOIN forms ON entries.rowid = forms.entry_rowid
                    JOIN languages ON languages.rowid = entries.language_rowid""" + "\n WHERE  " + conditions[0] + """\n ORDER BY entries.rowid ASC"""
     
    elif len(conditions)>1:
        condition = "\n WHERE " + " AND ".join(conditions)
        sql_lexeme +=f""" \n JOIN forms ON entries.rowid = forms.entry_rowid
                    JOIN languages ON languages.rowid = entries.language_rowid
                    {condition}
                    ORDER BY entries.rowid ASC"""
  
    
    return Database.execute(sql_lexeme, tuple(params)).fetchall()


def print_all_languages ():
    """
    Display the codes of all languages available in the database
    """
    return Database.execute("""SELECT code FROM languages ORDER BY code""" ).fetchall()


#-------- queries related to the class concept


def fetch_definition(rowid, lang: str):       
    """
    Retrieve the definition of a concept in a given language
    """
    sql_def = """SELECT definitions.definition, languages.code FROM definitions
                JOIN languages ON languages.rowid=definitions.language_rowid
                WHERE definitions.synset_rowid=? AND languages.code=?""" 
    
   
    return Database.execute(sql_def, (rowid, lang)).fetchone()


def fetch_senses_by_concept(rowid,lang: Optional[str] = None):
    """
    Retrieve the senses of a concept optionally filtered by language
    """
    sql_senses_concept=""" SELECT DISTINCT senses.rowid, senses.synset_rowid, senses.entry_rowid FROM senses"""
    params=[rowid]
                         
    if lang:
        sql_senses_concept += """\n JOIN entries ON entries.rowid=senses.entry_rowid 
                                     JOIN languages on entries.language_rowid=languages.rowid
                                     WHERE synset_rowid = ? AND languages.code=?
                                    ORDER BY senses.sense_index, senses.rowid"""
        params.append(lang)
    else:
        sql_senses_concept += """ \n WHERE synset_rowid = ?
                                    ORDER BY senses.sense_index, senses.rowid"""
        
    return Database.execute(sql_senses_concept, tuple(params)).fetchall()




def fetch_lexemes_by_concept(rowid,lang: Optional[str] = None):
    """
    Retrieve the lexemes related to a concept optionally filtered by language
    """
    sql_lexemes_concept=""" SELECT DISTINCT senses.entry_rowid FROM senses"""
    params=[rowid]
                         
    if lang:
        sql_lexemes_concept += """\n JOIN entries ON entries.rowid=senses.entry_rowid 
                                     JOIN languages on entries.language_rowid=languages.rowid
                                     WHERE senses.synset_rowid = ? AND languages.code=? 
                                     ORDER BY senses.entry_rowid ASC"""
        params.append(lang)
    else:
        sql_lexemes_concept += """ \n WHERE senses.synset_rowid = ?
                                    ORDER BY senses.entry_rowid ASC"""
        
    return Database.execute(sql_lexemes_concept, tuple(params)).fetchall()




def fetch_related_synsets(rowid,relation):
    """
    Retrieve the hyperonyms, hyponyms, meronyms or holonyms of a concept
    """
    sql_rel="""SELECT target_rowid, LOWER(synsets.pos), synsets.ili  FROM synset_relations
            JOIN synsets ON target_rowid=synsets.rowid
            WHERE source_rowid=? AND type_rowid=?
            ORDER BY target_rowid ASC"""
    
    return Database.execute(sql_rel, (rowid,relation)).fetchall()
   
  


#-------- queries related to the class Sense

def fetch_examples(sense_rowid):
    """
    Retrieve all examples of a particular sense
    """
    sql_examples = """ SELECT example, languages.code, example_annotations.sense_rowid, senses.synset_rowid, senses.entry_rowid, example_annotations.start_offset, example_annotations.end_offset FROM examples
                    JOIN sense_examples ON examples.rowid= sense_examples.example_rowid
                    JOIN example_annotations ON example_annotations.rowid=examples.rowid
                    JOIN senses ON senses.rowid=sense_examples.sense_rowid 
                    JOIN entries ON entries.rowid=senses.entry_rowid 
                    JOIN languages on entries.language_rowid=languages.rowid 
                    WHERE sense_examples.sense_rowid = ?
                    ORDER BY example ASC"""
    return Database.execute(sql_examples, (sense_rowid, )).fetchall()



def fetch_concept_by_sense(sense_rowid):
    """
    Retrieve the concept related to a sense
    """
    sql_sense_concept=""" SELECT rowid, LOWER(pos), ili FROM synsets                  
                    WHERE rowid = ?"""
    return Database.execute(sql_sense_concept, (sense_rowid, )).fetchone()


#-------- queries related to the class Lexeme


def find_language_lexeme (lex_rowid):
    """
    Retrieve the language of a lexeme
    """
    sql_lex_lang=""" SELECT code FROM languages     
                    JOIN entries ON entries.language_rowid = languages.rowid              
                    WHERE entries.rowid = ?"""
    return Database.execute(sql_lex_lang, (lex_rowid, )).fetchone()


def find_lemma(lex_rowid):
    """
    Retrieve the lemma of a lexeme
    """
    sql_lex_lemma=""" SELECT normalized_form FROM forms
                     WHERE rank=0 and entry_rowid= ?"""
    return Database.execute(sql_lex_lemma, (lex_rowid, )).fetchone()


def fetch_forms_by_lexeme(lex_rowid):
    """
    Retrieve all the forms of a lexeme
    """
    sql_lex_forms=""" SELECT form, entry_rowid, rank FROM forms
                     WHERE entry_rowid= ?
                     ORDER BY form ASC"""
    return Database.execute(sql_lex_forms, (lex_rowid, )).fetchall()


def fetch_senses_by_lexeme(lex_rowid):
    """
    Retrieve all the senses of a lexeme
    """
    sql_lex_senses="""SELECT rowid, synset_rowid, entry_rowid FROM senses
                    WHERE entry_rowid= ?
                    ORDER BY rowid ASC"""
    return Database.execute(sql_lex_senses, (lex_rowid, )).fetchall()


def fetch_concepts_by_lexeme(lex_rowid):
    """
    Retrieve all the concepts related to a lexeme
    """
    sql_lex_concepts="""SELECT synset_rowid, LOWER(synsets.pos), synsets.ili FROM senses
                    JOIN synsets ON  synsets.rowid=senses.synset_rowid
                    WHERE senses.entry_rowid= ?
                    ORDER BY synsets.rowid ASC"""
    return Database.execute(sql_lex_concepts, (lex_rowid, )).fetchall()




