from faker import Faker

fake = Faker()


class Payloads:

    def create_post(self, content: str, visibility: str, image_url: str = None):
        return {
            "content": content,
            "image_url": image_url,
            "visibility": visibility
        }

    def update_post(self, content: str,visibility: str=None, image_url: str = None) :
        payload = {}
        if content:
            payload["content"]=f"{content}"
        if visibility:
            payload["visibility"]=f"{visibility}"
        if image_url:
            payload["image_url"]=f"{image_url}"
        return payload

    def create_repost(self, repost_type: str=None, content: str=None):
        payload = {}
        if repost_type:
            payload["repost_type"]=f"{repost_type}"
        if content:
            payload["content"] = content

        return payload
