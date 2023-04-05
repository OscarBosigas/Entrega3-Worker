from datetime import datetime
from celery import Celery
import zipfile, py7zr, bz2, tarfile, rarfile
import os

app = Celery( 'tasks' , broker = 'redis://localhost:6379/0' )

@app.task
def compressZip(filename, zipname, newPath):
    zfile = zipfile.ZipFile(newPath + '/' + zipname, 'w')
    zfile.write(filename, compress_type = zipfile.ZIP_DEFLATED)
    zfile.close()
    os.remove(filename)

@app.task
def compress7z(filename, zipname, newPath):
    with py7zr.SevenZipFile(newPath + "/" + zipname, 'w') as archive:
        archive.writeall(filename)
    os.remove(filename)

@app.task
def comprimir_bz2(filename, zipname, newPath):
    with bz2.open(newPath + "/" + zipname, "wb") as f:
        with open(filename, "rb") as file:
            f.write(file.read())
    os.remove(filename)

@app.task
def compressTar(filename, zipname, newPath, option):
    if option == 'zip':
        with tarfile.open(newPath + "/" + zipname, "w:gz") as tar:
            tar.add(filename, arcname="archive/" + filename)
        os.remove(filename)
    if option == 'bz2':
        with tarfile.open(newPath + "/" + zipname, "w:bz2") as tar:
            tar.add(filename, arcname="archive/" + filename)
        os.remove(filename)

@app.task
def compressRar(filename, zipname, newPath):
        rar_obj = rarfile.RarFile(filename[0]+'.rar', mode='w')
        rar_obj.write(filename)
        rar_obj.close()
        rar_obj_path = os.path.join(newPath, filename+'.rar')
        os.makedirs(os.path.dirname(rar_obj_path), exist_ok=True)
        os.rename(filename+'.rar', rar_obj_path)
        os.remove(filename)