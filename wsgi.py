
import sys
import os 
from dotenv import load_dotenv

if __name__=="__main__":
    if sys.argv[1]=="prod":
        print("no prod configurations")
    elif sys.argv[1]=="dev":
        print("sourcing local variables")
        load_dotenv('dev.env')
        from app.server import create_app
        app=create_app(config_name="local")
        app.run(host="0.0.0.0", port=5000, debug=True)