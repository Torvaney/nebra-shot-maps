library(tidyverse)

data <- read_csv(here::here("data/constellations.csv"))


plot_stars <- function(data) {
  data %>%
    mutate(group = cumsum(weight != lag(weight, default = 0))) %>%
    ggplot(aes(x = x, y = y)) +
    geom_path(
      aes(size = weight, group = group),
      colour = "cornsilk",
      lineend = "round",
      alpha = 0.2
    ) +
    geom_point(
      aes(size = exp(mag)),
      shape = 21,
      colour = "cornsilk",
      fill = "white",
    ) +
    scale_size_continuous(limits = c(0, exp(7)), range = c(1, 7)) +
    theme_void() +
    theme(
      panel.background = element_rect(fill = "black"),
      legend.position = "none"
    )
}

# Does this only work because it's close to the equator?
data %>%
  filter(name == "Orion") %>%
  plot_stars()


data %>%
  filter(name == "Ursa Major") %>%
  plot_stars()


data %>%
  filter(name == "Hercules") %>%
  plot_stars()
