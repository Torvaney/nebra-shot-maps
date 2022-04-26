suppressPackageStartupMessages(library(tidyverse))
library(ggsoccer)
source(here::here("src", "R", "common.R"))

constellation <- parse_args()
data <- read_csv(here::here("data", "constellations", constellation, "shots.csv"))

plot_shots <- function(data) {
  data %>%
    ggplot(aes(x = x, y = y)) +
    annotate_pitch(
        colour = colours$link,
        fill   = colours$nightsky,
        goals  = goals_strip
    ) +
    geom_point(
      colour = "cornsilk",
      size = 3
    ) +
    theme_common()
}

plot_shots(data) %>%
  ggsave(here::here("data", "constellations", constellation, "shots.png"),
    plot = .,
    width = 6,
    height = 6*aspect_ratio
  )
