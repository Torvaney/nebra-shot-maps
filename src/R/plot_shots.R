suppressPackageStartupMessages(library(tidyverse))
library(ggsoccer)
source(here::here("src", "R", "common.R"))

constellation <- parse_args()
data <- read_csv(here::here("data", "constellations", constellation, "shots.csv"))

plot_shots <- function(data) {
  data %>%
    ggplot(aes(x = x, y = y)) +
    annotate_pitch(
        colour = "#5e5e5e",
        fill = "black",
        goals = goals_strip
    ) +
    geom_point(
      shape = 21,
      colour = "cornsilk",
      fill = "white",
      size = 3
    ) +
    theme_common()
}

plot_shots(data) %>%
  ggsave(here::here("data", "constellations", constellation, "shots.png"), plot = .)
