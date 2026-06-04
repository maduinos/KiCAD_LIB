# Maduinos KiCad Library

Personal KiCad symbol, footprint, and 3D model library used for Maduinos hardware experiments.

This repository is focused on practical board design assets for FPGA, memory, power, ADC, and connector related parts. The files are kept as plain KiCad library assets so they can be added to a KiCad project without extra build tooling.

## Repository Layout

```text
symbols/                 KiCad symbol libraries
footprints/              KiCad footprint libraries
footprints/*.pretty/     KiCad footprint library directories
3dmodels/                STEP/STP 3D model files
```

## Included Symbols

- AMD/Xilinx Zynq-7000 and Zynq UltraScale+ parts
  - `XC7Z010-1CLG400I`
  - `XC7Z020-1CLG400I`
  - `XC7Z030-2FFG676I`
  - `XCZU2CG-1SFVA625E`
- Memory and flash parts
  - `K4B4G1646E-BCMA`
  - `KLM8G1GETF-B041`
  - `MT25QU128ABA1EW9-0SIT`
- Mixed signal and power parts
  - `ADC128S102CIMT_NOPB`
  - `TLC5922DAPR`
  - `TPS65218D0RSLR`

## Included Footprints and 3D Models

The footprint libraries include BGA, FBGA, PDFN, DAP, PW, and RSL style packages used by the symbols above. Matching STEP/STP models are stored in `3dmodels/` where available.

Common footprint groups include:

- `CLG400_AMD`
- `CLG400_ZYNQ-7000_AMD`
- `FFG676/FFV676_AMD`
- `FBGA98_K4B4G1646E-BCMA_SAM`
- `KLMBG2JENB-B041_SAM`
- `PW0016A`
- `RSL0048B`
- `W-PDFN-8MLP8_W9_MRN`

## KiCad Usage

1. Clone this repository or add it as a submodule inside your hardware project.
2. In KiCad, open `Preferences` > `Manage Symbol Libraries`.
3. Add the required `symbols/*.kicad_sym` files as project or global symbol libraries.
4. Open `Preferences` > `Manage Footprint Libraries`.
5. Add the required `.pretty` directories under `footprints/`.
6. Configure the 3D model search path to point to this repository's `3dmodels/` directory if KiCad cannot resolve models automatically.

Project-local library registration is recommended so each board design keeps an explicit dependency on the library revision it was designed with.

## Validation Notes

- Check every symbol pinout against the current manufacturer datasheet before releasing a board.
- Check BGA orientation, pin 1 marking, courtyard, paste, and solder mask rules against the PCB manufacturer's process limits.
- Treat 3D models as mechanical fit references. They do not replace package drawing checks.
- When using manufacturer-derived package data, verify that the latest datasheet has not changed dimensions, pin names, or recommended land pattern details.
- Footprint filenames and internal footprint names are expected to stay synchronized.

## License

No license file has been selected yet. Until a license is added, ask the repository owner before reusing these assets outside Maduinos projects.
