import os
from beefutilities.IO import file_io

async def cleanup_tts_folder():
    temp_tts_path = file_io.construct_data_path("temp_tts_data")
    if os.path.exists(temp_tts_path):
        for filename in os.listdir(temp_tts_path):
            file_path = os.path.join(temp_tts_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted old TTS file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        os.makedirs(temp_tts_path)
        print(f"Created directory: {temp_tts_path}")
    return