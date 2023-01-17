#!/usr/bin/env python3
"""Module 8 operate on mongo collections"""


def list_all(mongo_collection):
    """returns [] if null or empty
    or return all items in list"""
    return [item for item in mongo_collection.find()]
