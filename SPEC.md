# 04 · Cable Bunny, the USB-C cable tester: SPEC

## Who it's for, and the use case

Anyone with a drawer of USB-C cables, which is everyone. Half of them are "charge-only" and silently
refuse to sync a phone, flash a microcontroller or connect a monitor, and nothing on the cable says
which. Plug both ends of a cable into the bunny's feet, boop its nose, and its ears tell you what the
cable really carries. Ten seconds per cable; sort the drawer once.

## The cute concept

A white bunny drawn in black ink, with gold cheeks and a heart on its chest. Its ears are the readout:
the left ear is "power" (VBUS, GND, CC), the right ear "data" (D+, D-, SBU), each line with its own
labelled LED. Its two feet are the two USB-C receptacles. Its nose is the button. The heart lights to
say "my battery is fine", so no light anywhere else always means "this wire is broken", never "dead
battery".

## Features

| | |
|---|---|
| Lines tested | VBUS, GND, CC, D+, D-, SBU (both SBU wires joined); either plug orientation at either end |
| Reading it | VBUS + GND + CC = charges · + D+ and D- = carries USB 2.0 data · + SBU = a full-featured cable (USB 3 / Thunderbolt / DisplayPort alt mode). The legend is printed on the back. |
| Not tested | the SuperSpeed pairs (the 16-pin receptacles have no contacts for them) and the cable's current rating or e-marker contents |
| Power | one CR2032, connected only while the nose is held: zero standby drain |
| Safety in a mistake | a B5819W Schottky stops a powered cable (a USB-A charger puts 5 V on VBUS) from ever charging the lithium cell; 150 Ω on every driven line and 220 Ω on every LED limit any short or a charger plugged into a foot |
| MCU | none: a button, a diode, 12 resistors and 7 LEDs |
| Board | 2 layers, white mask, black silk, ENIG; single-sided SMT, 25 placed parts; QR and legend on the back |

## Power budget and battery life

Only while the nose is pressed: each line LED ≈ 2.2 mA (2.75 V test rail, red/yellow Vf ≈ 1.85 V,
150 Ω + 220 Ω), the GND and heart LEDs ≈ 2.7 mA (330 Ω). A good full-featured cable lights all seven:
≈ 17 mA. A 3-second test uses ≈ 0.014 mAh, so the 180 mAh usable in a CR2032 is about **12,000 tests**.
Nothing draws current between tests; the cell ages on its shelf life. Design estimates from datasheet
typicals; no Cable Bunny has been built.

## BOM (100 units, live JLC/LCSC prices read 2026-10-05)

| Refs | Value | Qty | LCSC | MPN | Class | Unit @100 | Line |
|---|---|---|---|---|---|---|---|
| BT1 | CR2032 holder | 1 | C5213768 | 3034TR | extended | $0.3602 | $0.3602 |
| C1 | 10uF | 1 | C15850 | CL21A106KAYNNNE | basic | $0.0773 | $0.0773 |
| D1 | B5819W | 1 | C8598 | B5819W SL | basic | $0.0261 | $0.0261 |
| D2,D3,D7,D8 | Red (VBUS, CC, GND, heart) | 4 | C2286 | KT-0603R | basic | $0.0073 | $0.0292 |
| D4,D5,D6 | Yellow (D+, D-, SBU) | 3 | C2287 | KT-0603Y | extended | $0.0107 | $0.0321 |
| J1,J2 | USB-C | 2 | C165948 | TYPE-C-31-M-12 | extended | $0.1468 | $0.2936 |
| R1-R5 | 150 | 5 | C22808 | 0603WAF1500T5E | basic | $0.0015 | $0.0075 |
| R6-R10 | 220 | 5 | C22962 | 0603WAF2200T5E | basic | $0.0014 | $0.0070 |
| R11,R12 | 330 | 2 | C23138 | 0603WAF3300T5E | basic | $0.0016 | $0.0032 |
| SW1 | TS-1187A | 1 | C318884 | TS-1187A-B-A-B | basic | $0.0197 | $0.0197 |
| | **Parts** | | | | | | **$0.86** |
| | Extended-part loading fee ($3 x 3 / 100 boards) | | | | | | $0.09 |
| | **BOM per board @100** | | | | | | **$0.95** |

Not in the BOM: the PCB (2 layers, ENIG, 40.1 x 96.2 mm), assembly labour and the CR2032 cell.
Machine-readable, line by line: [`bom_cost.json`](bom_cost.json).

## Dimensions

40.1 x 96.2 mm (Edge.Cuts bounding box, pcbnew), 32.9 cm², 1.6 mm FR4. The two receptacles are 20 mm
apart, centre to centre, so two cable ends of any common overmould size fit side by side.

## Mounting plan (no enclosure)

It lives on the desk or in the cable drawer, lying on its back (flat, no parts on the back). Optional:
two clear 8 mm bumpons under the belly stop it sliding when you push a plug in. Its ears are long
enough to grip while you plug.

## Safety

3 V coin cell only, connected only while you press. The Schottky means a charger can never back-feed
the lithium cell; every path to a connector has its own resistor, so a shorted cable or a charger in
the wrong foot lights LEDs instead of heating anything. The receptacles' shells are not used as a
ground path at the far end, so a cable whose shield is good but whose ground wire is broken shows a
dark GND LED. Every corner of the outline is rounded (1.5 mm minimum).

**Coin cell, launch blocker.** A swallowed coin cell is a medical emergency. In the US, Reese's Law
(16 CFR part 1263, in force since March 2024) requires a consumer product's button or coin cell to be
secured so that it takes a tool, or two independent simultaneous hand movements, to remove, and it adds
warning-label and packaging requirements. A bare Keystone 3034 holder does not meet that. Before selling
this board assembled with a cell, add a screwed retainer over the cell (or ship it without one) and have
the product and its labels reviewed for compliance. Not done in rev A.

## Verification (measured by KiCad 10.0.6 on the files in this folder)

ERC 0 errors / 0 warnings · netlist round trip identical (22 nets) · routing 58 → 0 open (244 tracks,
27 vias) · DRC 0 errors / 0 unconnected / 0 parity, 2 warnings (`lib_footprint_mismatch` on J1 and J2:
the receptacles' overhanging footprint silk clipped on the placed copies) · DFM `jlcpcb_2layer` 0
errors · fab gate ready. Full numbers: [`report.json`](report.json), [`measured.json`](measured.json).

The first build had 2 `silk_edge_clearance` warnings: the SDK's silk stage tested only the four corners
of the back title, which straddled the notch between the ears. The stage now tests the whole box.

**Not built yet.** Not fabricated, assembled or powered. On the first prototypes, check each LED with a
known-good full-featured cable, a known charge-only cable, and an e-marked 5 A cable (its CC LED glows
dimmer: the plug's 1 kΩ Ra shunts it).
