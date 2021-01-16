
import sys
import os 
from dotenv import load_dotenv
from app.server import create_app

if __name__=="__main__":
    if sys.argv[1]=="prod":
        print("no prod configurations")
    elif sys.argv[1]=="dev":
        print("sourcing local variables")
        load_dotenv('dev.env')
        app=create_app(config_name="local")
        app.run(port=5000, debug=True)