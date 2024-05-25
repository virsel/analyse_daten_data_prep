import pandas as pd
from .arrangement import arrange_txt_en, arrange_txt_de
from wipo_ipc import Ipc

def get_description(ipc):
        try:
            if ipc == '':
                return ''
            return Ipc(ipc).classe.description
        except ValueError:
            raise
        except AttributeError as e:
            print(f"attr err on {ipc}")
            return Ipc(ipc).section.description

def ipc_to_description(ipc):
    if ipc == '':
        return ''
    ipc = ipc.split()[0].strip()
    i = 0
    while i < 4:
        try:
            return get_description(ipc)
        except:
            print(f"err on {ipc}")
            ipc = ipc[:-1]
        i += 1
    return ''

def arrange_ipc(df):
    mask_ipcnone = df['ipc_main'].isnull()

    # set ipc to content of sub ipc if main ipc is missing
    df.loc[mask_ipcnone, 'ipc_main'] = df.loc[mask_ipcnone, 'ipc_sub']
    
    df['ipc_main'].fillna('', inplace=True)
    
    df['ipc'] = df['ipc_main'].apply(ipc_to_description)
    df.drop(columns=['ipc_main', 'ipc_sub'], inplace=True)
    
    return df

def pipe_arrangement(df):
    df.rename(
        columns={
            "Veröffentlichungs-Nummer": "id",
            "Titel": "title",
            "Zusammenfassung": "abstract",
            "Veröffentlichungs-Datum": "pub_date",
            "IPC-Hauptklasse": "ipc_main",
            "IPC-Neben-/Indexklassen": "ipc_sub",
        },
        inplace=True,
    )
    
    df.dropna(subset=['abstract'], inplace=True)
    
    mask_en = df['title'].str.contains(r'\[EN\]') & df['abstract'].str.contains(r'\[EN\]')
    mask_de = df['title'].str.contains(r'\[DE\]') & df['abstract'].str.contains(r'\[DE\]')
    df_en = df[mask_en].copy()
    df_de = df[mask_de & (~mask_en)].copy()
    df_de['lang'] = 'de'
    df_en['lang'] = 'en'
    
    df_en[['title', 'abstract']] = df_en[['title', 'abstract']].apply(arrange_txt_en, axis=1)
    df_de[['title', 'abstract']] = df_de[['title', 'abstract']].apply(arrange_txt_de, axis=1)
    
    df = pd.concat([df_en, df_de], ignore_index=True)
    
    df.dropna(subset=['abstract'], inplace=True)
    df['pub_date'] = pd.to_datetime(df['pub_date'], format='%d.%m.%Y')
    df_filtered = df.sort_values(by='pub_date', ascending=False).drop_duplicates(subset='abstract')
    
    df_filtered['pub_year'] = df_filtered['pub_date'].dt.year
    df_filtered['text'] = df_filtered['title'] + '. ' + df_filtered['abstract']
    df_filtered.drop(columns=['title', 'abstract', 'pub_date'], inplace=True)
    
    df_res = arrange_ipc(df_filtered)
    
    return df_res