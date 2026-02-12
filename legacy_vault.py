import os
from collections import defaultdict

import torch
import torchaudio
import torchaudio.transforms as T


import os
from collections import defaultdict

import torch
import torchaudio
import torchaudio.transforms as T


def load_voice_notes(voice_notes_dir: str):
    """
    Load WhatsApp voice notes (.opus/.ogg/.wav/.m4a), resample to 16 kHz, normalize safely.

    Returns:
        list[dict]: Each entry has keys:
            - 'path': str
            - 'waveform': torch.Tensor [channels, time]
            - 'sample_rate': int (16_000)
            - 'text': None | str
    """
    dataset = []
    resampler_cache = defaultdict(lambda: None)

    if not os.path.isdir(voice_notes_dir):
        print(f"[ERROR] Voice notes dir does not exist: {voice_notes_dir}")
        return dataset

    for filename in os.listdir(voice_notes_dir):
        if not filename.lower().endswith((".opus", ".ogg", ".wav", ".m4a")):
            continue

        filepath = os.path.join(voice_notes_dir, filename)

        try:
            waveform, sr = torchaudio.load(filepath)

            # Ensure waveform is [channels, time]
            if waveform.dim() == 1:
                waveform = waveform.unsqueeze(0)

            # Resample if needed
            target_sr = 16000
            if sr != target_sr:
                if resampler_cache[sr] is None:
                    resampler_cache[sr] = T.Resample(orig_freq=sr, new_freq=target_sr)
                waveform = resampler_cache[sr](waveform)
            else:
                target_sr = sr

            # Safe normalization
            max_abs = waveform.abs().max()
            if max_abs > 0:
                waveform = waveform / max_abs
            else:
                print(f"[WARN] Zero-signal file, skipped normalization: {filename}")

            dataset.append(
                {
                    "path": filepath,
                    "waveform": waveform,
                    "sample_rate": target_sr,
                    "text": None,
                }
            )
            print(f"[LOAD OK] {filename} — shape {tuple(waveform.shape)} @ {target_sr} Hz")

        except Exception as e:
            print(f"[LOAD FAIL] {filename}: {e}")

    print(f"[SUMMARY] Loaded {len(dataset)} voice notes from {voice_notes_dir}")
    return dataset


