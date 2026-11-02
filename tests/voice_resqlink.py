
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
DURATION = 5
SAMPLES_PER_BIT = 20
NOISE_STD = 0.15


def record_voice():
    print("ResQLink: Voice Capture")
    input("Press Enter, then speak after recording starts...")

    print(f"Recording for {DURATION} seconds. Speak now!")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    audio = audio.flatten()
    audio = np.clip(audio, -1.0, 1.0)

    write("original_voice.wav", SAMPLE_RATE,
          (audio * 32767).astype(np.int16))

    print("Recording saved: original_voice.wav")
    return audio


def transmit_simulation(audio):
    # Quantize each audio sample to 8-bit unsigned data.
    pcm = np.round((audio + 1.0) * 127.5)
    pcm = np.clip(pcm, 0, 255).astype(np.uint8)

    # Convert bytes to a bit stream.
    bits = np.unpackbits(pcm)

    # BPSK: 0 -> +1, 1 -> -1.
    symbols = 1.0 - 2.0 * bits.astype(float)

    # Simulate a noisy channel using repeated symbols.
    repeated = np.repeat(symbols, SAMPLES_PER_BIT)
    rng = np.random.default_rng(42)
    received = repeated + rng.normal(
        0.0, NOISE_STD, size=repeated.size
    )

    # Recover one decision per bit.
    blocks = received.reshape(-1, SAMPLES_PER_BIT)
    recovered_bits = (blocks.mean(axis=1) < 0).astype(np.uint8)

    recovered_bytes = np.packbits(recovered_bits)
    recovered_pcm = recovered_bytes.astype(np.float32) / 127.5 - 1.0

    bit_errors = int(np.count_nonzero(bits != recovered_bits))
    ber = bit_errors / len(bits)

    print("\n--- ResQLink Voice Simulation ---")
    print(f"Audio samples : {len(audio)}")
    print(f"Transmitted bits: {len(bits)}")
    print(f"Bit errors    : {bit_errors}")
    print(f"Bit error rate: {ber:.6f}")
    print("No actual RF transmission occurred.")

    return np.clip(recovered_pcm, -1.0, 1.0)


def main():
    original = record_voice()
    recovered = transmit_simulation(original)

    write(
        "recovered_voice.wav",
        SAMPLE_RATE,
        (recovered * 32767).astype(np.int16)
    )

    print("\nPlaying recovered audio...")
    sd.play(recovered, SAMPLE_RATE)
    sd.wait()

    print("Saved recovered audio: recovered_voice.wav")
    print("ResQLink voice test complete.")


if __name__ == "__main__":
    main()
