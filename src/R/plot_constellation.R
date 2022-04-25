library(tidyverse)

constellation <- "Ori"

stars <- read_csv(here::here("data", "constellations", constellation, "stars.csv"))
links <- read_csv(here::here("data", "constellations", constellation, "links.csv"))

plot_stars <- function(stars, links) {
  links %>%
    mutate(group = cumsum(weight != lag(weight, default = 0))) %>%
    ggplot(aes(x = x, y = y)) +
    geom_path(
      aes(size = weight, group = group),
      colour = "#e3e2de",
      lineend = "round",
      alpha = 0.2
    ) +
    geom_point(
      aes(size = exp(mag)),
      colour = "cornsilk",
      fill = "white",
      data = stars
    ) +
    scale_size_continuous(limits = c(0, exp(7)), range = c(1, 7)) +
    theme_void() +
    theme(
      panel.background = element_rect(fill = "black"),
      legend.position = "none"
    )
}

plot_stars(stars, links)
