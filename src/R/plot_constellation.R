suppressPackageStartupMessages(library(tidyverse))
source(here::here("src", "R", "common.R"))

constellation <- parse_args()
stars <- read_csv(here::here("data", "constellations", constellation, "stars_transformed.csv"))
links <- read_csv(here::here("data", "constellations", constellation, "links_transformed.csv"))

plot_stars <- function(stars, links) {
  links %>%
    mutate(group = cumsum(weight != lag(weight, default = 0))) %>%
    ggplot(aes(x = x, y = y)) +
    geom_path(
      aes(group = group),
      colour = colours$link,
      lineend = "round",
      size = 0.5
    ) +
    geom_point(
      aes(size = exp(mag)),
      colour = "cornsilk",
      data = stars
    ) +
    scale_size_continuous(limits = c(0, exp(7)), range = c(1, 7)) +
    theme_common()
}

plot_stars(stars, links) %>%
  ggsave(
    here::here("data", "constellations", constellation, "stars.png"),
    plot = .,
    width = 6,
    height = 6*aspect_ratio
  )
