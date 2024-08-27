import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import math

app = Flask(__name__)

df = pd.read_csv('art-db.csv')

df['combined_content'] = df.apply(lambda row: row['description'] if pd.notnull(row['description']) 
                                   else (row['medium_display'] if pd.notnull(row['medium_display']) 
                                   else row['publication_history']), axis=1)

def compute_tf(text):
    tf_dict = {}
    words = text.split()
    for word in words:
        word = word.lower()
        tf_dict[word] = tf_dict.get(word, 0) + 1
    num_words = len(words)
    tf_dict = {word: count / num_words for word, count in tf_dict.items()}
    return tf_dict

def compute_idf(doc_list):
    idf_dict = {}
    N = len(doc_list)
    for doc in doc_list:
        for word in set(doc.split()):
            word = word.lower()
            idf_dict[word] = idf_dict.get(word, 0) + 1
    idf_dict = {word: math.log(N / count) for word, count in idf_dict.items()}
    return idf_dict

def compute_tfidf(tf, idf):
    tfidf = {word: tf_val * idf.get(word, 0) for word, tf_val in tf.items()}
    return tfidf

doc_list = df['combined_content'].fillna('').tolist()
tf_list = [compute_tf(doc) for doc in doc_list]
idf_dict = compute_idf(doc_list)
tfidf_list = [compute_tfidf(tf, idf_dict) for tf in tf_list]

def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

@app.route("/query", methods=['GET'])
def query():
    search_query = request.args.get('query', '')
    
    query_tf = compute_tf(search_query)
    query_tfidf = compute_tfidf(query_tf, idf_dict)
    
    similarities = [cosine_similarity(query_tfidf, tfidf) for tfidf in tfidf_list]
    
    related_docs_indices = np.argsort(similarities)[-10:][::-1]
    results = []

    for idx in related_docs_indices:
        relevance = similarities[idx]
        if relevance > 0:
            results.append({
                'title': df.iloc[idx]['title'],
                'artist': df.iloc[idx]['artist_title'],
                'date': df.iloc[idx]['date_display'],
                'content': df.iloc[idx]['combined_content'][:500],
                'relevance': similarities[idx]
            })
    
    response = {
        'results': results,
        'message': 'OK'
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006)
