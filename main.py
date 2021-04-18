from Tweet import Tweet


def main():
    print('1 - Extrair Tweets')
    print('2 - Imprimir Tweets')
    print('3 - Quantidade de Tweets MongoDb Atlas')
    print('4 - Gerar dataset em CSV')
    print('5 - Imprimir CSV')

    print('0 - Sair')
    op = int(input('Informe a Opção: '))

    if op == 1:
        Tweet.extrair_tweets()
    if op == 2:
        Tweet.imprimir_tweets()
    if op == 3:
        print(Tweet.count_tweets())
    if op == 4:
        Tweet.geraDataSetEmCsv()
    if op == 5:
        Tweet.imprimiCSV()
main()
