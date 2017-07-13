import requests
import structlog

log = structlog.getLogger()

def convert_raw_to_hydrus(raw_input):
    """convert raw result to hydrus format."""
    prediction = raw_input['prediction']
    result = []
    for key in prediction:
        namespace = None
        if key == 'character':
            namespace = 'character'
        elif key == 'copyright':
            namespace = 'series'
        elif key == 'general':
            pass
        elif key == 'rating':
            rating = 'rating:{}'.format(prediction['rating'][0][0])
            result.append(rating)
            continue
        else:
            log.debug('Unknown key', key=key)
        if not prediction[key]:
            continue
        for item, _ in prediction[key]:
            if namespace:
                result.append('{}:{}'.format(namespace, item))
            else:
                result.append(item)
    return '\n'.join(sorted(result))


class Session:
    """session."""

    def __init__(self):
        """init."""
        self.session = requests.Session()

    def get_tags(self, path, dump_html=False):
        """get tags."""
        url = 'http://demo.illustration2vec.net/upload'
        files = {'image': open(path, 'rb')}
        res = self.session.post(url=url, files=files)
        if res != 200:
            return {}
        return res.json()

    def get_hydrus_tags(self, path, dump_html=False):
        """get tags in hydrus format."""
        tags = self.get_tags()
        if not tags:
            return
        return convert_raw_to_hydrus(tags)
