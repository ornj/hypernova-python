# hypernova-python [![Build Status](https://travis-ci.org/ornj/hypernova-python.svg?branch=master)](https://travis-ci.org/ornj/hypernova-python)

> A Python client for the Hypernova service

## Getting Started

Install the python client from pypi

```sh
pip install hypernova
```

Once you have the client installed and an instance of the Hypernova service running, you can making requests is easy.

### Example

```python
import hypernova

renderer = hypernova.Renderer('http://localhost')
html = renderer.render({'MyComponent.js': {'name': 'Foo'}})
```

## Configuration
You can pass configuration options to `Renderer` at initialization.

* `url`: The address of the Hypernova service is listening, including port if necessary
* `plugins`: A list of plugins to use
* `timeout`: Number of seconds to wait for a response from the Hypernova service
* `headers`: Dictionary of HTTP headers to override the default. You will want to include `'Content-Type': 'application/json'`


## Plugins
You can implement custom events and alter requests through the [Plugin Lifecycle](https://github.com/airbnb/hypernova-node/blob/master/README.md#plugin-lifecycle-api). All lifecycle methods are optional.

### Example

```python
import hypernova
import random

class MyPlugin(object):
	def prepare_request(self, current_jobs, original_jobs):
		job = current_jobs.get('MyComponent.js')
		job.update({'random_int_for_reasons': random.randint(0, 100))
		return current_jobs
		
renderer = hypernova.Renderer('http://localhost', [MyPlugin()])
```
