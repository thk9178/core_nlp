from nltk.stem import WordNetLemmatizer, PorterStemmer
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
import gensim
from nltk.tag import pos_tag

# nltk.download('stopwords')
from nltk.corpus import stopwords



def DocuVec(docs, vector_size, min_count, cores, window, neg_sample, epochs, dm, dbow_words, seed=1234):
    stop_words = set(stopwords.words("english"))
    
    #docs = list(Document_list.values())
    split = [s.lower().strip().split(" ") for s in docs] # [doc_0, doc_1, ... , doc_n] 의 리스트 안에 있는 각 doc_i 리스트의 단어를 토큰화
    
    #split = [[ps.stem(s) for s in t] for t in split] # stemming
    split = [[lemmatizer.lemmatize(s) for s in t] for t in split] # lemmatizing
    
    split = [[s for s in t if s not in stop_words] for t in split] # stopwords 제거
    
    tagged_documents = []
    for i, s in enumerate(split):
        #print ('i :', i, 's :', s, '\n')
        tagged_documents.append(
            gensim.models.doc2vec.TaggedDocument(s, [i])
        )
    
    #Doc2Vec_model = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=min_count, workers=cores, window=10, seed=210419, negative=neg_sample) # PV-DM
    Doc2Vec_model = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=min_count, workers=cores, window=window, negative=neg_sample, dm=0, dbow_words=dbow_words, seed=seed) # PV-DBOW
    
    Doc2Vec_model.build_vocab(tagged_documents)
    
    Doc2Vec_model.train(tagged_documents, total_examples=len(tagged_documents), epochs=epochs, report_delay = 1)
    
    return(tagged_documents, Doc2Vec_model)


def DocuSim(Doc2Vec_model, new_document):
    stop_words = set(stopwords.words("english"))
    #print("== Document vector")
    new_doc = new_document.lower().split(" ")
    
    stem = [lemmatizer.lemmatize(s) for s in new_doc] # lemmatizing
    #stem = [ps.stem(s) for s in new_doc] # stemming
    
    final = [s for s in stem if s not in stop_words]

    new_doc_vector = Doc2Vec_model.infer_vector(final)
        
    #----------------------------------------
    # Use wor2vec similarity 
    # Document 전체에 대해서 similarity를 측정하여, 가장 가까운 word-vector를 사용해서 결과를 리턴.
    #print("== word similarity")
    #print(Doc2Vec_model.wv.similar_by_vector(new_doc_vector))
    
    #----------------------------------------
    # Use Doc2vec similarity
    # docvec.most_similar는 word에 대한 vector에 기반해서 처리됨.
    #print("== document similarity")
    doc_sim_lst = Doc2Vec_model.docvecs.most_similar(positive=[new_doc_vector], topn=len(Doc2Vec_model.docvecs))
    #for doc_id, sim in doc_sim_lst:
        #print(f"Document {doc_id} - similarity: {sim:.5f}")
    #print("== complete")
    return(doc_sim_lst)