def extract_insights(dataset):
    """
    Extract simple audio features from loaded waveforms.

    Returns:
        dict[path] -> feature dict
    """
    wisdom = {}

    for entry in dataset:
        waveform: torch.Tensor = entry["waveform"]
        sr: int = entry["sample_rate"]

        if waveform.dim() != 2:
            # Expect [channels, time]; skip malformed entries
            print(f"[INSIGHTS WARN] Unexpected waveform shape {waveform.shape} for {entry['path']}")
            continue

        num_channels, num_samples = waveform.shape
        dur_sec = num_samples / float(sr)

        # Power and RMS
        # Add a small epsilon to avoid nan in extreme edge cases
        power = waveform.pow(2).mean().item()
        rms = torch.sqrt(waveform.pow(2).mean() + 1e-12).item()

        wisdom[entry["path"]] = {
            "duration_sec": round(dur_sec, 2),
            "avg_energy": round(power, 6),
            "rms": round(rms, 6),
            "channels": num_channels,
            "text": entry.get("text"),  # placeholder for future Whisper transcription
        }

    print(f"[INSIGHTS] Extracted features for {len(wisdom)} files")
    return wisdom
    """
    dataset = []
    resampler_cache = defaultdict(lambda: None)

    if not os.path.isdir(voice_notes_dir):
        print(f"[ERROR] Voice notes dir does not exist: {voice_notes_dir}")
        return dataset

    for filename in os.listdir(voice_notes_dir):
        if not filename.lower().endswith((".opus", ".ogg", ".wav", ".m4a")):
            continue

        filepath = os.path.join(voice_notes_dir, filename)

        try:
            waveform, sr = torchaudio.load(filepath)

            # Ensure waveform is [channels, time]
            if waveform.dim() == 1:
                waveform = waveform.unsqueeze(0)

            # Resample if needed
            target_sr = 16000
            if sr != target_sr:
                if resampler_cache[sr] is None:
                    resampler_cache[sr] = T.Resample(orig_freq=sr, new_freq=target_sr)
                waveform = resampler_cache[sr](waveform)
            else:
                target_sr = sr

            # Safe normalization
            max_abs = waveform.abs().max()
            if max_abs > 0:
                waveform = waveform / max_abs
            else:
                print(f"[WARN] Zero-signal file, skipped normalization: {filename}")

            dataset.append(
                {
                    "path": filepath,
                    "waveform": waveform,
                    "sample_rate": target_sr,
                    "text": None,
                }
            )
            print(f"[LOAD OK] {filename} — shape {tuple(waveform.shape)} @ {target_sr} Hz")

        except Exception as e:
            print(f"[LOAD FAIL] {filename}: {e}")

    print(f"[SUMMARY] Loaded {len(dataset)} voice notes from {voice_notes_dir}")
    return dataset


def extract_insights(dataset):
    """
    Extract simple audio features from loaded waveforms.

    Returns:
        dict[path] -> feature dict
    """
    wisdom = {}

    for entry in dataset:
        waveform: torch.Tensor = entry["waveform"]
        sr: int = entry["sample_rate"]

        if waveform.dim() != 2:
            # Expect [channels, time]; skip malformed entries
            print(f"[INSIGHTS WARN] Unexpected waveform shape {waveform.shape} for {entry['path']}")
            continue

        num_channels, num_samples = waveform.shape
        dur_sec = num_samples / float(sr)

        # Power and RMS
        # Add a small epsilon to avoid nan in extreme edge cases
        power = waveform.pow(2).mean().item()
        rms = torch.sqrt(waveform.pow(2).mean() + 1e-12).item()

        wisdom[entry["path"]] = {
            "duration_sec": round(dur_sec, 2),
            "avg_energy": round(power, 6),
            "rms": round(rms, 6),
            "channels": num_channels,
            "text": entry.get("text"),  # placeholder for future Whisper transcription
        }

    print(f"[INSIGHTS] Extracted features for {len(wisdom)} files")
    return wisdomLoad WhatsApp voice notes (.opus/.ogg/.wav/.m4a), resample to 16kHz, normalize safely."""
    import os
    from collections import defaultdict

    dataset = []
    resampler_cache = defaultdict(lambda: None)  # reuse resampler per original sr

    for filename in os.listdir(voice_notes_dir):
        if filename.lower().endswith(('.opus', '.ogg', '.wav', '.m4a')):
            filepath = os.path.join(voice_notes_dir, filename)
            try:
                waveform, sr = torchaudio.load(filepath)
                
                # Force 2D shape: [channels, samples]
                if waveform.dim() == 1:
                    waveform = waveform.unsqueeze(0)  # mono → [1, samples]

                # Resample only if needed, cache resampler
                if sr != 16000:
                    if resampler_cache[sr] is None:
                        resampler_cache[sr] = T.Resample(sr, 16000)
                    waveform = resampler_cache[sr](waveform)

                # Safe normalization: avoid div-by-zero
                max_abs = waveform.abs().max()
                if max_abs > 0:
                    waveform = waveform / max_abs
                else:
                    print(f"[WARN] Zero-signal file skipped normalization: {filename}")

                dataset.append({
                    'path': filepath,
                    'waveform': waveform,
                    'sample_rate': 16000,
                    'text': None
                })
                print(f"[LOAD OK] {filename} — shape {waveform.shape} @ 16kHz")
            except Exception as e:
                print(f"[LOAD FAIL] {filename}: {e}")

    print(f"[SUMMARY] Loaded {len(dataset)} voice notes")
    return dataset

def save_checkpoint(model, path: str | None = None):
    """
    TODO: save to disk if path is provided.
    """
    # if path is not None:
    #     torch.save(model.state_dict(), path)
    return model


def embed_query(text: str) -> torch.Tensor:
    """
    Very simple 'embedding': just length as a float tensor.
    Replace with real text encoder later.
    """
    return torch.tensor([[float(len(text))]], dtype=torch.float32)


def generate_response(model, emb: torch.Tensor, wisdom) -> torch.Tensor:
    """
    Placeholder 'response embedding' used only for loss.
    Return a tensor so compute_loss can work.
    """
    # Simple linear map: response = 0.01 * emb
    return 0.01 * emb


def compute_loss(model, resp_emb: torch.Tensor) -> torch.Tensor:
    """
    Simple MSE loss pushing resp_emb towards 1.0.
    resp_emb shape: [1, 1]
    """
    target = torch.tensor([[1.0]], dtype=torch.float32, device=resp_emb.device)
    return (resp_emb - target).pow(2).mean()


def perturb_data(interaction: dict) -> dict:
    """
    Tiny text perturbation stub.
    """
    return {**interaction, "query": interaction["query"] + " [perturbed]"}


def augment_wisdom(wisdom, interaction):
    """
    TODO: update wisdom embeddings with this interaction.
    """
    return wisdom


