"""DECLARED FINAL (w5r2-music-recipe-numbers): avg81 = equal-weight average of the final scores of the 81-member family grid.FAMILY_AVG
(clip eps in {1e-5,1e-4,1e-3} x essentia ridge alpha in {3e3,1e4,3e4} x GBM size in {40,80,160 iterations} x MERT weight in {0.5,1,2}; member weights 1/1/1.5, median fill as in the recipe)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import procs
PREDICTORS = {"final_avg81": procs.avg_family()}
