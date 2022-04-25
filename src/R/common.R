suppressPackageStartupMessages(library(tidyverse))


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


theme_common <- function() {
    list(
        coord_flip(xlim = c(50, 105), ylim = c(-1, 101)),
        ggsoccer::theme_pitch(),
        theme(panel.background = element_rect(fill = "black"),
              legend.position = "none")
    )
}
