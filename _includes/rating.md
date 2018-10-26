## Current rating

{% assign sorted = include.members %}
{% for member in sorted %}
- `{{ member.name }}` - {{ member.count }}
{% endfor %}
