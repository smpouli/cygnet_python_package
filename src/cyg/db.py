
from pathlib import Path
import urllib.request
import os, gzip, shutil
import sqlite3

# database checking and downloading
path_to_installed_database=Path('src/cyg/data/cygnet.db')

if path_to_installed_database.exists():   
    # connexion to the database
    conn = sqlite3.connect('src/cyg/data/cygnet.db')
    Database = conn.cursor()
else:    
    download_url = "https://github.com/rowanhm/cygnet/releases/latest/download/cygnet.db.gz"
    
    gz_file = Path("src/cyg/data/cygnet.db.gz")
    output_file = Path("src/cyg/data/cygnet.db")
  
    
    try:
        # Download
        print ("The Cygnet database needs to be downloaded. This will happen only once.")
        print ("Downloading Cygnet database...")
        urllib.request.urlretrieve(download_url, gz_file)
        print ("Cygnet database successfully downloaded.")
        # Decompress
        with gzip.open(gz_file, "rb") as gz:
            with open(output_file, "wb") as output:
                shutil.copyfileobj(gz, output)

        os.remove(gz_file)
        print("Cygnet database successfully extracted and stored.")
        
        # connexion to the database
        conn = sqlite3.connect('src/cyg/data/cygnet.db')
        Database = conn.cursor()
    except:
        print ("An error occurred, please try again or look at the help file in the data folder.")

       

    
