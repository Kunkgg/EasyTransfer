# coding:utf-8
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
# import config
import shutil
import time
import logging
import subprocess
import requests
import multiprocessing

import click

from .MyQR import myqr
from .config import UPLOAD_FOLDER
from .config import SERVER_HOST
from .config import SERVER_PORT
from . import server

logging.basicConfig(
                format='%(asctime)s - %(levelname)s - %(message)s',
                filename='log',
                level=logging.INFO
                            )
@click.group()
def cli():
    """easytransfer"""
    

@cli.command('f')
@click.argument('srcf_path')
def trans_file(srcf_path):
    """transfer file by local file path"""
    lauch_server()
    filepath = cp_file_to_tmpdir(srcf_path, dstdir=UPLOAD_FOLDER)
    if filepath:
        key_strs = make_key_strs(filepath)
        generate_cqcode(key_strs)
        logging.info('Transfer file:{}'.format(srcf_path))

@cli.command('m')
@click.argument('message')
def trans_message(message):
    """transfer message"""
    lauch_server()
    url = 'http://{}:{}/'.format(SERVER_HOST, SERVER_PORT)
    data = {'message': message}
    res = requests.post(url,data=data)
    if res.status_code == 200:
        logging.info('Transfer message:{}'.format(message))
        key_strs = make_key_strs()
        generate_cqcode(key_strs)
    else:
        logging.info('Transfer message failed')

@cli.command('h')
def open_index():
    """show index page cqcode"""
    lauch_server()
    key_strs = make_key_strs()
    generate_cqcode(key_strs)


def cp_file_to_tmpdir(srcf_path, dstdir=UPLOAD_FOLDER):
    """
    copy the source file to the flask upload folder,
    return the absolute path of the dstfile.
    """
    if os.path.exists(srcf_path):
        basename = os.path.basename(srcf_path)
        dstf_path = os.path.join(dstdir, basename)
        if os.path.isfile(srcf_path):
            try:
                return shutil.copy(srcf_path, dstf_path)
            except OSError as e:
                logging.info('src:{},dst:{};Why:{}'.format(
                                            srcf_path, dstf_path,e))
        elif os.path.isdir(srcf_path):
            try :
                return shutil.copytree(srcf_path, dstf_path, symlinks=True)
            except OSError as e:
                logging.info('src:{},dst:{};Why:{}'.format(
                                            srcf_path, dstf_path,e))
        else:
            logging.info("Don't surpport this file type")
            raise OSError
    else: 
        print("srcf_path is not exist.")
        logging.info("srcf_path is not exist.")
        # raise OSError


def lauch_server():
    """lauch flask server"""
    try:
        subprocess.Popen(['python', server.__file__])
    except OSError:
        pass

def make_key_strs(filepath=None):
    """make the URL string"""
    # get the server's network interface IP 
    server_ip = subprocess.check_output(['hostname', '--all-ip-addresses']).decode().strip()
    if filepath is None:
        key_strs = 'http://{ip}:{port}/'.format(
        **{
            'ip':server_ip,
            'port':SERVER_PORT
        }
    )
    else:
        key_strs = 'http://{ip}:{port}/{tmpdirname}/{filename}'.format(
            **{
                'ip':server_ip,
                'port':SERVER_PORT,
                'tmpdirname':os.path.basename(UPLOAD_FOLDER),
                'filename':os.path.basename(filepath)
            }
        )
    return key_strs
    
def generate_cqcode(strs):
    """generate cqcode by using myqr lib"""
    myqr.run(
        strs,
        version=1,
        level='H',
        picture=None,
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name=None,
        save_dir=os.getcwd()
	    )

