import tweepy
from AutenticacaoMongoDb import AutenticacaoMongoDb
from AutenticacaoApiTwitter import AutenticacaoApiTwitter

db = AutenticacaoMongoDb.autenticaERetornaInstanciaDoBancoDeDados()
auth = AutenticacaoApiTwitter.autentica()

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if not hasattr(status, "retweeted_status"):
            try:
                insere_mongodb(status)
                print(status.extended_tweet["full_text"])
                print("\n")
            except AttributeError:
                insere_mongodb(status)
                print(status.text)
                print("\n")

    def on_error(self, status_code):
        print("Erro com o código:", status_code)
        return True


def insere_mongodb(status):
    db.covid19.insert_one({
        "id_usuario": status.user.id_str,
        "nome_usuario": status.user.screen_name,
        "id_tweet": status.id_str,
        "tweet": status.text,
        "quantidade_caracteres": str(len(status.text)),
        "data_criacao_tweet": status.created_at,
        "quantidade_retweets": status.retweet_count,
        "localizacao_usuario": status.user.location,
        "descricao_usuario": status.user.description,
        "quantidade_seguidores_usuario": status.user.followers_count,
        "data_criacao_conta_usuario": status.user.created_at
    })
