def parse( ins ):
    query = "%20".join(ins)
    return query.replace('=','%3d')