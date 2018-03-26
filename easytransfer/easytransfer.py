# coding:utf-8
import os
import shutil
import time
import logging
import subprocess

import click

import server
from MyQR import myqr
from config import UPLOAD_FOLDER
from config import SERVER_HOST
from config import SERVER_PORT

logging.basicConfig(
                format='%(asctime)s - %(levelname)s - %(message)s',
                filename='log',
                level=logging.INFO
                            )


@click.command()
@click.argument('srcf_path')
def trans_file(srcf_path):
    subprocess.Popen(['python', 'server.py'])
    filepath = cp_file_to_tmpdir(srcf_path, dstdir=UPLOAD_FOLDER)
    if filepath:
        key_strs = make_key_strs(filepath)
        generate_cqcode(key_strs)

def cp_file_to_tmpdir(srcf_path, dstdir=UPLOAD_FOLDER):
    if os.path.exists(srcf_path):
        basename = os.path.basename(srcf_path)
        dstf_path = os.path.join(dstdir, basename)
        if os.path.isfile(srcf_path):
            try:
                return shutil.copy(srcf_path,dstf_path)
            except OSError as e:
                logging.info('src:{},dst:{};Why:{}'.format(
                                            srcf_path,dstf_path,e))
        elif os.path.isdir(srcf_path):
            try :
                return shutil.copytree(srcf_path,dstf_path,symlinks=True)
            except OSError as e:
                logging.info('src:{},dst:{};Why:{}'.format(
                                            srcf_path,dstf_path,e))
        else:
            logging.info("Don't surpport this file type")
            raise OSError
    else: 
        print("srcf_path is not exist.")
        logging.info("srcf_path is not exist.")
        # raise OSError


def lauch_server():
    try:
        server.app.run(host=SERVER_HOST, port=SERVER_PORT)
    except OSError:
        pass

def make_key_strs(filepath):
    server_ip = subprocess.check_output(['hostname', '--all-ip-addresses']).decode().strip()
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


if __name__=='__main__':
    srcf_path = './log'
    trans_file()
    # cp_file_to_tmpdir('./tests',TMPDIR)
    # lauch_server()