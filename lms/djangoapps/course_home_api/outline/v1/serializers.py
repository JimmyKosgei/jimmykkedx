"""
Outline Tab Serializers.
"""


from rest_framework import serializers
from lms.djangoapps.courseware.date_summary import VerificationDeadlineDate

class CourseToolSerializer(serializers.Serializer):
    """
    Serializer for Course Tool Objects
    """
    analytics_id = serializers.CharField()
    title = serializers.CharField()
    url = serializers.SerializerMethodField()

    def get_url(self, tool):
        course_key = self.context.get('course_key')
        url = tool.url(course_key)
        request = self.context.get('request')
        return request.build_absolute_uri(url)


class DateSummarySerializer(serializers.Serializer):
    """
    Serializer for Date Summary Objects.
    """
    date = serializers.DateTimeField()
    date_type = serializers.CharField()
    description = serializers.CharField()
    learner_has_access = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    title = serializers.CharField()
    link_text = serializers.CharField()
    title_html = serializers.CharField()

    def get_learner_has_access(self, block):
        learner_is_full_access = self.context.get('learner_is_full_access', False)
        block_is_verified = (getattr(block, 'contains_gated_content', False) or
                             isinstance(block, VerificationDeadlineDate))
        return (not block_is_verified) or learner_is_full_access

    def get_link(self, block):
        if block.link:
            request = self.context.get('request')
            return request.build_absolute_uri(block.link)
        return ''


class OutlineTabSerializer(serializers.Serializer):
    """
    Serializer for the Outline Tab
    """
    course_tools = CourseToolSerializer(many=True)
    course_date_blocks = DateSummarySerializer(many=True)
    dates_tab_link = serializers.CharField()
    user_timezone = serializers.CharField()
