#!/usr/bin/env python3

import logging

import pandas as pd
import sqlalchemy


ENGINE = sqlalchemy.create_engine(sqlalchemy.engine.url.URL.create(
    drivername='postgresql+psycopg2',
    username='catalog',
    password='catalog',
    database='catalog',
))


CHUNKSIZE = 1 << 10


def table2():
    names = 'ID,SourceID,RAdeg,DEdeg,Per,R21,phi21,T_0,gmag,rmag,Per_g,Per_r,Num_g,Num_r,R21_g,R21_r,phi21_g,phi21_r,R2_g,R2_r,Amp_g,Amp_r,log_FAP_g,log_FAP_r,Type,Delta_min_g,Delta_min_r'
    df = pd.read_csv(
        'https://zenodo.org/record/3886372/files/Table2.txt.zip?download=1',
        compression = 'zip',
        skiprows=34,
        header=None,
        delim_whitespace=True,
        names=names.split(','),
    )
    df.to_sql('table2', ENGINE, chunksize=CHUNKSIZE, index=False)


def table6():
    names = 'ID,RAdeg,DEdeg,gmag,rmag,Per_g,Per_r,Amp_g,Amp_r,Num_g,Num_r,log_FAP_g,log_FAP_r'
    df = pd.read_csv(
        'https://zenodo.org/record/3886372/files/Table6.txt.zip?download=1',
        compression='zip',
        skiprows=20,
        header=None,
        delim_whitespace=True,
        names=names.split(','),
    )
    df.to_sql('table6', ENGINE, chunksize=CHUNKSIZE, index=False)


def main():
    logging.basicConfig(level=logging.INFO)

    logging.info('Adding Table2.txt')
    table2()
    logging.info('Adding Table6.txt')
    table6()


if __name__ == '__main__':
    main()
