import streamlit as st
from spacy import displacy
import spacy
import pandas as pd
import io
import gensim
from spacy.lang.en import English
from gensim.parsing.preprocessing import remove_stopwords

HTML_WRAPPER = """<div style="overflow-x: auto; border: none solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

HTML = "<a href='https://www.teacheron.com/tutor-profile/4uQK?r=4uQK' target='_blank' style='display: inline-block;'><img src='https://www.teacheron.com/resources/assets/img/badges/viewMyProfile.png' style='width: 336px !important; height: 144px !important'></a>"

def removeStopwords(text):
    return remove_stopwords(text)

@st.cache(suppress_st_warning=True)
def addPatterns():
    
    st.write("Data not loaded from cache..")
    #regex = r"(?:(?:north|south|center|central)(?:[\s+|-](?:east|west))?|east|west)"   
    regexKeyword = r'(?i)(surround|near|next|close)'   
    regexDistanceKeyword = r'(?i)(miles|kilometer|km)'
    regexDigit = r'(\d+\s*)'
    regexCardinal = r'(?i)(north|east|south|center|centeral|west)'
    regexSpaceDash = r'(\s+|-)'
    df = pd.read_csv('cities.csv')
    patterns = []
    for index, row in df.iterrows():
        
        patternCardinal = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        patternOrdinal = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}},{"LOWER":{"REGEX": regexSpaceDash}},{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        patternKeywords = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexKeyword}}, {"LOWER":row['name'].lower()}]}
        
        patternDistance = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexDigit}}, {"LOWER":{"REGEX": regexDistanceKeyword}}, {"LOWER":row['name'].lower()}]}
        
        patterns.append(patternCardinal)
        patterns.append(patternOrdinal)
        patterns.append(patternKeywords)
        patterns.append(patternDistance)
    
    df = pd.read_csv('countries.csv')
    for index, row in df.iterrows():
        
        patternCardinal = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        patternOrdinal = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexCardinal}},{"LOWER":{"REGEX": regexSpaceDash}},{"LOWER":{"REGEX": regexCardinal}}, {"LOWER":row['name'].lower()}]}
        
        patternKeywords = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexKeyword}}, {"LOWER":row['name'].lower()}]}
        patternDistance = {"label": "GPE", "pattern": [{"LOWER":{"REGEX": regexDigit}}, {"LOWER":{"REGEX": regexDistanceKeyword}}, {"LOWER":row['name'].lower()}]}
        
        patterns.append(patternCardinal)
        patterns.append(patternOrdinal)
        patterns.append(patternKeywords)
        patterns.append(patternDistance)
    
    return patterns  
 
@st.cache(allow_output_mutation=True)
def init_custom_ner():
    nlp = English()
    ruler = nlp.add_pipe("entity_ruler", config={"validate": True})
    ruler.from_disk("pipeline/entity_ruler/")
    return nlp


def main():
	
	#st.set_page_config(layout="wide")
	
    st.title("GeoX - RSI Extraction")
    
    user_input = st.text_area("Enter your text", "")
    if st.button('Extract') and len(user_input) > 0:
        
        nlp = init_custom_ner()
        #nlp.to_disk("pipeline")
        doc = nlp(removeStopwords(user_input))
        html = displacy.render(doc,style="ent")
        html = html.replace("\n","")
        st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
        #for entity in doc.ents:
        #    st.text(entity.text + "  ------  "+ entity.label_)
      
    #st.write(HTML ,unsafe_allow_html=True)
if __name__ == '__main__':
	main()	