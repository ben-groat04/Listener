"""Round-1 reference predictor ca_local (w3r1-content-audio, time-local MERT window logits), exposed under its own name for the final runs.
Usage: python3 -W ignore -m evalkit.run predictors/w3r2-audio-taste/predict.py predictors/w3r2-audio-taste/ref_ca_local.py"""
import sys; sys.path.insert(0, "/home/user/Listener/taste-model/predictors/w3r1-content-audio")
import predict as _p
PREDICTORS = {"ca_local": _p.make(mode="local")}
