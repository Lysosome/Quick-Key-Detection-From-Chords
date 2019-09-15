Welcome to the repo for the quick-key-finder algorithm! This is a lightweight algorithm for inferring the overall key of a song from its chords.

This repo was developed as part of the project "Learning Shared Vector Representations of Lyrics and Chords in Music" by Greer, T., Singla, K., Ma, B., and Narayanan, S. at the Signal Analysis & Interpretation Laboratory at the University of Southern Califonia.
You can find our paper in the proceedings of ICASSP, Brighton, UK, 2019.

The algorithm itself is described in the "findTonicNum" function in the file findTonic.py. To test the algorithm, you can run

python count_cadences_multisong_tonic_tester.py

with Python 3.x, which will predict the tonic key of the first 50 songs in "chords_uku_english_only_songmarkers.txt", our dataset of chord arrangements from Ukutabs.com.
