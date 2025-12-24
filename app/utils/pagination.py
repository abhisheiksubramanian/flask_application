def paginate(query, page, size):
    page = max(page, 1)
    size = min(size, 100)
    return query.paginate(page=page, per_page=size, error_out=False)
