import setuptools
import reddit_subscribers_count

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="reddit_subscribers_count",
        version=reddit_subscribers_count.__version__,
        author="dbeley",
        author_email="dbeley@protonmail.com",
        description="Scrap subreddits subscribers count",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dbeley/reddit_subscribers_count",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={
            "console_scripts": [
                "reddit_subscribers_count=reddit_subscribers_count.__main__:main"
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"
            ],
        install_requires=[
            'praw',
            ]
        )
