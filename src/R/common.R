suppressPackageStartupMessages(library(tidyverse))


colours <- list(
    nightsky = "#0b1026",
    link     = "#5e5e5e",
    star     = "cornsilk"
)

parse_args <- function() {
    args <- commandArgs(trailingOnly = TRUE)
    constellation <- args[1]

    if (!constellation_is_valid(constellation)) {
        message(str_glue("Constellation {constellation} has no match.json! Skipping."))
        quit(save="no", status=0)
    }

    constellation
}

constellation_is_valid <- function(constellation) {
    file.exists(here::here("data", "constellations", constellation, "match.json"))
}

aspect_ratio <- 60/100

theme_common <- function() {
    list(
        coord_flip(xlim = c(50, 105), ylim = c(-1, 101)),
        ggsoccer::theme_pitch(aspect_ratio = aspect_ratio),
        theme(panel.background = element_rect(fill = colours$nightsky),
              plot.background  = element_rect(fill = colours$nightsky, colour = NULL),
              legend.position  = "none")
    )
}
