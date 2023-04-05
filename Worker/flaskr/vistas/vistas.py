from flask_restful import Resource
from flask import request,  request, send_file
from flask_jwt_extended import jwt_required, create_access_token
from ..modelos import *
import zipfile
import rarfile
#from pylzma import compress
import tarfile
import os
import smtplib
from datetime import datetime

usaurioSchema = UsersSchema()
taskSchema = TasksSchema()


        
class CompressZip(Resource):
    def post(self):
        # Obtener los archivos enviados desde el formulario
        files = request.files.getlist('file')
        file_names = [file.filename for file in files]
        # Crear un objeto ZipFile
        zip_obj = zipfile.ZipFile(file_names[0]+'.zip', 'w', zipfile.ZIP_DEFLATED)
        # Iterar sobre cada archivo y agregarlo al objeto ZipFile
        for file in files:
            filename = file.filename
            file.save(filename)
            zip_obj.write(filename)
            os.remove(filename)
        # Cerrar el objeto ZipFile
        zip_obj.close()
        # Enviar el archivo comprimido al cliente
        ##return send_file('archivos_comprimidos.zip', as_attachment=True)
        zip_obj_path = os.path.join('files/compressed', file_names[0]+'.zip')
        os.makedirs(os.path.dirname(zip_obj_path), exist_ok=True)
        os.rename(file_names[0]+'.zip', zip_obj_path)
        return {'mensaje':'comprimido correctamente'}
    
class CompressRar(Resource):
    def post(self):
         # Obtener los archivos enviados desde el formulario
        files = request.files.getlist('files')
        file_names = [file.filename for file in files]
        # Crear un objeto RarFile
        rar_obj = rarfile.RarFile(file_names[0]+'.rar', mode='w')
        # Agregar los archivos al objeto RarFile
        for file in files:
            rar_obj.write(file.filename)
        # Cerrar el objeto RarFile
        rar_obj.close()
        # Guardar el archivo comprimido en una carpeta local en el servidor
        rar_obj_path = os.path.join('files/compressed', file_names[0]+'.rar')
        os.makedirs(os.path.dirname(rar_obj_path), exist_ok=True)
        os.rename(file_names[0]+'.rar', rar_obj_path)
        return {'mensaje':'comprimido correctamente'}

class Compress7Z(Resource):
    def post(self):
        # Obtener el archivo a comprimir del cuerpo de la solicitud
        file = request.files['file']
        # Leer el contenido del archivo
        content = file.read()
        # Comprimir el contenido del archivo
        compressed_content = compress(content)
        # Escribir el contenido comprimido en un nuevo archivo
        with open('compressed_file.7z', 'wb') as f:
            f.write(compressed_content)
        return {'mensaje':'comprimido correctamente'}
    

class CompressTar(Resource):
    def post(self):
        files = request.files.getlist('file')        
        file_names = [file.filename for file in files]
        # Crear un archivo TAR vacío
        with tarfile.open(file_names[0]+'.tar', 'w') as tar:
            # Agregar cada archivo al archivo TAR
            for file in files:
                # Guardar el archivo en el sistema de archivos temporal
                file.save(file.filename)
                # Agregar el archivo al archivo TAR
                tar.add(file.filename)
        # Eliminar los archivos temporales
        for file in files:
            os.remove(file.filename)
        
        return {'mensaje':'comprimido correctamente'}
        
def sendEmail(email, msg):
    sender = 'oscar7bosigas@gmail.com'
    password = 'wtknllydvcnkbwrr'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender, email, msg)
    server.quit()
    

class SaveTask(Resource):
    jwt_required()
    def post(self):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        nueva_tarea = Tasks(email=request.json['email'],status="uploaded",timestamp=current_time,filename=request.json['filename'],format=request.json['format'])
        db.session.add(nueva_tarea)
        db.session.commit()
        sendEmail(request.json['email'], 'Proceso de compresion iniciado')
        return {'mensaje':'Agregado'}