# India Fourier Visualizer

A public, no-index experiment at [nilansa.github.io/india-fourier/](https://nilansa.github.io/india-fourier/).

Task ID: `india-fourier-20261113-a1`. The full visualizer is `/explainer/explainers/india-fourier-visualizer-2026-11-13.html`.

## Method

- Natural Earth 1:110m India polygon, via [geo-boundaries-world-110m](https://github.com/datasets/geo-boundaries-world-110m) (ODC-PDDL).
- 135 unique polygon vertices, projected to a flat plane with a longitude scale of cos(21 degrees); no islands; not a political or survey map.
- Resample the closed ring to 768 equal-arc-length points; compute a complex discrete Fourier transform.
- Reconstruct `z_K(theta)=c_0+sum_{n=1..K}(c_n exp(i*n*theta)+c_-n exp(-i*n*theta))`, K=1..128.
- Changing theta rotates each vector while the Fourier coefficients remain fixed. Increasing K adds two harmonic terms.
- Show RMS point error relative to the diagonal of the same simplified input border.

## Numeric verification

K=1: approximately 9.51%; K=8: 1.453%; K=24: 0.559%; K=96: 0.077% RMS error of the normalized boundary diagonal. These measure reconstruction fit to the generalized source, not geographic accuracy.

The web experiment is client-side and needs no JavaScript framework or API key. It can export the active coefficients as CSV.
