def publish(topics, entry_id):
    '''
    Publish an update to subscribed clients.

    - `topics`: a list of absolute URLs for topics
    - `entry_id`: atom:id of the updated entry
    '''
    from subhub.models import DistributionTask
    for topic in topics:
        DistributionTask.objects.add(topic, entry_id)
    DistributionTask.objects.process()
