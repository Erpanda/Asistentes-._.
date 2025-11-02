import speech_recognition as sr

r = sr.Recognizer()

# Buscar automáticamente el Realtek
micros = sr.Microphone.list_microphone_names()
indice = None

for i, nombre in enumerate(micros):
    if "Realtek" in nombre:
        indice = i
        break

# Usar el Realtek encontrado
mic = sr.Microphone(device_index=indice)

print("🎤 Usando micrófono Realtek")
print("Habla ahora... (Di 'salir' para terminar)\n")

while True:
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    
    try:
        texto = r.recognize_google(audio, language="es-ES")
        print(f"➡️ {texto}\n")
        
        if "salir" in texto.lower():
            break
            
    except:
        print("❌ No entendí\n")