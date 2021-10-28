import { min, max, range } from "lodash-es";
import pokemons from "./pokemons.json";
import points from "./points.json";

const xs = points.map((p) => p[0]);
const ys = points.map((p) => p[1]);
const xMin = min(xs) - 1;
const xMax = max(xs) + 1;
const yMin = min(ys) - 1;
const yMax = max(ys) + 1;
const dx = xMax - xMin;
const dy = yMax - yMin;

const centroids = [
  [-143.09721396, 51.69741775],
  [69.67250791, -52.70479393],
  [481.11023181, 281.82817426],
];

const $points = document.getElementById("points");
const $centroids = document.getElementById("centroids");

$points.innerHTML = points
  .map((point, i) => {
    const top = (1 - (point[1] - yMin) / dy) * 100;
    const left = ((point[0] - xMin) / dx) * 100;
    const pokemon = pokemons[i];

    return `<div class="point" data-gen="${pokemon.generation}" style="top:${top}%;left:${left}%">
        <img width="50" height="50" src="${pokemon.image}"/>
    </div>`;
  })
  .join("");

$centroids.innerHTML = centroids
  .map((point, i) => {
    const top = (1 - (point[1] - yMin) / dy) * 100;
    const left = ((point[0] - xMin) / dx) * 100;

    return `<div class="centroid" style="top:${top}%;left:${left}%"></div>`;
  })
  .join("");

const $controls = document.getElementById("controls");

range(0, 8).forEach((i) => {
  const $button = document.createElement("button");
  $button.innerHTML = `Gen ${i + 1}`;

  $button.addEventListener("click", () => {
    document
      .querySelectorAll(`.point:not([data-gen="${i + 1}"])`)
      .forEach((el) => el.classList.add("hidden"));
    document
      .querySelectorAll(`.point[data-gen="${i + 1}"]`)
      .forEach((el) => el.classList.remove("hidden"));
  });

  $controls.append($button);
});
