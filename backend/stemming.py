from demucs import pretrained
from demucs.apply import apply_model
from typing import Optional
from pathlib import Path
import torch
import torchaudio

base_dir = Path(r"D:\Music\Data")
vocals_dir = base_dir / "Vocals"
instrumental_dir = base_dir / "Instrumental"
original_dir = base_dir / "Original"
karaoke_dir = base_dir / "Karaoke"

vocals_dir.mkdir(parents=True, exist_ok=True)
instrumental_dir.mkdir(parents=True, exist_ok=True)
original_dir.mkdir(parents=True, exist_ok=True)
karaoke_dir.mkdir(parents=True, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
demucs_model = pretrained.get_model('mdx_extra').to(device)


def separate_and_save(input_file_path: Path, base_name: str):
    vocals_output_path = vocals_dir / f"{base_name}.wav"
    instrumental_output_path = instrumental_dir / f"{base_name}.wav"

    if vocals_output_path.exists() and instrumental_output_path.exists():
        return vocals_output_path.name, instrumental_output_path.name

    audio, sample_rate = torchaudio.load(str(input_file_path))
    if audio.shape[0] == 1:
        audio = torch.cat([audio, audio])

    if sample_rate != 44100:
        resample_transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=44100)
        audio = resample_transform(audio)

    audio = audio.to(device).unsqueeze(0)

    with torch.no_grad():
        estimates = apply_model(demucs_model, audio, overlap=0.25)

    vocals = estimates[0][3].to("cpu")
    instrumental = (estimates[0][0] + estimates[0][1] + estimates[0][2]).to("cpu")

    torchaudio.save(str(vocals_output_path), vocals, 44100)
    torchaudio.save(str(instrumental_output_path), instrumental, 44100)

    return vocals_output_path.name, instrumental_output_path.name


separate_and_save("/usr/local/home/u200298/Downloads/rushhour/backend/downloads/A Bar Song (Tipsy) - Shaboozey.mp3", "Eoin")