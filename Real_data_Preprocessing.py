import sys

import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join('./')))
class Preprocess_Task:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    def convert_to_datetime(self, df, column: str):

        df[column] = pd.to_datetime(
            df[column], errors='coerce')
        return df
    def convert_to_float(self, df, column: str):
        self.df[column] = df[column].astype(float)
        return self.df
    def drop_variables(self, df):
        df_before_filling = df.copy()
        df = df[df.columns[df.isnull().mean() < 0.3]]
        missing_cols = df.columns[df.isnull().mean() > 0]
        print(missing_cols)
        return df, df_before_filling, missing_cols
    def clean_feature_name(self, df):
        df.columns = [column.replace(' ', '_').lower()
                      for column in df.columns]
        return df
    def rename_columns(self, df: pd.DataFrame, column: str, new_column: str):
        df[column] = df[column].rename(new_column)
        dfRenamed = df.rename({column: new_column}, axis=1)
        return dfRenamed
    def fill_numerical_variables(self, df):
        df_single = df
        cols = df_single.columns
        num_cols = df_single.select_dtypes(include=np.number).columns
        df_single.loc[:, num_cols] = df_single.loc[:, num_cols].fillna(
            df_single.loc[:, num_cols].median())
        print(num_cols)
        print(df_single.loc[:, num_cols].median())
        return cols, df_single, num_cols
    def fill_categorical_variables(self, df, cols, num_cols, df_single):

        cat_cols = list(set(cols) - set(num_cols))
        df_single.loc[:, cat_cols] = df_single.loc[:, cat_cols].fillna(
            df.loc[:, cat_cols].mode().iloc[0])
        df_cols = df_single.columns
        print(cat_cols)
        print(df_single.loc[:, cat_cols].mode().iloc[0])
        return df_cols, df_single, cat_cols

    def drop_duplicates(self, df):
        df = df.drop_duplicates()
        return df
    def convert_bytes_to_megabytes(self, df, col):

        megabyte = 1*10e+5
        megabyte_col = df[col] / megabyte
        return megabyte_col
df=pd.read_csv("E:\\10xAccademy_Practice\\Week 1\\Data\\Week1_challenge_data_source(CSV).csv")
dd=Preprocess_Task(df)
dd.drop_duplicates(df)
dd.fill_numerical_variables(df)
