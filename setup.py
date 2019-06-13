import setuptools
import subreddit_tracker

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subreddit_tracker",
    version=subreddit_tracker.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="Exports subscribers and live users count from subreddits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/subreddit_tracker",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "subreddit_tracker=subreddit_tracker.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["praw"],
)
