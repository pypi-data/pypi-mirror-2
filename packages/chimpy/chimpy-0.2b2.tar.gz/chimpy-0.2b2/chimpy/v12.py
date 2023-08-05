from chimpy import Connection as BaseConnection

class Connection(BaseConnection):
    """mailchimp api v. 1.2 connection """

    version = '1.2'

    def campaigns(self, filters={}, start=0, limit=50):
        """Get the list of campaigns and their details matching the specified filters.
        Timestamps should be passed as datatime objects.

        http://www.mailchimp.com/api/1.2/campaigns.func.php
        """

        return self._api_call(method='campaigns', filters=filters, start=start, limit=limit)
