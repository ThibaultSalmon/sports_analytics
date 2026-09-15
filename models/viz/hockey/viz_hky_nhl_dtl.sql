{{ config(
    alias = 'HKY_NHL_DETAILS'

)}}

select *
from {{ ref('prp_hky_nhl_dtl') }}