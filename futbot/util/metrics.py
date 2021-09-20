''' Metric module: updates metrics values '''

from typing import Dict
import futbot.util.files as fs
import futbot.util.date as date_util

METRICS_PATH = './metrics.json'

# Metrics names
TWITTER = 'twitter'
INSTAGRAM = 'instagram'
DATE_FROM = 'date_from'
LAST_UPDATE = 'last_update'
TWEETED_TOURNAMENTS = 'tweeted_tournaments'
TWEETED_MATCHES = 'tweeted_matches'
SENT_TWITTER_MESSAGES = 'sent_twitter_messages'
POSTED_STORIES = 'posted_stories'

def update_metric(metric_name: str, new_value: int) -> None:
    """
        Update a metric
        Parameters
        ----------
        metric_name: str
            name of the metric
        new_value: int
            new value for the metric
    """
    metrics = read_or_create_metric()
    updated = False
    
    if metric_name in metrics[INSTAGRAM].keys():
        metrics[INSTAGRAM][metric_name] = new_value
        updated = True
    elif metric_name in metrics[TWITTER].keys():
        metrics[TWITTER][metric_name] = new_value
        updated = True
    else:
        print('Wrong metric_name! -> [{}]'.format(metric_name))
    
    if updated:
        metrics[LAST_UPDATE] = str(date_util.get_actual_datetime())
        fs.write_json_file(metrics, METRICS_PATH)
        print('METRICS -> [{}] metric updated to [{}]'.format(metric_name, new_value))

def increase_metric(metric_name: str, increment: int) -> None:
    """
        Increase the value of a metric

        Parameters
        ----------
        metric_name: str
            name of the metric
        increment: int
            the increment for the metric
    """
    if increment > 0:
        actual_value = get_metric(metric_name)
        if type(actual_value) == int:
            new_value = get_metric(metric_name) + increment
            update_metric(metric_name, new_value)

def get_metric(metric_name: str) -> int:
    """
        Returns the value for metric_name
        
        Parameters
        ----------
        metric_name: str
            name of the metric
        
        Returns
        -------
        int
            value of the metric
    """
    metrics = read_or_create_metric()

    if metric_name in metrics[INSTAGRAM].keys():
        return metrics[INSTAGRAM][metric_name]
    elif metric_name in metrics[TWITTER].keys():
        return metrics[TWITTER][metric_name]

    print('Wrong metric_name! -> [{}]'.format(metric_name))
    return None

def read_or_create_metric() -> Dict:
    """
        Reads saved metrics, or creates metrics dict

        Returns
        -------
        dict
            metric dict
    """
    metrics = fs.read_json_file(METRICS_PATH)
    if not metrics:
        print('metrics.json not found. Creating new metrics.')
        metrics = get_metric_template()
    return metrics

def get_metric_template() -> Dict:
    return {
        str(DATE_FROM) : str(date_util.get_actual_datetime()),
        str(TWITTER) : {
            str(TWEETED_MATCHES) : 0,
            str(TWEETED_TOURNAMENTS) : 0,
            str(SENT_TWITTER_MESSAGES) : 0
        },
        str(INSTAGRAM) : {
            str(POSTED_STORIES) : 0
        },
        str(LAST_UPDATE): ""
    }
