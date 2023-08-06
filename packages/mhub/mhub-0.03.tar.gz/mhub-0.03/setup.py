import os
from distutils.core import setup

setup(
    name = "mhub",
    version = "0.03",
    author = "JingleManSweep",
    author_email = "jinglemansweep@gmail.com",
    description = "AMQP Based Home Automation Framework",
    url = "http://github.com/jingleman/MHub",
    packages = ["mhub", "mhub.plugins"],
    scripts = [
        os.path.join("bin", "mhub-server"),
        os.path.join("bin", "mhub-client")
    ],
    requires = [
        "yaml"
    ]
)