
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
        ggplot2::coord_flip(xlim = c(50, 105), ylim = c(-1, 101)),
        ggsoccer::theme_pitch(aspect_ratio = aspect_ratio),
        ggplot2::theme(
            panel.background = ggplot2::element_rect(fill = colours$nightsky),
            plot.background  = ggplot2::element_rect(fill = colours$nightsky, colour = NULL),
            legend.position  = "none"
        )
    )
}

star_cols <- readr::cols(
    mag = readr::col_double(),
    ra = readr::col_double(),
    npd = readr::col_double(),
    dec = readr::col_double(),
    bayer = readr::col_character(),
    superscript = readr::col_character(),
    constellation = readr::col_character(),
    name = readr::col_character(),
    ra_radians = readr::col_double(),
    dec_radians = readr::col_double(),
    raw_x = readr::col_double(),
    raw_y = readr::col_double(),
    x = readr::col_double(),
    y = readr::col_double()
)

shot_cols <- readr::cols(
    id = readr::col_character(),
    game_id = readr::col_double(),
    team_id = readr::col_double(),
    team = readr::col_character(),
    game_label = readr::col_character(),
    kickoff = readr::col_datetime(),
    x = readr::col_double(),
    y = readr::col_double(),
    event_type = readr::col_character()
)
