import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from flask import Flask, request, jsonify

app = Flask(__name__)

df = pd.read_csv('art-db.csv')

df['combined_content'] = df.apply(lambda row: row['description'] if pd.notnull(row['description']) 
                                   else (row['medium_display'] if pd.notnull(row['medium_display']) 
                                   else row['publication_history']), axis=1)

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined_content'].fillna(''))

@app.route("/query", methods=['GET'])
def query():
    search_query = request.args.get('query', '')
    
    query_tfidf = vectorizer.transform([search_query])
    cosine_similarities = linear_kernel(query_tfidf, tfidf_matrix).flatten()
    
    related_docs_indices = cosine_similarities.argsort()[-10:][::-1]
    results = []
    
    for idx in related_docs_indices:
        if cosine_similarities[idx] > 0:
            results.append({
                'title': df.iloc[idx]['title'],
                    'artist': df.iloc[idx]['artist_title'],
                    'date': df.iloc[idx]['date_display'],
                    'content': df.iloc[idx]['combined_content'][:500],
                    'relevance': cosine_similarities[idx]
            })
    
    response = {
        'results': results,
        'message': 'OK'
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006)