def detect_emotion(text: str) -> str:
    """
    TODO: sentiment/emotion model.
    """
    return "neutral"


def synthesize_speech(model, text: str, emotion: str) -> str:
    """
    TODO: hook into TTS system.
    For now, return fake file path.
    """
    return "dummy_audio_path.wav"


def infuse_wisdom(model, emb: torch.Tensor, wisdom) -> str:
    """
    TODO: actually condition generation on emb + wisdom.
    """
    return "Infused wisdom text"


def tokenize_update(data, label: str) -> str:
    """
    TODO: stable hashing of model or interaction state.
    For now, return a stub string.
    """
    return f"hash_stub_{label}"


def commit_version(repo: str, tag: str, hash_val: str):
    """
    TODO: integrate with git / DVC.
    """
    print(f"[LegacyVault] Committed {repo}:{tag} with hash {hash_val}")


# ---------------------------------------
# Genesis: Initial Clone Accumulation
# ---------------------------------------

def initialize_soul(voice_notes_dir: str,
                    base_model: str = "facebook/hubert-large-ls960-ft"):
    """
    Bootstraps the 'soul model' from HuBERT + initial voice notes.
    """
    processor = Wav2Vec2Processor.from_pretrained(base_model)
    model = HubertForCTC.from_pretrained(base_model)

    dataset = load_voice_notes(voice_notes_dir)
    wisdom_embeddings = extract_insights(dataset)

    # Dummy training loop (replace with real audio fine-tuning)
    for epoch in range(5):
        loss = train_on_dataset(model, processor, dataset)
        print(f"[Genesis] Epoch {epoch+1} dummy loss: {loss.item():.4f}")

    soul_model = save_checkpoint(model)
    hash_val = tokenize_update(soul_model.state_dict(), "Genesis Soul")
    commit_version("LegacyVault", "v0.1", hash_val)

    return soul_model, wisdom_embeddings


# ---------------------------------------
# Markup: Evolution Loop — Reptile Spice
# ---------------------------------------

def evolve_soul(soul_model: nn.Module,
                new_interaction: dict,
                wisdom_embeddings,
                min_threshold: float = 0.85):
    """
    Lightweight Reptile-style update based on a single interaction + feedback.
    new_interaction = {"query": <str>, "feedback": <float>, ...}
    """
    feedback = new_interaction.get("feedback", 0.0)
    if feedback < min_threshold:
        print("[Markup] Drift detected — feedback too low, skipping update.")
        return soul_model, wisdom_embeddings

    optimizer = optim.Adam(soul_model.parameters(), lr=1e-3)
    initial_params = {name: param.detach().clone()
                      for name, param in soul_model.named_parameters()}

    # Reptile inner loops (still using dummy loss for now)
    for step in range(5):
        perturbed = perturb_data(new_interaction)
        emb = embed_query(perturbed["query"])
        resp_emb = generate_response(soul_model, emb, wisdom_embeddings)
        loss = compute_loss(soul_model, resp_emb)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"[Markup] Inner step {step+1} loss: {loss.item():.4f}")

    # Reptile meta-update: move 10% towards new params
    with torch.no_grad():
        for name, param in soul_model.named_parameters():
            param.data = initial_params[name] + (param.data - initial_params[name]) * 0.1

    wisdom_embeddings = augment_wisdom(wisdom_embeddings, new_interaction)
    new_hash = tokenize_update(soul_model.state_dict(), "Evolution v2")
    commit_version("LegacyVault", "v2", new_hash)

    return soul_model, wisdom_embeddings


# ---------------------------------------
# Distribution: Legacy Query Phase
# ---------------------------------------

def query_vault(soul_model: nn.Module,
                user_query: str,
                descendant_id: str,
                wisdom_embeddings):
    """
    Single entrypoint for querying the vault:
    - embed query
    - generate 'wise' text
    - optionally inject Ronism
    - synthesize speech
    - return interaction + hash
    """
    emb = embed_query(user_query)
    raw_response = infuse_wisdom(soul_model, emb, wisdom_embeddings)

    # 10% easter-egg chance
    if torch.rand(1).item() < 0.10:
        raw_response += " (Ronism: No head to swell — just stars to soar! 🚀)"

    emotion = detect_emotion(user_query)
    voice_audio = synthesize_speech(soul_model, raw_response, emotion)

    interaction = {
        "query": user_query,
        "response": raw_response,
        "feedback": None,
        "descendant_id": descendant_id,
    }

    interaction_hash = tokenize_update(interaction, f"Query {descendant_id}")
    return voice_audio, interaction, interaction_hash