from setuptools import setup, find_packages

setup(
    name="quantum-duality-theory",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask==2.0.1",
        "flask-cors==3.0.10",
        "flask-limiter==3.5.0",
        "flask-swagger-ui==4.11.1",
        "gunicorn==20.1.0",
        "numpy>=1.24.3",
        "scipy>=1.10.1",
        "python-dotenv>=0.19.0",
        "redis>=4.0.0",
        "werkzeug<2.1.0",
        "networkx>=2.6.0"
    ],
    python_requires=">=3.8",
    author="Quantum Duality Theory Team",
    author_email="team@quantumduality.com",
    description="A quantum duality theory implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/quantum-duality-theory",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 