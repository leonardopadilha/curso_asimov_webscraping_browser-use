import logging

def books_logger() -> logging.Logger:
    # Criando um logger
    logger = logging.getLogger("books")

    # Definindo o nível do logger
    logger.setLevel(logging.INFO)  
    # Criando o formato do log
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Criando um handler para salvar os logs em um arquivo
    file_handler = logging.FileHandler('books.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)  # Adicionando o handler de arquivo

    # Criando um handler para mostrar os logs no console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)  # Adicionando o handler de console

    return logger