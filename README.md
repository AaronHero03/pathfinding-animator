# Pathfinder visualizator

## DESCRIPTION

This repository is a fork of the original maps-pathfinding project by @santifiorino, which was used for the YouTube video "Comparing Algorithms: A\* vs Dijkstra, on the city's map."

This version has been specifically modified to include and document the necessary logic to generate dynamic, frame-by-frame animations of the A\* and Dijkstra pathfinding algorithms as they explore the city map. These animations provide a clear, visual comparison of the search process, showing which roads are considered before the final path is found.

![paragit](assets/dijkstra_animation.gif)

## INTRODUCTION

The experiments conducted in the original work can now be easily reproduced, with the added capability of saving each intermediate frame to create a complete visual animation of the search process.

The main focus of this fork is to implement the printing mechanism to save every intermediate step, allowing users to generate high-quality MP4 or GIF animations directly from the python script.
