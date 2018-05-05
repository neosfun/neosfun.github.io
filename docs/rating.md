## Current rating

{% assign sorted = include.members %}
{% for member in sorted %}
- `{{ member.name }}` - {{ member.solved_num }} Quests Solved
{% endfor %}
