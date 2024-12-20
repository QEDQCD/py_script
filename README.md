\# OpenStack Neutron API Multi-threaded Requester

 

\## Table of Contents

 

\- [Introduction](#introduction)

\- [Prerequisites](#prerequisites)

\- [Installation](#installation)

\- [Usage](#usage)

\- [Configuration](#configuration)

\- [Multi-threading](#multi-threading)

\- [Environment Variables](#environment-variables)

\- [Error Handling](#error-handling)

\- [Contributing](#contributing)

\- [License](#license)

 

\## Introduction

 

This project demonstrates how to use Python's `concurrent.futures.ThreadPoolExecutor` to perform multi-threaded requests against the OpenStack Neutron API. It includes functionality for obtaining an authentication token, listing subnets via the Neutron CLI, and making direct HTTP GET requests to the Neutron API endpoint.

 

\## Prerequisites

 

Before running this script, ensure that you have:

 

\- Installed Python 3.x

\- Configured OpenStack CLI (`openstack` and `neutron`) on your system.

\- Created a GitHub repository where you want to push your local changes.

\- A `.gitignore` file to exclude unnecessary files from version control.

 

Ensure that the OpenStack environment variables are set up correctly using the `admin-openrc` script provided by your cloud provider.

 

\## Installation

 

1. Clone this repository:

  \```bash

  git clone https://github.com/qcdqed/py_script.git

