from setuptools import setup, find_packages
from ButtonPaginator import __version__

with open("README.md", "r", encoding="utf-8") as rdme:
    long_description = rdme.read()

setup(
    name="dpy-slash-button-paginator",
    license="MIT",
    version=__version__,
    description="Unofficial button paginator using discord_slash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="catalyst4222",
    author_email="catalyst4222@gmail.com",
    url="https://github.com/catalyst4222/ButtonPaginator",
    download_url="https://github.com/Catalyst4222/ButtonPaginator/archive/refs/tags/v1.0.tar.gz",
    packages=find_packages(),
    keywords=["discord.py", "paginaion", "button", "components", "discord_slash", "discord-interactions"],
    python_requires=">=3.6",
    install_requires=["discord.py", "discord-py-slash-command"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
