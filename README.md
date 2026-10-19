# Who Is Tapping? Wrist-Worn Acousto-Kinematic Biometrics from Thumb–Finger Tap Rhythms

Code, firmware and hardware for the paper *Who Is Tapping? Wrist-Worn Acousto-Kinematic Biometrics from Thumb–Finger Tap Rhythms*
(Md. Azizul Hakim Bappy and Hossen Asiful Mustafa, *Pattern Recognition*, **[YEAR]**).

A wrist-worn device records a six-axis IMU (polled at 1 kHz) and a 16 kHz skin-contact microphone
while the user taps the thumb against the fingertips in a fixed four-tap sequence (middle, middle,
index, middle). A frozen recognition pipeline verifies the user from the tap sound conducted to the
wrist, the wrist kinematics and the timing and shape of the taps. The sequence itself is public:
impostors perform the same sequence at their own natural timing.

- **Processed dataset:** Zenodo, DOI **[ZENODO_DATA_DOI]**
- **This code, archived:** Zenodo, DOI **[ZENODO_CODE_DOI]**

## Repository layout

| Path | Contents |
|---|---|
| `checkpoint_c035/` | The frozen recogniser: feature extraction (`checkpoint_engine.py`, `run_checkpoint.py`) and parameters (`parameters.json`, which records the engine's SHA-256). Do not modify. |
| `analysis/results/` | Main results (`make_results.py`), baselines and ablations (`make_baselines.py`), gyroscope ablation (`make_gyro.py`), loader for the released features (`release_data.py`). Output: `analysis/results/out/`. |
| `analysis/session2.py` | Cross-session study (session 2, 20 days later). |
| `analysis/tables/` | The paper's result tables as LaTeX (`make_tables.py`). |
| `analysis/figures/` | The paper's data figures (`make_figures.py`, style in `figstyle.py`) and the TikZ sources of the pipeline and protocol diagrams. |
| `dataset_collector/` | *Tap Studio*: Flask app for data collection, with live enrollment and verification by the frozen recogniser. |
| `firmware/` | Acquisition firmware for the ESP32-S3 (FreeRTOS tasks; IMU polled at 1 kHz over I²C, 16 kHz I²S microphone, packets with CRC over USB serial at 921,600 baud). |
| `hardware/` | Enclosure (STL) and parts list. |
| `hardware/esp32_benchmark/` | C port of the frozen verifier for the ESP32-S3 (`tap_verify_esp32/`), the host script that times it and checks it against the Python engine (`esp32_bench.py`), the energy estimate (`energy_estimate.py`) and the measured results (`results/`). |
| `reproduce.py` | Runs every analysis from the processed dataset and checks the headline numbers. |

## Reproduce the paper

```bash
python -m pip install -r requirements.txt
# download the Zenodo dataset and put its files into data/
python reproduce.py
```

`reproduce.py` runs the analyses, the baselines and ablations, the cross-session study, the tables,
the figures and the energy estimate on the released features (about 10 minutes on a laptop), and
compares the headline numbers with `analysis/expected_results.json`.

The released features cover every table and every data figure, with two exceptions that need the
raw recordings: the audio waveform in the signal figure (its envelope is drawn) and the figure that
follows one tap through feature extraction (`fig_descriptors`). Feature extraction itself also needs
the raw recordings (see below); their SHA-256 checksums are part of the dataset, so recordings
obtained on request can be verified against the ones used in the paper. With the raw recordings in
`dataset/` and `2nd session/`, the same scripts run end to end from raw data.

The ESP32-S3 timings come from `hardware/esp32_benchmark/esp32_bench.py`, which needs the board and
the raw recordings; its measured results are included in `hardware/esp32_benchmark/results/`.

## Data availability

The processed features are public (CC BY 4.0, Zenodo). The raw sensor recordings are available from
the corresponding author on reasonable request, subject to approval by the Institutional Review
Board of Bangladesh University of Engineering and Technology (BUET) and a data-use agreement.

## Live demo

```bash
cd dataset_collector
python -m pip install -r requirements.txt
set SENSOR_PORT=COM6   # the board's serial port (default COM3); on Linux/macOS: export SENSOR_PORT=/dev/ttyACM0
python app.py          # http://127.0.0.1:5000
```

Page *04 Authenticate* enrolls a user with five episodes of the tap sequence and verifies new
attempts in real time.

## Citation

See `CITATION.cff`, or cite the paper: **[FULL REFERENCE]**.

## Licence

Code and firmware: MIT (`LICENSE`). Hardware design: **[HARDWARE_LICENCE, e.g. CERN-OHL-P-2.0]**.
Dataset: CC BY 4.0 (Zenodo).
