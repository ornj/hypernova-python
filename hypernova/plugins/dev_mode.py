import json


def render_stack(error):
    return '\n  '.join(error.get('stack'))


def render_error(component_name, data):
    return """
      <div style="background-color: #ff5a5f; color: #fff; padding: 12px;">
        <p style="margin: 0">
          <strong>Warning!</strong>
          The <code>{}</code> component failed to render with Hypernova. 
          Error stack:
        </p>
        <pre style="padding: 0 20px; white-space: pre-wrap;">{}</pre>
      </div>
      {}
    """.format(
        component_name, render_stack(data.get('error')), data.get('html')
    )


def render_error_or_html(data):
    if data.get('error'):
        return render_error(data.get('error')) 
    return data.get('html')


class DevModePlugin(object):
    """Plugin to enable additional logging from Hypernova"""

    def __init__(self, logger):
        self.logger = logger

    def after_response(self, current_response, original_response):
        updated = current_response.copy()
        for name, data in updated.iteritems():
            if data.get('error'):
                data['html'] = render_error(name, data) 
        return updated

    def on_error(self, error, jobs):
        self.logger.debug(render_stack(error))
