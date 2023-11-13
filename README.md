# Cloud Stress Tester

## Overview

The **cloud-stress-tester** project is designed to test the performance of scheduling and scaling algorithms in cloud clusters. It consists of a Python-based stress-test client (**stress-test-client**) for performing load testing and a web application (**stress-test-web**) for scaling and scheduling.

## Components

### 1. Stress Test Client (stress-test-client)

The stress-test-client is responsible for periodically sending requests to the deployed stress-test-web application within the cluster. These requests include queries for a specified number of users and insertions of a specified number of users.

### 2. Stress Test Web Application (stress-test-web)

The stress-test-web application provides six interfaces for performing insert and query operations on Redis and MySQL. These operations include querying and inserting a specified number of users, inserting a single user, and inserting a specified number of users.

## Workflow

The stress-test-client reads datasets and periodically sends requests to the stress-test-web deployed in the cluster. The stress-test-web processes these requests and performs insert and query operations on Redis and MySQL based on the specified interfaces.

## Usage

To use the project, follow these steps:

1. **Preprocessing Data:**
   - Utilize the scripts in the `preprocess_script` folder to preprocess the Azure Functions Blob Access Trace 2020 dataset.
   - Sort the data based on timestamps and perform periodic statistical analysis to generate ordered datasets and datasets specifying the number of requests to be initiated in each period.

2. **Load Testing:**
   - Use the `stress_simulator.py` script to read the generated datasets and perform service request load testing.

3. **Web Application Deployment:**
   - Deploy the stress-test-web application to the cloud service cluster.

## Additional Information

- The stress-test-web application supports operations on both MySQL and Redis.
- The project aims to assess the performance of scheduling and scaling algorithms in cloud clusters.

## Acknowledgments

This project was developed as part of [RunUSA]. We appreciate the support and contributions of all team members.

## License

This project is licensed under the [Your License] - see the [LICENSE.md](LICENSE.md) file for details.
