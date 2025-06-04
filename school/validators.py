from rest_framework import serializers


def validate_url(url):
    allowed_domains = [
        "youtube.com",
        "www.youtube.com",
        "127.0.0.1:8000",
    ]
    if not any(domain in url for domain in allowed_domains):
        raise serializers.ValidationError("Ссылка ведет на сторонний ресурс!")
    return url
