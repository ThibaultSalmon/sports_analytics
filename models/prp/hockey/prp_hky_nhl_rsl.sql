{{ config(
    alias ='HKY_NHL_RSL'

)}}

select 
"id" as id,
"League" as league,
"Season" as season,
"Date" as game_date,
"Time" as game_time,
case 
    when "Overtime/TAB" = 'Après TAB' then 'After shootout' 
    when "Overtime/TAB" = 'Après prol.' then 'After overtime' 
end as overtime_or_shootout,
"Id game (Flashscore)" as game_id,
"Game" as game,
"Home team" as home_team,
"Away team" as away_team,
concat("Result home", ' - ', "Result away") as final_score,
"Result game" as result_game,
case 
    when ("Result game" = 'H') or ("Result home" > "Result away") THEN "Home team"
    when ("Result game" = 'A') or ("Result home" < "Result away") THEN "Away team"
end as winning_team,
"Total goals" as total_goals,
"Total goals before overtime" as goals_before_overtime,
"Result home" as home_goals,
"Result away" as away_goals,
"Result 1st TT" as first_TT_winner,
"Goals 1st TT" as first_TT_goals,
"More than 1,5 goals 1st TT" as over_1_5_goals_1st_TT,
"1st TT - home" as home_goals_1st_TT,
"1st TT - away" as away_goals_1st_TT,
"Result 2nd TT" as second_TT_winner,
"Goals 2nd TT" as second_TT_goals,
"More than 1,5 goals 2nd TT" as over_1_5_goals_2nd_TT,
"2nd TT - home" as home_goals_2nd_TT,
"2nd TT - away" as away_goals_2nd_TT,
"Result 3rd TT" as third_TT_winner,
"Goals 3rd TT" as third_TT_goals,
"More than 1,5 goals 3rd TT" as over_1_5_goals_3rd_TT,
"3rd TT - home" as home_goals_3rd_TT,
"3rd TT - away" as away_goals_3rd_TT,
"TT with more goals" as most_goals_period,
"4th TT - home" as home_goals_overtime,
"4th TT - away" as away_goals_overtime,
"5th TT - home" as home_goals_shootout,
"5th TT - away" as away_goals_shootout,
"+4,5 goals" as over_4_5_goals,
"+5,5 goals" as over_5_5_goals,
"+6,5 goals" as over_6_5_goals,
"+7,5 goals" as over_7_5_goals

from {{ source('raw', 'HKY_NHL_RSL') }}