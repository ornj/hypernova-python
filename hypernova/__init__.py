import json
import requests


def render_html(name, data):
    return """
        <div data-hypernova-key="{name}"></div>
        <script type="application/json" data-hypernova-key="{name}">
        <!--{data}--></script>
    """.format(name=name, data=json.dumps(data))


def render_fallback(error, jobs):
    results = {}
    for name, job in jobs.iteritems():
        results[name] = {
            'error': None,
            'html': render_html(name, job.get('data')),
            'job': job
        }
    return {'error': error, 'results': results}


def results_to_html(results):
    return ''.join([r.get('html') for r in results.values()])


class Renderer(object):

    def __init__(self, url, plugins=None, timeout=None, headers=None):
        self.url = url
        self.plugins = plugins or []
        self.timeout = timeout or 1
        self.headers = headers or {'Content-Type': 'application/json'}

    def plugin_reduce(self, event_name, fn, init=None):
        return reduce(
            lambda a, b: fn(getattr(b, event_name), a) if hasattr(b, event_name) else a,
            self.plugins, init
        )

    def create_jobs(self, jobs):
        created = {}
        for job_name, job_data in jobs.iteritems():
            job_data = self.plugin_reduce(
                'get_view_data', 
                lambda plugin, new_data: plugin(job_name, new_data),
                job_data
            )
            created[job_name] = {'name': job_name, 'data': job_data}
        return created

    def prepare_request(self, jobs):
        jobs_hash = self.plugin_reduce(
            'prepare_request', lambda plugin, obj: plugin(obj, jobs), jobs
        )
        should_send_request = self.plugin_reduce(
            'should_send_request', 
            lambda plugin, obj: obj and plugin(jobs_hash), 
            True
        )
        return {
            'should_send_request': should_send_request, 'jobs_hash': jobs_hash
        }

    def render(self, data):
        jobs = self.create_jobs(data)
        request_data = self.prepare_request(jobs)
        jobs_hash = request_data.get('jobs_hash')

        # TODO: Don't send if no jobs_hash
        
        if request_data.get('should_send_request'):
            self.plugin_reduce(
                'will_send_request', lambda plugin, _: plugin(jobs_hash)
            )
            response = requests.post(
                self.url, 
                json=jobs_hash, 
                headers=self.headers, 
                timeout=self.timeout
            )
            if response.ok:
                response_data = response.json()
            else:
                response_data = render_fallback(
                    response.json().get('error'), jobs_hash
                )
        else:
            response_data = render_fallback(None, jobs_hash)

        results = response_data.get('results')
        error = response_data.get('error')
        
        if error:
            self.plugin_reduce(
                'on_error', lambda plugin, _: plugin(error, results)
            )

        successful_jobs = []
        for name, body in results.iteritems():
            body['job'] = jobs_hash.get(name)
            error = body.get('error')
            if error:
                body['html'] = render_html(name, data.get(name))
                self.plugin_reduce(
                    'on_error', lambda plugin, body: plugin(error, body)
                )
            else:
                successful_jobs.append(body)

        self.plugin_reduce(
            'on_success', lambda plugin, _: plugin(successful_jobs)
        )

        if self.plugins:
            results = self.plugin_reduce(
                'after_response', 
                lambda plugin, obj: plugin(obj, results), 
                results
            )
        
        # TODO Maybe, 9. If an error is encountered then call 
        #      onError(error, jobs) and assert that the fallback HTML 
        #      is provided.
        #
        #      Basically, handle plugins raising exceptions.

        return results_to_html(results)
