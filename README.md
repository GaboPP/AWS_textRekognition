# AWS_textRekognition
Aplicativo para detectar texto en una imagen, bajo el servico de amazon.
Se debe tener instalada la libreria boto3, por lo que hay que ejecutar:
> pip install boto3

Para ejecuar pedir credenciales para acceder al bucket y rellenar los campos aws_access_key_id, aws_secret_access_key, aws_session_token:
>  client = boto3.client(\
>        'rekognition',\
>        # Hard coded strings as credentials, not recommended.\
>        aws_access_key_id="",\
>        aws_secret_access_key="",\
>        aws_session_token=""\
>   )

ejecutar:
  > python aws_rk.py
  
Si se quere probar con otras imagenes editar la lista 'images' en el código.
