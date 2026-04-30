"""
Script untuk menyimpan model SVM dan TF-IDF vectorizer
Jalankan script ini setelah notebook training selesai
"""

import pandas as pd
import numpy as np
import pickle
import re
import unicodedata
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# =====================================================
# PREPROCESSING FUNCTIONS
# =====================================================

obfuscation_dict = {
    # === HURUF (ENCLOSED / SQUARE) ===
    "🅰": "a", "🅱": "b", "🅲": "c", "🅳": "d", "🅴": "e",
    "🅵": "f", "🅶": "g", "🅷": "h", "🅸": "i", "🅹": "j",
    "🅺": "k", "🅻": "l", "🅼": "m", "🅽": "n", "🅾": "o",
    "🅿": "p", "🆀": "q", "🆁": "r", "🆂": "s", "🆃": "t",
    "🆄": "u", "🆅": "v", "🆆": "w", "🆇": "x", "🆈": "y",
    "🆉": "z",
    "🅰️": "a", "🅱️": "b", "🅾️": "o", "🅿️": "p",
    # === HURUF LINGKARAN ===
    "ⓐ": "a", "ⓑ": "b", "ⓒ": "c", "ⓓ": "d", "ⓔ": "e",
    "ⓕ": "f", "ⓖ": "g", "ⓗ": "h", "ⓘ": "i", "ⓙ": "j",
    "ⓚ": "k", "ⓛ": "l", "ⓜ": "m", "ⓝ": "n", "ⓞ": "o",
    "ⓟ": "p", "ⓠ": "q", "ⓡ": "r", "ⓢ": "s", "ⓣ": "t",
    "ⓤ": "u", "ⓥ": "v", "ⓦ": "w", "ⓧ": "x", "ⓨ": "y",
    "ⓩ": "z",
    # === HURUF LINGKARAN KAPITAL ===
    "Ⓐ": "a", "Ⓑ": "b", "Ⓒ": "c", "Ⓓ": "d", "Ⓔ": "e",
    "Ⓕ": "f", "Ⓖ": "g", "Ⓗ": "h", "Ⓘ": "i", "Ⓙ": "j",
    "Ⓚ": "k", "Ⓛ": "l", "Ⓜ": "m", "Ⓝ": "n", "Ⓞ": "o",
    "Ⓟ": "p", "Ⓠ": "q", "Ⓡ": "r", "Ⓢ": "s", "Ⓣ": "t",
    "Ⓤ": "u", "Ⓥ": "v", "Ⓦ": "w", "Ⓧ": "x", "Ⓨ": "y",
    "Ⓩ": "z",
    # === ANGKA LINGKARAN ===
    "⓪": "0", "①": "1", "②": "2", "③": "3", "④": "4",
    "⑤": "5", "⑥": "6", "⑦": "7", "⑧": "8", "⑨": "9",
    "❶": "1", "❷": "2", "❸": "3", "❹": "4", "❺": "5",
    "❻": "6", "❼": "7", "❽": "8", "❾": "9",
    # === EMOJI ANGKA ===
    "0️⃣": "0", "1️⃣": "1", "2️⃣": "2", "3️⃣": "3",
    "4️⃣": "4", "5️⃣": "5", "6️⃣": "6",
    "7️⃣": "7", "8️⃣": "8", "9️⃣": "9",
    # === SIMBOL UMUM ===
    "@": "a", "$": "s", "!": "i", "€": "e",
}

pattern = re.compile("|".join(map(re.escape, obfuscation_dict.keys())))

def replace_obfuscation(text):
    """Replace obfuscation characters"""
    return pattern.sub(lambda x: obfuscation_dict[x.group()], text)

def normalize_unicode(text):
    """Normalize unicode characters"""
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text

def normalize_urls(text):
    """Replace URLs with 'iniurl'"""
    url_pattern = r'(https?://\S+|www\.\S+)'
    return re.sub(url_pattern, 'iniurl', text)

def clean_text(text):
    """Clean text: lowercase, remove special chars, handle spacing"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    """Complete preprocessing pipeline"""
    # 1. Unicode normalization
    text = normalize_unicode(text)
    # 2. Replace obfuscation
    text = replace_obfuscation(text)
    # 3. Normalize unicode again
    text = normalize_unicode(text)
    # 4. Replace URLs
    text = normalize_urls(text)
    # 5. Clean text
    text = clean_text(text)
    return text

# =====================================================
# MAIN - SAVE MODEL
# =====================================================

if __name__ == "__main__":
    print("Loading dataset...")
    df = pd.read_csv('../dataset/dataset_judol_clean.csv')
    
    print(f"Dataset shape: {df.shape}")
    
    # Prepare data
    X = df['comment_text_clean']
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # TF-IDF vectorization
    print("\nCreating TF-IDF vectorizer...")
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 1))
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    print(f"TF-IDF shape: {X_train_tfidf.shape}")
    
    # Train SVM Baseline Model
    print("\nTraining SVM Baseline Model...")
    model_svm = SVC(kernel='linear', class_weight='balanced', probability=True)
    model_svm.fit(X_train_tfidf, y_train)
    
    # Evaluate
    train_score = model_svm.score(X_train_tfidf, y_train)
    test_score = model_svm.score(X_test_tfidf, y_test)
    
    print(f"Training Score: {train_score:.4f}")
    print(f"Test Score: {test_score:.4f}")
    
    # Save model
    print("\nSaving model and vectorizer...")
    with open('models/svm_model.pkl', 'wb') as f:
        pickle.dump(model_svm, f)
    print("✓ Model saved: models/svm_model.pkl")
    
    with open('models/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    print("✓ Vectorizer saved: models/tfidf_vectorizer.pkl")
    
    # Save preprocessing function
    with open('models/preprocessing_dict.pkl', 'wb') as f:
        pickle.dump(obfuscation_dict, f)
    print("✓ Preprocessing dict saved: models/preprocessing_dict.pkl")
    
    print("\n✓ All models saved successfully!")
