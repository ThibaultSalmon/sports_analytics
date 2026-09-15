{{ config(
    alias ='HKY_NHL_DTL'

)}}

select 
"id" as id,
"Match ID" as game_id,
"Venue" as venue,
"Attendance" as attendance,
case 
    when "Stage Name" = '1. période' then '1st TT'
    when "Stage Name" = '2. période' then '2nd TT'
    when "Stage Name" = '3. période' then '3rd TT'
    when "Stage Name" = 'Prolongation' then 'Overtime'
    when "Stage Name" = 'Tirs aux buts' then 'Shootout'
end as period,
"Incident Team" as incident_team,
"Participant" as player,
"Incident" as incident_type,
"Subname" as incident_detail,
"Time" as incident_time

from {{ source('raw', 'HKY_NHL_DTL') }}