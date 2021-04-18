import tweepy
from CustomStreamListener import CustomStreamListener
from AutenticacaoApiTwitter import AutenticacaoApiTwitter
from AutenticacaoMongoDb import AutenticacaoMongoDb
import string
import nltk
from nltk import tokenize
import pandas as pd
from nltk.corpus import stopwords
import re
import csv

db = AutenticacaoMongoDb.autenticaERetornaInstanciaDoBancoDeDados()
auth = AutenticacaoApiTwitter.autentica()


class Tweet:

    @staticmethod
    def extrair_tweets():

        parametros = ['covid', 'covid19', 'pandemia', 'isolamento social', 'vacina']
        print("\nExtraindo tweets...")

        streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener())
        streaming_api.filter(follow=None, track=parametros, languages=["pt"])

    @staticmethod
    def imprimir_tweets():
        for tweet in db.covid19.find():
            print('\n')
            print('Tweet: ' + str(tweet['tweet']))

    @staticmethod
    def count_tweets():
        return db.covid19.count_documents({})

    @staticmethod
    def geraDataSetEmCsv():

        with open("resources/datasets/dataset_tweets_covid19.csv", "w", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(["id_usuario", "nome_usuario", "id_tweet", "tweet", "quantidade_caracteres",
                             "data_criacao_tweet", "quantidade_retweets", "localizacao_usuario", "descricao_usuario",
                             "quantidade_seguidores_usuario", "data_criacao_conta_usuario"])

            for tweet in db.covid19.find():
                writer.writerow([tweet['id_usuario'], tweet['nome_usuario'], tweet['id_tweet'], tweet['tweet'],
                                 tweet['quantidade_caracteres'], tweet['data_criacao_tweet'],
                                 tweet['quantidade_retweets'], tweet['localizacao_usuario'], tweet['descricao_usuario'],
                                 tweet['quantidade_seguidores_usuario'], tweet['data_criacao_conta_usuario']])

    @staticmethod
    def imprimiCSV():

        dataset = pd.read_csv('resources/datasets/dataset_tweets_covid19.csv', encoding='utf-8')
        dataset.drop_duplicates(['tweet'], inplace=True)
        tweets = dataset['tweet']

        tweets = [PreProcessamento(i) for i in tweets]

        for tweet in tweets:
            print(tweet)
            print("\n")


def PreProcessamento(instancia):
    stemmer = nltk.stem.RSLPStemmer()

    instancia = re.sub(r"http\S+", "", instancia).lower().replace('.', '').replace(';', '').replace('-', '').replace(
        ':', '').replace(')', '')

    stopwords = set(nltk.corpus.stopwords.words('portuguese'))

    palavras = [stemmer.stem(i) for i in instancia.split() if not i in stopwords]

    return " ".join(palavras)