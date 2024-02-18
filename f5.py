import ffmpeg
import numpy as np
from scipy.io.wavfile import write


from scipy.io.wavfile import write
import re


def f5_encode(
    audio_file_path: str, message: str, block_size: int, output_file: str
) -> None:
    # Menyandikan pesan ke dalam file audio
    # Encode the message into the audio file
    audio_data = (
        ffmpeg.input(audio_file_path)
        .output("pipe:", format="wav")
        .run(capture_stdout=True, capture_stderr=True)
    )
    audio_samples = np.frombuffer(audio_data[0], np.int16)

    # Modify the audio data to embed the message
    modified_audio_samples = audio_samples.copy()
    for i, char in enumerate(message):
        start = i * block_size
        end = (i + 1) * block_size
        block_audio = modified_audio_samples[start:end]

        # Embed the current message character into the audio block
        block_audio = np.bitwise_and(block_audio, 0xFFFE)
        block_audio = np.bitwise_or(block_audio, ord(char))

        # Update the audio data with the modified audio block
        modified_audio_samples[start:end] = block_audio

    # Extract sampling rate from ffmpeg output
    output_str = audio_data[1].decode("utf-8")  # Decode bytes to string
    match = re.search(r"(\d+) Hz", output_str)
    if match:
        sampling_rate = int(match.group(1))
    else:
        raise ValueError("Sampling rate not found in ffmpeg output")

    # Save the modified audio data to the output file
    write(output_file, sampling_rate, modified_audio_samples)


# Contoh penggunaan
# f5_encode ("carrier.wav", "testimoni", 1024, "output_audio.wav")


def f5_decode(audio_file_path: str, block_size: int, output_file: str) -> None:
    # Mendekripsi pesan dari file audio
    audio_input = ffmpeg.input(audio_file_path)
    audio_output = ffmpeg.output(audio_input, "pipe:", format="wav")
    audio = audio_output.run(capture_stdout=True, capture_stderr=True)

    # Mengonversi byte audio menjadi array numpy
    audio_data = np.frombuffer(audio[0], np.int16)

    # Inisialisasi variabel untuk menyimpan pesan yang diekstraksi
    extracted_message = ""

    # Melakukan loop pada setiap blok audio dan mengekstraksi bit LSB dari setiap blok
    for i in range(len(audio_data) // block_size):
        start = i * block_size
        end = (i + 1) * block_size
        block_audio = audio_data[start:end]

        # Mendapatkan bit LSB dari setiap blok audio
        extracted_bits = np.bitwise_and(block_audio, 1)

        # Mengonversi bit LSB menjadi karakter dan menambahkannya ke pesan yang diekstraksi
        extracted_char = "".join(str(bit) for bit in extracted_bits)

        extracted_message += extracted_char

    # Mengembalikan pesan yang diekstraksi
    return extracted_message


encoded_audio_file = "output_audio.wav"
output_text_file = "output_text.txt"

# Encode the message into the audio file
f5_encode("carrier.wav", "testimoni", 1024, encoded_audio_file)
print("Pesan berhasil disisipkan dalam file audio.")

# Decode the message from the encoded audio file
decoded_message = f5_decode(encoded_audio_file, 1024, output_text_file)
print("Pesan berhasil diekstrak dari file audio:")
print(decoded_message)
