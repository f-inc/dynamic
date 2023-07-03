# Dynamic ⚡️

**Disclaimer:** This documentation is intended for the alpha founders.inc community launch. Some portions of this documentation, such as the setup, are expected to change. Please keep that in mind for future reference.

## What is Dynamic?

Easy-to-use framework to enable building, deploying, and scaling LLM applications.

## Table of Contents

1. [Getting Started](#getting-started)
   a. [Installation](#installation)
   <!-- b. [Concepts](#concepts) -->
2. [Building Your Application](#building-your-application)
   a. [Dynamic Alpha - what can you do?](#dynamic-alpha---what-can-you-do)
   b. [Project Structure](#project-structure)
   c. [Routing](#routing)
   d. [Callables](#callables)
   e. [Langchain Agents](#langchain-agents)
   f. [Langchain Chains](#langchain-chains)

## Getting Started

### Installation

**Note:** There are instructions for the alpha version, these are expected to update once the wheel is released into a public artifactory.

1. Start a virtual environment
2. Given a python wheel provided by Aman, run:

```bash
$ pip install <path_to_wheel>
# example
$ pip install dist/dynamic-0.0.1-py3-none-any.whl
```

3. **(optional)** Test that the module is functional in your console by running:

```bash
$ python -c "import dynamic"
```

<!-- ### Concepts -->

## Building Your Application

### Dynamic Alpha - what can you do?

As of right now, the following features for an API built on dynamic are available:

1. Simple, normal `GET`, `PUT`, `POST`, and `DELETE` endpoints are represented by a callable function.

2. Given a langchain chain or agent, a simple endpoint will be generated that will return agent/chain output given a prompt.

3. Given an agent, a websocket endpoint can be generated that will stream all of the agent's output in real-time.

### Project Structure

### Routing

### Callables

### Langchain Chains

### Langchain Agents
