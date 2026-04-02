import pandas as pd


def preprocess(df,region_df):


    # filter summer olympics
    df = df[df['Season'] == 'Summer']

    # merge only once
    df = df.merge(region_df, how='left', on='NOC')

    # remove duplicates
    df.drop_duplicates(inplace=True)

    # medals to one-hot (only once)
    medals_df = pd.get_dummies(df['Medal'])
    df = pd.concat([df, medals_df], axis=1)

    return df