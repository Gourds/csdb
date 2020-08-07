# -*- coding: utf-8 -*-

import click
from flask import current_app
from flask.cli import AppGroup
from csdb.extensions import db
import pymysql

init_db = AppGroup('init_db')


@init_db.command('create_db')
@click.option('--drop', is_flag=True, help='Create after Drop')
def create_db(drop):
    click.echo('Create database {}'.format(current_app.config['SQLALCHEMY_DATABASE_URI']))
    conn = pymysql.connect(host=current_app.config['DB_HOST'],
                           user=current_app.config['DB_USER'],
                           password=current_app.config['DB_PWD'],
                           port=int(current_app.config['DB_PORT']),
                           charset='utf8mb4')
    cursor = conn.cursor()
    if drop:
        click.confirm('This operation will drop the database, do you want to continue?', abort=True)
        sql = f"DROP DATABASE {current_app.config['DB_NAME']}"
        cursor.execute(sql)

    sql = f"CREATE DATABASE IF NOT EXISTS {current_app.config['DB_NAME']}"
    cursor.execute(sql)
    cursor.close()
    click.echo('Finished.')

@init_db.command('create_tables')
@click.option('--drop', is_flag=True, help='Create after drop.')
def create_tables(drop):
    """Create the table."""
    click.echo('Create the table...{}'.format(current_app.config['SQLALCHEMY_DATABASE_URI']))
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Dropped tables.')
    db.create_all()
    click.echo('Finished.')