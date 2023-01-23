try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv()) #finds where the .env is
except:
    ...