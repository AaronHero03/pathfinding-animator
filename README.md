# Pathfinder visualizator

This repository is a fork of the original maps-pathfinding project by @santifiorino, which was used for the YouTube video "Comparing Algorithms: A\* vs Dijkstra, on the city's map."

This version has been specifically modified to include and document the necessary logic to generate dynamic, frame-by-frame animations of the Dijkstra pathfinding algorithms as they explore the city map. These animations provide a clear, visual comparison of the search process, showing which roads are considered before the final path is found.

> **Dijkstra visualization**

<div align="center">
  <img src="assets/dijkstra_animation.gif" width="650" alt="Animated GIF showing the Dijkstra algorithm searching for the path on a city map.">
</div>

## Introduction

The experiments conducted in the original work can now be easily reproduced, with the added capability of saving each intermediate frame to create a complete visual animation of the search process.

The main focus of this fork is to implement the printing mechanism to save every intermediate step, allowing users to generate high-quality MP4 or GIF animations directly from the python script.

## Installation

This project requires Python and uses the following main libraries: **osmnx** and **matplotlib**.

To quickly set up the environment, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/AaronHero03/pathfinding-animator.git](https://github.com/AaronHero03/pathfinding-animator.git)
   cd pathfinding-animator
   ```

2. **Install dependencies:** Use the provided `requirements.txt` file to install all necessary packages via pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis:** Open the `main.py` file in and setup your personal preferences to run.

## Credits and original repo

This project is based on the excellent work of @santifiorino. Original Repository: https://github.com/santifiorino/maps-pathfinding
