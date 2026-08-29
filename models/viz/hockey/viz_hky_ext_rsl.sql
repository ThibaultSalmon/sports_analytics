{{ config(
    alias = 'HKY_EXT_MATCHES'

)}}

select *
from {{ ref('prp_hky_ext_rsl') }}