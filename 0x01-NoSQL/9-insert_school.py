#!/usr/bin/env python3
"""Module 9 insert new obj"""


def insert_school(mongo_collection, **kwargs):
    """Returns the new obj id"""
    newObj = mongo_collection.insert_one(kwargs)
    return newObj.inserted_id
