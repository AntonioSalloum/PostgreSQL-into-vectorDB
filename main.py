import os
import psycopg2
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from pgvector.psycopg2 import register_vector

texts = [
    "Type: Apartment, City: Beirut, Bedrooms: 2, Bathrooms: 1, Size: 90sqm",
    "Type: Apartment, City: Tripoli, Bedrooms: 2, Bathrooms: 1, Size: 90sqm",
    "Type: Apartment, City: Jounieh, Bedrooms: 2, Bathrooms: 2, Size: 90sqm",
    "Type: Apartment, City: Beirut, Bedrooms: 3, Bathrooms: 2, Size: 120sqm",
    "Type: Apartment, City: Byblos, Bedrooms: 3, Bathrooms: 2, Size: 120sqm",
    "Type: Apartment, City: Beirut, Bedrooms: 1, Bathrooms: 1, Size: 55sqm",
    "Type: Studio, City: Beirut, Bedrooms: 1, Bathrooms: 1, Size: 40sqm",
    "Type: Studio, City: Tripoli, Bathrooms: 1, Size: 40sqm",
    "Type: Villa, City: Jounieh, Bedrooms: 4, Bathrooms: 3, Size: 250sqm",
    "Type: Villa, City: Byblos, Bedrooms: 4, Bathrooms: 3, Size: 250sqm",
    "Type: Villa, City: Beirut, Bedrooms: 5, Bathrooms: 4, Size: 300sqm",
    "Type: Duplex, City: Beirut, Bedrooms: 3, Bathrooms: 3, Size: 150sqm",
    "Type: Duplex, City: Tripoli, Bedrooms: 3, Bathrooms: 3, Size: 150sqm",
]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
embeddings_list = embeddings.embed_documents(texts)

# print(embeddings_list[0])

connections = psycopg2.connect(dbname="ragdb", user="postgres", password = "Asalloum1234", host="localhost", port="5432")
register_vector(connections)
cursor = connections.cursor()

# for i in range(len(embeddings_list)):
#     embedding = np.array(embeddings_list[i])
#     content = texts[i]
#     cursor.execute("INSERT INTO items (content, embedding) VALUES(%s, %s)", (content, embedding))


connections.commit()
cursor.close()
connections.close()


new_text = "Type: Apartment, City: Zahle, Bedrooms: 2, Bathrooms: 2, Size: 100sqm" 
new_embedding = embeddings.embed_query(new_text)

new_connections = psycopg2.connect(dbname="ragdb", user="postgres", password = "Asalloum1234", host="localhost", port="5432")
register_vector(new_connections)
new_cursor = new_connections.cursor()

new_cursor.execute(
    """
    SELECT id, content
    FROM items
    ORDER BY embedding <-> %s::vector
    LIMIT 5
    """,
    (new_embedding,) 
)

# results = new_cursor.fetchall()
# for row in results:
#     print(row)


text_3 = "Type: Duplex, City: Beirut, Bedrooms: 5, Bathrooms: 2, Size: 250sqm"
embedding_3 = embeddings.embed_query(text_3)

connections_3 = psycopg2.connect(dbname="ragdb", user="postgres", password = "Asalloum1234", host="localhost", port="5432")
register_vector(connections_3)
cursor_3 = connections_3.cursor()

cursor_3.execute(
""" 
SELECT id, content
FROM items
ORDER BY embedding <-> %s::vector
LIMIT 5
""", (embedding_3,)
)

results_3 = cursor_3.fetchall()
for row in results_3:
    print(row)