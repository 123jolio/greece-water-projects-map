# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import re
import os
from streamlit.components.v1 import components

# Set page config first
st.set_page_config(
    page_title="Διαδραστικός Χάρτης Έργων Ύδρευσης",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Greek regions and prefectures with coordinates
GREEK_PREFECTURES_COORDS = {
    # Ανατολική Μακεδονία - Θράκη
    'Έβρος': {'lat': 40.8477, 'lon': 25.8738, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Ξάνθη': {'lat': 41.1355, 'lon': 24.8882, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Ροδόπη': {'lat': 41.1179, 'lon': 25.4064, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Καβάλα': {'lat': 40.9396, 'lon': 24.4019, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Δράμα': {'lat': 41.1533, 'lon': 24.1428, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    
    # Κεντρική Μακεδονία
    'Θεσσαλονίκη': {'lat': 40.6401, 'lon': 22.9444, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Ημαθία': {'lat': 40.5167, 'lon': 22.2, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Πέλλα': {'lat': 40.8, 'lon': 22.5, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Πιερία': {'lat': 40.3, 'lon': 22.6, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Σέρρες': {'lat': 41.0856, 'lon': 23.5469, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Κιλκίς': {'lat': 40.9939, 'lon': 22.8750, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Χαλκιδική': {'lat': 40.2, 'lon': 23.3, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Άγιον Όρος': {'lat': 40.16, 'lon': 24.28, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},

    # Δυτική Μακεδονία
    'Κοζάνη': {'lat': 40.30, 'lon': 21.78, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},
    'Γρεβενά': {'lat': 40.0833, 'lon': 21.4167, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},
    'Καστοριά': {'lat': 40.5167, 'lon': 21.2667, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},
    'Φλώρινα': {'lat': 40.7833, 'lon': 21.4167, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},

    # Ήπειρος
    'Άρτα': {'lat': 39.1667, 'lon': 20.9833, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    'Θεσπρωτία': {'lat': 39.5, 'lon': 20.25, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    'Ιωάννινα': {'lat': 39.6667, 'lon': 20.85, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    'Πρέβεζα': {'lat': 39.0833, 'lon': 20.75, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    
    # Αττική
    'Αττική': {'lat': 37.9838, 'lon': 23.7275, 'region': 'Αττική', 'color': '#45B7D1'},
    'Άγιο Όρος': {'lat': 40.2575, 'lon': 24.3258, 'region': 'Άγιο Όρος', 'color': '#D2B4DE'},
    'Νήσων (Αττική)': {'lat': 37.4, 'lon': 23.5, 'region': 'Αττική', 'color': '#45B7D1'},
    
    # Θεσσαλία
    'Θεσσαλία': {'lat': 39.6339, 'lon': 22.4194, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Λάρισα': {'lat': 39.6339, 'lon': 22.4194, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Μαγνησία': {'lat': 39.3681, 'lon': 22.9426, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Τρίκαλα': {'lat': 39.555, 'lon': 21.768, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Καρδίτσα': {'lat': 39.364, 'lon': 21.921, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    
    # Στερεά Ελλάδα
    'Στερεά Ελλάδα': {'lat': 38.5, 'lon': 22.5, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Εύβοια': {'lat': 38.5, 'lon': 24.0, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Βοιωτία': {'lat': 38.367, 'lon': 23.1, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Φθιώτιδα': {'lat': 38.9, 'lon': 22.4, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Φωκίδα': {'lat': 38.5, 'lon': 22.5, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Ευρυτανία': {'lat': 38.9, 'lon': 21.6, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    
    # Δυτική Ελλάδα
    'Αχαΐα': {'lat': 38.2466, 'lon': 21.7346, 'region': 'Δυτική Ελλάδα', 'color': '#DDA0DD'},
    'Αιτωλοακαρνανία': {'lat': 38.6, 'lon': 21.4, 'region': 'Δυτική Ελλάδα', 'color': '#DDA0DD'},
    'Ηλεία': {'lat': 37.8, 'lon': 21.3, 'region': 'Δυτική Ελλάδα', 'color': '#DDA0DD'},
    
    # Πελοπόννησος
    'Πελοπόννησος': {'lat': 37.5, 'lon': 22.3, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Αργολίδα': {'lat': 37.5, 'lon': 22.8, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Αρκαδία': {'lat': 37.4, 'lon': 22.3, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Κορινθία': {'lat': 37.9, 'lon': 22.9, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Λακωνία': {'lat': 37.0, 'lon': 22.4, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Μεσσηνία': {'lat': 37.0, 'lon': 21.9, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    
    # Ιόνια νησιά
    'Κέρκυρα': {'lat': 39.6243, 'lon': 19.9217, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Κεφαλληνία': {'lat': 38.1742, 'lon': 20.5275, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Ιθάκη': {'lat': 38.364, 'lon': 20.722, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Λευκάδα': {'lat': 38.8267, 'lon': 20.7033, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Ζάκυνθος': {'lat': 37.7833, 'lon': 20.9000, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    
    # Νότιο Αιγαίο
    'Νότιο Αιγαίο': {'lat': 36.4, 'lon': 25.4, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κυκλάδες': {'lat': 37.0, 'lon': 25.0, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Δωδεκάνησα': {'lat': 36.4, 'lon': 27.2, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Νάξος': {'lat': 37.1036, 'lon': 25.3779, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Πάρος': {'lat': 37.084, 'lon': 25.148, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Θήρα': {'lat': 36.3932, 'lon': 25.4615, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Τήνος': {'lat': 37.5375, 'lon': 25.1618, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Ρόδος': {'lat': 36.434, 'lon': 28.217, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Άνδρος': {'lat': 37.8333, 'lon': 24.9333, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κάλυμνος': {'lat': 36.95, 'lon': 26.9833, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Μήλος': {'lat': 36.7467, 'lon': 24.4444, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κως': {'lat': 36.894, 'lon': 27.288, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κέα - Κύθνος': {'lat': 37.65, 'lon': 24.3333, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κάρπαθος': {'lat': 35.507, 'lon': 27.213, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    
    # Βόρειο Αιγαίο
    'Βόρειο Αιγαίο': {'lat': 39.1, 'lon': 26.0, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Λέσβος': {'lat': 39.1, 'lon': 26.5, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Κρήτη': {'lat': 35.2401, 'lon': 24.8093, 'region': 'Κρήτη', 'color': '#FAD7A0'},
    'Χίος': {'lat': 38.4, 'lon': 26.1, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Σάμος': {'lat': 37.7, 'lon': 26.8, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Λήμνος': {'lat': 39.9167, 'lon': 25.2500, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Ικαρία': {'lat': 37.6167, 'lon': 26.1500, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    
    # Κρήτη
    'Κρήτη': {'lat': 35.3, 'lon': 24.8, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Ηράκλειο': {'lat': 35.3387, 'lon': 25.1442, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Χανιά': {'lat': 35.5, 'lon': 23.8, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Ρέθυμνο': {'lat': 35.4, 'lon': 24.5, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Λασίθι': {'lat': 35.2, 'lon': 25.7, 'region': 'Κρήτη', 'color': '#F8C471'},
    
    # Ήπειρος
    'Ήπειρος': {'lat': 39.5, 'lon': 20.5, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Ιωάννινα': {'lat': 39.6650, 'lon': 20.8537, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Άρτα': {'lat': 39.16, 'lon': 20.98, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Πρέβεζα': {'lat': 38.96, 'lon': 20.75, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Θεσπρωτία': {'lat': 39.5, 'lon': 20.2, 'region': 'Ήπειρος', 'color': '#82E0AA'},
}

# Comprehensive DEYA to Prefecture mapping - ΠΟΛΥ ΕΚΤΕΤΑΜΕΝΟ
DEYA_TO_PREFECTURE = {
    # Existing Entries...
    'ΔΕΥΑ ΑΒΔΗΡΩΝ': 'Ξάνθη', 'ΔΕΥΑ ΑΒΔΗΡΩΝ ': 'Ξάνθη',
    'ΔΕΥΑ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ': 'Έβρος', 'ΔΕΥΑ ΑΛΕΞΆΝΔΡΟΥΠΟΛΗΣ': 'Έβρος',
    'ΔΕΥΑ ΔΙΔΥΜΟΤΕΙΧΟΥ': 'Έβρος', 'ΔΕΥΑ ΟΡΕΣΤΙΑΔΑΣ': 'Έβρος',
    'ΔΕΥΑ ΞΑΝΘΗΣ': 'Ξάνθη', 'ΔΕΥΑ ΞΆΝΘΗΣ': 'Ξάνθη',
    'ΔΕΥΑ ΚΟΜΟΤΗΝΗΣ': 'Ροδόπη', 'ΔΕΥΑ ΚΟΜΟΤΉΝΗΣ': 'Ροδόπη',
    'ΔΕΥΑ ΚΑΒΑΛΑΣ': 'Καβάλα', 'ΔΕΥΑ ΚΑΒΆΛΑΣ': 'Καβάλα',
    'ΔΕΥΑ ΘΑΣΟΥ': 'Καβάλα', 'ΔΕΥΑ ΘΆΣΟΥ': 'Καβάλα',
    'ΔΕΥΑ ΠΑΓΓΑΙΟΥ': 'Καβάλα', 'ΔΕΥΑ ΠΑΓΓΑΊΟΥ': 'Καβάλα',
    'ΔΕΥΑ ΝΕΣΤΟΥ': 'Καβάλα', 'ΔΕΥΑ ΝΈΣΤΟΥ': 'Καβάλα', 'ΔΕΥΑ ΝΕΣΤΟΥ ': 'Καβάλα',
    'ΔΕΥΑ ΔΡΑΜΑΣ': 'Δράμα', 'ΔΕΥΑ ΔΡΆΜΑΣ': 'Δράμα',
    'Δήμος ΔΟΞΑΤΟΥ': 'Δράμα', 'Δήμος ΠΡΟΣΟΤΣΑΝΗΣ': 'Δράμα',
    'ΔΉΜΟΣ ΠΡΟΣΟΤΣΆΝΗΣ': 'Δράμα', 'Δήμος ΣΟΥΦΛΙΟΥ': 'Έβρος',
    'Δήμος ΙΑΣΜΟΥ': 'Ροδόπη', 'Δήμος ΜΑΡΩΝΕΙΑΣ - ΣΑΠΩΝ': 'Ροδόπη',
    'Δήμος ΚΑΤΩ ΝΕΥΡΟΚΟΠΙΟΥ': 'Δράμα', 'Δήμος ΠΑΡΑΝΕΣΤΙΟΥ': 'Δράμα',
    'Δήμος ΣΑΜΟΘΡΑΚΗΣ': 'Έβρος', 'Δήμος ΤΟΠΕΙΡΟΥ': 'Ξάνθη',
    'Δήμος ΜΥΚΗΣ': 'Ξάνθη', 'ΔΉΜΟΣ ΜΥΚΉΣ': 'Ξάνθη',
    'ΔΕΥΑ ΘΕΡΜΑΪΚΟΥ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΘΕΡΜΑΪΚΟΎ ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΒΕΡΟΙΑΣ': 'Ημαθία', 'ΔΕΥΑ ΒΈΡΟΙΑΣ': 'Ημαθία',
    'ΔΕΥΑ ΑΛΕΞΑΝΔΡΕΙΑΣ': 'Ημαθία', 'ΔΕΥΑ ΑΛΕΞΆΝΔΡΕΙΑΣ': 'Ημαθία',
    'ΔΕΥΑ Έδεσσας': 'Πέλλα', 'ΔΕΥΑ ΕΔΕΣΣΑΣ': 'Πέλλα',
    'ΔΕΥΑ ΑΛΜΩΠΙΑΣ': 'Πέλλα', 'ΔΕΥΑ ΑΛΜΩΠΊΑΣ': 'Πέλλα', 'ΔΕΥΑ ΑΛΜΩΠΙΑΣ ': 'Πέλλα',
    'ΔΕΥΑ ΔΙΟΥ-ΟΛΥΜΠΟΥ': 'Πιερία', 'ΔΕΥΑ ΔΊΟΥ-ΟΛΎΜΠΟΥ': 'Πιερία',
    'ΔΕΥΑ ΒΙΣΑΛΤΙΑΣ': 'Σέρρες', 'ΔΕΥΑ ΒΙΣΑΛΤΊΑΣ': 'Σέρρες',
    'ΔΕΥΑ ΗΡΑΚΛΕΙΑΣ': 'Σέρρες', 'ΔΕΥΑ ΗΡΑΚΛΕΊΑΣ': 'Σέρρες',
    'ΔΕΥΑ ΒΟΛΒΗΣ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΒΟΛΒΉΣ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΒΟΛΒΗΣ ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΔΗΜΟΥ ΔΕΛΤΑ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΔΉΜΟΥ ΔΈΛΤΑ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΚΙΛΚΙΣ': 'Κιλκίς', 'ΔΕΥΑ ΚΙΛΚΊΣ': 'Κιλκίς',
    'ΕΥΔΑΠ': 'Αττική', 'Ε.Υ.Δ.Α.Π.': 'Αττική',
    'ΔΕΥΑ ΒΟΛΟΥ': 'Μαγνησία', 'ΔΕΥΑ ΒΌΛΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΛΑΡΙΣΑΣ': 'Λάρισα', 'ΔΕΥΑ ΛΆΡΙΣΑΣ': 'Λάρισα',
    'ΔΕΥΑ ΤΡΙΚΑΛΩΝ': 'Τρίκαλα', 'ΔΕΥΑ ΤΡΙΚΆΛΩΝ': 'Τρίκαλα',
    'ΔΕΥΑ ΚΑΡΔΙΤΣΑΣ': 'Καρδίτσα', 'ΔΕΥΑ ΚΑΡΔΊΤΣΑΣ': 'Καρδίτσα',
    'ΔΕΥΑ ΚΕΡΚΥΡΑΣ': 'Κέρκυρα', 'ΔΕΥΑ ΚΈΡΚΥΡΑΣ': 'Κέρκυρα',
    'ΔΕΥΑ ΚΕΦΑΛΛΗΝΙΑΣ': 'Κεφαλληνία', 'ΔΕΥΑ ΚΕΦΑΛΛΗΝΊΑΣ': 'Κεφαλληνία',
    'ΔΕΥΑ ΖΑΚΥΝΘΟΥ': 'Ζάκυνθος', 'ΔΕΥΑ ΖΑΚΎΝΘΟΥ': 'Ζάκυνθος',
    'ΔΕΥΑ ΛΕΥΚΑΔΟΣ': 'Λευκάδα', 'ΔΕΥΑ ΛΕΥΚΆΔΟΣ': 'Λευκάδα',
    'ΔΕΥΑ ΑΙΓΙΑΛΕΙΑΣ': 'Αχαΐα', 'ΔΕΥΑ ΑΙΓΙΑΛΕΊΑΣ': 'Αχαΐα',
    'ΔΕΥΑ ΠΑΤΡΑΣ': 'Αχαΐα', 'ΔΕΥΑ ΠΆΤΡΑΣ': 'Αχαΐα',
    'ΔΕΥΑ ΜΕΣΟΛΟΓΓΙΟΥ': 'Αιτωλοακαρνανία', 'ΔΕΥΑ ΜΕΣΟΛΟΓΓΊΟΥ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΠΥΡΓΟΥ': 'Ηλεία', 'ΔΕΥΑ ΠΎΡΓΟΥ': 'Ηλεία',
    'ΔΕΥΑ ΧΑΛΚΙΔΑΣ': 'Εύβοια', 'ΔΕΥΑ ΧΑΛΚΊΔΑΣ': 'Εύβοια',
    'ΔΕΥΑ ΛΙΒΑΔΕΙΑΣ': 'Βοιωτία', 'ΔΕΥΑ ΛΙΒΑΔΕΊΑΣ': 'Βοιωτία',
    'ΔΕΥΑ ΛΑΜΙΑΣ': 'Φθιώτιδα', 'ΔΕΥΑ ΛΑΜΊΑΣ': 'Φθιώτιδα',
    'ΔΕΥΑ ΗΡΑΚΛΕΙΟΥ': 'Ηράκλειο', 'ΔΕΥΑ ΗΡΑΚΛΕΊΟΥ': 'Ηράκλειο',
    'ΔΕΥΑ ΧΑΝΙΩΝ': 'Χανιά', 'ΔΕΥΑ ΧΑΝΊΩΝ': 'Χανιά',
    'ΔΕΥΑ ΡΕΘΥΜΝΟΥ': 'Ρέθυμνο', 'ΔΕΥΑ ΡΕΘΎΜΝΟΥ': 'Ρέθυμνο',
    'ΔΕΥΑ ΛΑΣΙΘΙΟΥ': 'Λασίθι', 'ΔΕΥΑ ΛΑΣΙΘΊΟΥ': 'Λασίθι',
    'ΔΕΥΑ ΙΩΑΝΝΙΝΩΝ': 'Ιωάννινα', 'ΔΕΥΑ ΙΩΑΝΝΊΝΩΝ': 'Ιωάννινα',
    'ΔΕΥΑ ΑΡΤΑΣ': 'Άρτα', 'ΔΕΥΑ ΆΡΤΑΣ': 'Άρτα',
    'ΔΕΥΑ ΠΡΕΒΕΖΑΣ': 'Πρέβεζα', 'ΔΕΥΑ ΠΡΈΒΕΖΑΣ': 'Πρέβεζα',
    'ΔΕΥΑ ΚΟΡΙΝΘΟΥ': 'Κορινθία', 'ΔΕΥΑ ΚΟΡΊΝΘΟΥ': 'Κορινθία',
    'ΔΕΥΑ ΑΡΓΟΛΙΔΑΣ': 'Αργολίδα', 'ΔΕΥΑ ΑΡΓΟΛΊΔΑΣ': 'Αργολίδα',
    'ΔΕΥΑ ΣΠΑΡΤΗΣ': 'Λακωνία', 'ΔΕΥΑ ΣΠΆΡΤΗΣ': 'Λακωνία',
    'ΔΕΥΑ ΚΑΛΑΜΑΤΑΣ': 'Μεσσηνία', 'ΔΕΥΑ ΚΑΛΑΜΆΤΑΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΤΡΙΠΟΛΗΣ': 'Αρκαδία', 'ΔΕΥΑ ΤΡΊΠΟΛΗΣ': 'Αρκαδία',
    'ΔΕΥΑ ΣΥΡΟΥ': 'Κυκλάδες', 'ΔΕΥΑ ΣΎΡΟΥ': 'Κυκλάδες',
    'ΔΕΥΑ ΜΥΚΟΝΟΥ': 'Κυκλάδες', 'ΔΕΥΑ ΜΥΚΌΝΟΥ': 'Κυκλάδες',
    'ΔΕΥΑ ΣΑΝΤΟΡΙΝΗΣ': 'Κυκλάδες', 'ΔΕΥΑ ΣΑΝΤΟΡΊΝΗΣ': 'Κυκλάδες',
    'ΔΕΥΑ ΡΟΔΟΥ': 'Δωδεκάνησα', 'ΔΕΥΑ ΡΌΔΟΥ': 'Δωδεκάνησα',
    'ΔΕΥΑ ΚΩ': 'Δωδεκάνησα', 'ΔΕΥΑ ΚΩΣ': 'Δωδεκάνησα',
    'ΔΕΥΑ ΜΥΤΙΛΗΝΗΣ': 'Λέσβος', 'ΔΕΥΑ ΜΥΤΙΛΉΝΗΣ': 'Λέσβος',
    'ΔΕΥΑ ΧΙΟΥ': 'Χίος', 'ΔΕΥΑ ΧΊΟΥ': 'Χίος',
    'ΔΕΥΑ ΣΑΜΟΥ': 'Σάμος', 'ΔΕΥΑ ΣΆΜΟΥ': 'Σάμος',
    'ΔΕΥΑ ΛΗΜΝΟΥ': 'Λήμνος', 'ΔΕΥΑ ΛΉΜΝΟΥ': 'Λήμνος',
    
    # --- ΝΕΕΣ ΠΡΟΣΘΗΚΕΣ ---
    'ΔΕΥΑ ΒΟΡΕΙΟΥ ΑΞΟΝΑ ΧΑΝΙΩΝ': 'Χανιά',
    'ΔΕΥΑ ΘΗΒΑΙΩΝ': 'Βοιωτία',
    'ΔΗΜΟΣ ΑΝΩΓΕΙΩΝ': 'Ρέθυμνο',
    'ΔΕΥΑ ΠΑΙΟΝΙΑΣ': 'Κιλκίς',
    'ΔΕΥΑ ΧΑΛΚΗΔΟΝΟΣ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΚΥΜΗΣ - ΑΛΙΒΕΡΙΟΥ': 'Εύβοια',
    'ΔΕΥΑ. ΔΙΟΥ ΟΛΥΜΠΟΥ': 'Πιερία',
    'ΔΗΜΟΣ ΛΗΜΝΟΥ': 'Λήμνος',
    'ΔΕΥΑ ΛΕΣΒΟΥ': 'Λέσβος',
    'ΔΕΥΑ ΣΕΡΡΩΝ': 'Σέρρες',
    'ΔΕΥΑ ΑΓΡΙΝΙΟΥ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΠΥΛΟΥ-ΝΕΣΤΟΡΟΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΔΕΛΦΩΝ': 'Φωκίδα',
    'ΔΗΜΟΣ ΑΜΟΡΓΟΥ': 'Νάξος',
    'ΔΕΥΑ ΜΑΛΕΒΙΖΙΟΥ': 'Ηράκλειο',
    'ΔΕΥΑ ΠΑΡΟΥ': 'Πάρος',
    'ΔΗΜΟΣ ΦΥΛΗΣ': 'Αττική',
    'ΔΕΥΑ ΜΕΤΕΩΡΩΝ': 'Τρίκαλα',
    'ΔΕΥΑ ΘΗΡΑΣ': 'Θήρα',
    'ΔΗΜΟΣ ΤΗΝΟΥ': 'Τήνος',
    'ΔΕΥΑ ΣΚΟΠΕΛΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΕΡΜΙΟΝΙΔΑΣ (ΚΡΑΝΙΔΙΟΥ)': 'Αργολίδα',
    'ΔΗΜΟΣ ΜΑΚΡΑΚΩΜΗΣ': 'Φθιώτιδα',
    'ΔΕΥΑ ΤΥΡΝΑΒΟΥ': 'Λάρισα',
    'ΔΕΥΑ ΚΕΦΑΛΟΝΙΑΣ': 'Κεφαλληνία',
    'ΔΗΜΟΣ ΝΑΞΟΥ ΚΑΙ ΜΙΚΡΩΝ ΚΥΚΛΑΔΩΝ': 'Νάξος',
    'ΔΗΜΟΣ ΜΟΝΕΜΒΑΣΙΑΣ': 'Λακωνία',
    'ΔΕΥΑ ΜΙΝΩΑ ΠΕΔΙΑΔΑΣ': 'Ηράκλειο',
    'ΔΕΥΑ ΠΑΤΡΕΩΝ': 'Αχαΐα',
    'ΔΗΜΟΣ ΑΡΙΣΤΟΤΕΛΗ': 'Χαλκιδική',
    'ΔΕΥΑ ΧΕΡΣΟΝΗΣΟΥ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΑΡΧΑΝΩΝ ΑΣΤΕΡΟΥΣΙΩΝ': 'Ηράκλειο',
    'ΔΕΥΑ ΑΡΓΟΥΣ - ΜΥΚΗΝΩΝ': 'Αργολίδα',
    'ΟΡΓΑΝΙΣΜΟΣ ΑΝΑΠΤΥΞΗΣ ΚΡΗΤΗΣ Α.Ε. (ΟΑΚ ΑΕ)': 'Κρήτη',
    'ΔΕΥΑ ΕΛΑΣΣΟΝΑΣ': 'Λάρισα',
    'ΔΗΜΟΣ ΑΜΥΝΤΑΙΟΥ': 'Φλώρινα',
    'ΔΕΥΑ ΠΑΛΑΜΑ': 'Καρδίτσα',
    'ΔΗΜΟΣ ΑΜΦΙΚΛΕΙΑΣ -ΕΛΑΤΕΙΑΣ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΑΜΦΙΛΟΧΙΑΣ': 'Αιτωλοακαρνανία',
    'ΔΗΜΟΣ ΑΡΓΟΥΣ ΟΡΕΣΤΙΚΟΥ': 'Καστοριά',
    'ΙΜ ΜΕΓΙΣΤΗΣ ΛΑΥΡΑΣ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΓΑΥΔΟΥ': 'Χανιά',
    'ΔΕΥΑ ΞΥΛΟΚΑΣΤΡΟΥ - ΕΥΡΩΣΤΙΝΗΣ': 'Κορινθία',
    'ΔΗΜΟΣ ΟΙΧΑΛΙΑΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΚΑΣΤΟΡΙΑΣ': 'Καστοριά',
    'ΔΕΥΑ ΒΟΪΟΥ': 'Κοζάνη',
    'ΔΗΜΟΣ ΣΕΡΒΙΩΝ': 'Κοζάνη',
    'ΔΗΜΟΣ ΛΙΜΝΗΣ ΠΛΑΣΤΗΡΑ': 'Καρδίτσα',
    'ΔΕΥΑ ΕΡΕΤΡΙΑΣ': 'Εύβοια',
    'ΔΕΥΑ ΝΑΥΠΛΙΕΩΝ': 'Αργολίδα',
    'ΔΗΜΟΣ ΔΥΤΙΚΗΣ ΜΑΝΗΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΒΟΡΕΙΑΣ ΚΥΝΟΥΡΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΕΜΜΑΝΟΥΗΛ ΠΑΠΠΑ': 'Σέρρες',
    'ΔΗΜΟΣ ΔΩΔΩΝΗΣ': 'Ιωάννινα',
    'ΙΜ ΣΙΜΩΝΟΣ ΠΕΤΡΑΣ': 'Άγιον Όρος',
    'ΙΜ ΞΕΝΟΦΩΝΤΟΣ': 'Άγιον Όρος',
    'ΔΕΥΑ. ΠΕΛΛΑΣ': 'Πέλλα',
    'ΔΗΜΟΣ ΛΕΥΚΑΔΑΣ': 'Λευκάδα',
    'ΔΗΜΟΣ ΠΡΕΒΕΖΗΣ': 'Πρέβεζα',
    'ΔΗΜΟΣ ΠΑΡΓΑΣ': 'Πρέβεζα',
    'ΔΗΜΟΣ ΜΕΤΣΟΒΟΥ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΞΗΡΟΜΕΡΟΥ': 'Αιτωλοακαρνανία',
    'ΔΗΜΟΣ ΔΩΡΙΔΟΣ': 'Φωκίδα',
    'ΔΗΜΟΣ ΓΟΡΤΥΝΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΙΕΡΑΠΕΤΡΑΣ': 'Λασίθι',
    'ΔΗΜΟΣ ΛΟΚΡΩΝ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΔΙΣΤΟΜΟΥ - ΑΡΑΧΟΒΑΣ - ΑΝΤΙΚΥΡΑΣ': 'Βοιωτία',
    'ΔΗΜΟΣ ΚΑΡΥΣΤΟΥ': 'Εύβοια',
    'ΔΗΜΟΣ ΤΡΟΙΖΗΝΙΑΣ ΜΕΘΑΝΩΝ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΦΙΛΙΑΤΩΝ': 'Θεσπρωτία',
    'ΔΕΥΑ ΦΑΡΣΑΛΩΝ': 'Λάρισα',
    'ΔΕΥΑ ΑΡΧΑΙΑΣ ΟΛΥΜΠΙΑΣ': 'Ηλεία',
    'ΔΗΜΟΣ ΖΙΤΣΑΣ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΣΕΡΙΦΟΥ': 'Μήλος',
    'ΔΗΜΟΣ ΑΓΙΟΥ ΕΥΣΤΡΑΤΙΟΥ': 'Λήμνος',
    'ΔΗΜΟΣ ΜΕΓΑΛΟΠΟΛΗΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΤΗΛΟΥ': 'Ρόδος',
    'ΔΗΜΟΣ ΠΡΕΣΠΩΝ': 'Φλώρινα',
    'ΔΗΜΟΣ ΑΚΤΙΟΥ - ΒΟΝΙΤΣΑΣ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΝΑΥΠΑΚΤΙΑΣ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΧΑΛΚΙΔΕΩΝ': 'Εύβοια',
    'ΔΕΥΑ ΛΟΥΤΡΑΚΙΟΥ - ΠΕΡΑΧΩΡΑΣ': 'Κορινθία',
    'ΔΕΥΑ ΣΙΚΥΩΝΙΩΝ': 'Κορινθία',
    'ΔΗΜΟΣ ΑΓΡΑΦΩΝ': 'Ευρυτανία',
    'ΔΗΜΟΣ ΣΤΥΛΙΔΑΣ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΑΝΔΡΟΥ': 'Άνδρος',
    'ΔΗΜΟΣ ΕΥΡΩΤΑ': 'Λακωνία',
    'ΔΗΜΟΣ ΑΣΤΥΠΑΛΑΙΑΣ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΑΛΙΑΡΤΟΥ ΘΕΣΠΕΩΝ': 'Βοιωτία',
    'ΔΕΥΑ ΣΚΥΔΡΑΣ': 'Πέλλα',
    'ΔΕΥΑ ΘΕΡΜΗΣ': 'Θεσσαλονίκη',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΛΕΚΑΝΟΠΕΔΙΟΥ ΙΩΑΝΝΙΝΩΝ': 'Ιωάννινα',
    'ΔΕΥΑ ΡΗΓΑ ΦΕΡΑΙΟΥ': 'Μαγνησία',
    'ΔΗΜΟΣ ΣΟΥΛΙΟΥ': 'Θεσπρωτία',
    'ΔΗΜΟΣ ΑΛΟΝΝΗΣΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΠΥΛΗΣ ΤΡΙΚΑΛΩΝ': 'Τρίκαλα',
    'ΔΕΥΑ ΣΚΙΑΘΟΥ': 'Μαγνησία',
    'ΔΗΜΟΣ ΒΟΡΕΙΩΝ ΤΖΟΥΜΕΡΚΩΝ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΚΟΝΙΤΣΑΣ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΠΩΓΩΝΙΟΥ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΑΜΑΡΙΟΥ': 'Ρέθυμνο',
    'ΔΗΜΟΣ ΒΕΛΟΥ ΒΟΧΑΣ': 'Κορινθία',
    'ΔΕΥΑ ΗΓΟΥΜΕΝΙΤΣΑΣ': 'Θεσπρωτία',
    'ΔΗΜΟΣ ΚΕΝΤΡΙΚΩΝ ΤΖΟΥΜΕΡΚΩΝ': 'Άρτα',
    'ΔΗΜΟΣ ΠΑΞΩΝ': 'Κέρκυρα',
    'ΔΕΥΑ ΜΥΛΟΠΟΤΑΜΟΥ': 'Ρέθυμνο',
    'ΔΕΥΑ ΣΕΛΙΝΟΥ': 'Χανιά',
    'ΔΗΜΟΣ ΓΟΡΤΥΝΑΣ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΜΕΓΑΡΕΩΝ': 'Αττική',
    'ΔΕΥΑ ΣΥΜΗΣ': 'Ρόδος',
    'ΔΗΜΟΣ ΟΡΧΟΜΕΝΟΥ': 'Βοιωτία',
    'ΔΗΜΟΣ ΚΑΛΑΒΡΥΤΩΝ': 'Αχαΐα',
    'ΙΜ ΔΟΧΕΙΑΡΙΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΠΥΛΑΙΑΣ - ΧΟΡΤΙΑΤΗ': 'Θεσσαλονίκη',
    'ΙΜ ΓΡΗΓΟΡΙΟΥ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΝΕΑΣ ΠΡΟΠΟΝΤΙΔΑΣ': 'Χαλκιδική',
    'ΔΕΥΑ ΑΡΤΑΙΩΝ': 'Άρτα',
    'ΔΗΜΟΣ ΖΗΡΟΥ': 'Πρέβεζα',
    'ΔΗΜΟΣ ΚΑΜΕΝΩΝ ΒΟΥΡΛΩΝ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΔΟΜΟΚΟΥ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΠΗΝΕΙΟΥ': 'Ηλεία',
    'ΔΗΜΟΣ ΚΥΘΗΡΩΝ': 'Νήσων (Αττική)',
    'ΔΕΥΑ ΣΗΤΕΙΑΣ ΛΑΣΙΘΙΟΥ': 'Λασίθι',
    'ΔΗΜΟΣ ΧΑΛΚΗΣ': 'Ρόδος',
    'ΔΕΥΑ ΛΑΥΡΕΩΤΙΚΗΣ': 'Αττική',
    'ΔΗΜΟΣ ΡΑΦΗΝΑΣ - ΠΙΚΕΡΜΙΟΥ': 'Αττική',
    'ΔΕΥΑ ΜΕΣΣΗΝΗΣ': 'Μεσσηνία',
    'ΔΗΜΟΣ ΠΟΡΟΥ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΗΡΩΙΚΗΣ Ν. ΨΑΡΩΝ': 'Χίος',
    'ΔΗΜΟΣ ΔΥΤΙΚΗΣ ΣΑΜΟΥ': 'Σάμος',
    'ΔΕΥΑ ΤΡΙΦΥΛΙΑΣ': 'Μεσσηνία',
    'ΔΗΜΟΣ ΝΟΤΙΑΣ ΚΥΝΟΥΡΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΠΟΛΥΓΥΡΟΥ': 'Χαλκιδική',
    'ΔΗΜΟΣ ΖΑΓΟΡΙΟΥ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΖΑΓΟΡΑΣ - ΜΟΥΡΕΣΙΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΖΑΧΑΡΩΣ': 'Ηλεία',
    'ΔΕΥΑ ΦΛΩΡΙΝΑΣ': 'Φλώρινα',
    'ΔΗΜΟΣ ΝΕΣΤΟΡΙΟΥ': 'Καστοριά',
    'ΔΕΥΑ ΓΡΕΒΕΝΩΝ': 'Γρεβενά',
    'ΙΜ ΙΒΗΡΩΝ': 'Άγιον Όρος',
    'ΙΜ ΞΗΡΟΠΟΤΑΜΟΥ': 'Άγιον Όρος',
    'ΙΜ ΠΑΝΤΟΚΡΑΤΟΡΟΣ': 'Άγιον Όρος',
    'ΙΜ ΖΩΓΡΑΦΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΛΑΓΚΑΔΑ': 'Θεσσαλονίκη',
    'ΔΗΜΟΣ ΤΑΝΑΓΡΑΣ': 'Βοιωτία',
    'ΔΗΜΟΣ ΝΙΚΟΛΑΟΥ ΣΚΟΥΦΑ': 'Άρτα',
    'ΔΕΥΑ ΦΑΡΚΑΔΟΝΑΣ': 'Τρίκαλα',
    'ΔΕΥΑ ΑΛΜΥΡΟΥ': 'Μαγνησία',
    'ΔΗΜΟΣ ΔΙΟΝΥΣΟΥ': 'Αττική',
    'ΔΕΥΑ.ΝΑΟΥΣΑΣ': 'Ημαθία',
    'ΔΗΜΟΣ ΓΕΩΡΓΙΟΥ ΚΑΡΑΪΣΚΑΚΗ': 'Άρτα',
    'ΙΜ ΚΟΥΤΛΟΥΜΟΥΣΙΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΩΡΑΙΟΚΑΣΤΡΟΥ': 'Θεσσαλονίκη',
    'ΙΜ ΕΣΦΙΓΜΕΝΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΔΥΜΑΙΩΝ': 'Αχαΐα',
    'ΔΕΥΑ ΑΓΙΑΣ': 'Λάρισα',
    'ΔΗΜΟΣ ΙΘΑΚΗΣ': 'Ιθάκη',
    'ΙΜ ΣΤΑΥΡΟΝΙΚΗΤΑ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΒΕΛΒΕΝΤΟΥ': 'Κοζάνη',
    'ΔΕΥΑ ΣΟΦΑΔΩΝ': 'Καρδίτσα',
    'ΔΗΜΟΣ ΚΕΑΣ': 'Κέα - Κύθνος',
    'ΔΗΜΟΣ ΚΙΣΣΑΜΟΥ': 'Χανιά',
    'ΔΗΜΟΣ ΑΠΟΚΟΡΩΝΟΥ': 'Χανιά',
    'ΔΗΜΟΣ ΣΠΑΤΩΝ ΑΡΤΕΜΙΔΟΣ': 'Αττική',
    'ΔΗΜΟΣ ΝΙΣΥΡΟΥ': 'Κως',
    'ΔΕΥΑ ΚΑΛΥΜΝΟΥ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΙΣΤΙΑΙΑΣ - ΑΙΔΗΨΟΥ': 'Εύβοια',
    'ΔΗΜΟΣ ΜΑΝΔΡΑΣ-ΕΙΔΥΛΛΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΑΙΓΙΝΑΣ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΛΕΡΟΥ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΣΠΕΤΣΩΝ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΑΓΚΙΣΤΡΙΟΥ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΣΚΥΡΟΥ': 'Εύβοια',
    'ΔΗΜΟΣ ΕΡΥΜΑΝΘΟΥ': 'Αχαΐα',
    'ΔΗΜΟΣ ΚΥΘΝΟΥ': 'Κέα - Κύθνος',
    'ΔΗΜΟΣ ΗΡΩΪΚΗΣ ΝΗΣΟΥ ΚΑΣΟΥ': 'Κάρπαθος',
    'ΔΕΥΑ ΔΕΣΚΑΤΗΣ': 'Γρεβενά',
    'ΙΜ ΦΙΛΟΘΕΟΥ': 'Άγιον Όρος',
    'ΙΜ ΧΙΛΑΝΔΑΡΙΟΥ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΠΥΔΝΑΣ-ΚΟΛΙΝΔΡΟΥ': 'Πιερία',
    'ΔΕΥΑ ΦΑΙΣΤΟΥ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΦΟΛΕΓΑΝΔΡΟΥ': 'Θήρα',
    'ΔΗΜΟΣ ΜΗΛΟΥ': 'Μήλος',
    'ΔΗΜΟΣ ΣΙΚΙΝΟΥ': 'Θήρα',
    'ΔΗΜΟΣ ΟΙΝΟΥΣΣΩΝ': 'Χίος',
    'ΔΕΥΑ ΑΝΑΤΟΛΙΚΗΣ ΜΑΝΗΣ': 'Λακωνία',
    'ΔΗΜΟΣ ΚΡΩΠΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΣΑΡΩΝΙΚΟΥ': 'Αττική',
    'ΔΕΥΑ ΠΕΛΛΑΣ': 'Πέλλα',
    'ΔΗΜΟΣ ΑΜΦΙΠΟΛΗΣ': 'Σέρρες',
    'ΔΗΜΟΣ ΣΙΘΩΝΙΑΣ': 'Χαλκιδική',
    'ΔΗΜΟΣ ΚΑΣΣΑΝΔΡΑΣ': 'Χαλκιδική',
    'ΙΜ ΒΑΤΟΠΑΙΔΙΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΝΑΟΥΣΑΣ': 'Ημαθία',
    'ΔΗΜΟΣ ΘΕΡΜΟΥ': 'Αιτωλοακαρνανία',
    'ΔΗΜΟΣ ΗΛΙΔΑΣ': 'Ηλεία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΚΑΡΔΙΤΣΑΣ ΚΑΙ ΛΟΙΠΩΝ ΔΗΜΩΝ': 'Καρδίτσα',
    'ΔΗΜΟΣ ΑΡΓΙΘΕΑΣ': 'Καρδίτσα',
    'ΔΕΥΑ ΣΙΝΤΙΚΗΣ': 'Σέρρες',
    'ΔΗΜΟΣ ΔΙΟΥ-ΟΛΥΜΠΟΥ': 'Πιερία',
    'ΔΗΜΟΣ ΜΑΡΚΟΠΟΥΛΟΥ ΜΕΣΟΓΑΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΚΗΦΙΣΙΑΣ': 'Αττική',
    'ΔΕΥΑ ΜΑΝΤΟΥΔΙΟΥ-ΛΙΜΝΗΣ-ΑΓΙΑΣ ΑΝΝΑΣ': 'Εύβοια',
    'ΔΙΑΒΑΘΜΙΔΙΚΟΣ ΣΥΝΔΕΣΜΟΣ ΗΛΕΙΑΣ ΤΗΣ ΠΕΡΙΦΕΡΕΙΑΣ ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ': 'Ηλεία',
    'ΔΗΜΟΣ ΚΑΡΠΕΝΗΣΙΟΥ': 'Ευρυτανία',
    'ΔΗΜΟΣ ΑΝΔΡΑΒΙΔΑΣ - ΚΥΛΛΗΝΗΣ': 'Ηλεία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ Ο.Τ.Α. Ν. ΦΘΙΩΤΙΔΑΣ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΠΑΙΑΝΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΣΑΛΑΜΙΝΑΣ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΥΔΡΑΣ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΩΡΩΠΙΩΝ': 'Αττική',
    'ΔΗΜΟΣ ΒΡΙΛΗΣΣΙΩΝ': 'Αττική',
    'ΔΗΜΟΣ ΚΑΡΠΑΘΟΥ': 'Κάρπαθος',
    'ΔΗΜΟΣ ΑΓΑΘΟΝΗΣΙΟΥ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΑΝΑΦΗΣ': 'Θήρα',
    'ΔΗΜΟΣ ΕΛΑΦΟΝΗΣΟΥ': 'Λακωνία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΔΗΜΩΝ ΚΑΛΑΜΑΤΑΣ - ΜΕΣΣΗΝΗΣ': 'Μεσσηνία',
    'ΔΗΜΟΣ ΛΕΙΨΩΝ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΚΙΜΩΛΟΥ': 'Μήλος',
    'ΔΗΜΟΣ ΑΝΤΙΠΑΡΟΥ': 'Πάρος',
    'ΔΗΜΟΣ ΣΙΦΝΟΥ': 'Μήλος',
    'ΠΕΡΙΦΕΡΕΙΑ ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ': 'Νότιο Αιγαίο',
    'ΔΗΜΟΣΙΗΤΩΝ': 'Θήρα', 
    'ΔΗΜΟΣ ΟΡΟΠΕΔΙΟΥ ΛΑΣΙΘΙΟΥ': 'Λασίθι',
    'ΔΗΜΟΣ ΣΦΑΚΙΩΝ': 'Χανιά',

    # Corrections for unmapped items
    'ΔΕΥΑ ΚΙΛΕΛΕΡ': 'Λάρισα',
    'ΔΗΜΟΣ ΝΟΤΙΟΥ ΠΗΛΙΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΒΟΡΕΙΟΥ ΑΞΟΝΑ ΧΑΝΙΩΝ': 'Χανιά',

    # New batch of unmapped items from user
    'ΙΜ ΑΓΙΟΥ ΠΑΥΛΟΥ': 'Άγιο Όρος',
    'ΔΕΥΑ ΚΟΖΑΝΗΣ': 'Κοζάνη',
    'ΕΥΑΘ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΜΟΥΖΑΚΙΟΥ': 'Καρδίτσα',
    'ΔΕΥΑ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ': 'Λασίθι',
    'ΔΗΜΟΣ ΙΚΑΡΙΑΣ': 'Σάμος',
    'ΔΗΜΟΣ ΑΓΙΟΥ ΒΑΣΙΛΕΙΟΥ': 'Ρέθυμνο',
    'ΔΗΜΟΣ ΒΙΑΝΝΟΥ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΝΕΑΣ ΖΙΧΝΗΣ': 'Σέρρες',
    'ΔΕΥΑ ΚΑΤΕΡΙΝΗΣ': 'Πιερία',
    'ΔΕΥΑ ΖΑΚΥΝΘΙΩΝ': 'Ζάκυνθος',
    'ΔΕΥΑ ΤΕΜΠΩΝ': 'Λάρισα',
    'ΔΕΥΑ ΕΟΡΔΑΙΑΣ': 'Κοζάνη',
    'ΔΗΜΟΣ ΑΝΑΤΟΛΙΚΗΣ ΣΑΜΟΥ': 'Σάμος',
    'ΔΗΜΟΣ ΜΑΡΑΘΩΝΟΣ': 'Αττική',
    'ΔΕΥΑ ΕΠΙΔΑΥΡΟΥ': 'Αργολίδα',
    'ΔΗΜΟΣ ΦΟΥΡΝΩΝ ΚΟΡΣΕΩΝ': 'Σάμος',
    'ΔΗΜΟΣ ΑΜΥΝΤΑΙΟΥ': 'Φλώρινα',
    'ΔΕΥΑ ΒΟΡΕΙΑΣ ΚΥΝΟΥΡΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΗΛΙΔΑΣ': 'Ηλεία',
    'ΔΗΜΟΣ ΣΑΛΑΜΙΝΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΘΕΡΜΟΥ': 'Αιτωλοακαρνανία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΔΗΜΩΝ ΚΑΛΑΜΑΤΑΣ - ΜΕΣΣΗΝΗΣ & ΚΟΙΝΟΤΗΤΩΝ ΠΕΡΙΟΧΗΣ ΚΑΛΑΜΑΤΑΣ': 'Μεσσηνία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ Ο.Τ.Α. Ν. ΦΘΙΩΤΙΔΑΣ ΑΠΟ ΠΗΓΕΣ "ΚΑΝΑΛΙΑ" ΠΥΡΓΟΥ ΥΠΑΤΗΣ': 'Φθιώτιδα',
    'ΟΤΑ Β\' ΒΑΘΜΟΥ ΠΕΡΙΦΕΡΕΙΑ ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ': 'Νότιο Αιγαίο'
}

def normalize_greek(text):
    """
    Normalizes a Greek string by converting to uppercase, removing accents,
    and stripping extra whitespace and punctuation.
    """
    if not isinstance(text, str):
        return ''
        
    text = text.upper().strip()
    
    # Define accent mappings
    replacements = {
        'Ά': 'Α', 'Έ': 'Ε', 'Ή': 'Η', 'Ί': 'Ι', 'Ό': 'Ο', 'Ύ': 'Υ', 'Ώ': 'Ω',
        'Ϊ': 'Ι', 'Ϋ': 'Υ'
    }
    
    for accented, unaccented in replacements.items():
        text = text.replace(accented, unaccented)
        
    # Remove common punctuation and collapse whitespace
    text = re.sub(r'[\.\(\)-]', ' ', text) # Replace punctuation with a space
    text = re.sub(r'\s+', ' ', text).strip() # Collapse multiple spaces to one and strip again
    
    return text

@st.cache_data(ttl=3600, show_spinner="Analyzing Excel file...")
def load_and_analyze_excel_enhanced(excel_file):
    """Enhanced loading with comprehensive data analysis."""
    try:
        df = pd.read_excel(excel_file, sheet_name=0)
        
        # Basic data cleaning
        df = df.dropna(how='all')
        
        # Clean string columns
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(['nan', 'None', '', 'NaN'], pd.NA)
        
        # Add prefecture mapping
        water_utility_col = None
        for col_name in ['Φορέας Ύδρευσης', 'ΔΕΥΑ', 'Φορέας', 'Water_Utility']:
            if col_name in df.columns:
                water_utility_col = col_name
                break
        
        if water_utility_col is None:
            df['Φορέας Ύδρευσης'] = 'Άγνωστος'
            water_utility_col = 'Φορέας Ύδρευσης'
        
        # Create normalized mapping
        df['normalized_utility'] = df[water_utility_col].apply(normalize_greek)
        normalized_map = {normalize_greek(k): v for k, v in DEYA_TO_PREFECTURE.items()}
        df['Νομός'] = df['normalized_utility'].map(normalized_map).fillna('Άλλος')
        
        # Add region mapping
        df['Περιφέρεια'] = df['Νομός'].map(
            lambda x: GREEK_PREFECTURES_COORDS.get(x, {}).get('region', 'Άλλη')
        )
        
        # Convert budget column if exists
        budget_column = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
        if budget_column in df.columns:
            df[budget_column] = df[budget_column].astype(str).str.replace(',', '').str.replace('€', '').str.replace(' ', '')
            df[budget_column] = pd.to_numeric(df[budget_column], errors='coerce')
        
        # Add project type column
        if 'Κατηγορία Έργου' not in df.columns:
            df['Κατηγορία Έργου'] = 'Άλλο'
        
        return df
        
    except Exception as e:
        st.error(f"❌ Σφάλμα φόρτωσης: {e}")
        return None

def create_interactive_map_by_prefecture(df):
    """Create interactive map showing projects by prefecture (νομός)."""
    center_lat, center_lon = 39.0, 22.0
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=6, 
        tiles='OpenStreetMap'
    )
    
    # ... (rest of the function remains the same)

    # Enhanced legend with more regions
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 320px; height: 240px; 
                background-color: white; border:3px solid grey; z-index:9999; 
                font-size:11px; padding: 12px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    <h4 style="margin-top: 0; color: #333; text-align: center;">🗺️ Χάρτης Έργων ανά Νομό</h4>
    <hr style="margin: 8px 0;">
    <div style="columns: 2; column-gap: 15px;">
    <p><i class="fa fa-circle" style="color:#FF6B6B"></i> Ανατ. Μακεδονία - Θράκη</p>
    <p><i class="fa fa-circle" style="color:#4ECDC4"></i> Κεντρική Μακεδονία</p>
    <p><i class="fa fa-circle" style="color:#45B7D1"></i> Αττική</p>
    <p><i class="fa fa-circle" style="color:#96CEB4"></i> Θεσσαλία</p>
    <p><i class="fa fa-circle" style="color:#FFEAA7"></i> Στερεά Ελλάδα</p>
    <p><i class="fa fa-circle" style="color:#DDA0DD"></i> Δυτική Ελλάδα</p>
    <p><i class="fa fa-circle" style="color:#98D8C8"></i> Πελοπόννησος</p>
    <p><i class="fa fa-circle" style="color:#F7DC6F"></i> Ιόνια νησιά</p>
    <p><i class="fa fa-circle" style="color:#BB8FCE"></i> Νότιο Αιγαίο</p>
    <p><i class="fa fa-circle" style="color:#85C1E9"></i> Βόρειο Αιγαίο</p>
    <p><i class="fa fa-circle" style="color:#F8C471"></i> Κρήτη</p>
    <p><i class="fa fa-circle" style="color:#82E0AA"></i> Ήπειρος</p>
    </div>
    <hr style="margin: 8px 0;">
    <p style="text-align: center; font-size: 10px; color: #666;">
    <strong>Μέγεθος κύκλου</strong> = Αριθμός έργων ανά νομό<br>
    <strong>Αριθμός</strong> = Συνολικά έργα νομού
    </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

def create_interactive_charts(df, selected_region=None, selected_prefecture=None):
    """Create interactive Plotly charts."""
    
    # ... (rest of the function remains the same)

def main():
    """Main function to run the Streamlit app."""
    # Add custom CSS for better performance
    st.markdown("""
    <style>
        /* Hide Streamlit default elements */
        .main > div:first-child { padding-top: 0; }
        /* Optimize rendering */
        .stDataFrame { width: 100% !important; }
        /* Improve sidebar performance */
        .sidebar .sidebar-content { will-change: auto; }
    </style>
    """, unsafe_allow_html=True)
    
    # --- Sidebar --- #
    with st.sidebar:
        # Clear cache button
        if st.button('🔄 Επαναφόρτωση & Καθαρισμός Cache'):
            st.cache_data.clear()
            st.rerun()
            
        # FIXED: Simplified logo loading
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        elif os.path.exists("loho.png"):
            st.image("loho.png", use_container_width=True)
        else:
            st.markdown("### 🗺️ Έργα Ύδρευσης")
            
        st.title("🗺️ Διαδραστικός Χάρτης Έργων Ύδρευσης")
        st.markdown("---")
    
    # Main content
    st.title("🗺️ Διαδραστικός Χάρτης Έργων Ύδρευσης Ελλάδας")
    st.markdown("**🚀 Διαδραστική ανάλυση έργων ύδρευσης ανά νομό και περιφέρεια**")
    
    # Enhanced sidebar
    with st.sidebar:
        st.header("📂 Φόρτωση Δεδομένων")
        
        uploaded_file = st.file_uploader(
            "📊 Ανεβάστε το Excel αρχείο:", 
            type=['xlsx', 'xls'],
            help="Επιλέξτε αρχείο Excel με έργα ύδρευσης"
        )
        
        if uploaded_file:
            with st.spinner("⏳ Φόρτωση και ανάλυση δεδομένων..."):
                df = load_and_analyze_excel_enhanced(uploaded_file)
                
                if df is not None:
                    # Cache the loaded dataframe
                    st.session_state['df'] = df
                    
                    # Show success message with data stats
                    st.success(f"✅ Φορτώθηκαν {len(df):,} εγγραφές με {len(df.columns)} πεδία")
                    
                    # Enhanced statistics in expander for better organization
                    with st.expander("📊 Συνοπτικά Στατιστικά", expanded=True):
                        # Regional breakdown with progress bars
                        if 'Περιφέρεια' in df.columns:
                            st.subheader("🗺️ Έργα ανά Περιφέρεια")
                            region_counts = df['Περιφέρεια'].value_counts()
                            total = len(df)
                            
                            # Show top 5 regions with progress bars
                            for region, count in region_counts.head(5).items():
                                percentage = (count / total) * 100
                                st.write(f"**{region}**")
                                st.progress(percentage / 100, f"{count:,} έργα ({percentage:.1f}%)")
                            
                            # Show "other" if there are more regions
                            if len(region_counts) > 5:
                                other_count = total - sum(region_counts.head(5))
                                other_percentage = (other_count / total) * 100
                                st.write(f"**Άλλες Περιφέρειες**")
                                st.progress(other_percentage / 100, f"{other_count:,} έργα ({other_percentage:.1f}%)")
                        
                        # Top prefectures with metrics
                        prefecture_counts = df['Νομός'].value_counts()
                        st.write("**🏛️ Top 5 Νομοί:**")
                        for prefecture, count in prefecture_counts.head(5).items():
                            st.write(f"• {prefecture}: {count}")
                else:
                    st.error("❌ Αποτυχία φόρτωσης αρχείου")
                    return
        else:
            st.info("👆 Ανεβάστε το Excel αρχείο για να ξεκινήσετε")
            return
    
    # Check if data exists
    if 'df' not in st.session_state:
        st.info("📁 Παρακαλώ φορτώστε το Excel αρχείο από την πλαϊνή μπάρα")
        return
    
    df = st.session_state['df']
    
    # Enhanced filter section
    st.subheader("🎯 Φίλτρα Επιλογής")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        regions = ['Όλες'] + sorted(df['Περιφέρεια'].unique().tolist())
        selected_region = st.selectbox(
            "🗺️ Περιφέρεια:",
            regions,
            key="region_selector"
        )
    
    with col2:
        # Dynamic prefecture selection
        if selected_region and selected_region != 'Όλες':
            available_prefectures = sorted(df[df['Περιφέρεια'] == selected_region]['Νομός'].unique())
        else:
            available_prefectures = sorted(df['Νομός'].unique())
        
        prefectures = ['Όλοι'] + available_prefectures
        selected_prefecture = st.selectbox(
            "🏛️ Νομός:",
            prefectures,
            key="prefecture_selector"
        )
    
    with col3:
        # Quick project type filter
        project_types = ['Όλα'] + sorted(df['Κατηγορία Έργου'].dropna().unique())
        selected_type = st.selectbox(
            "🏗️ Είδος Έργου:",
            project_types,
            key="quick_type_filter"
        )
    
    # Apply quick filter
    display_df = df.copy()
    if selected_type != 'Όλα':
        display_df = display_df[display_df['Κατηγορία Έργου'] == selected_type]
    
    # Διαδραστική αναζήτηση
    with st.expander("🔍 Αναζήτηση Έργων", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_title = st.text_input(
                "🔍 Αναζήτηση στον τίτλο:",
                key="search_title"
            )
        
        with col2:
            search_deya = st.selectbox(
                "🏢 ΔΕΥΑ/Δήμος:",
                ['Όλα'] + sorted(df['Φορέας Ύδρευσης'].unique()),
                key="search_deya"
            )
        
        with col3:
            # Φίλτρο προϋπολογισμού
            budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
            if budget_col in df.columns:
                budget_values = df[budget_col].dropna()
                if len(budget_values) > 0:
                    min_budget, max_budget = st.slider(
                        "💰 Εύρος Προϋπολογισμού (€):",
                        min_value=int(budget_values.min()),
                        max_value=int(budget_values.max()),
                        value=(int(budget_values.min()), int(budget_values.max())),
                        step=10000,
                        key="budget_slider"
                    )
        
        # Εφαρμογή φίλτρων αναζήτησης
        search_df = df.copy()
        
        if search_title:
            title_col = next((col for col in df.columns if 'τίτλος' in col.lower()), None)
            if title_col:
                search_df = search_df[search_df[title_col].str.contains(search_title, case=False, na=False)]
        
        if search_deya != 'Όλα':
            search_df = search_df[search_df['Φορέας Ύδρευσης'] == search_deya]
        
        if budget_col in df.columns and 'min_budget' in locals():
            search_df = search_df[
                (search_df[budget_col] >= min_budget) & 
                (search_df[budget_col] <= max_budget)
            ]
        
        if len(search_df) != len(df):
            st.success(f"🎯 Βρέθηκαν {len(search_df):,} έργα που ταιριάζουν στα κριτήρια")
            
            # Εμφάνιση αποτελεσμάτων
            display_columns = [
                col for col in ['Τίτλος Έργου', 'Φορέας Ύδρευσης', 'Νομός', budget_col, 'Κατηγορία Έργου']
                if col in search_df.columns
            ]
            
            st.dataframe(search_df[display_columns].head(10), use_container_width=True)
            
            if len(search_df) > 10:
                st.info(f"📋 Εμφανίζονται τα πρώτα 10 από {len(search_df)} αποτελέσματα")
            
            # Ενημέρωση των display_df για τις καρτέλες
            display_df = search_df.copy()

    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Διαδραστικός Χάρτης ανά Νομό", 
        "📊 Διαδραστικά Γραφήματα", 
        "📋 Συγκεντρωτικοί Πίνακες",
        "🔍 Ανάλυση Προόδου Έργων",
        "📍 Λεπτομερής Ανάλυση ανά Νομό/Δήμο"
    ])

    with tab1:
        st.subheader("🗺️ Διαδραστικός Χάρτης ανά Νομό")
        m = create_interactive_map_by_prefecture(display_df)
        map_html = m._repr_html_()
        components.html(map_html, height=500)  # Display the map using HTML
        
        if 'selected_prefecture_from_map' in st.session_state and st.session_state['selected_prefecture_from_map']:
            st.subheader(f"Έργα για το Νομό: {st.session_state['selected_prefecture_from_map']}")
            prefecture_projects = display_df[display_df['Νομός'] == st.session_state['selected_prefecture_from_map']]
            st.dataframe(prefecture_projects, use_container_width=True)
    
    with tab2:
        create_interactive_charts(display_df, selected_region, selected_prefecture)
    
    with tab3:
        create_summary_tables(display_df, selected_region, selected_prefecture)
    
    with tab4:
        create_project_progress_analysis(display_df, selected_region, selected_prefecture)

    with tab5:
        create_detailed_regional_analysis(display_df, selected_region, selected_prefecture)

    # Data export functionality
    with st.expander("📁 Εξαγωγή Δεδομένων"):
        export_format = st.selectbox("Επιλέξτε μορφή εξαγωγής:", ["CSV", "Excel"])
        
        if export_format == "CSV":
            csv_data = convert_df_to_csv(display_df)
            st.download_button(
                label="📥 Εξαγωγή CSV",
                data=csv_data,
                file_name="water_projects_data.csv",
                mime="text/csv"
            )
        elif export_format == "Excel":
            excel_data = convert_df_to_excel(display_df)
            st.download_button(
                label="📥 Εξαγωγή Excel", 
                data=excel_data,
                file_name="water_projects_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def convert_df_to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    return output.getvalue()

def create_detailed_regional_analysis(df, selected_region=None, selected_prefecture=None):
    """Λεπτομερής ανάλυση έργων ανά νομό και δήμο με προϋπολογισμούς."""
    
    st.subheader("📍 Λεπτομερής Ανάλυση ανά Νομό/Δήμο")
    st.markdown("Εξερευνήστε αναλυτικά τα έργα, προϋπολογισμούς και στατιστικά για κάθε νομό και δήμο")
    
    # Φίλτρα επιλογής
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analysis_level = st.radio(
            "🎯 Επίπεδο Ανάλυσης:",
            ["Ανά Νομό", "Ανά Δήμο/ΔΕΥΑ", "Σύγκριση Νομών"],
            key="analysis_level"
        )
    
    with col2:
        # Επιλογή συγκεκριμένου νομού για βαθύτερη ανάλυση
        prefectures_list = ['Όλοι'] + sorted(df['Νομός'].unique().tolist())
        focus_prefecture = st.selectbox(
            "🏛️ Επιλογή Νομού για Ανάλυση:",
            prefectures_list,
            key="focus_prefecture"
        )
    
    with col3:
        # Επιλογή παραμέτρου ανάλυσης
        analysis_param = st.selectbox(
            "📊 Παράμετρος Ανάλυσης:",
            ["Προϋπολογισμός", "Αριθμός Έργων", "Πληθυσμός", "Χρόνος Ολοκλήρωσης"],
            key="analysis_param"
        )
    
    # Ανάλυση ανά επίπεδο
    if analysis_level == "Ανά Νομό":
        create_prefecture_analysis(df, analysis_param, focus_prefecture)
    elif analysis_level == "Ανά Δήμο/ΔΕΥΑ":
        create_municipality_analysis(df, analysis_param, focus_prefecture)
    else:
        create_prefecture_comparison(df, analysis_param)

def create_prefecture_analysis(df, analysis_param, focus_prefecture):
    """Ανάλυση ανά νομό."""
    st.subheader("🏛️ Ανάλυση ανά Νομό")
    
    # Προετοιμασία δεδομένων
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    pop_col = next((col for col in df.columns if 'πληθυσμός' in col.lower()), None)
    time_col = next((col for col in df.columns if any(word in col.lower() for word in ['χρόνος', 'μήνες'])), None)
    
    # Ομαδοποίηση ανά νομό
    prefecture_stats = df.groupby('Νομός').agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        budget_col: ['sum', 'mean', 'count'] if budget_col in df.columns and df[budget_col].notna().sum() > 0 else 'count',
        pop_col: 'sum' if pop_col else 'count',
        time_col: 'mean' if time_col else 'count'
    }).round(2)
    
    # Flatten columns
    prefecture_stats.columns = [
        'Αριθμός Έργων', 'Αριθμός ΔΕΥΑ/Δήμων', 
        'Συνολικός Προϋπολογισμός', 'Μέσος Προϋπολογισμός', 'Έργα με Προϋπολογισμό',
        'Συνολικός Πληθυσμός', 'Μέση Διάρκεια (μήνες)'
    ]
    
    # Top 10 νομοί
    if analysis_param == "Προϋπολογισμός" and 'Συνολικός Προϋπολογισμός' in prefecture_stats.columns:
        sorted_stats = prefecture_stats.nlargest(10, 'Συνολικός Προϋπολογισμός')
        metric_col = 'Συνολικός Προϋπολογισμός'
    else:
        sorted_stats = prefecture_stats.nlargest(10, 'Αριθμός Έργων')
        metric_col = 'Αριθμός Έργων'
    
    # Δημιουργία γραφημάτων
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart για top νομούς
        fig = go.Figure(data=[go.Bar(
            y=sorted_stats.index,
            x=sorted_stats[metric_col],
            orientation='h',
            marker=dict(
                color=sorted_stats[metric_col],
                colorscale='viridis',
                showscale=True
            ),
            text=[f"{x:,.0f}" for x in sorted_stats[metric_col]],
            textposition='auto'
        )])
        
        fig.update_layout(
            title=f"🏆 Top 10 Νομοί - {analysis_param}",
            xaxis_title=analysis_param,
            yaxis_title="Νομός",
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart για περιφερειακή κατανομή
        region_stats = df.groupby('Περιφέρεια')['Α/Α'].count().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=region_stats['Περιφέρεια'],
            values=region_stats['Α/Α'],
            hole=0.3,
            textinfo='label+percent',
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        
        fig.update_layout(
            title="🗺️ Κατανομή Έργων ανά Περιφέρεια",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Λεπτομερής πίνακας
    st.subheader("📋 Λεπτομερής Πίνακας Νομών")
    
    # Μορφοποίηση αριθμών
    display_stats = prefecture_stats.copy()
    if 'Συνολικός Προϋπολογισμός' in display_stats.columns:
        display_stats['Συνολικός Προϋπολογισμός'] = display_stats['Συνολικός Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
        display_stats['Μέσος Προϋπολογισμός'] = display_stats['Μέσος Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
    
    st.dataframe(display_stats.sort_values('Αριθμός Έργων', ascending=False), use_container_width=True)
    
    # Εάν επιλέχθηκε συγκεκριμένος νομός
    if focus_prefecture != 'Όλοι':
        st.subheader(f"🔍 Εις Βάθος Ανάλυση: {focus_prefecture}")
        create_single_prefecture_deep_dive(df, focus_prefecture)

def create_municipality_analysis(df, analysis_param, focus_prefecture):
    """Ανάλυση ανά δήμο/ΔΕΥΑ."""
    st.subheader("🏢 Ανάλυση ανά Δήμο/ΔΕΥΑ")
    
    # Φιλτράρισμα δεδομένων
    if focus_prefecture != 'Όλοι':
        filtered_df = df[df['Νομός'] == focus_prefecture]
        st.info(f"📍 Εμφάνιση δεδομένων για το Νομό: **{focus_prefecture}**")
    else:
        filtered_df = df.copy()
    
    # Προετοιμασία δεδομένων
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    
    municipality_stats = filtered_df.groupby(['Φορέας Ύδρευσης', 'Νομός']).agg({
        'Α/Α': 'count',
        budget_col: ['sum', 'mean'] if budget_col in filtered_df.columns else 'count',
        'Κατηγορία Έργου': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
    }).round(2)
    
    # Flatten columns
    municipality_stats.columns = ['Αριθμός Έργων', 'Συνολικός Προϋπολογισμός', 'Μέσος Προϋπολογισμός', 'Κύρια Κατηγορία']
    municipality_stats = municipality_stats.reset_index()
    
    # Sorting
    if analysis_param == "Προϋπολογισμός":
        municipality_stats = municipality_stats.sort_values('Συνολικός Προϋπολογισμός', ascending=False)
    else:
        municipality_stats = municipality_stats.sort_values('Αριθμός Έργων', ascending=False)
    
    # Top 15 δήμοι
    top_municipalities = municipality_stats.head(15)
    
    # Γραφήματα
    col1, col2 = st.columns(2)
    
    with col1:
        # Horizontal bar chart
        fig = go.Figure(data=[go.Bar(
            y=[f"{row['Φορέας Ύδρευσης'][:25]}..." if len(row['Φορέας Ύδρευσης']) > 25 else row['Φορέας Ύδρευσης'] 
               for _, row in top_municipalities.iterrows()],
            x=top_municipalities['Αριθμός Έργων'],
            orientation='h',
            marker=dict(
                color=top_municipalities['Αριθμός Έργων'],
                colorscale='blues',
                showscale=True
            ),
            text=top_municipalities['Αριθμός Έργων'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Έργα: %{x}<br><extra></extra>'
        )])
        
        fig.update_layout(
            title="🏆 Top 15 Δήμοι/ΔΕΥΑ (Αριθμός Έργων)",
            xaxis_title="Αριθμός Έργων",
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Συνολικός Προϋπολογισμός' in top_municipalities.columns:
            # Scatter plot: Έργα vs Προϋπολογισμός
            fig = go.Figure(data=[go.Scatter(
                x=top_municipalities['Αριθμός Έργων'],
                y=top_municipalities['Συνολικός Προϋπολογισμός'],
                mode='markers+text',
                text=[name[:10] + "..." if len(name) > 10 else name 
                      for name in top_municipalities['Φορέας Ύδρευσης']],
                textposition='top center',
                marker=dict(
                    size=top_municipalities['Αριθμός Έργων'] * 2,
                    color=top_municipalities['Συνολικός Προϋπολογισμός'],
                    colorscale='viridis',
                    showscale=True,
                    colorbar=dict(title="Προϋπολογισμός")
                ),
                hovertemplate='<b>%{text}</b><br>Έργα: %{x}<br>Προϋπολογισμός: €%{y:,.0f}<br><extra></extra>'
            )])
            
            fig.update_layout(
                title="💰 Σχέση Έργων - Προϋπολογισμού",
                xaxis_title="Αριθμός Έργων",
                yaxis_title="Συνολικός Προϋπολογισμός (€)",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Λεπτομερής πίνακας
    st.subheader("📊 Πλήρης Πίνακας Δήμων/ΔΕΥΑ")
    
    # Μορφοποίηση
    display_municipalities = municipality_stats.copy()
    if 'Συνολικός Προϋπολογισμός' in display_municipalities.columns:
        display_municipalities['Συνολικός Προϋπολογισμός'] = display_municipalities['Συνολικός Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
        display_municipalities['Μέσος Προϋπολογισμός'] = display_municipalities['Μέσος Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
    
    # Pagination
    page_size = 20
    total_pages = len(display_municipalities) // page_size + (1 if len(display_municipalities) % page_size > 0 else 0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page_number = st.selectbox(
            f"📄 Επιλέξτε σελίδα (1-{total_pages}):",
            range(1, total_pages + 1),
            key="municipality_page"
        )
    
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    
    st.dataframe(
        display_municipalities.iloc[start_idx:end_idx],
        use_container_width=True
    )
    
    # Στατιστικά
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏢 Συνολικοί Δήμοι/ΔΕΥΑ", len(municipality_stats))
    with col2:
        total_projects = municipality_stats['Αριθμός Έργων'].sum()
        st.metric("🏗️ Συνολικά Έργα", f"{total_projects:,}")
    with col3:
        if 'Συνολικός Προϋπολογισμός' in municipality_stats.columns:
            total_budget = municipality_stats['Συνολικός Προϋπολογισμός'].sum()
            st.metric("💰 Συνολικός Προϋπολογισμός", f"€{total_budget:,.0f}")
    with col4:
        avg_projects = municipality_stats['Αριθμός Έργων'].mean()
        st.metric("📊 Μέσος Αριθμός Έργων/Δήμο", f"{avg_projects:.1f}")

def create_prefecture_comparison(df, analysis_param):
    """Σύγκριση νομών."""
    st.subheader("⚖️ Σύγκριση Νομών")
    
    # Επιλογή νομών για σύγκριση
    col1, col2 = st.columns(2)
    
    with col1:
        available_prefectures = sorted(df['Νομός'].unique().tolist())
        selected_prefectures = st.multiselect(
            "📍 Επιλέξτε Νομούς για Σύγκριση (max 6):",
            available_prefectures,
            default=available_prefectures[:6],
            max_selections=6,
            key="comparison_prefectures"
        )
    
    with col2:
        comparison_metrics = st.multiselect(
            "📊 Επιλέξτε Μετρικές:",
            ["Αριθμός Έργων", "Προϋπολογισμός", "Αριθμός ΔΕΥΑ", "Μέση Διάρκεια"],
            default=["Αριθμός Έργων", "Προϋπολογισμός"],
            key="comparison_metrics"
        )
    
    if not selected_prefectures:
        st.warning("⚠️ Επιλέξτε τουλάχιστον έναν νομό για σύγκριση")
        return
    
    # Φιλτράρισμα και προετοιμασία δεδομένων
    comparison_df = df[df['Νομός'].isin(selected_prefectures)]
    
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    time_col = next((col for col in df.columns if any(word in col.lower() for word in ['χρόνος', 'μήνες'])), None)
    
    comparison_stats = comparison_df.groupby('Νομός').agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        budget_col: 'sum' if budget_col in comparison_df.columns else 'count',
        time_col: 'mean' if time_col else 'count'
    }).round(2)
    
    comparison_stats.columns = ['Αριθμός Έργων', 'Αριθμός ΔΕΥΑ', 'Προϋπολογισμός', 'Μέση Διάρκεια']
    
    # Radar chart για σύγκριση
    if len(selected_prefectures) <= 3:
        fig = go.Figure()
        
        for prefecture in selected_prefectures:
            if prefecture in comparison_stats.index:
                values = []
                for metric in comparison_metrics:
                    if metric in comparison_stats.columns:
                        # Normalize values (0-100 scale)
                        max_val = comparison_stats[metric].max()
                        normalized_val = (comparison_stats.loc[prefecture, metric] / max_val) * 100
                        values.append(normalized_val)
                
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],  # Close the polygon
                    theta=comparison_metrics + [comparison_metrics[0]],
                    fill='toself',
                    name=prefecture
                ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="📊 Σύγκριση Νομών (Normalized σε κλίμακα 0-100)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Bar charts για κάθε μετρική
    for i, metric in enumerate(comparison_metrics):
        if metric in comparison_stats.columns:
            col1, col2 = st.columns(2) if i % 2 == 0 else (col2, col1)
            
            with col1 if i % 2 == 0 else col2:
                fig = go.Figure(data=[go.Bar(
                    x=comparison_stats.index,
                    y=comparison_stats[metric],
                    marker=dict(
                        color=comparison_stats[metric],
                        colorscale='viridis'
                    ),
                    text=[f"{x:,.0f}" for x in comparison_stats[metric]],
                    textposition='auto'
                )])
                
                fig.update_layout(
                    title=f"📊 {metric}",
                    xaxis_title="Νομός",
                    yaxis_title=metric,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Σύγκριση σε πίνακα
    st.subheader("📋 Συγκριτικός Πίνακας")
    
    display_comparison = comparison_stats.copy()
    if 'Προϋπολογισμός' in display_comparison.columns:
        display_comparison['Προϋπολογισμός'] = display_comparison['Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
    
    st.dataframe(display_comparison.sort_values('Αριθμός Έργων', ascending=False), use_container_width=True)

def create_single_prefecture_deep_dive(df, prefecture_name):
    """Εις βάθος ανάλυση συγκεκριμένου νομού."""
    prefecture_df = df[df['Νομός'] == prefecture_name].copy()
    
    if len(prefecture_df) == 0:
        st.warning(f"⚠️ Δεν βρέθηκαν έργα για το νομό {prefecture_name}")
        return
    
    # Βασικά στατιστικά
    col1, col2, col3, col4 = st.columns(4)
    
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    
    with col1:
        total_projects = len(prefecture_df)
        st.metric("🏗️ Συνολικά Έργα", f"{total_projects:,}")
    
    with col2:
        unique_deya = len(prefecture_df['Φορέας Ύδρευσης'].unique())
        st.metric("🏢 ΔΕΥΑ/Δήμοι", unique_deya)
    
    with col3:
        if budget_col in prefecture_df.columns:
            total_budget = prefecture_df[budget_col].sum()
            st.metric("💰 Συνολικός Προϋπολογισμός", f"€{total_budget:,.0f}")
    
    with col4:
        if budget_col in prefecture_df.columns:
            avg_budget = prefecture_df[budget_col].mean()
            st.metric("📊 Μέσος Προϋπολογισμός", f"€{avg_budget:,.0f}")
    
    # Κατανομή ανά ΔΕΥΑ
    col1, col2 = st.columns(2)
    
    with col1:
        deya_counts = prefecture_df['Φορέας Ύδρευσης'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=deya_counts.index,
            values=deya_counts.values,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Έργα: %{value}<br>Ποσοστό: %{percent}<br><extra></extra>'
        )])
        
        fig.update_layout(
            title=f"🏢 Κατανομή Έργων ανά ΔΕΥΑ/Δήμο - {prefecture_name}",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Κατηγορία Έργου' in prefecture_df.columns:
            category_counts = prefecture_df['Κατηγορία Έργου'].value_counts()
            
            fig = go.Figure(data=[go.Bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                marker=dict(
                    color=category_counts.values,
                    colorscale='blues'
                ),
                text=category_counts.values,
                textposition='auto'
            )])
            
            fig.update_layout(
                title=f"🏗️ Κατηγορίες Έργων - {prefecture_name}",
                xaxis_title="Αριθμός Έργων",
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Λίστα όλων των έργων
    st.subheader(f"📋 Πλήρης Λίστα Έργων - {prefecture_name}")
    
    # Επιλογή στηλών για εμφάνιση
    available_columns = [col for col in prefecture_df.columns if col not in ['normalized_utility']]
    default_columns = [
        'Τίτλος Έργου', 'Φορέας Ύδρευσης', 
        budget_col if budget_col in prefecture_df.columns else 'Κατηγορία Έργου',
        'Κατηγορία Έργου'
    ]
    
    selected_columns = st.multiselect(
        "📊 Επιλέξτε στήλες για εμφάνιση:",
        available_columns,
        default=[col for col in default_columns if col in available_columns],
        key=f"columns_{prefecture_name}"
    )
    
    if selected_columns:
        # Φίλτρο για ΔΕΥΑ
        selected_deya = st.multiselect(
            "🏢 Φιλτράρισμα ανά ΔΕΥΑ (προαιρετικό):",
            sorted(prefecture_df['Φορέας Ύδρευσης'].unique()),
            key=f"deya_filter_{prefecture_name}"
        )
        
        display_df = prefecture_df.copy()
        if selected_deya:
            display_df = display_df[display_df['Φορέας Ύδρευσης'].isin(selected_deya)]
        
        # Μορφοποίηση προϋπολογισμού αν υπάρχει
        if budget_col in selected_columns and budget_col in display_df.columns:
            display_df[budget_col] = display_df[budget_col].apply(
                lambda x: f"€{x:,.0f}" if pd.notna(x) and x != 0 else "N/A"
            )
        
        st.dataframe(
            display_df[selected_columns].reset_index(drop=True),
            use_container_width=True
        )
        
        # Κουμπί εξαγωγής
        csv = display_df[selected_columns].to_csv(index=False)
        st.download_button(
            label=f"📥 Εξαγωγή σε CSV - {prefecture_name}",
            data=csv,
            file_name=f"projects_{prefecture_name}.csv",
            mime="text/csv"
        )

def create_export_summary(df):
    """Δημιουργία συγκεντρωτικών δεδομένων για εξαγωγή."""
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    
    summary = df.groupby(['Περιφέρεια', 'Νομός']).agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        budget_col: ['sum', 'mean', 'count'] if budget_col in df.columns else 'count'
    })
    
    return summary

def create_prefecture_export(df):
    """Εξαγωγή δεδομένων ανά νομό."""
    return df.groupby('Νομός').agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        'Περιφέρεια': 'first'
    }).reset_index()

def create_municipality_export(df):
    """Εξαγωγή δεδομένων ανά δήμο."""
    return df.groupby(['Φορέας Ύδρευσης', 'Νομός']).agg({
        'Α/Α': 'count',
        'Περιφέρεια': 'first'
    }).reset_index()

    # Export δεδομένων
    st.subheader("📥 Εξαγωγή Δεδομένων")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Εξαγωγή Συγκεντρωτικών", key="export_summary"):
            summary_data = create_export_summary(display_df)
            csv = summary_data.to_csv(index=True)
            st.download_button(
                label="⬇️ Κατέβασμα CSV",
                data=csv,
                file_name="water_projects_summary.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🏛️ Εξαγωγή ανά Νομό", key="export_prefectures"):
            prefecture_data = create_prefecture_export(display_df)
            csv = prefecture_data.to_csv(index=False)
            st.download_button(
                label="⬇️ Κατέβασμα CSV",
                data=csv,
                file_name="projects_by_prefecture.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🏢 Εξαγωγή ανά ΔΕΥΑ", key="export_municipalities"):
            municipality_data = create_municipality_export(display_df)
            csv = municipality_data.to_csv(index=False)
            st.download_button(
                label="⬇️ Κατέβασμα CSV",
                data=csv,
                file_name="projects_by_municipality.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()