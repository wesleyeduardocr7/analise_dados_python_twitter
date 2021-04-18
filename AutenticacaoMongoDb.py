from pymongo import MongoClient

class AutenticacaoMongoDb:

    @staticmethod
    def autenticaERetornaInstanciaDoBancoDeDados():
        client = MongoClient("Insira a Autenticação com o MongoDb")
        db = client.get_database('tweets_covid19')
        return db
