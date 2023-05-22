import io

from gensim import corpora
from gensim.models import LdaModel
import nltk
from matplotlib import pyplot as plt
# from nltk.corpus import stopwords
from wordcloud import WordCloud

# nltk.download('punkt')
from nltk import word_tokenize

# stopwords = set(stopwords.words('english'))


# def preprocess_text(text):
#     tokens = word_tokenize(text.lower())
#     tokens = [token for token in tokens if token.isalpha() and token not in stopwords]
#     return tokens


def LDA_100(preprocessed_documents):
    dictionary = corpora.Dictionary(preprocessed_documents)
    corpus = [dictionary.doc2bow(doc) for doc in preprocessed_documents]
    num_topics = 5
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    topic_dict = {}
    for topic in lda_model.print_topics(num_topics=num_topics, num_words=5):
        words = topic[1].split('+')
        topic_words = {}
        for word in words:
            word_prob = word.strip().split('*')
            word = word_prob[1].strip().strip('"')
            probability = float(word_prob[0].strip())
            topic_words[word] = probability
        topic_dict[topic[0]] = topic_words
    print(topic_dict)
    return topic_dict


def draw_word_cloud(lda_dict):
    for key, value in lda_dict.items():
        wordcloud = WordCloud(width=800, height=400, background_color='white')
        wordcloud.generate_from_frequencies(value)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        buffer = io.BytesIO()
        wordcloud.to_image().save(buffer, format='PNG')
        buffer.seek(0)
        image_data = buffer.getvalue()
        yield image_data

