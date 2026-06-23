def pagination(
        page: int = 1,
        limit:int = 4
):
    offset = (page - 1) * limit 

    return offset,limit