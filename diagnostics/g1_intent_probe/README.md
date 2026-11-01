# Original G1 intent diagnostic templates

Do not install these templates directly. No native helper or launcher descriptor is
shipped here. Use `tools/build_g1_probe.py --target-bound-intent` with the installed
AGOT source to generate a PRIVATE standalone probe outside this checkout. The
generated helper contains proprietary installed code and must never be published.
See docs/G1_INTENT_PROBE.md. No engine behavior, AI policy or compatibility verified.
