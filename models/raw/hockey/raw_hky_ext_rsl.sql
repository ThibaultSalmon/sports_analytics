select *
from {{ source('raw', 'HKY_EXT_RSL') }}