# Ceck requirements
import Pruefe_Requirements  # Führt das Skript aus und installiert fehlende Pakete

import streamlit as st
import fitz  # PyMuPDF
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from collections import defaultdict



# Ensure the punkt tokenizer is downloaded
nltk.download('punkt')

# Load spaCy German model
nlp = spacy.load('de_core_news_sm')

# Function to extract text from a PDF
def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    return text

# Function to identify definitions and explanations using spaCy
def identify_definitions_explanations_spacy(text):
    doc = nlp(text)
    explanations = []
    definition_patterns = ['definiert als', 'im Folgenden als', 'wird als']

    for sent in doc.sents:
        for pattern in definition_patterns:
            if pattern in sent.text:
                explanations.append(sent.text)
                break

    return explanations

# Function to analyze consistency
def analyze_consistency(explanations):
    explanation_counts = defaultdict(int)
    for explanation in explanations:
        explanation_counts[explanation] += 1

    inconsistent_explanations = {exp: count for exp, count in explanation_counts.items() if count == 1}
    
    # Debugging print statements
    print(f"Explanation Counts: {dict(explanation_counts)}")
    print(f"Inconsistent Explanations: {inconsistent_explanations}")

    return inconsistent_explanations

# Function to annotate PDF with feedback and return the pages with inconsistencies
def annotate_pdf_with_feedback(input_pdf, output_pdf, feedback):
    doc = fitz.open(input_pdf)
    inconsistency_pages = set()  # Use a set to track unique pages with inconsistencies
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        for explanation in feedback:
            if explanation in text:
                highlight_area = page.search_for(explanation)
                if highlight_area:
                    inconsistency_pages.add(page_num + 1)  # Add page number to set (1-indexed)
                    for rect in highlight_area:
                        highlight = page.add_highlight_annot(rect)
                        highlight.set_colors(stroke=(1, 0, 0))  # Red highlight
                        highlight.update()

                    # Add a side comment
                    comment_rect = fitz.Rect(rect.x1 + 10, rect.y1, rect.x1 + 300, rect.y1 + 30)
                    comment = f"Inconsistent explanation: '{explanation}'"
                    page.add_freetext_annot(
                        comment_rect,
                        comment,
                        fontsize=10,
                        fontname="helv",
                        text_color=(1, 0, 0),
                        fill_color=(1, 1, 1),
                        border_color=(0, 0, 0)
                    )

    doc.save(output_pdf)
    return inconsistency_pages

# Function to generate comparative charts
def generate_comparative_charts(data, current_file, output_image_sentences, output_image_avg_sentence_length):
    df = pd.DataFrame(data)
    
    current_file_data = df[df['Titel Dokument'] == current_file]
    other_files_data = df[df['Titel Dokument'] != current_file]

    # Chart for Anzahl der Sätze
    avg_sentences_others = other_files_data['Anzahl der Sätze'].mean()
    plt.figure(figsize=(10, 5))
    plt.bar(current_file_data['Titel Dokument'], current_file_data['Anzahl der Sätze'], color='blue', label='Current File')
    plt.axhline(y=avg_sentences_others, color='r', linestyle='--', label='Durchschnitt der anderen')
    plt.xlabel('Titel Dokument')
    plt.ylabel('Anzahl der Sätze')
    plt.legend()
    plt.title('Vergleichende Analyse der Anzahl der Sätze')
    plt.savefig(output_image_sentences)
    plt.close()

    # Chart for Durchschnittliche Satzlänge
    avg_sentence_length_others = other_files_data['Durchschnittliche Satzlänge'].mean()
    plt.figure(figsize=(10, 5))
    plt.bar(current_file_data['Titel Dokument'], current_file_data['Durchschnittliche Satzlänge'], color='blue', label='Current File')
    plt.axhline(y=avg_sentence_length_others, color='r', linestyle='--', label='Durchschnitt der anderen')
    plt.xlabel('Titel Dokument')
    plt.ylabel('Durchschnittliche Satzlänge')
    plt.legend()
    plt.title('Vergleichende Analyse der durchschnittlichen Satzlängen')
    plt.savefig(output_image_avg_sentence_length)
    plt.close()

# Function to add charts to PDF
def add_charts_to_pdf(input_pdf, output_pdf, chart_image_sentences, chart_image_avg_sentence_length):
    doc = fitz.open(input_pdf)
    doc.new_page()  # Add a new page at the end of the PDF document
    
    # Get the last page (newly added page)
    page = doc[-1]
    
    # Insert the chart image for Anzahl der Sätze
    rect1 = fitz.Rect(0, 0, 595, 421)  # Half of A4 size in points (72 points per inch)
    page.insert_image(rect1, filename=chart_image_sentences)

    # Insert the chart image for Durchschnittliche Satzlänge
    rect2 = fitz.Rect(0, 421, 595, 842)  # Second half of A4 size in points (72 points per inch)
    page.insert_image(rect2, filename=chart_image_avg_sentence_length)
    
    # Use incremental save when modifying an existing PDF
    doc.save(output_pdf, incremental=True, encryption=doc.is_encrypted)

