import streamlit as st
import spacy
import pandas as pd
import io
import gensim
from spacy.lang.en import English
from gensim.parsing.preprocessing import remove_stopwords


def removeStopwords(text):
    return remove_stopwords(text)

@st.cache
def addPatterns():
    
    regex = r"(?:(?:north|south|center|central)(?:[\s+|-](?:east|west))?|east|west)"   
    regexKeyword = r'(?i)(surround|near|next|close)'   
    regexDistanceKeyword = r'(?i)(miles|kilometer|km)'
    regexDigit = r'(\d+)'
    regexCardinal = r'(?i)(north|east|south|center|west)'
    regexSpaceDash = r'(\s+|-)'
    df = pd.read_csv('cities.csv')
    patterns = []
    for index, row in df.iterrows():
        
        patternCardinal = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        patternMixCardinal1 = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}},{"LOWER":{"REGEX": regexSpaceDash}},{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        pattern1 = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexKeyword}}, {"LOWER":row['name'].lower()}]}
        
        patternDistance = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexDigit}}, {"LOWER":{"REGEX": regexDistanceKeyword}}, {"LOWER":row['name'].lower()}]}
        
        patterns.append(patternCardinal)
        patterns.append(patternMixCardinal1)
        
        patterns.append(pattern1)
        patterns.append(patternDistance)
    
    df = pd.read_csv('countries.csv')
    for index, row in df.iterrows():
        
        patternCardinal = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        patternMixCardinal1 = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}},{"LOWER":{"REGEX": regexSpaceDash}},{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        
        pattern1 = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexKeyword}}, {"LOWER":row['name'].lower()}]}
        patternDistance = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexDigit}}, {"LOWER":{"REGEX": regexDistanceKeyword}}, {"LOWER":row['name'].lower()}]}
        
        patterns.append(patternCardinal)
        patterns.append(patternMixCardinal1)
        patterns.append(pattern1)
        patterns.append(patternDistance)
    
    return patterns  
 

def main():
	
	#st.set_page_config(layout="wide")
	
    st.title("RSE Extraction")
    print("spacy=="+spacy.__version__)
    print("gensim=="+gensim.__version__)
    print("streamlit=="+st.__version__)
    print("pandas=="+pd.__version__)
    
    user_input = st.text_area("Enter your text", "I am including some different relative spatial locations for the sack of example like north of America, south america, south of the GERMANY, north-east belgium and north of the France etc. If we go to some of the examples in cities like north of montpellier and south paris. Moreover, if we look to some other cities like north Innsbruck, south of munich, east berlin and South of AMSTERDAM. Moreover, there are some other spatial entities like surrounding of Montpellier, nearby Lyon, West to Bolzano, 80 km from Paris.")
    if st.button('Extract') and len(user_input) > 0:
        
        nlp = English()
        ruler = nlp.add_pipe("entity_ruler", config={"validate": True})
        patterns = addPatterns()
        ruler.add_patterns(patterns)
        nlp.to_disk("pipeline")
        doc = nlp(removeStopwords(user_input))
        for entity in doc.ents:
            st.text(entity.text + "  ------  "+ entity.label_)
      
   
if __name__ == '__main__':
	main()	