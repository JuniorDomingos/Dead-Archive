import sounddevice as sd
import numpy as np
import wave
import time
from datetime import datetime
from ftplib import FTP

# Configurações de gravação
duration = 1200  # Duração de cada gravação em segundos
interval_seconds = 60 # Intervalo de gravação em segundos (20 minutos)

# Configurações FTP
ftp_host = '192.168.1.252'  # Host do servidor FTP
ftp_user = 'guiche-01'  # Usuário do FTP
ftp_password = '123456'  # Senha do FTP
ftp_directory = '/Audios/guiche-01/'  # Diretório no servidor FTP onde os arquivos serão enviados

def record_audio():
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_filename = f"recording_{current_time}.wav"  # Nome do arquivo com data e hora
    print(f"Gravando áudio em {output_filename} por {duration} segundos...")
    
    # Configuração da gravação de áudio do microfone
    fs = 44100  # Taxa de amostragem (samples por segundo)
    channels = 2  # Número de canais (estéreo)
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype=np.int16)
    sd.wait()  # Aguarda até que a gravação esteja completa

    # Salvar o áudio em um arquivo WAV
    wavefile = wave.open(output_filename, 'wb')
    wavefile.setnchannels(channels)
    wavefile.setsampwidth(2)  # Largura de amostra de 2 bytes (16 bits)
    wavefile.setframerate(fs)
    wavefile.writeframes(b''.join(recording))
    wavefile.close()
    print(f"Áudio gravado em {output_filename}")
    
    # Enviar arquivo via FTP
    send_via_ftp(output_filename)

def send_via_ftp(filename):
    try:
        # Conectar ao servidor FTP
        ftp = FTP(ftp_host)
        ftp.login(ftp_user, ftp_password)

        # Navegar para o diretório desejado
        ftp.cwd(ftp_directory)

        # Abrir o arquivo localmente e enviá-lo via FTP
        with open(filename, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)

        print(f"Arquivo {filename} enviado via FTP para {ftp_host}/{ftp_directory}")
        ftp.quit()
    except Exception as e:
        print(f"Erro ao enviar arquivo via FTP: {e}")

# Loop infinito para gravar a cada intervalo
while True:
    record_audio()
    print(f"Aguardando próximo intervalo de {interval_seconds} segundos...")
    time.sleep(interval_seconds)