# Function to format numbers in European style
def format_number(value, decimals=2):
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Streamlit app title
st.title("Auswertung PDFs")

uploaded_files = st.file_uploader("PDFs hochladen", type="pdf", accept_multiple_files=True)

if uploaded_files:
    data = []
    display_data = []  # formatted data for display
    for uploaded_file in uploaded_files:
        input_pdf = uploaded_file.name
        with open(input_pdf, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text
        text = extract_text(uploaded_file)

        # Identify definitions and explanations using spaCy
        explanations = identify_definitions_explanations_spacy(text)

        # Analyze consistency
        inconsistent_explanations = analyze_consistency(explanations)

        # Annotate PDF with feedback and return pages with inconsistencies
        output_pdf = f"annotated_{input_pdf}"
        inconsistency_pages = annotate_pdf_with_feedback(input_pdf, output_pdf, inconsistent_explanations)

        num_sentences = len(sent_tokenize(text, language='german'))
        total_words = sum(len(word_tokenize(sentence, language='german')) for sentence in sent_tokenize(text, language='german'))
        avg_sentence_length = total_words / num_sentences if num_sentences > 0 else 0

        # Convert unique pages with inconsistencies to a comma-separated string
        pages_with_inconsistencies = ', '.join(map(str, sorted(inconsistency_pages))) if inconsistency_pages else 'None'

        # Count the number of unique pages with inconsistencies
        count_of_inconsistencies = len(inconsistency_pages)

        data.append({
            'Titel Dokument': input_pdf,
            'Anzahl der Sätze': num_sentences,
            'Durchschnittliche Satzlänge': avg_sentence_length,
            'Anzahl der Inkonsistenzen': count_of_inconsistencies,
            'Seiten mit Inkonsistenzen': pages_with_inconsistencies
        })

        display_data.append({
            'Titel Dokument': input_pdf,
            'Anzahl der Sätze': format_number(num_sentences, 0),
            'Durchschnittliche Satzlänge': format_number(avg_sentence_length, 2),
            'Anzahl der Inkonsistenzen': count_of_inconsistencies,
            'Seiten mit Inkonsistenzen': pages_with_inconsistencies
        })

        # Generate and add comparative charts
        chart_image_sentences = f"chart_sentences_{input_pdf}.png"
        chart_image_avg_sentence_length = f"chart_avg_sentence_length_{input_pdf}.png"
        generate_comparative_charts(data, input_pdf, chart_image_sentences, chart_image_avg_sentence_length)
        add_charts_to_pdf(output_pdf, output_pdf, chart_image_sentences, chart_image_avg_sentence_length)

        # Create download button for annotated PDF
        with open(output_pdf, "rb") as file:
            st.download_button(
                label=f"Download annotated {input_pdf}",
                data=file,
                file_name=output_pdf,
                mime="application/pdf"
            )

    # Display analysis results in a table
    df_display = pd.DataFrame(display_data)
    st.table(df_display)

    # Display chart for average sentence length
    st.write("Durchschnittliche Satzlänge")
    plt.figure(figsize=(10, 5))
    plt.bar(df_display['Titel Dokument'], df_display['Durchschnittliche Satzlänge'].apply(lambda x: float(x.replace(',', '.'))), color=['blue', 'orange', 'green'])
    plt.axhline(y=pd.DataFrame(data)['Durchschnittliche Satzlänge'].mean(), color='r', linestyle='--', label='Durchschnitt')
    plt.xlabel('Titel Dokument')
    plt.ylabel('Durchschnittliche Satzlänge')
    plt.legend()
    st.pyplot(plt)

    # Display chart for number of sentences
    st.write("Anzahl der Sätze")
    plt.figure(figsize=(10, 5))
    plt.bar(df_display['Titel Dokument'], df_display['Anzahl der Sätze'].apply(lambda x: float(x.replace(',', '.'))), color=['blue', 'orange', 'green'])
    plt.axhline(y=pd.DataFrame(data)['Anzahl der Sätze'].mean(), color='r', linestyle='--', label='Durchschnitt')
    plt.xlabel('Titel Dokument')
    plt.ylabel('Anzahl der Sätze')
    plt.legend()
    st.pyplot(plt)
