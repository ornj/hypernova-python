class PluginGetViewData(object):
    def __init__(self, view_name, return_data):
        self.view_name = view_name
        self.return_data = return_data

    def get_view_data(self, view_name, data):
        if view_name == self.view_name:
            return self.return_data


class PluginGetViewDataDoNothing(object):
    def get_view_data(self, view_name, data):
        return data


class PluginPrepareRequest(object):
    def __init__(self, view_name, to_append):
        self.view_name = view_name
        self.to_append = to_append

    def prepare_request(self, current_jobs, original_jobs):
        job = current_jobs.get(self.view_name)
        if job:
            job.update(self.to_append)
        return current_jobs


class PluginShouldSendRequestTrue(object):
    def should_send_request(self, jobs):
        return True


class PluginShouldSendRequestFalse(object):
    def should_send_request(self, jobs):
        return False


class PluginWillSendRequest(object):
    def will_send_request(self, jobs):
        pass


class PluginOnSuccess(object):
    def on_success(self, successful_jobs):
        pass


class PluginOnError(object):
    def on_error(self, error, jobs):
        pass
