from fastapi import HTTPException


def raise_exception(message, status_code):
    return HTTPException(status_code=status_code, detail=message)
