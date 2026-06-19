from faker import Faker

fake = Faker()


# users/params.py
from dataclasses import dataclass
from common.base_params import PaginationParams



@dataclass
class GetUserFollowsParams(PaginationParams):
    ...
