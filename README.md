# dither

## dither/img
the main file here is img/dither.py
it works like so
(square brackets denote optional arguments)
dither.py INPUT_FILE \[bit depth (1..8)\] \[color type (grey, color)\] \[dither type (floydsteinberg, sierralite, burkes, sierra2, jarvis, sierra3, stucki, ostromoukhov, shiaufan, all)\]


## dither/ciedither
this is a failed experiment with colorimetry
main file is ciedither/ciedither.py
cie.py is also a fast (for idiomatic python) colorimetry library so if that's your thing
