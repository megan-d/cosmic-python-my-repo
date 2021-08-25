from setuptools import setup, find_packages

setup(
    name="allocation", version="0.2", packages=["allocation", "allocation.adapters", "allocation.domain", "allocation.entrypoints", "allocation.service_layer"],
)