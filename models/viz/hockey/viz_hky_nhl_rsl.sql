{{ config(
    alias = 'HKY_NHL_MATCHES'

)}}

select *
from {{ ref('prp_hky_nhl_rsl') }}