import torch
import torchaudio
import logging
from fastapi import HTTPException
from demucs import pretrained
from demucs.apply import apply_model
from pathlib import Path

def separate_and_save(input_file: str, output_prefix: str):
    logging.info("Starting separate_and_save")
    
    input_file_path = Path(input_file)
    vocals_output_path = Path(f"{output_prefix}_vocals.wav")
    instrumental_output_path = Path(f"{output_prefix}_instrumental.wav")

    if vocals_output_path.exists() and instrumental_output_path.exists():
        logging.info("Separated files already exist, returning cached paths")
        return str(vocals_output_path), str(instrumental_output_path)

    if not input_file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found after download.")
    
    try:
        logging.info(f"Loading audio file: {input_file_path}")
        audio, sample_rate = torchaudio.load(str(input_file_path))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to load audio file: {e}")

    if audio.shape[0] == 1:
        logging.info("Duplicating mono channel to stereo")
        audio = torch.cat([audio, audio])

    if sample_rate != 44100:
        logging.info(f"Resampling audio from {sample_rate} to 44100 Hz")
        resample_transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=44100)
        audio = resample_transform(audio)
        sample_rate = 44100

    audio = audio.unsqueeze(0)
    logging.info("Added batch dimension to audio")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    audio = audio.to(device)
    demucs_model = pretrained.get_model('mdx').to(device)

    try:
        logging.info("Applying Demucs model to separate sources")
        with torch.no_grad():
            estimates = apply_model(demucs_model, audio, overlap=0.25)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model application failed: {e}")

    vocals = estimates[0][3].cpu()
    instrumental = (estimates[0][0] + estimates[0][1] + estimates[0][2]).cpu()

    logging.info(f"Saving vocals to: {vocals_output_path}")
    torchaudio.save(str(vocals_output_path), vocals, sample_rate)
    
    logging.info(f"Saving instrumental to: {instrumental_output_path}")
    torchaudio.save(str(instrumental_output_path), instrumental, sample_rate)

    logging.info("Finished separate_and_save")
    return str(vocals_output_path), str(instrumental_output_path)