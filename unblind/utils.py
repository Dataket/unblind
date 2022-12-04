
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import wget
import zipfile
import os
import json

datasets_urls = {
's1': 'https://api.plataformadigitalnacional.org/bulks-conteos/download?sistema=s1&elemento=zip',
's2': 'https://api.plataformadigitalnacional.org/bulks-conteos/download?sistema=s2&elemento=zip',
's3s': 'https://api.plataformadigitalnacional.org/bulks-conteos/download?sistema=s3s&elemento=zip',
's3p': 'https://api.plataformadigitalnacional.org/bulks-conteos/download?sistema=s3p&elemento=zip',
}

def get_datasets(to_path = 'data/'):

    data = {
        's1': None,
        's2': None,
        's3s': None,
        's3p': None,
    }

    # Create data folder if it doesn't exist
    if not os.path.exists(to_path):
        os.makedirs(to_path)

    for key, url in datasets_urls.items():
        print('Loading dataset: {}'.format(key))
        # Download file
        filename = wget.download(url, out=to_path)

        # Create folder
        folder = os.path.join(to_path, key)
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Unzip file
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(folder)

        # Remove zip file
        os.remove(filename)

