with

games as (
  select
    base_game.*,
    home_team.name || ' ' || goals1 || ' - ' || goals2 || ' ' || away_team.name as game_label
  from base_game
  join base_team as home_team
    on home_team.id = base_game.team1_id
  join base_team as away_team
    on away_team.id = base_game.team2_id
  where tournament_id in (2, 3, 4, 5, 22)
),

shots as (
  select
    base_event.id,
    game_id,
    base_event.team_id,
    base_team.name as team,
    games.game_label,
    games.kickoff,
    x,
    y,
    base_eventtype."name" as event_type
  from base_event
  join base_eventtype
    on base_eventtype.id = base_event.type_id
  join games
    on games.id = base_event.game_id
  join base_team
    on base_team.id = base_event.team_id
  where base_eventtype."name" in ('Goal', 'Post', 'Attempt Saved', 'Miss')
)


select * from shots;
