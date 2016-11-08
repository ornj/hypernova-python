import json
import hypernova
import mock
import mocks
import plugins
import unittest


class TestRenderer(unittest.TestCase):
    
    @mock.patch('requests.post', side_effect=mocks.make_server_timeout)
    def test_request_fail(self, mock_post):
        renderer = hypernova.Renderer('http://localhost')
        html = renderer.render({'component': {'foo': 'bar'}})
        self.assertIsInstance(html, str)    


class TestPlugins(unittest.TestCase):
    
    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    def test_no_plugins(self, mock_post):
        renderer = hypernova.Renderer('http://localhost')
        html = renderer.render({'component': {'foo': 'bar'}})
        self.assertEqual(html, '<p>{}</p>'.format(json.dumps({'foo': 'bar'})))
        
    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    def test_plugin_get_view_data(self, mock_post):
        expected_data = {'foo': 'bar'}
        renderer = hypernova.Renderer('http://localhost', [
            plugins.PluginGetViewData('component', expected_data)
        ])
        html = renderer.render({'component': {}})
        data = mock_post.call_args[1]['json']['component']['data']
        self.assertEqual(data, expected_data)
        self.assertEqual(html, '<p>{}</p>'.format(json.dumps(expected_data)))

    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    def test_plugin_get_view_data_no_return(self, mock_post):
        renderer = hypernova.Renderer(
            'http://localhost', [plugins.PluginGetViewDataDoNothing()]
        )
        html = renderer.render({'component': {'foo': 'bar'}})
        self.assertEqual(html, '<p>{}</p>'.format(json.dumps({'foo': 'bar'})))

    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    def test_plugin_prepare_request(self, mock_post):
        to_append = {'extra': 1}
        renderer = hypernova.Renderer('http://localhost', [
            plugins.PluginPrepareRequest('component', to_append)
        ])
        html = renderer.render({'component': {}})
        component_data = mock_post.call_args[1]['json']['component']
        self.assertEqual(component_data.get('extra'), to_append.get('extra'))

    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    def test_plugin_should_send_request_true(self, mock_post):
        renderer = hypernova.Renderer(
            'http://localhost', [plugins.PluginShouldSendRequestTrue()]
        )
        html = renderer.render({'component': {}})
        self.assertTrue(mock_post.called)

    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    def test_plugin_should_send_request_false(self, mock_post):
        renderer = hypernova.Renderer(
            'http://localhost', [plugins.PluginShouldSendRequestFalse()]
        )
        html = renderer.render({'component': {}})
        self.assertFalse(mock_post.called)

    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    def test_plugin_should_send_request_any_false(self, mock_post):
        renderer = hypernova.Renderer('http://localhost', [
            plugins.PluginShouldSendRequestTrue(), 
            plugins.PluginShouldSendRequestFalse()
        ])
        html = renderer.render({'component': {}})
        self.assertFalse(mock_post.called)
    
    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    @mock.patch.object(plugins.PluginWillSendRequest, 'will_send_request', autospec=True)
    def test_plugin_will_send_request(self, mock_plugin, mock_post):
        renderer = hypernova.Renderer('http://localhost', [
            plugins.PluginShouldSendRequestTrue(), 
            plugins.PluginWillSendRequest()
        ])
        renderer.render({'component': {}})
        self.assertTrue(mock_plugin.called)

    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    @mock.patch.object(plugins.PluginWillSendRequest, 'will_send_request', autospec=True)
    def test_plugin_will_send_request_false(self, mock_plugin, mock_post):
        renderer = hypernova.Renderer('http://localhost', [
            plugins.PluginShouldSendRequestFalse(), 
            plugins.PluginWillSendRequest()
        ])
        renderer.render({'component': {}})
        self.assertFalse(mock_plugin.called)

    @mock.patch('requests.post', side_effect=mocks.make_response_ok)
    @mock.patch.object(plugins.PluginOnSuccess, 'on_success', autospec=True)
    def test_plugin_on_success(self, mock_plugin, mock_post):
        renderer = hypernova.Renderer('http://localhost', [plugins.
            PluginOnSuccess()
        ])
        renderer.render({'component': {}})
        self.assertEqual(1, mock_plugin.call_count)

    @mock.patch('requests.post', side_effect=mocks.make_response_component_error)
    @mock.patch.object(plugins.PluginOnError, 'on_error', autospec=True)
    def test_plugin_on_error_component(self, mock_plugin, mock_post):
        renderer = hypernova.Renderer('http://localhost', [
            plugins.PluginOnError()
        ])
        renderer.render({'component': {}})
        self.assertEqual(1, mock_plugin.call_count)

    @mock.patch('requests.post', side_effect=mocks.make_response_server_error)
    @mock.patch.object(plugins.PluginOnError, 'on_error', autospec=True)
    def test_plugin_on_error_response(self, mock_plugin, mock_post):
        renderer = hypernova.Renderer('http://localhost', [
            plugins.PluginOnError()
        ])
        renderer.render({'component': {}})
        self.assertEqual(1, mock_plugin.call_count)
