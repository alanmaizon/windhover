from flask import url_for

def generate_pagination(page, total_pages, sort_by, sort_order, search_query):
    """
    Generate pagination data for templates.
    """
    pagination = {
        "previous": None if page <= 1 else url_for(
            'current_route', page=page - 1, sortby=sort_by, order=sort_order, search=search_query
        ),
        "next": None if page >= total_pages else url_for(
            'current_route', page=page + 1, sortby=sort_by, order=sort_order, search=search_query
        ),
        "pages": []
    }

    # Add first page
    if total_pages > 0:
        pagination["pages"].append({
            "number": 1,
            "url": url_for('current_route', page=1, sortby=sort_by, order=sort_order, search=search_query),
            "active": page == 1
        })

    # Add middle ellipsis if needed
    if page > 3:
        pagination["pages"].append({"number": "...", "url": None, "active": False})

    # Add current page
    if page > 1 and page < total_pages:
        pagination["pages"].append({
            "number": page,
            "url": None,  # Active page has no link
            "active": True
        })

    # Add last ellipsis if needed
    if page < total_pages - 2:
        pagination["pages"].append({"number": "...", "url": None, "active": False})

    # Add last page
    if total_pages > 1:
        pagination["pages"].append({
            "number": total_pages,
            "url": url_for('current_route', page=total_pages, sortby=sort_by, order=sort_order, search=search_query),
            "active": page == total_pages
        })

    return pagination
