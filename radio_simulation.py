"""
ResQLink: Digital Radio Signal Simulation
----------------------------------------
Demonstrates a simplified BPSK transmit/channel/receive chain in software.

IMPORTANT:
- This program simulates a radio-like waveform; it does NOT transmit RF.
- It is a learning prototype for digital modulation and demodulation.
- Real over-the-air transmission requires suitable, compliant RF hardware.
"""

import numpy as np
import matplotlib.pyplot as plt


def bits_to_bpsk(bits: np.ndarray) -> np.ndarray:
    """Map bit 0 -> +1 and bit 1 -> -1 (BPSK symbols)."""
    return 1.0 - 2.0 * bits.astype(float)


def modulate_bpsk(bits: np.ndarray, samples_per_bit: int = 100,
                  carrier_cycles_per_bit: int = 5) -> tuple[np.ndarray, np.ndarray]:
    """Generate a real-valued BPSK passband waveform for display/simulation."""
    symbols = bits_to_bpsk(bits)
    t = np.arange(len(bits) * samples_per_bit) / samples_per_bit
    phase = 2.0 * np.pi * carrier_cycles_per_bit * t
    symbol_stream = np.repeat(symbols, samples_per_bit)
    tx_wave = symbol_stream * np.cos(phase)
    return t, tx_wave


def demodulate_bpsk(rx_wave: np.ndarray, bits_count: int,
                    samples_per_bit: int = 100,
                    carrier_cycles_per_bit: int = 5) -> np.ndarray:
    """Coherently demodulate using a matching carrier and integrate per bit."""
    t = np.arange(len(rx_wave)) / samples_per_bit
    reference = np.cos(2.0 * np.pi * carrier_cycles_per_bit * t)
    mixed = rx_wave * reference
    chunks = mixed.reshape(bits_count, samples_per_bit)
    decision_metric = chunks.sum(axis=1)
    # The transmitter maps 0 to +1 and 1 to -1.
    return (decision_metric < 0).astype(np.uint8)


def run_simulation() -> None:
    rng = np.random.default_rng(7)  # fixed seed makes the demo reproducible
    message = "RESQLINK SOS"
    payload = np.fromiter(
        (int(bit) for char in message for bit in format(ord(char), "08b")),
        dtype=np.uint8
    )

    samples_per_bit = 100
    carrier_cycles_per_bit = 5
    noise_std = 0.35

    t, tx = modulate_bpsk(payload, samples_per_bit, carrier_cycles_per_bit)
    noise = rng.normal(0.0, noise_std, size=tx.size)
    rx = tx + noise
    recovered = demodulate_bpsk(
        rx, len(payload), samples_per_bit, carrier_cycles_per_bit
    )

    errors = int(np.count_nonzero(payload != recovered))
    ber = errors / len(payload)
    recovered_text_bits = "".join(str(int(b)) for b in recovered)
    recovered_bytes = [
        recovered_text_bits[i:i + 8]
        for i in range(0, len(recovered_text_bits), 8)
    ]
    recovered_message = "".join(
        chr(int(byte, 2)) for byte in recovered_bytes if len(byte) == 8
    )

    print("=" * 58)
    print("ResQLink — Digital Radio Signal Simulation")
    print("=" * 58)
    print(f"Original message : {message!r}")
    print(f"Recovered message: {recovered_message!r}")
    print(f"Payload bits     : {len(payload)}")
    print(f"Bit errors       : {errors}")
    print(f"Bit error rate   : {ber:.4f}")
    print("Result           :", "PASS" if errors == 0 else "CHECK NOISE / PARAMETERS")
    print()
    print("This is a SOFTWARE SIMULATION. No RF signal was transmitted.")

    # Show a readable excerpt rather than all bits.
    show_bits = min(12, len(payload))
    samples_to_show = show_bits * samples_per_bit
    bit_times = np.arange(show_bits + 1)

    fig, axes = plt.subplots(4, 1, figsize=(12, 9), constrained_layout=True)
    fig.suptitle("ResQLink — BPSK Digital Radio Simulation", fontsize=16, fontweight="bold")

    axes[0].step(np.arange(show_bits), payload[:show_bits], where="post")
    axes[0].set_title("1. Original digital bits (excerpt)")
if __name__ == "__main__":
    run_simulation()
