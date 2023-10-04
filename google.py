import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

companies_df = pd.read_csv('Input/companies.csv')

sector_keywords = {
    'Industri': ['industri', 'manufaktur', 'manufacturer', 'produksi', 'memproduksi'],
    'Perdagangan': ['wholesaler', 'distributor', 'penjualan', 'supplier', 'distribusi', 'dealer', 'honda', 'suplai',
                    'retail', 'grocers'],
    'Jasa Keuangan dan Asuransi': ['BPR', 'Bank', 'Perbankan', 'Asuransi', 'assurance', 'insurance'],
    'Kesehatan': ['Rumah sakit'],
    'Pendidikan': ['Sekolah', 'Pesantren', 'Yayasan'],
    'Real Estate': ['Real Estate', 'Perumahan', 'Villa', 'properti', 'property', 'developer'],
    'Jasa Perusahaan': ['konsultasi', 'pelatihan', 'konsultan', 'consultant', 'consulting', 'training', 'service', 'ac',
                        'manajemen korporat', 'outsorcing', 'keamanan', 'service'],
    'Jasa Lainnya': ['percetakan', 'digital printing', 'printing', 'limbah', 'pengolahan', 'waste', 'periklanan',
                     'advertising'],
    'Transportasi': ['pengiriman', 'sewa', 'penyewaan', 'delivery'],
    'Akomodasi dan Makan Minum': ['perjalanan', 'wisata', 'hotel', 'catering', 'travel', 'agency'],
    'Konstruksi': ['Contractor', 'Kontraktor', 'Konstruksi', 'Indokontraktor', 'construction'],
    'Informasi Komunikasi': ['Telekomunikasi', 'Komunikasi', 'Telecommunication', 'Telecommunications', 'internet',
                             'technology'],
    'Pertanian': ['pertanian', 'peternakan', 'farm'],
    'Pertambangan': ['pertambangan', 'tambang', 'mining'],
    'Energi': ['energi', 'listrik', 'minyak', 'gas'],
    'Hukum': ['hukum', 'pengacara', 'advokat'],
    'Media dan Hiburan': ['media', 'hiburan', 'film', 'musik'],
    'Otomotif': ['otomotif', 'mobil', 'motor'],
    'Pemerintahan': ['pemerintahan', 'pemerintah', 'dinas', 'kementerian'],
    'Teknologi': ['teknologi', 'software', 'hardware'],
}


def get_sector(company, index):
    try:
        query = f"{company} sector"
        response = requests.get(f"https://www.google.com/search?q={query}")
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text().lower()
        for sector, keywords in sector_keywords.items():
            if any(keyword in text_content for keyword in keywords):
                print(f"Processed {index + 1}/{len(companies_df)}: {company} -> {sector}")
                return sector
            print(f"Processed {index + 1}/{len(companies_df)}: {company} -> Unknown")
        return "Unknown"
    except Exception as e:
        print(f"Error at {index + 1}/{len(companies_df)}: {company} -> {str(e)}")
        companies_df.to_csv('Output/perusahaan_google.csv', index=False)  # Save progress
        return "Error"


# Process each company
for index, row in companies_df.iterrows():
    companies_df.at[index, 'Sector'] = get_sector(row['company'], index)
    time.sleep(2)  # Delay to avoid rate limiting

    # Save the results to a new CSV file
    companies_df.to_csv('Output/perusahaan_google.csv', index=False)
