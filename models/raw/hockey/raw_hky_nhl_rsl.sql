select *
from {{ source('raw', 'HKY_NHL_RSL') }}